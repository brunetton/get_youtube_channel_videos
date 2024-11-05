#!python3
# -*- coding: utf-8 -*-

"""
List all videos from ginve youtube channel (newer first).

Example:
- first get channel ID from channel name
{self_filename} search RosasLounge
- then list videos
{self_filename} get UCPFvsXRt_9InJA9XeBGpRaA

Usage:
    {self_filename} search <channel_name>
    {self_filename} get <channel_id> [options]
    {self_filename} -h | --help

Options:
    --limit <number>        Limit the number of results
"""

import os
from pathlib import Path

from docopt import docopt
from dotenv import load_dotenv
from googleapiclient.discovery import build


def search_channel_ID(channel_name):
    youtube = build("youtube", "v3", developerKey=API_KEY)
    request = youtube.search().list(
        part="snippet", type="channel", q=channel_name, maxResults=1
    )
    response = request.execute()

    if "items" in response and len(response["items"]) > 0:
        channel_snippet = response["items"][0]["snippet"]
        print(f"- title: {channel_snippet["title"]}")
        print(f"- description: {channel_snippet["description"]}")
        print(f"- ID: {channel_snippet["channelId"]}")
    else:
        print("Error: not found :(")


def list_videos(channel_id, max_results):
    youtube = build("youtube", "v3", developerKey=API_KEY)

    nb_results = 0
    next_page_token = None

    while True:
        results_per_request = min(50, max_results - nb_results if max_results else 50)
        res = (
            youtube.search()
            .list(
                channelId=channel_id,
                part="snippet",
                type="video",
                order="date",
                pageToken=next_page_token,
                maxResults=results_per_request,
            )
            .execute()
        )

        for video in res["items"]:
            print(f"Title: {video['snippet']['title']}")
            print(f"URL: https://www.youtube.com/watch?v={video['id']['videoId']}")
            print()

        nb_results += results_per_request
        next_page_token = res.get("nextPageToken")
        if not next_page_token or (max_results and nb_results >= max_results):
            break


args = docopt(__doc__.format(self_filename=Path(__file__).name))
load_dotenv()
if not os.getenv("API_KEY"):
    print("API_KEY environment variable must be defined")
API_KEY = os.getenv("API_KEY")

if args["<channel_name>"]:
    search_channel_ID(args["<channel_name>"])
elif args["<channel_id>"]:
    list_videos(args["<channel_id>"], int(args["--limit"]) if args["--limit"] else None)
