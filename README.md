# Youtube channel videos list

## Installation and usage

- clone the repo or download as zip file
- get a Youtube API from https://console.developers.google.com
- crate a `.env` file containing this key:
    ```
    API_KEY=.......
    ```
- using [UV](https://docs.astral.sh/uv/):
  - get channel ID from channel name:

        uv run get_youtube_channel_videos.py search RosasLounge
      => UCPFvsXRt_9InJA9XeBGpRaA

  - use this ID to list channel's videos:

        uv run get_youtube_channel_videos.py get UCPFvsXRt_9InJA9XeBGpRaA
