import logging

""" Custom formatter for weather warnings, alerts and maintenance"""
class WeatherStationFormatter(logging.Formatter):

    grey = "\x1b[38;20m"
    green = "\x1b[32;20m"
    yellow = "\x1b[33;20m"
    orange = "\x1b[38;5;208;20m"
    red = "\x1b[31;20m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"
    format = "%(asctime)s - %(levelname)s - %(message)s"

    # Complete missues of logging levels :)
    FORMATS = {
        logging.DEBUG: grey + format + reset, # Code messages sent
        logging.INFO: green + format + reset, # No critical messages
        logging.WARNING: orange + format + reset, # Weather warnings
        logging.ERROR: red + format + reset, # Alerts
        logging.CRITICAL: bold_red + format + reset # Critical alerts
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)