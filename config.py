import os
from threading import Lock
from dotenv import load_dotenv

"""
This file is for global configurations.
Message broker url, other environment path are included here.
"""

class Config:
    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(Config, cls).__new__(cls)
                    cls._instance.load_config()
        return cls._instance

    def load_config(self):
        load_dotenv()  # Load environment variables from .env file
        self.REDIS_URL = os.getenv("REDIS_URL")

        self.STATIC_DATA_PATH=os.getenv("STATIC_DATA_PATH")
        self.TEMPLATE_PATH=os.getenv("TEMPLATE_PATH")

        self.SENSOR_DATA_PATH_R=os.getenv("SENSOR_DATA_PATH_R")
        self.SENSOR_DATA_PATH_W=os.getenv("SENSOR_DATA_PATH_W")
        # Load more variables as needed

# Create a singleton instance
CONFIG_GLOB = Config()
