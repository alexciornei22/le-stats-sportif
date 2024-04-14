Ciornei Alexandru-Ștefan 334CD

# Le Stats Sportif

### Summary

The app initializes the core data structures and objects, including the DataIngestor which parses the given csv file and stores the data within it.
When the server receives a query request it submits the corresponding task to a ThreadPoolExecutor, gives it a `job_id`, logs the request data and returns
the job_id for the response. In the `get_results` endpoint, the server checks if the job's corresponding `future` object has finished and reads it's result from the output file or
returns a still running status message if necessary. When the graceful_shutdown request is sent, the ThreadPoolExecutor is shut down, waits for the remaining jobs to finish and does
not allow further jobs to be submitted, allowing the app to be stopped safely.

### Implementation

The source code files are located in the [/app](/app) directory and implement following functionalities:
- [__init__.py](/app/__init__.py) Initializes the important data structures used by the API (the DataIngestor, ThreadPoolExecutor, job dictionary and counter)
- [data_ingestor.py](/app/data_ingestor.py) Contains the classes used to read and store the information from the csv dataset using [csv.DictReader](https://docs.python.org/3/library/csv.html#csv.DictReader)
and offers several methods to easily retrieve that data in the other parts of the app.
- [queries.py](/app/queries.py) Methods for each query job to be submitted to the ThreadPoolExecutor and helper/wrapper methods
- [routes.py](/app/routes.py) The Flask routes and endpoints used to create a query job and retrieve it's results
- [log.py](/app/log.py) Defines and initializes the logger using a [RotatingFileHandler](https://docs.python.org/3/library/logging.handlers.html#rotatingfilehandler)
and GMT time formatting
