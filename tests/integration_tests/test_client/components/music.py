class Music:
    """Музыка"""
    def __init__(
            self,
            url: str,
            duration_seconds: float,
            bpm: int | None,
            custom_bpm: int | None,
    ):
        self.url = url
        self.duration_seconds = duration_seconds
        self.bpm = bpm
        self.custom_bpm = custom_bpm
