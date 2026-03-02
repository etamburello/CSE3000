from sunau import AUDIO_UNKNOWN_SIZE
import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    quasi_columns = ["age", "gender", "zip3"]
    merged = pd.merge(anon_df, aux_df, on=quasi_columns)

    uniques = merged[merged.groupby(quasi_columns)["age"].transform("count") == 1]

    anon_id = anon_df.columns[0]
    aux_id = aux_df.columns[0]
    return uniques[[anon_id, aux_id]].rename(columns={anon_id: "anon_id", aux_id: "matched_name"})


def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    total = len(anon_df)
    matched = len(matches_df)
    return matched/total