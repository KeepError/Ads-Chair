import whisper
import numpy as np
import app.nlp_config as cfg


class NLPModel:
    def __init__(self):
        self.model = whisper.load_model(cfg.MODEL_SIZE, device=cfg.DEVICE)

    def detect(self, audio: str | np.ndarray):
        if isinstance(audio, np.ndarray):
            audio = audio.astype(np.float32)

        transcript = self.model.transcribe(audio, word_timestamps=True, verbose=True)
        return self._get_intervals(transcript)

    @staticmethod
    def _get_intervals(transcript, word_level=False):
        boundaries = []
        for segment in transcript['segments']:
            if word_level:
                for word in segment['words']:
                    boundaries.append([word['start'], word['end']])
            else:
                boundaries.append([segment['start'], segment['end']])

        pauses = [(s2[0] - s1[1], s1[1], s2[0]) for s1, s2 in zip(boundaries, boundaries[1:])]
        intervals = [p[1:] for p in pauses if p[0] > cfg.DETECTION_THRESHOLD_SEC]

        if not intervals:
            return [p[1:] for p in sorted(pauses, key=lambda x: x[0])[-3:]]

        return intervals
