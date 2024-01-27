from tempfile import NamedTemporaryFile

from aubio import source, tempo
from ffmpeg.asyncio import FFmpeg
from numpy import median, diff


async def get_file_bpm(path, params=None):
    """Определение BPM для музыкального файла"""
    if params is None:
        params = {}
    win_s = params.get('win_s', 512)               # fft size
    hop_s = params.get('hop_s', win_s // 2)        # hop size
    samplerate = params.get('samplerate', 44100)

    with NamedTemporaryFile(suffix=".wav") as temp_file:
        temp_file_path = temp_file.name
        ffmpeg = (
            FFmpeg()
            .option("y")
            .input(path)
            .output(temp_file_path)
        )
        await ffmpeg.execute()

        s = source(path, samplerate, hop_s)
        samplerate = s.samplerate
        o = tempo("specdiff", win_s, hop_s, samplerate)

        # List of beats, in samples
        beats = []
        # Total number of frames read
        total_frames = 0

        while True:
            samples, read = s()
            is_beat = o(samples)
            if is_beat:
                this_beat = o.get_last_s()
                beats.append(this_beat)
                # if first beat or beat found on first frame
                if total_frames == 0 or is_beat[0] == 1:
                    print("%f" % this_beat)
            total_frames += read
            if read < hop_s:
                break

        # Convert to periods and to bpm
        if len(beats) > 1:
            bpms = 60. / diff(beats)
            return median(bpms)
        else:
            return 0
