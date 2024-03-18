from prometheus_client import Gauge

from app.session import session

current_time_gauge = Gauge("current_time", "Current time in the audio.")
user_active_gauge = Gauge("user_active", "User activity.")
audio_moment_appropriate_gauge = Gauge("audio_moment_appropriate", "Audio moment appropriate.")
show_ads_gauge = Gauge("show_ads", "Show ads.")


def update_metrics():
    """
    Function to update the metrics.
    """
    current_time_gauge.set(session.current_time)
    user_active_gauge.set(int(session.is_user_active()))
    audio_moment_appropriate_gauge.set(int(session.is_audio_moment_appropriate()))
    show_ads_gauge.set(int(session.show_ads()))
