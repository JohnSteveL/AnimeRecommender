from utils.common import read_yaml
from config.path_config import *

from src.data_processing import DataProcessor
from src.model_trainer import ModelTrainer

if __name__=="__main__":
    data_processor = DataProcessor(ANIMELIST_CSV,PROCESSED_DIR)
    data_processor.run()

    model_trainer = ModelTrainer(CONFIG_PATH,PROCESSED_DIR)
    model_trainer.train_model()