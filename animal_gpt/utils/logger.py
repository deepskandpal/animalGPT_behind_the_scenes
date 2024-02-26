import logging
from logging.handlers import RotatingFileHandler
import time
import uuid
import pandas as pd
from  animal_gpt.utils.bq_class import BQ
from  animal_gpt.utils.config import (
    default_logs_db
)
import numpy as np

bq = BQ()
log_filename = f'logs/app_{time.strftime("%Y-%m-%d")}.log'

class Logs:
    def __init__(self, log_filename):
        self.log_formatter = logging.Formatter('%(message)s', datefmt='%Y-%m-%d %H:%M:%S')
        self.log_handler = RotatingFileHandler(log_filename, maxBytes=10*1024*1024, backupCount=5)
        self.log_handler.setFormatter(self.log_formatter)
        self.logger = logging.getLogger('my_logger')
        self.logger.setLevel(logging.INFO)
        self.logger.addHandler(self.log_handler)


    def log_info(self, log_entry):
        self.logger.info(log_entry)

    def read_log_file(self, log_filename):
        log_entries = []
        with open(log_filename, 'r') as log_file:
            for line in log_file:
                line = line.strip()
                if line:
                    try:
                        log_entry = eval(line)
                        log_entries.append(log_entry)
                    except Exception as e:
                        print(f"Error processing log entry: {e}")
        return pd.DataFrame(log_entries)
    
    def get_max_date_log(self):
        """
        TBD
        """
        pass


logger = Logs(log_filename)


def log(func):
    def wrapper(*args, **kwargs):
        # Call the original function
        output, probabilities, thumbs_value ,prompt_selected = func(*args, **kwargs)
        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
        # Log the activity
        user_input = args[0]  # Assuming user_input is the first argument
        act_id = str(uuid.uuid4())
        logs_dict = {
                'log_level': 'INFO',
                'timestamp': timestamp,
                'user_input': user_input,
                'thumbs_value': thumbs_value,  # You might want to adjust this based on your logic
                'response': output,
                'activity_id': act_id,
                'probability': probabilities,
                'prompt_selected':prompt_selected
            }
        logs = pd.DataFrame(
            data=logs_dict,
            index=[0]
        )

        logs = logs.fillna(np.nan)
        schema = {
            'log_level': str,
            'timestamp': str,
            'user_input': str,
            'thumbs_value': str,
            'response': str,
            'activity_id': str,
            'probability':float,
            'prompt_selected':str

        }
        logs = logs.astype(schema)

        # Print or save logs as needed
        # logger.log_info(logs_dict)
        bq.to_bq(logs, default_logs_db)

        return output

    return wrapper