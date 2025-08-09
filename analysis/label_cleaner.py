import pandas as pd
import re
import os  # To check if input file exists

# --- Configuration ---

# --- !!! --- USER: Please update these paths and names --- !!! ---
INPUT_EXCEL_FILE = r"C:\Users\SebastianAeschbach(G\Dropbox\Cursus\Cursus\Psychology\Cursus_Psychology\Master\ValuesHierarchy_test_March+12,+2025_20.55\ValuesHierarchy_test_March 12, 2025_20.55.xlsx"  # Replace with your input Excel filename
OUTPUT_EXCEL_FILE = r"C:\Users\SebastianAeschbach(G\Dropbox\Cursus\Cursus\Psychology\Cursus_Psychology\Master\cleaned_labels.xlsx"  # Name for the output file)
SHEET_NAME = 'Sheet0'  # Replace with the name of the sheet containing labels (or None if only one sheet)
# --- !!! --- End of User Configuration --- !!! ---

# Define the six core values
CORE_VALUES = ["Authority", "Care", "Fairness", "Liberty", "Loyalty", "Sanctity"]

# Define corrections for known typos or abbreviations
CORRECTIONS = {
    "Faireness": "Fairness",
    "Sanctit": "Sanctity",
    "Authorit": "Authority",
    "Sanvtity": "Sanctity",
    # Add more if found based on full list review
}

# Define corrections for outlier labels based on context
# Renaming these specific outliers happens first
OUTLIER_CORRECTIONS = {
    "Question-35_1": "QH1-FairnessAuthority_1",  # Based on previous contextual analysis
    "QH6_1": "QH6-AuthoritySanctity_1",  # Based on previous contextual analysis
}


# --- Label Cleaning and Standardization Function ---

def clean_and_refactor_label(label):
    """
    Cleans typos, standardizes value names and order, and refactors a label string.
    Handles non-string inputs by converting them first.

    Args:
        label (any): The original label (will be converted to string).

    Returns:
        str: The cleaned and refactored label string, or a placeholder if parsing fails.
    """
    if pd.isna(label) or label is None:  # Handle empty cells
        return ""

    original_label = str(label).strip()  # Ensure input is treated as string and remove whitespace

    # Skip processing if the label is empty after stripping
    if not original_label:
        return ""

    # Apply outlier corrections first to get a parsable structure
    corrected_for_outlier = OUTLIER_CORRECTIONS.get(original_label, original_label)

    # Basic parsing using delimiters '-' and '_'
    parts = corrected_for_outlier.split('-')

    # If there's no hyphen, try to see if this is a special case we can handle
    if len(parts) != 2:
        # Check if it's a known format without a hyphen
        if original_label in OUTLIER_CORRECTIONS:
            # Already handled above
            pass
        else:
            # Try to find any core values in the string
            found_values = []
            for value in CORE_VALUES:
                if value.lower() in original_label.lower():
                    found_values.append(value)

            if len(found_values) >= 2:
                # We found at least two values, construct a label
                prefix = "Q"  # Default prefix
                value1, value2 = sorted(found_values[:2])  # Take first two values found
                return f"{prefix}-{value1}{value2}_1"  # Default suffix
            else:
                # Can't parse this format
                return f"PARSE_ERROR: No hyphen in '{original_label}'"

    prefix = parts[0]
    suffix_part = parts[1]

    # Handle the suffix part
    suffix_parts = suffix_part.split('_')
    values_str = ""
    suffix = ""

    if len(suffix_parts) >= 2:  # Allow for suffixes like _1a, take only first part
        values_str = suffix_parts[0]
        suffix = suffix_parts[1]
    elif len(suffix_parts) == 1:
        values_str = suffix_parts[0]
        suffix = "1"  # Default suffix to 1 if missing
    else:
        return f"PARSE_ERROR: No values in '{original_label}'"

    # Apply typo corrections to the values string
    temp_values_str = values_str
    for typo, correction in CORRECTIONS.items():
        temp_values_str = temp_values_str.replace(typo, correction)

    # Extract value pairs
    v1, v2 = None, None
    # Sort core values by length descending to match longer names first
    sorted_core_values = sorted(CORE_VALUES, key = len, reverse = True)

    # First attempt: direct matching
    for val1_candidate in sorted_core_values:
        # Check if string starts with value1 and the rest is value2
        if temp_values_str.startswith(val1_candidate):
            remaining = temp_values_str[len(val1_candidate):]
            if remaining in CORE_VALUES:
                v1 = val1_candidate
                v2 = remaining
                break
        # Check if string ends with value2 and the rest is value1
        elif temp_values_str.endswith(val1_candidate):
            remaining = temp_values_str[:-len(val1_candidate)]
            if remaining in CORE_VALUES:
                v1 = remaining
                v2 = val1_candidate
                break  # Found a valid pair

    # Second attempt: case-insensitive matching if first attempt failed
    if v1 is None or v2 is None:
        temp_values_str_lower = temp_values_str.lower()
        for val1_candidate in sorted_core_values:
            val1_lower = val1_candidate.lower()
            # Check if string starts with value1 (case insensitive)
            if temp_values_str_lower.startswith(val1_lower):
                remaining = temp_values_str[len(val1_lower):]
                for val2_candidate in CORE_VALUES:
                    if remaining.lower() == val2_candidate.lower():
                        v1 = val1_candidate  # Use original case
                        v2 = val2_candidate  # Use original case
                        break
                if v1 and v2:
                    break

    # Third attempt: splitting on capital letters
    if v1 is None or v2 is None:
        # Try splitting based on internal uppercase letters as fallback
        potential_split = re.split(r'(?<=[a-z])(?=[A-Z])', temp_values_str)
        if len(potential_split) == 2:
            # Check if the split parts match core values (case insensitive)
            part1, part2 = potential_split
            for val1 in CORE_VALUES:
                if part1.lower() == val1.lower():
                    for val2 in CORE_VALUES:
                        if part2.lower() == val2.lower():
                            v1 = val1  # Use original case
                            v2 = val2  # Use original case
                            break
                    if v1 and v2:
                        break

    # Fourth attempt: find any two core values in the string
    if v1 is None or v2 is None:
        found_values = []
        for value in CORE_VALUES:
            if value.lower() in temp_values_str.lower():
                found_values.append(value)

        if len(found_values) >= 2:
            v1 = found_values[0]
            v2 = found_values[1]

    # If we still couldn't find two values, return an error
    if v1 is None or v2 is None:
        return f"PARSE_ERROR: Could not identify values in '{original_label}'"

    # Standardize order (alphabetical)
    value1_alpha, value2_alpha = sorted([v1, v2])

    # Reconstruct the cleaned label
    cleaned_label = f"{prefix}-{value1_alpha}{value2_alpha}_{suffix}"

    return cleaned_label


