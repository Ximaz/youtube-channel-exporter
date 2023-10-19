import logging
import os
import multiprocessing
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
                lambda filename: filename.startswith(video.title),
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

    video_path = video.download(output_path=output_path)
    if isinstance(logger, logging.Logger):
        logger.info("Video '%s' downloaded as '%s'.", video_url, video_path)


def download_videos(
    video_urls: typing.Iterable[str],
    output_path: str,
    cpu_core: int = 4,
    skip_existing: bool = True,
    logger: logging.Logger | None = None,
):
    pool = multiprocessing.Pool(processes=cpu_core)
    for video_url in video_urls:
        pool.apply_async(
            func=download_video,
            kwds=dict(
                video_url=video_url,
                output_path=output_path,
                skip_existing=skip_existing,
                logger=logger,
            ),
        )
    pool.close()
    pool.join()