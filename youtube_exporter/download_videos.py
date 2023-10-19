import os
import threading
import typing


import pytube


def _batch_list(
    iterable: list, batches: int
) -> typing.Generator[list, typing.Any, None]:
    for i in range(0, len(iterable), batches):
        yield iterable[i : i + batches]


def download_video(video_url: str, output_path: str, skip_if_exists: bool = True):
    youtube_video = pytube.YouTube(url=video_url)

    if skip_if_exists:
        is_already_downloaded = any(
            map(
                lambda filename: filename.startswith(video.title),
                os.listdir(output_path),
            )
        )
        if is_already_downloaded:
            return

    video = youtube_video.streams.get_highest_resolution()

    if video is None:
        print(f"Unable to download the video at '{video_url}'")
    else:
        video.download(output_path=output_path)


def download_videos(
    video_urls: typing.Iterable[str],
    output_path: str,
    batches: int = 4,
    skip_existing: bool = True,
):
    threads = list(
        map(
            lambda video_url: threading.Thread(
                target=download_video, args=(video_url, output_path, skip_existing)
            ),
            video_urls,
        )
    )

    for batch in _batch_list(iterable=threads, batches=batches):
        for thread in batch:
            thread.start()

        for thread in batch:
            thread.join()
