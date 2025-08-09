import pandas as pd
import numpy as np
from scipy.stats import pearsonr, spearmanr

###############################################################################
# 1. LOAD THE DATA FROM EXCEL
###############################################################################
# Replace 'your_file.xlsx' with the actual path to your Excel file.
# Adjust sheet_name, header, skiprows, etc. as needed for your file.
df = pd.read_excel(
    r'C:\Users\SebastianAeschbach(G\Dropbox\Cursus\Cursus\Psychology\Cursus_Psychology\Master\Classeur2.xlsx',
    header = 1,
    skiprows = [2],
    sheet_name = 0
)

print(df.head())
print(df)

###############################################################################
# 2. DEFINE YOUR CORE VALUES & PHASE 1 COLUMNS
###############################################################################
values_list = ["Care", "Fairness", "Sanctity", "Authority", "Loyalty", "Liberty"]
phase1_cols = [v + "_phase1" for v in values_list]

for col in phase1_cols:
    if col not in df.columns:
        print(f"Warning: column {col} not found in DataFrame. Please check spelling.")


###############################################################################
# 3. HELPER TO PARSE PAIRWISE COLUMNS (E.G. "QH6-FairnessLoyalty_1")
###############################################################################
def parse_pairwise_column(col_name):
    """
    Attempt to parse a column like 'QH6-FairnessLoyalty_1'
    to extract the two values: ('Fairness', 'Loyalty'), etc.
    Returns (value1, value2) or None if not recognized.
    """
    if '-' not in col_name:
        return None

    # Example split: "QH6" and "FairnessLoyalty_1"
    left, right = col_name.split('-', 1)

    # Remove trailing underscores/numbers from the right side:
    right_clean = right.split('_')[0]  # e.g. 'FairnessLoyalty_1' -> 'FairnessLoyalty'

    found_values = []
    for val in values_list:
        if val in right_clean:
            found_values.append(val)

    # We only consider it valid if we find exactly 2 distinct values
    if len(found_values) == 2:
        return found_values[0], found_values[1]
    else:
        return None  # Return None if not exactly 2 recognized values


###############################################################################
# 4. COLLECT ALL PAIRWISE COLUMNS AND ACCUMULATE PARTIAL SCORES
###############################################################################
pairwise_cols = []
for c in df.columns:
    if parse_pairwise_column(c) is not None:
        pairwise_cols.append(c)

# Prepare structure to hold partial scores for each participant
# derived_scores[i] is a dict with key=Value, value=list of partial contributions
derived_scores = []
for i in range(len(df)):
    derived_scores.append({v: [] for v in values_list})

# Fill partial scores from each question
for c in pairwise_cols:
    val_pair = parse_pairwise_column(c)
    if val_pair is None:
        continue
    v1, v2 = val_pair
    for i in range(len(df)):
        x = df.loc[i, c]
        if pd.isnull(x):
            # If the cell is empty, skip
            continue
        # If participant answered x for (v1 vs. v2),
        # v1 gets x, v2 gets (100 - x)
        derived_scores[i][v1].append(x)
        derived_scores[i][v2].append(100 - x)

# Compute final averaged derived scores per participant
final_derived_scores = []
for i in range(len(df)):
    participant_dict = {}
    for v in values_list:
        partial_list = derived_scores[i][v]
        if len(partial_list) == 0:
            participant_dict[v] = np.nan
        else:
            participant_dict[v] = np.mean(partial_list)
    final_derived_scores.append(participant_dict)

# Convert to a DataFrame
df_derived = pd.DataFrame(final_derived_scores)

###############################################################################
# 5. COMBINE PHASE 1 AND DERIVED SCORES INTO A "WIDE" FORMAT
###############################################################################
comparison_df = pd.concat([df[phase1_cols].reset_index(drop = True),
                           df_derived.reset_index(drop = True)], axis = 1)

# Rename derived columns for clarity
rename_dict = {}
for v in values_list:
    rename_dict[v] = v + "_derived"

# Also rename the phase1 columns to remain consistent, if desired:
# (They might already be named Care_phase1, etc. so it might be optional)
# For clarity, let's unify them:
comparison_df.rename(columns = rename_dict, inplace = True)

print("\n=== WIDE FORMAT (Phase 1 + Derived) ===")
print(comparison_df.head())


###############################################################################
# 6. CREATE RANKS (PHASE 1 & DERIVED) AND MERGE INTO A SINGLE DataFrame
###############################################################################
def rank_values_for_participant(participant_data_, which="phase1"):
    """
    Given a row (participant_data_), produce ranks for the 6 values
    in the chosen set (phase1 or derived).
    Returns a dict with rank columns for each value.
    """
    if which == "phase1":
        cols = [f"{v}_phase1" for v in values_list]
    else:
        cols = [f"{v}_derived" for v in values_list]

    sub_series = participant_data_[cols]
    # rank in descending order (higher scores = rank 1)
    ranks = sub_series.rank(ascending = False, method = 'dense')

    out_dict = {}
    for v in values_list:
        col_name = f"{v}_{which}"
        rank_col_name = f"{v}_{which}_rank"
        out_dict[rank_col_name] = ranks[col_name]
    return out_dict


