import logging
import os
import threading
import typing


import pytube


def _batch_list(
    iterable: list, batches: int
) -> typing.Generator[list, typing.Any, None]:
    for i in range(0, len(iterable), batches):
        yield iterable[i : i + batches]


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
        logger.info("Video '%s' downloaded as '%s'.", video_path)


def download_videos(
    video_urls: typing.Iterable[str],
    output_path: str,
    batches: int = 4,
    skip_existing: bool = True,
    logger: logging.Logger | None = None,
):
    threads = list(
        map(
            lambda video_url: threading.Thread(
                target=download_video,
                kwargs=dict(
                    video_url=video_url,
                    output_path=output_path,
                    skip_existing=skip_existing,
                    logger=logger,
                ),
            ),
            video_urls,
        )
    )

    batch_number = 1
    for batch in _batch_list(iterable=threads, batches=batches):
        if isinstance(logger, logging.Logger):
            logger.info("Starting batch n°%d of size %d.", batch_number, len(batch))

        for thread in batch:
            thread.start()

        for thread in batch:
            thread.join()

        batch_number += 1