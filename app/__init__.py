from concurrent.futures import ThreadPoolExecutor
from flask import Flask
from app.data_ingestor import DataIngestor

webserver = Flask(__name__)
webserver.tasks_runner = ThreadPoolExecutor()

data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

webserver.job_counter = 1

webserver.futures = {}
