class Error(Exception):
    """Base class for our exceptions"""
    pass


class Unavailable(Error):
    """Raised when an external API (GHIBLI) is unavailable"""
    pass
