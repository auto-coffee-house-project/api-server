class ObjectDoesNotExistError(Exception):
    """Raised when the object does not exist in the DB."""

    def __init__(self, message: str, **kwargs):
        """
        Args:
            message: Message to be displayed.
            **params: Passed arguments to retrieve the object from DB.
        """
        self.message = message
        self.kwargs = kwargs
        super().__init__(self.message)
