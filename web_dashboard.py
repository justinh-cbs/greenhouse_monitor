#!/usr/bin/env python3
import csv
import os
from datetime import datetime, timedelta

DATA_FILE = "greenhouse_data.csv"
PORT = 8080

HTML_TEMPLATE = """
"""

class DataReader:
    @staticmethod
    def read_csv_data(filename):
        """Read data from the CSV file and return as a list of dictionaries"""
        if not os.path.exists(filename):
            return []

        data = []
        try:
            with open(filename, "r") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    data.append(row)
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return []

        return data

    @staticmethod
    def get_current_reading(data):
        """Get the most recent reading from the data"""
        if not data:
            return None
        return data[-1]

    @staticmethod
    def parse_timestamp(ts_str):
        """Parse timestamp string to datetime object"""
        try:
            return datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            return datetime.now()

    @staticmethod
    def get_timeframe_data(data, hours=None):
        """Filter data to only include readings from the last n hours, or all if hours is None"""
        if not data or hours is None:
            return data

        now = datetime.now()
        cutoff = now - timedelta(hours=hours)

        return [
            row for row in data if DataReader.parse_timestamp(row["timestamp"]) > cutoff
        ]
