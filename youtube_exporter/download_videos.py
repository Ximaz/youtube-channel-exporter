import concurrent.futures
import logging
import os
import urllib.error
import typing

import pytube


def download_video(
    video_url: str,
    output_path: str,
    skip_existing: bool = True,
    logger: logging.Logger | None = None,
):
    youtube_video = pytube.YouTube(url=video_url)

    video = youtube_video.streams.get_highest_resolution()

    if video is None:
        if isinstance(logger, logging.Logger):
            logger.warning("Unable to download the video '%s'.", video_url)
        return

    try:
        video_path = video.download(output_path=output_path, skip_existing=skip_existing, max_retries=3)
    except urllib.error.HTTPError:
        if isinstance(logger, logging.Logger):
            logger.error("Unable to download the Video '%s'.", video_url)
    else:
        if isinstance(logger, logging.Logger):
            logger.info("Video '%s' downloaded as '%s'.", video_url, video_path)


def download_videos(
    video_urls: typing.Iterable[str],
    output_path: str,
    threads: int = 4,
    skip_existing: bool = True,
    logger: logging.Logger | None = None,
):
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as pool:
        queue = [
            pool.submit(
                download_video,
                video_url=video_url,
                output_path=output_path,
                skip_existing=skip_existing,
                logger=logger,
            )
            for video_url in video_urls
        ]
        for task in concurrent.futures.as_completed(fs=queue):
            try:
                task.result()
            except Exception:
                exception = task.exception()
                if isinstance(logger, logging.Logger):
                    logger.error("An exception occured : %s", ' '.join(exception.args))


