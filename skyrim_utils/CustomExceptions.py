

class InvalidCSVFormatException(Exception):
    """
    Invalid CSV file format.
    """
    pass


class InvalidVoiceTypeException(Exception):
    """
    Invalid voice type choosen. This means there is not sample available for this voice type.
    """
    pass


class InvalidEmotionException(Exception):
    """
    Invalid emotion selected. This means the selected emotion cannot be prompt-enginiered.
    """
    pass


class InvalidIntensityException(Exception):
    """
    Invalid intensity selected. Valid values range from 0 to 100.
    """
    pass


class InvalidTextException(Exception):
    """
    Invalid text selected.
    """
    pass


class InvalidFilePathException(Exception):
    """
    Selected path does not exists or is invalid.
    """
    pass
