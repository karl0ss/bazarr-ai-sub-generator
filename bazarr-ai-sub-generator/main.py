import os
import warnings
import tempfile
import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.files import filename, write_srt
from utils.ffmpeg import get_audio, add_subtitles_to_mp4
from utils.bazarr import get_wanted_episodes, get_episode_details, sync_series
from utils.sonarr import update_show_in_sonarr
from utils.whisper import WhisperAI


def process_episode(episode, model_args, args, audio_channel, sample_interval, processing_episodes, completed_episodes):
    """Process a single episode for subtitle generation."""
    episode_id = episode["sonarrEpisodeId"]

    try:
        # Double-check that this episode is still wanted before processing
        current_wanted = get_wanted_episodes()
        still_wanted = any(ep["sonarrEpisodeId"] == episode_id for ep in current_wanted["data"])

        if not still_wanted:
            processing_episodes.discard(episode_id)
            return f"Skipped (no longer wanted): {episode['seriesTitle']} - {episode['episode_number']}"

        print(f"Processing {episode['seriesTitle']} - {episode['episode_number']}")
        episode_data = get_episode_details(episode_id)
        audios = get_audio([episode_data["path"]], audio_channel, sample_interval)
        subtitles = get_subtitles(audios, tempfile.gettempdir(), model_args, args)

        add_subtitles_to_mp4(subtitles)
        update_show_in_sonarr(episode["sonarrSeriesId"])
        time.sleep(5)
        sync_series()

        processing_episodes.discard(episode_id)
        completed_episodes.append(episode_id)
        return f"Completed: {episode['seriesTitle']} - {episode['episode_number']}"
    except Exception as e:
        processing_episodes.discard(episode_id)
        return f"Failed {episode['seriesTitle']} - {episode['episode_number']}: {str(e)}"


def process(args: dict):
    model_name: str = args.pop("model")
    language: str = args.pop("language")
    sample_interval: str = args.pop("sample_interval")
    audio_channel: str = args.pop("audio_channel")
    workers: int = args.pop("workers", 1)

    if model_name.endswith(".en"):
        warnings.warn(
            f"{model_name} is an English-only model, forcing English detection."
        )
        args["language"] = "en"
    # if translate task used and language argument is set, then use it
    elif language != "auto":
        args["language"] = language

    model_args = {}
    model_args["model_size_or_path"] = model_name
    model_args["device"] = args.pop("device")
    model_args["compute_type"] = args.pop("compute_type")

    list_of_episodes_needing_subtitles = get_wanted_episodes()
    print(
        f"Found {list_of_episodes_needing_subtitles['total']} episodes needing subtitles."
    )
    print(f"Processing with {workers} concurrent worker(s)...")

    # Thread-safe tracking of episodes being processed and completed
    processing_episodes = set()
    completed_episodes_list = []
    total_episodes = len(list_of_episodes_needing_subtitles["data"])

    # Filter episodes to avoid duplicates and respect concurrent processing limits
    episodes_to_process = []
    for episode in list_of_episodes_needing_subtitles["data"]:
        episode_id = episode["sonarrEpisodeId"]
        if episode_id not in processing_episodes:
            processing_episodes.add(episode_id)
            episodes_to_process.append(episode)

    print(f"Starting processing of {len(episodes_to_process)} unique episodes...")

    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Submit episodes for processing with tracking sets
        future_to_episode = {
            executor.submit(process_episode, episode, model_args, args, audio_channel, sample_interval, processing_episodes, completed_episodes_list): episode
            for episode in episodes_to_process
        }

        # Collect results as they complete
        completed_count = 0
        for future in as_completed(future_to_episode):
            completed_count += 1
            result = future.result()
            print(f"[{completed_count}/{total_episodes}] {result}")

    print(f"Processing complete. {len(completed_episodes_list)} episodes processed successfully.")


def get_subtitles(
    audio_paths: list, output_dir: str, model_args: dict, transcribe_args: dict
):
    model = WhisperAI(model_args, transcribe_args)

    subtitles_path = {}

    for path, audio_path in audio_paths.items():
        print(f"Generating subtitles for {filename(path)}... This might take a while.")
        srt_path = os.path.join(output_dir, f"{filename(path)}.srt")

        segments = model.transcribe(audio_path)

        with open(srt_path, "w", encoding="utf-8") as srt:
            write_srt(segments, file=srt)

        subtitles_path[path] = srt_path

    return subtitles_path
