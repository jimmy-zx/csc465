class Config:  # pylint: disable=too-few-public-methods
    def __init__(
            self,
            trace: bool = False,
            debug: bool = False,
    ) -> None:
        self.trace = trace
        self.debug = debug


config = Config()
