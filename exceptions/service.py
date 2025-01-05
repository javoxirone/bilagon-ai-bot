class ServerError(Exception):
    """
    ServerError exception, raised when a service catches an error from db or any other lower level of a program.
    """

    def __init__(self, message: str = "No additional message"):
        """
        Initialize the custom ServerError exception object.

        :param message: Additional message.
        :type message: str
        """
        super().__init__(f"Something went wrong on the server ({message})")
