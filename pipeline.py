from prefect import flow, task, get_run_logger
from src.data_collection import collect_data
from src.data_preprocessing import preprocess_data
from src.data_storage import create_tables, insert_data_from_csv
import pandas as pd

@task
def collect_data_task():
    collect_data()

@task
def preprocess_data_task():
    raw_data_path = 'data/raw/moscow_flats_dataset.csv'
    processed_data_path = 'data/preprocessed/moscow_flats_dataset_preprocessing.csv'
    preprocess_data(pd.read_csv(raw_data_path),processed_data_path)

@task
def store_data_task():
    create_tables()
    insert_data_from_csv('data/preprocessed/moscow_flats_dataset_preprocessing.csv')

@flow
def analytics_pipeline():
    logger = get_run_logger()
    logger.info('Начало сбора данных')
    collect_data_task()
    logger.info('Конец сбора данных')
    logger.info('Начало обработки данных')
    preprocess_data_task()
    logger.info('Конец обработки данных')
    logger.info('Начало загрузки данных в БД')
    store_data_task()
    logger.info('Конец загрузки данных в БД')

if __name__ == "__main__":
    analytics_pipeline()
