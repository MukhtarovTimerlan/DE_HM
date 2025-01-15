from sqlalchemy import create_engine, Column, Integer, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd


DATABASE_URL = 'sqlite:///db/apartments.db'
engine = create_engine(DATABASE_URL, echo=True)
Base = declarative_base()

class Apartment(Base):
    __tablename__ = 'apartments'

    id = Column(Integer, primary_key=True)
    price = Column(Float)
    min_to_metro = Column(Float)
    floor = Column(Float)
    construction_year = Column(Float)
    is_new = Column(Float)
    is_apartments = Column(Float)
    ceiling_height = Column(Float)
    number_of_rooms = Column(Float)
    reg_ЗАО = Column(Boolean)
    reg_САО = Column(Boolean)
    reg_СВАО = Column(Boolean)
    reg_СЗАО = Column(Boolean)
    reg_ЦАО = Column(Boolean)
    reg_ЮАО = Column(Boolean)
    reg_ЮВАО = Column(Boolean)
    reg_ЮЗАО = Column(Boolean)


def create_tables():
    Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

def insert_data_from_csv(file_path):
    """
    Загружает данные из CSV-файла и сохраняет их в базе данных.
    """
    session = Session()

    df = pd.read_csv(file_path)

    apartments = [
        Apartment(
            price=row['price'],
            min_to_metro=row['min_to_metro'],
            floor=row['floor'],
            construction_year=row['construction_year'],
            is_new=bool(row['is_new']),
            is_apartments=bool(row['is_apartments']),
            ceiling_height=row['ceiling_height'],
            number_of_rooms=row['number_of_rooms'],
            reg_ЗАО=bool(row['reg_ЗАО']),
            reg_САО=bool(row['reg_САО']),
            reg_СВАО=bool(row['reg_СВАО']),
            reg_СЗАО=bool(row['reg_СЗАО']),
            reg_ЦАО=bool(row['reg_ЦАО']),
            reg_ЮАО=bool(row['reg_ЮАО']),
            reg_ЮВАО=bool(row['reg_ЮВАО']),
            reg_ЮЗАО=bool(row['reg_ЮЗАО'])
        )
        for _, row in df.iterrows()
    ]

    session.bulk_save_objects(apartments)
    session.commit()
    session.close()

def query_apartments(max_price: float):
    """
    Выполняет запрос к базе данных для получения квартир с ценой ниже max_price.
    """
    session = Session()
    results = session.query(Apartment).filter(Apartment.price < max_price).all()
    session.close()
    return results
