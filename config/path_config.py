import os
from pathlib import Path

'''
DATA INGESTION
'''

RAW_DIR = Path("artifacts/raw")
CONFIG_PATH = Path("config/config.yaml")

ANIMELIST_CSV = RAW_DIR / "animelist.csv"
ANIME_CSV = RAW_DIR / "anime.csv"
ANIMESYNOPSIS_CSV = RAW_DIR / "anime_with_synopsis.csv"

'''
DATA PROCESSING
'''

PROCESSED_DIR = Path("artifacts/processed")

X_TRAIN_ARRAY = PROCESSED_DIR / "X_train_array.pkl"
X_TEST_ARRAY = PROCESSED_DIR / "X_test_array.pkl"
Y_TRAIN = PROCESSED_DIR / "y_train.pkl"
Y_TEST = PROCESSED_DIR / "y_test.pkl"

RATING_DF = PROCESSED_DIR / "rating.csv"
DF = PROCESSED_DIR / "anime_df.csv"
SYNOPSIS_DF = PROCESSED_DIR / "synopsis_df.csv"

USER2USER_ENCODED = PROCESSED_DIR / "user2user_encoded.pkl"
USER2USER_DECODED = PROCESSED_DIR / "user2user_decoded.pkl"

ANIME2ANIME_ENCODED = PROCESSED_DIR / "anime2anime_encoded.pkl"
ANIME2ANIME_DECODED = PROCESSED_DIR / "anime2anime_decoded.pkl"

'''
MODEL TRAINING
'''
MODEL_DIR = Path("artifacts/model")
WEIGHTS_DIR = Path("artifacts/weights")
CHECKPOINT_DIR = Path("artifacts/model_checkpoint")

MODEL_PATH = MODEL_DIR / "model.h5"
ANIME_WEIGHTS_PATH = WEIGHTS_DIR / "anime_weights.pkl"
USER_WEIGHTS_PATH = WEIGHTS_DIR / "user_weights.pkl"
CHECKPOINT_FILE_PATH = CHECKPOINT_DIR / "weights.weights.h5"