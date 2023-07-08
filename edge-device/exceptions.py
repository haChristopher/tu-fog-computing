"""List of custom exeptions for the edge device"""

class NoAckException(Exception):
    "Raised when no or the wrong ACK is received"
    pass

class ConnectionError(Exception):
    "Raised when the client cant connect to the server"
    pass