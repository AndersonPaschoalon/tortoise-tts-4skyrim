"""
Custom exception I create for my scripts.
"""

class InvalidCSVFormatException(Exception):
    pass


class InvalidVoiceTypeException(Exception):
    pass


class InvalidEmotionException(Exception):
    pass


class InvalidIntensityException(Exception):
    pass


class InvalidTextException(Exception):
    pass


class InvalidFilePathException(Exception):
    pass