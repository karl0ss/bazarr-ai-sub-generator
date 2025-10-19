# bazarr-ai-sub-generator

This is a fork of [faster-auto-subtitle](https://github.com/Sirozha1337/faster-auto-subtitle) using [faster-whisper](https://github.com/SYSTRAN/faster-whisper) implementation.

This repository uses `ffmpeg` and [OpenAI's Whisper](https://openai.com/blog/whisper) to automatically generate and overlay subtitles on any video.

This script will connect to your Bazarr instance to get a list of shows that require subtitles and start processing each video to create, by default Engligh subs, these are then written to the file as Soft subtitles.

It will then send an update to Sonarr and once that is done update the file in Bazarr and move onto the next file.

Clunky, and slow, but works.

## Installation


## Usage

<!-- The following command will generate a `subtitled/video.mp4` file contained the input video with overlayed subtitles.

    faster_auto_subtitle /path/to/video.mp4 -o subtitled/

The default setting (which selects the `small` model) works well for transcribing English. You can optionally use a bigger model for better results (especially with other languages). The available models are `tiny`, `tiny.en`, `base`, `base.en`, `small`, `small.en`, `medium`, `medium.en`, `large`, `large-v1`, `large-v2`, `large-v3`.

    faster_auto_subtitle /path/to/video.mp4 --model medium

Adding `--task translate` will translate the subtitles into English:

    faster_auto_subtitle /path/to/video.mp4 --task translate

Run the following to view all available options:

    faster_auto_subtitle --help

## Tips

The tool also exposes a couple of model parameters, that you can tweak to increase accuracy.

Higher `beam_size` usually leads to greater accuracy, but slows down the process.

Setting higher `no_speech_threshold` could be useful for videos with a lot of background noise to stop Whisper from "hallucinating" subtitles for it.

In my experience settings option `condition_on_previous_text` to `False` dramatically increases accurracy for videos like TV Shows with an intro song at the start. 

You can use `sample_interval` parameter to generate subtitles for a portion of the video to play around with those parameters:

    faster_auto_subtitle /path/to/video.mp4 --model medium --sample_interval 00:05:30-00:07:00 --condition_on_previous_text False --beam_size 6 --no_speech_threshold 0.7

## License

This script is open-source and licensed under the MIT License. For more details, check the [LICENSE](LICENSE) file. -->