all_phase1_ranks = []
all_derived_ranks = []

for i in range(len(comparison_df)):
    participant_data = comparison_df.iloc[i]
    p1_ranks = rank_values_for_participant(participant_data, which = "phase1")
    d_ranks = rank_values_for_participant(participant_data, which = "derived")
    all_phase1_ranks.append(p1_ranks)
    all_derived_ranks.append(d_ranks)

df_phase1_ranks = pd.DataFrame(all_phase1_ranks)
df_derived_ranks = pd.DataFrame(all_derived_ranks)

comparison_df_ranks = pd.concat(
    [comparison_df, df_phase1_ranks, df_derived_ranks],
    axis = 1
)

###############################################################################
# 7. SIMPLE DESCRIPTIVE STATISTICS
###############################################################################
print("\n=== Means of Phase 1 Scores (original) ===")
print(comparison_df[[f"{v}_phase1" for v in values_list]].mean())

print("\n=== Means of Derived Scores ===")
print(comparison_df[[f"{v}_derived" for v in values_list]].mean())

print("\n=== Correlations between Phase 1 and Derived (per value) ===")
for v in values_list:
    phase1_col = f"{v}_phase1"
    derived_col = f"{v}_derived"
    tmp = comparison_df[[phase1_col, derived_col]].dropna()
    if len(tmp) < 2:
        print(f"{v}: Not enough data to compute correlation.")
        continue
    pear_r, pear_p = pearsonr(tmp[phase1_col], tmp[derived_col])
    spear_r, spear_p = spearmanr(tmp[phase1_col], tmp[derived_col])
    print(f"{v}: Pearson r={pear_r:.3f} (p={pear_p:.3g}), Spearman r={spear_r:.3f} (p={spear_p:.3g})")

# Spearman correlation of the rank profiles per participant
rank_correlations = []
for i in range(len(comparison_df_ranks)):
    p1_r = [comparison_df_ranks.iloc[i][f"{v}_phase1_rank"] for v in values_list]
    d_r = [comparison_df_ranks.iloc[i][f"{v}_derived_rank"] for v in values_list]
    # If any is NaN, skip
    if np.isnan(p1_r).any() or np.isnan(d_r).any():
        continue
    r_corr, _ = spearmanr(p1_r, d_r)
    rank_correlations.append(r_corr)

if rank_correlations:
    print("\n=== Average Spearman correlation of ordinal hierarchies (Phase1 vs Derived) ===")
    print(f"Mean correlation: {np.mean(rank_correlations):.3f}")
    print(f"SD correlation:   {np.std(rank_correlations, ddof = 1):.3f}")
else:
    print("No rank correlations computed (maybe missing data).")

###############################################################################
# 8. CREATE A LONG-FORM TABLE SHOWING DECOMPOSED SCORES
###############################################################################
# We want one row per participant × value, with:
#  - Phase1 score
#  - For each pairwise question that includes this value, the partial score
#  - The final derived score
#
# Example logic: if QH1-FairnessLoyalty_1 = 45, then:
#  - "Fairness" row gets "45" in the QH1-FairnessLoyalty_1 column
#  - "Loyalty" row gets "55" in that column
#  - Other values get NaN for that column
###############################################################################
long_columns = ["participant_id", "value", "phase1_score"] + pairwise_cols + ["derived_score"]
long_data = []

for i in range(len(df)):
    # You might have an explicit participant ID column in your DataFrame;
    # for demonstration, we'll just use i (the row index) as an ID
    participant_id = i

    for v in values_list:
        row_dict = {"participant_id": participant_id, "value": v}

        # Phase1 score if it exists
        phase1_col = f"{v}_phase1"
        if phase1_col in df.columns:
            row_dict["phase1_score"] = df.loc[i, phase1_col]
        else:
            row_dict["phase1_score"] = np.nan

        # For each question, put partial score if relevant
        for pc in pairwise_cols:
            val_pair = parse_pairwise_column(pc)
            if val_pair and v in val_pair:
                x = df.loc[i, pc]
                if pd.isnull(x):
                    row_dict[pc] = np.nan
                else:
                    # If v is the first in the pair, partial = x
                    # else partial = 100 - x
                    if v == val_pair[0]:
                        row_dict[pc] = x
                    else:
                        row_dict[pc] = 100 - x
            else:
                # This question did not involve this value
                row_dict[pc] = np.nan

        # Add the final derived average for that participant-value
        row_dict["derived_score"] = final_derived_scores[i][v]

        long_data.append(row_dict)

df_long = pd.DataFrame(long_data, columns = long_columns)

print("\n=== LONG FORMAT TABLE ===")
print(df_long.head(30))  # Print first 30 rows for inspection

###############################################################################
# 9. EXPORT RESULTS
###############################################################################
# 1) The wide format with ranks
comparison_df_ranks.to_excel("comparison_output.xlsx", index = False)

# 2) The long format with partial decomposition
df_long.to_excel("long_format_decomposition.xlsx", index = False)

print("\nDone!")
print(" - 'comparison_output.xlsx': wide format with phase1 + derived + ranks.")
print(" - 'long_format_decomposition.xlsx': one row per participant-value,")
print("   including the partial scores from each pairwise question.")
