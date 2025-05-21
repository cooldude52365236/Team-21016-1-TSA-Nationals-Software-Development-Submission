# This is Team No. 21016-1 submission for TSA Nationals 2025 Software Development. The website is https://ecoimpactnationalstsa2025.replit.app

import os
import pandas as pd
from sqlalchemy import create_engine, Column, Float, Integer, String, DateTime, Table, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

db_available = False
engine = None
session = None
metadata = None
environmental_metrics = None

SQLITE_URL = "sqlite:///agricultural_metrics.db"
logger.info(f"Setting up SQLite database at {SQLITE_URL}")

try:
    engine = create_engine(SQLITE_URL)

    Session = sessionmaker(bind=engine)
    session = Session()

    metadata = MetaData()

    environmental_metrics = Table(
        'environmental_metrics', 
        metadata,
        Column('id', Integer, primary_key=True),
        Column('date', DateTime, nullable=False),
        Column('temperature', Float, nullable=False),
        Column('humidity', Float, nullable=False),
        Column('soil_moisture', Float, nullable=False),
        Column('water_usage', Float, nullable=False),
        Column('energy_consumption', Float, nullable=False),
    )

    metadata.create_all(engine)

    db_available = True
    logger.info("Successfully set up SQLite database")

except Exception as e:
    logger.error(f"Database setup error: {e}")
    logger.info("Falling back to sample data")

def load_data_from_db():
    if not db_available:
        logger.info("Database not available, using sample data")
        from data.sample_data import get_environmental_data
        return get_environmental_data()

    try:
        query = "SELECT * FROM environmental_metrics ORDER BY date"
        df = pd.read_sql(query, engine)

        if len(df) == 0:
            logger.info("No data in database, initializing with sample data")
            from data.sample_data import get_environmental_data
            sample_data = get_environmental_data()

            insert_data(sample_data)

            df = pd.read_sql(query, engine)

        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date'])
            logger.info("Converted date column to datetime")

        return df
    except Exception as e:
        logger.error(f"Error loading data from database: {e}")

        from data.sample_data import get_environmental_data
        return get_environmental_data()

def insert_data(df):
    if not db_available:
        logger.warning("Database not available, cannot insert data")
        return

    try:
        df_copy = df.copy()

        if 'date' in df_copy.columns:
            df_copy['date'] = pd.to_datetime(df_copy['date'])

        df_copy.to_sql('environmental_metrics', engine, if_exists='append', index=False)
        logger.info(f"Inserted {len(df_copy)} records into database")
    except Exception as e:
        logger.error(f"Error inserting data into database: {e}")

def add_metrics_record(temperature, humidity, soil_moisture, water_usage, energy_consumption):
    if not db_available:
        logger.warning("Database not available, cannot add new metrics record")
        return False

    try:
        new_record = {
            'date': datetime.now(),
            'temperature': temperature,
            'humidity': humidity,
            'soil_moisture': soil_moisture,
            'water_usage': water_usage,
            'energy_consumption': energy_consumption
        }

        df = pd.DataFrame([new_record])
        insert_data(df)
        logger.info("Added new metrics record successfully")
        return True
    except Exception as e:
        logger.error(f"Error adding new metrics record: {e}")
        return False

def check_connection():
    if not db_available or engine is None:
        return False

    try:
        with engine.connect() as conn:
            return True
    except Exception as e:
        logger.error(f"Database connection check failed: {e}")
        return False
