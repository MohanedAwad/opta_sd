class OptaSDAPIError(Exception):
    """Base exception for all opta-sdapi errors."""
    pass


class ConfigurationError(OptaSDAPIError):
    """Raised when the client is misconfigured (missing token / domain)."""
    pass


class APIError(OptaSDAPIError):
    """Raised when the OPTA API returns a non-2xx HTTP response."""

    def __init__(self, status_code: int, message: str = ""):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class ParseError(OptaSDAPIError):
    """Raised when the response body cannot be parsed."""
    pass


class MissingParameterError(OptaSDAPIError):
    """Raised when a required URL parameter is not set."""
    pass