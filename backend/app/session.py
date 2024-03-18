class Session:
    def __init__(self):
        self.current_time = 0
        self.user_active = False

    def upload_file(self, audio_file_data: bytes) -> None:
        pass

    def set_time(self, seconds: int) -> None:
        self.current_time = seconds

    def set_user_active(self, active: bool) -> None:
        self.user_active = active

    def show_ads(self) -> bool:
        return self.is_user_active() and self.is_audio_moment_appropriate()

    def is_user_active(self) -> bool:
        return self.user_active

    def is_audio_moment_appropriate(self) -> bool:
        return self.current_time > 5


session = Session()
