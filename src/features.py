from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Sequence

import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix, hstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler

MANUAL_FEATURE_COLUMNS = [
    "has_url",
    "has_shorturl",
    "has_phone",
    "has_money",
    "has_bank_account",
    "bank_mention",
    "fraud_keyword_count",
    "exclamation_count",
    "capslock_ratio",
    "msg_length",
]


@dataclass
class FeatureBundle:
    matrix: csr_matrix
    text_vectorizer: TfidfVectorizer
    manual_feature_columns: List[str]
    scaler: StandardScaler | None = None
    log_msg_length: bool = True  # Whether msg_length was log-transformed
    msg_length_idx: int = -1  # Index of msg_length in manual features


def build_text_vectorizer(
    max_features: int = 5000,
    ngram_range: tuple[int, int] = (1, 2),
) -> TfidfVectorizer:
    return TfidfVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        lowercase=False,
        token_pattern=r"(?u)\b\w+\b",
    )


def _manual_feature_frame(df: pd.DataFrame, feature_columns: Sequence[str] = MANUAL_FEATURE_COLUMNS) -> pd.DataFrame:
    frame = df.reindex(columns=feature_columns).fillna(0.0)
    return frame.astype(float)


def build_feature_bundle(
    df: pd.DataFrame,
    text_col: str = "clean_text",
    feature_columns: Sequence[str] = MANUAL_FEATURE_COLUMNS,
    max_features: int = 5000,
    ngram_range: tuple[int, int] = (1, 2),
) -> tuple[FeatureBundle, csr_matrix]:
    if text_col not in df.columns:
        raise KeyError(f"Missing text column: {text_col}")

    texts = df[text_col].fillna("").astype(str)
    vectorizer = build_text_vectorizer(max_features=max_features, ngram_range=ngram_range)
    text_matrix = vectorizer.fit_transform(texts)
    
    # Xử lý manual features với log transform cho msg_length
    manual_frame = _manual_feature_frame(df, feature_columns=feature_columns)
    
    # Tìm index của msg_length
    msg_length_idx = -1
    if "msg_length" in manual_frame.columns:
        msg_length_idx = list(manual_frame.columns).index("msg_length")
    
    # Log transform msg_length: log(x + 1) để giảm phạm vi
    if msg_length_idx >= 0:
        manual_frame.iloc[:, msg_length_idx] = np.log1p(manual_frame.iloc[:, msg_length_idx])
    
    # StandardScaler cho tất cả features (bao gồm log-transformed msg_length)
    scaler = StandardScaler()
    manual_matrix_scaled = scaler.fit_transform(manual_frame)
    
    # Shift về positive range để compatible với sparse matrix
    manual_matrix_scaled = manual_matrix_scaled + 3
    
    # Giảm trọng số manual features xuống 0.5x để cân bằng với TF-IDF
    manual_matrix_scaled = manual_matrix_scaled * 0.5
    manual_matrix = csr_matrix(manual_matrix_scaled)
    
    matrix = hstack([text_matrix, manual_matrix], format="csr")
    bundle = FeatureBundle(
        matrix=matrix,
        text_vectorizer=vectorizer,
        manual_feature_columns=list(feature_columns),
        scaler=scaler,
        log_msg_length=True,
        msg_length_idx=msg_length_idx,
    )
    return bundle, matrix


def transform_feature_bundle(bundle: FeatureBundle, df: pd.DataFrame, text_col: str = "clean_text") -> csr_matrix:
    if text_col not in df.columns:
        raise KeyError(f"Missing text column: {text_col}")

    texts = df[text_col].fillna("").astype(str)
    text_matrix = bundle.text_vectorizer.transform(texts)
    
    manual_frame = _manual_feature_frame(df, feature_columns=bundle.manual_feature_columns)
    
    # Apply log transform to msg_length (same as in training)
    if bundle.log_msg_length and bundle.msg_length_idx >= 0:
        manual_frame.iloc[:, bundle.msg_length_idx] = np.log1p(manual_frame.iloc[:, bundle.msg_length_idx])
    
    if bundle.scaler is not None:
        manual_matrix_scaled = bundle.scaler.transform(manual_frame)
        # Shift về positive range
        manual_matrix_scaled = manual_matrix_scaled + 3
        manual_matrix_scaled = manual_matrix_scaled * 0.5
    else:
        manual_matrix_scaled = manual_frame.to_numpy()
        
    manual_matrix = csr_matrix(manual_matrix_scaled)
    return hstack([text_matrix, manual_matrix], format="csr")


def feature_names(bundle: FeatureBundle) -> List[str]:
    text_features = list(bundle.text_vectorizer.get_feature_names_out())
    return text_features + list(bundle.manual_feature_columns)
