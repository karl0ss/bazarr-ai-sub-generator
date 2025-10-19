import os
import tempfile
import ffmpeg
from .files import filename


def get_audio(paths: list, audio_channel_index: int, sample_interval: list):
    temp_dir = tempfile.gettempdir()

    audio_paths = {}

    for path in paths:
        print(f"Extracting audio from {filename(path)}...")
        output_path = os.path.join(temp_dir, f"{filename(path)}.wav")

        ffmpeg_input_args = {}
        if sample_interval is not None:
            ffmpeg_input_args["ss"] = str(sample_interval[0])

        ffmpeg_output_args = {}
        ffmpeg_output_args["acodec"] = "pcm_s16le"
        ffmpeg_output_args["ac"] = "1"
        ffmpeg_output_args["ar"] = "16k"
        ffmpeg_output_args["map"] = "0:a:" + str(audio_channel_index)
        if sample_interval is not None:
            ffmpeg_output_args["t"] = str(sample_interval[1] - sample_interval[0])

        ffmpeg.input(path, **ffmpeg_input_args).output(
            output_path, **ffmpeg_output_args
        ).run(quiet=True, overwrite_output=True)

        audio_paths[path] = output_path

    return audio_paths


def add_subtitles_to_mp4(subtitles: dict):
    input_file = list(subtitles.keys())[0]
    subtitle_file = subtitles[input_file]
    output_file = input_file
    os.rename(input_file, input_file + "_edit")

    input_stream = ffmpeg.input(input_file + "_edit")
    subtitle_stream = ffmpeg.input(subtitle_file)

    # Combine input video and subtitle
    output = ffmpeg.output(
        input_stream,
        subtitle_stream,
        output_file.replace(".mkv", ".mp4"),
        c="copy",
        **{"c:s": "mov_text"},
        **{"metadata:s:s:0": "language=eng"},
    )
    ffmpeg.run(output, quiet=True, overwrite_output=True)
    os.remove(input_file + "_edit")
    # remove tempfiles
    os.remove(subtitle_file)
    os.remove(subtitle_file.replace(".srt", ".wav"))
