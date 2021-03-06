import os
import logging
from typing import Iterator, List

from googleapiclient.discovery import build
from pymongo import MongoClient, ReplaceOne, DESCENDING
from pymongo.collection import Collection

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]

logging.getLogger("apiclient.discovery_cache").setLevel(logging.WARNING)


def search_videos(param: str, max_pages: int = 5) -> Iterator[List[dict]]:
    """
    :param param:
    :param max_pages:
    :return:
    returns a list of items by page with 'param' arguments, up to max_pages.
    """
    youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
    search_request = youtube.search().list(
        part="id",
        q=param,
        type="video",
        maxResults=50,
    )

    i = 0
    while search_request and i < max_pages:
        search_response = search_request.execute()
        video_ids = [item["id"]["videoId"] for item in search_response["items"]]

        videos_response = youtube.videos().list(
            part="snippet,statistics",
            id=','.join(video_ids),
        ).execute()

        yield videos_response["items"]
        search_request = youtube.search.list_next(search_request, search_response)
        i += 1


def save_to_mongodb(collection: Collection, items: List[dict]):
    """
    convert and save a searching result to a MongoDB bson file.
    """
    for item in items:
        item["_id"] = item["id"]

        for key, value in item["statistics"].items():
            item["statistics"][key] = int(value)

    operations = [ReplaceOne({"_id": item["_id"]}, item, upsert=True) for item in items]
    result = collection.bulk_write(operations)
    logging.info(f"upserted {result.upserted_count} documents")


def show_top_videos(collection: Collection, top: int):
    """
    show most popular videos from db.
    to store videos correctly on the database, avoid using best-videos feature from youtube.videos API.
    """
    for item in collection.find().sort("statistics.viewCount", DESCENDING).limit(top):
        print(item["statistics"]["viewCount"], item["snippet"]["title"])


def main():
    mongo = MongoClient("localhost", 27017)
    collection = mongo.youtube.videos

    for item in search_videos("YOUTUBEAPI"):
        save_to_mongodb(collection, item)

    show_top_videos(collection, 5)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
