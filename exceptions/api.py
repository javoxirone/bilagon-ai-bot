class APIServerError(Exception):
    """
    Represents an error related to an external API server.

    This exception is used to encapsulate errors happening during interactions
    with an external API server. It provides a detailed error message describing
    the nature of the issue.

    :ivar message: The error message describing the specific issue with the
        API interaction.
    :type message: str
    """
    def __init__(self, message: str = "No additional message"):
        """
        Represents a custom exception raised when interacting with an external API.

        This exception provides additional context regarding issues that
        occurred during API interaction by allowing an optional message to
        be specified.

        :param message: A string message providing additional details about the
            API-related issue.
        """
        super().__init__(f"Something went wrong while working with external API ({message})")
