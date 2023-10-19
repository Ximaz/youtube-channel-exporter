import logging
import typing

import requests


def _in_between(value: int, _min: int, _max: int):
    return _min if value < _min else _max if value > _max else value


def _get_channel_videos_page(
    google_api_key: str,
    channel_id: str,
    next_page_token: str | None = None,
    max_result: int = 50,
) -> dict:
    return requests.get(
        url=f"https://youtube.googleapis.com/youtube/v3/search",
        params={
            "part": "id",
            "channelId": channel_id,
            "maxResults": _in_between(value=max_result, _min=1, _max=50),
            "pageToken": next_page_token,
            "key": google_api_key,
        },
        headers={
            "Accept": "application/json",
        },
    ).json()


def _reduce_videos_page_to_video_ids(videos_page: dict) -> list[str]:
    return [
        item["id"]["videoId"]
        for item in videos_page.get("items", [])
        if item["id"]["kind"] == "youtube#video"
    ]


def get_channel_video_ids(
    google_api_key: str, channel_id: str, logger: logging.Logger | None = None
) -> typing.Generator[str, typing.Any, None]:
    next_page_token = ""

    while next_page_token is not None:
        videos_page = _get_channel_videos_page(
            google_api_key=google_api_key,
            channel_id=channel_id,
            next_page_token=next_page_token,
        )

        for video_id in _reduce_videos_page_to_video_ids(videos_page=videos_page):
            if isinstance(logger, logging.Logger):
                logger.info("Found video ID : '%s'.", video_id)

            yield video_id

        next_page_token = videos_page.get("nextPageToken", None)


def get_channel_video_urls(
    google_api_key: str, channel_id: str, logger: logging.Logger | None = None
) -> typing.Generator[str, typing.Any, None]:
    for video_id in get_channel_video_ids(
        google_api_key=google_api_key, channel_id=channel_id
    ):
        url = f"https://www.youtube.com/watch?v={video_id}"
        if isinstance(logger, logging.Logger):
            logger.info("Found video : '%s'.", url)

        yield url