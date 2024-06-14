import logging.config

LOGGING = {
    "version":1,
    "root":{
        "handlers" : ["console", "file"],
        "level": "INFO"
    },
    "handlers":{
        "console":{
            "formatter": "std_out",
            "class": "logging.StreamHandler",
            "level": "INFO"
        },
    "file": {
        "formatter": "std_out",
        "class": "logging.FileHandler",
        "level": "INFO",
        "filename": "logfile.log",
        "mode": "a",
        "encoding": "utf-8",
    },        
    },
    "formatters":{
        "std_out": {
            "format": "%(levelname)-7.7s %(asctime)s [%(name)s] %(message)s",
            "datefmt":"%Y-%m-%dT%H:%M:%S%z"
        }
    },
}

logging.config.dictConfig(LOGGING)
