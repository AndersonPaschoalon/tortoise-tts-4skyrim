import logging
import sys
import os

class LoggingStream:

    _is_initialize = False
    _stdout_bkp = None
    _stderr_bkp = None
    _logger = None

    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass  # No action needed, just here to satisfy file-like object interface

    @staticmethod
    def initialize(log_dir="", log_file="app.log"):
        """
        Initialize the LoggingStream, so the print messages will be redirected to a log file.
        """
        if log_dir.strip() != "":
            os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, log_file)

        print(f"Using log_file {log_file}")
        if not LoggingStream._is_initialize:
            # Set up logging
            logging.basicConfig(
                level=logging.DEBUG,
                format='%(asctime)s [%(levelname)s] %(message)s',
                handlers=[
                    logging.FileHandler(log_file_path),
                    logging.StreamHandler(sys.stdout)
                ]
            )
            LoggingStream._stdout_bkp = sys.stdout
            LoggingStream._stderr_bkp = sys.stderr

            LoggingStream._logger = logging.getLogger(__name__)

            # Redirect stdout to logging
            sys.stdout = LoggingStream(LoggingStream._logger, logging.INFO)

            # Redirect stderr to logging as warnings
            sys.stderr = LoggingStream(LoggingStream._logger, logging.ERROR)

            LoggingStream._is_initialize = True

    @staticmethod
    def finalize():
        """
        Reset the LoggingStream class.
        """
        sys.stdout = LoggingStream._stdout_bkp
        sys.stderr = LoggingStream._stderr_bkp
        LoggingStream._is_initialize = False

    @staticmethod
    def debug(message):
        if LoggingStream._logger:
            LoggingStream._logger.debug(message)

    @staticmethod
    def info(message):
        if LoggingStream._logger:
            LoggingStream._logger.info(message)

    @staticmethod
    def warning(message):
        if LoggingStream._logger:
            LoggingStream._logger.warning(message)

    @staticmethod
    def error(message):
        if LoggingStream._logger:
            LoggingStream._logger.error(message)

    @staticmethod
    def critical(message):
        if LoggingStream._logger:
            LoggingStream._logger.critical(message)

"""
# Example usage
LoggingStream.initialize()

print("This is an info message.")
LoggingStream.debug("This is a debug message.")
LoggingStream.info("This is an info message.")
LoggingStream.warning("This is a warning message.")
LoggingStream.error("This is an error message.")
LoggingStream.critical("This is a critical message.")

try:
    raise ValueError("This is an error message raised as an exception.")
except ValueError as e:
    LoggingStream.error(f"Exception caught: {e}")

LoggingStream.finalize()

print("This is a regular print message.")

"""


