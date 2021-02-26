import os
import logging

from os.path import join, exists
from pathlib import Path

# ==============================================================================
# ServiceLogger
# ==============================================================================


class ServiceLogger():
    '''
    Interface method to log data for this service
    '''
# |----------------------------------------------------------------------------|
# Class Variables
# |----------------------------------------------------------------------------|
    _singleton = None

# |----------------------------------------------------------------------------|
# Constructor
# |----------------------------------------------------------------------------|
    def __init__(self):
        if ServiceLogger._singleton is not None:
            raise Exception("This is a singleton class")
        else:
            ServiceLogger._singleton = self
            self._service_name = ""

# |---------------------------End of Constructor------------------------------|

# |----------------------------------------------------------------------------|
# get
# |----------------------------------------------------------------------------|
    @staticmethod
    def get():
        if ServiceLogger._singleton is None:
            ServiceLogger()
        return ServiceLogger._singleton

# |------------------------------End of get-----------------------------------|

# |----------------------------------------------------------------------------|
# initialize
# |----------------------------------------------------------------------------|
    def initialize(self, service_name):
        self._service_name = service_name
        home_path = str(Path.home())
        service_log_path = join(home_path, "service_logs", self._service_name)
        if not exists(service_log_path):
            os.makedirs(service_log_path, exist_ok=True)

        service_log_filename = "{}.log".format(self._service_name)
        service_log_file_path = join(service_log_path, service_log_filename)

        # Create the logger.
        logger = logging.getLogger(self._service_name)
        logger.setLevel(logging.DEBUG)

        # Create formatter.
        formatter = logging.Formatter("[%(name)s] [%(asctime)s] "
                                      "[%(levelname)s] : %(message)s",
                                      datefmt='%d/%m/%Y %I:%M:%S %p')

        # Create console handler and set level to debug.
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(formatter)
        logger.addHandler(ch)

        fh = logging.FileHandler(service_log_file_path)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

# |----------------------End of initialize-----------------------------------|

# |----------------------------------------------------------------------------|
# log_debug
# |----------------------------------------------------------------------------|
    def log_debug(self, log_msg):
        if self._service_name:
            logger = logging.getLogger(self._service_name)
            logger.debug("{}".format(log_msg))

# |----------------------End of log_debug-------------------------------------|

# |----------------------------------------------------------------------------|
# log_info
# |----------------------------------------------------------------------------|
    def log_info(self, log_msg):
        if self._service_name:
            logger = logging.getLogger(self._service_name)
            logger.info("{}".format(log_msg))

# |----------------------End of log_info--------------------------------------|

# |----------------------------------------------------------------------------|
# log_error
# |----------------------------------------------------------------------------|
    def log_error(self, log_msg):
        if self._service_name:
            logger = logging.getLogger(self._service_name)
            logger.error("{}".format(log_msg))

# |----------------------End of log_error-------------------------------------|
