import os
import logging
from typing import Iterator, List

from googleapiclient.discovery import build
from pymongo import MongoClient, ReplaceOne, DESCENDING
from pymongo.collection import Collection

YOUTUBE_API_KEY = os.environ["YOUTUBE_API_KEY"]
logging.getLogger("apiclient.discovery_cache").setLevel(logging.WARNING)


def search_videos(param):
    pass


def save_to_mongodb(collection, item):
    pass


def main():
    mongo = MongoClient("localhost", 27017)
    collection = mongo.youtube.videos

    for item in search_videos("YOUTUBEAPI"):
        save_to_mongodb(collection, item)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()