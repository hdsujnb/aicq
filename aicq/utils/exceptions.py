class ICQAPIError(Exception):
    def __init__(self, message):
        super().__init__(message)

class ValidationError(ICQAPIError):
    pass

class NetworkError(ICQAPIError):
    pass