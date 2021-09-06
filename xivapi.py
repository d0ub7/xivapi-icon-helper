import asyncio
import logging
import argparse

import aiohttp

import pyxivapi
from pyxivapi.models import Filter, Sort

# ADD YOUR API KEY HERE
API_KEY = ""

URL_PREFIX = "https://xivapi.com/i/"
async def fetch_example_results():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="name of skill to fetch")
    args = parser.parse_args()

    print(f"searching xivapi for {args.name}")
    client = pyxivapi.XIVAPIClient(api_key=API_KEY)
    action = await client.index_search(
            name=args.name, 
            indexes=["Action"], 
            columns=["Name", "IconHD"], 
            filters=[
                Filter("ClassJobLevel", "gte", 0)
            ],
            string_algo="match"
        )

    for item in action['Results']:
        for k, v in item.items():
            print (v.replace("/i/", URL_PREFIX))
    await client.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_example_results())