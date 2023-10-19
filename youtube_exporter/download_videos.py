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

    if skip_existing:
        is_already_downloaded = any(
            map(
                lambda filename: filename.startswith(youtube_video.title)
                and os.path.getsize(os.path.join(output_path, filename)) > 0,
                os.listdir(output_path),
            )
        )
        if is_already_downloaded:
            if isinstance(logger, logging.Logger):
                logger.info(
                    "Skipping video '%s' because it already got downloaded.", video_url
                )
            return

    video = youtube_video.streams.get_highest_resolution()

    if video is None:
        if isinstance(logger, logging.Logger):
            logger.warning("Unable to download the video '%s'.", video_url)
        return

    if isinstance(logger, logging.Logger):
        logger.info("Downloading video '%s' into '%s'.", video_url, output_path)

    try:
        video_path = video.download(output_path=output_path, max_retries=10)
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
            task.result()
