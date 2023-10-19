# YouTube Channel Exporter

Download all videos produced by a YouTube channel and create backups. The day the channel disapear, you still have your most favourite videos. Be careful though to respect copyrights and everything around the work behind those videos, as you won't own them.

# Requirements

A `Google API` key which can access the `YouTube Data V3` API. You can create one here : [https://console.cloud.google.com/apis/dashboard](https://console.cloud.google.com/apis/dashboard).

You also must install the python requirements. You can do so with the following command :
```bash
python -m pip install -r requirements.txt
```

# Code snippet

Here is an example on how to use the project :

```python
import os
import dotenv # python -m pip install python-dotenv
from youtube_exporter import download_videos, get_channel_video_urls

dotenv.load_dotenv(".env")

def main():
    channel_id = "THE_CHANNEL_ID"

    if not os.path.exists(channel_id):
        os.mkdir(channel_id)

    if not os.path.exists(channel_id):
        print(
            f"Unable to create the downlaod folder for the channel '{channel_id}'."
        )
        continue

    video_urls = get_channel_video_urls(
        google_api_key=os.environ["GOOGLE_API_KEY"], channel_id=channel_id
    )

    download_videos(video_urls=video_urls, output_path=channel_id, batches=4)

if __name__ == "__main__":
    main()
```

Have fun.
