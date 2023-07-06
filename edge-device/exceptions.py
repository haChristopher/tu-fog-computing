"""List of custom exeptions for the edge device"""

class NoAckException(Exception):
    "Raised when no or the wrong ACK is received"
    pass
