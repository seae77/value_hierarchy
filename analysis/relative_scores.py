import itertools
from tabulate import tabulate  # Optional: for nice table formatting

# Install using: pip install tabulate

# --- Configuration ---

# Define the six core values
CORE_VALUES = ["Authority", "Care", "Fairness", "Liberty", "Loyalty", "Sanctity"]

# --- Input Data: P1Q Scores ---
# Using the example scores provided earlier in the conversation
# Keys are simplified here for clarity in grouping
p1q_scores_raw = {
    ("Care", "Fairness"): [70, 71, 70],  # Scores represent Care
    ("Sanctity", "Authority"): [32, 36, 31],  # Scores represent Sanctity
    ("Loyalty", "Liberty"): [65, 65, 34],  # Scores represent Loyalty
}

# Define which value the RAW score represents for measured pairs
# Key: tuple(ValueRepresented, OtherValue)
p1q_score_representation_info = {
    ("Care", "Fairness"): "Care",
    ("Sanctity", "Authority"): "Sanctity",
    ("Loyalty", "Liberty"): "Loyalty",
}

# --- 1. Calculate Average Individual Scores from P1Q Data ---

print("Calculating Average Individual Scores from P1Q data...")
avg_individual_scores = {val: None for val in CORE_VALUES}
# Store avg raw score for measured pairs to use later
avg_measured_raw_scores = {}

temp_avg_individual_scores = {val: [] for val in CORE_VALUES}

for (valA, valB), scores in p1q_scores_raw.items():
    if not scores: continue
    avg_s = sum(scores) / len(scores)

    # Store average raw score for the measured pair
    # Ensure key is standardized alphabetically for later lookup
    pair_alpha = tuple(sorted((valA, valB)))
    avg_measured_raw_scores[pair_alpha] = avg_s

    # Determine which value the score S represents
    represents_value = p1q_score_representation_info.get((valA, valB))
    if not represents_value:
        print(f"Error: P1Q score representation definition missing for pair {(valA, valB)}")
        continue

    # Get the other value
    other_value = valB if represents_value == valA else valA

    # Calculate the individual scores based on S
    score_represents = avg_s
    score_other = 100 - avg_s

    # Store the calculated individual scores temporarily
    temp_avg_individual_scores[represents_value].append(score_represents)
    temp_avg_individual_scores[other_value].append(score_other)

# Average the calculated individual scores (trivial in this case as each value appears once)
for value, score_list in temp_avg_individual_scores.items():
    if score_list:
        avg_individual_scores[value] = sum(score_list) / len(score_list)
    else:
        print(f"Warning: No P1Q data found to calculate average score for {value}")

print("\nAverage Individual Scores (based on P1Q):")
for value, score in avg_individual_scores.items():
    if score is not None:
        print(f"- {value}: {score:.2f}")
    else:
        print(f"- {value}: Not Measured in P1Q")

# --- 2. Calculate/Retrieve Relative Scores for All 15 Pairs ---

all_pairs = list(itertools.combinations(CORE_VALUES, 2))
all_pairs_sorted = [tuple(sorted(p)) for p in all_pairs]  # Ensure alphabetical order

final_scores = {}  # Store results: {pair: {"score": float, "type": str}}

print("\nCalculating/Retrieving Relative Scores for All 15 Pairs (P1Q Based)...")
for pair in all_pairs_sorted:
    val1, val2 = pair  # val1 is alphabetically first

    # Check if this pair was directly measured in P1Q
    if pair in avg_measured_raw_scores:
        avg_s = avg_measured_raw_scores[pair]
        # Find the original (non-alphabetical) key to get representation info
        original_key = None
        for k in p1q_score_representation_info.keys():
            if set(k) == set(pair):
                original_key = k
                break
        represents_value = p1q_score_representation_info.get(original_key)

        score_val1 = None
        if represents_value == val1:
            score_val1 = avg_s
        elif represents_value == val2:
            score_val1 = 100 - avg_s

        if score_val1 is not None:
            final_scores[pair] = {"score": score_val1, "type": "Measured Avg"}
        else:
            print(f"Error processing measured pair {pair}")
            final_scores[pair] = {"score": None, "type": "Error"}

    # If not measured, calculate estimate using normalization
    else:
        avg_score_val1 = avg_individual_scores.get(val1)
        avg_score_val2 = avg_individual_scores.get(val2)

        if avg_score_val1 is not None and avg_score_val2 is not None:
            total = avg_score_val1 + avg_score_val2
            if total == 0:
                estimated_score = 50.0
            else:
                estimated_score = (avg_score_val1 / total) * 100
            final_scores[pair] = {"score": estimated_score, "type": "Calculated Estimate"}
        else:
            print(f"Warning: Cannot calculate estimate for {pair} due to missing avg individual score(s).")
            final_scores[pair] = {"score": None, "type": "Calculation Failed"}

# --- 3. Produce Ranked Table ---

print("\nGenerating Ranked Table based on P1Q scores and estimates...")

table_data = []
for pair, data in final_scores.items():
    if data["score"] is not None:
        pair_str = f"{pair[0]} vs {pair[1]}"
        table_data.append([pair_str, data["score"], data["type"]])
    else:
        pair_str = f"{pair[0]} vs {pair[1]}"
        table_data.append([pair_str, "N/A", data["type"]])

# Sort by score (descending), handle N/A scores by placing them last
table_data.sort(key = lambda row: row[1] if isinstance(row[1], (int, float)) else -float('inf'), reverse = True)

# Add Rank
ranked_table_data = []
for i, row in enumerate(table_data):
    ranked_table_data.append([i + 1] + row)

# Define headers
headers = ["Rank", "Value Pair (Value 1 vs Value 2)", "Relative Score (for Value 1)", "Type"]

# Print the table using tabulate
print("\nRanked Table of Relative Scores for Value Pairs (P1Q Based)")
print("(Score represents preference for Value 1)")
print(tabulate(ranked_table_data, headers = headers, floatfmt = ".2f", tablefmt = "grid"))

print("\nNote: 'Calculated Estimate' scores rely on the assumption that average")
print("individual scores derived from specific P1Q pairs are comparable and")
print("reflect positions on an absolute hierarchy.")
