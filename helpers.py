from rapidfuzz import process, fuzz
import pandas as pd

# Normalize – lowercase, strip whitespace, remove periods/punctuation
def normalize_feature(feature):
    normalized = (
        feature
        .astype(str)
        .str.lower()
        .str.strip()
        .str.replace(r'[^\w\s]', '', regex=True)
    )
    return normalized

# Mapping abbreviations and known variations
def map_variations(feature, variation_mapping):
    mapped_feature = feature.replace(variation_mapping)
    return mapped_feature

# Function to snap typos to the closest official value
def standardize_feature(val, choices, threshold=85):
    if pd.isna(val) or val in choices:
        return val
    
    # Find the best match
    match, score, _ = process.extractOne(val, choices, scorer=fuzz.WRatio)
    
    # Only replace if the similarity score is above the threshold (0-100)
    return match if score >= threshold else val

# Fuzzy matching for typos
# fuzzy_list = "source of truth" list of valid values
def fuzzy_match(feature, fuzzy_list):
    unique_vals = feature.unique()
    fuzzy_map = {val: standardize_feature(val, fuzzy_list) for val in unique_vals}
    
    mapped_feature = feature.map(fuzzy_map)
    return mapped_feature

# cleans the categorical data of a feature column
def clean_category_feature(feature, variation_mapping, fuzzy_list):
    normalized = normalize_feature(feature)
    mapped_feature = map_variations(normalized, variation_mapping)
    cleaned_feature = fuzzy_match(mapped_feature, fuzzy_list)
    return cleaned_feature

# Return a side-by-side comparison of everything that was modified
# Combine original and cleaned into a temporary audit table
def audit_changes(cleaned_feature, original_feature):
    audit_df = pd.DataFrame({
        'before': original_feature,
        'after': cleaned_feature
    })

    changed = audit_df[audit_df['before'].str.lower().str.strip() != audit_df['after']]

    audit_summary = (
        changed
        .value_counts(dropna=False)
        .reset_index(name='row_count')
    )

    return audit_summary

# Print side-by-side comparison and unique values of the feature
def print_audit_summary(cleaned_feature, original_feature):
    audit_summary = audit_changes(cleaned_feature, original_feature)

    print(audit_summary.to_string(index=False))
    print(cleaned_feature.value_counts().head(50))