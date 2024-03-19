import math

from app.detector import NLPModel

class Session:
    def __init__(self):
        self.current_time = 0
        self.user_active = False
        self.intervals = []

    def upload_file(self, audio_file_data: bytes) -> None:
        path = "file"
        with open(path, "wb") as audio_file:
            audio_file.write(audio_file_data)
        self.intervals = NLPModel().detect(path)

    def set_time(self, seconds: int) -> None:
        self.current_time = seconds

    def set_user_active(self, active: bool) -> None:
        self.user_active = active

    def is_user_active(self) -> bool:
        return self.user_active

    def is_audio_moment_appropriate(self) -> bool:
        for start, end in self.intervals:
            if int(start) <= self.current_time <= math.ceil(end):
                return True
        return False

    def time_until_appropriate_moment(self) -> int:
        for start, end in self.intervals:
            if int(start) > self.current_time:
                return int(start - self.current_time)
        return -1

    def show_ads(self) -> bool:
        return self.is_user_active() and self.is_audio_moment_appropriate()


session = Session()