# --- Main Processing Logic ---

print(f"Attempting to read Excel file: {INPUT_EXCEL_FILE}")

# Check if input file exists
if not os.path.exists(INPUT_EXCEL_FILE):
    print(f"Error: Input file not found at '{INPUT_EXCEL_FILE}'")
    exit()

try:
    # Read the specified sheet (or the first sheet if SHEET_NAME is None)
    df = pd.read_excel(INPUT_EXCEL_FILE, sheet_name = SHEET_NAME)
    print(f"Successfully read sheet '{SHEET_NAME if SHEET_NAME else 'Default'}' from {INPUT_EXCEL_FILE}.")
    print("\nDataFrame preview:")
    print(df.head())
    print("\nAll columns:")
    for i, col in enumerate(df.columns):
        print(f"  {i + 1}. {col}")

    # Define label columns as all columns from column number 14 to the end
    all_columns = list(df.columns)
    label_columns = all_columns[13:]  # 0-based indexing, so column 14 is at index 13

    if not label_columns:
        print("Warning: No columns were found from column 14 onwards.")
        print(f"Total columns: {len(all_columns)}")
        exit()

    print("\nColumns selected for processing (from column 14 onwards):")
    for i, col in enumerate(label_columns):
        print(f"  {i + 1}. {col}")

    # Print sample values from the first label column to help with debugging
    if label_columns:
        first_col = label_columns[0]
        print(f"\nSample values from first column to be processed ({first_col}):")
        sample_values = df[first_col].dropna().head(5).tolist()
        for i, val in enumerate(sample_values):
            print(f"  {i + 1}. {val}")

    print(f"Found {len(label_columns)} columns that appear to contain labels:")
    for col in label_columns:
        print(f"  - {col}")

    # Process each identified label column
    total_errors = 0
    for column in label_columns:
        print(f"\nCleaning labels in column: '{column}'...")

        # Apply the cleaning function to the column
        # Use .astype(str) to handle potential numbers or NaNs in the column
        cleaned_labels = df[column].astype(str).apply(clean_and_refactor_label)

        # Count errors and collect error examples
        error_mask = cleaned_labels.str.startswith("PARSE_ERROR")
        error_count = error_mask.sum()
        total_errors += error_count

        if error_count > 0:
            print(f"  Warning: Encountered {error_count} parsing errors in column '{column}'.")

            # Show examples of errors (up to 3)
            error_examples = df.loc[error_mask, column].head(3).tolist()
            print("  Error examples:")
            for i, example in enumerate(error_examples):
                print(f"    {i + 1}. Original: '{example}'")
                print(f"       Error: '{cleaned_labels[error_mask].iloc[i]}'")

        # Replace the original column with the cleaned labels
        df[column] = cleaned_labels
        print(f"  Cleaned {len(cleaned_labels) - error_count} labels in column '{column}'.")

    if total_errors > 0:
        print(f"\nTotal parsing errors across all columns: {total_errors}")
        print("Rows with errors will show 'PARSE_ERROR...' in the output columns.")

    print("\nLabel cleaning completed for all identified columns.")

    # Write the modified DataFrame to a new Excel file
    print(f"Writing cleaned data to {OUTPUT_EXCEL_FILE}...")
    df.to_excel(OUTPUT_EXCEL_FILE, sheet_name = 'Cleaned Data', index = False)
    print(f"Successfully saved cleaned data to {OUTPUT_EXCEL_FILE}")

except FileNotFoundError:
    print(f"Error: Input file not found at '{INPUT_EXCEL_FILE}'")
except Exception as e:
    print(f"An error occurred: {e}")
