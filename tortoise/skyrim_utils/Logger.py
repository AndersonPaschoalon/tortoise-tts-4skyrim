import logging
import sys

class LoggingStream:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self.linebuf = ''

    def write(self, buf):
        for line in buf.rstrip().splitlines():
            self.logger.log(self.log_level, line.rstrip())

    def flush(self):
        pass  # No action needed, just here to satisfy file-like object interface

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

# Redirect stdout to logging
sys.stdout = LoggingStream(logger, logging.INFO)

# Redirect stderr to logging as warnings
sys.stderr = LoggingStream(logger, logging.WARNING)

# Test logging
print("This is an info message.")
raise ValueError("This is a warning message.")  # This will be captured as a warning
