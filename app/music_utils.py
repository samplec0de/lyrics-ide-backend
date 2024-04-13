"""Модуль для работы с музыкальными файлами"""
import asyncio
import json
from asyncio import subprocess
from tempfile import NamedTemporaryFile

from aubio import source, tempo  # pylint: disable=no-name-in-module
from ffmpeg.asyncio import FFmpeg
from numpy import median, diff


# pylint: disable=too-many-locals
async def get_file_bpm(path) -> int | None:
    """Определение BPM для музыкального файла"""
    win_s = 512  # fft size
    hop_s = win_s // 2  # hop size
    samplerate = 44100

    with NamedTemporaryFile(suffix=".wav") as temporary_file:
        temporary_file_path = temporary_file.name
        ffmpeg_process = FFmpeg().option("y").input(path).output(temporary_file_path)
        await ffmpeg_process.execute()

        audio_source = source(temporary_file_path, hop_size=hop_s)
        samplerate = audio_source.samplerate
        tempo_detector = tempo("specdiff", win_s, hop_s, samplerate)

        beat_times = []
        total_audio_frames = 0

        while True:
            audio_samples, frames_read = audio_source()
            beat_detected = tempo_detector(audio_samples)
            if beat_detected:
                current_beat_time = tempo_detector.get_last_s()
                beat_times.append(current_beat_time)
                if total_audio_frames == 0 or beat_detected[0] == 1:
                    print(current_beat_time)
            total_audio_frames += frames_read
            if frames_read < hop_s:
                break

        if len(beat_times) > 1:
            beats_per_minute = 60.0 / diff(beat_times)
            return int(median(beats_per_minute))
        return None


# pylint: enable=too-many-locals


async def get_song_duration(file_path) -> float | None:
    """Определение длительности музыкального файла"""
    cmd = ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", file_path]

    process = await asyncio.create_subprocess_exec(*cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    stdout, stderr = await process.communicate()
    print(stderr.decode())

    if process.returncode != 0:
        return None

    result = json.loads(stdout.decode())
    duration = float(result["format"]["duration"])
    return duration
