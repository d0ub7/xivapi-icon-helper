import asyncio
import logging
import argparse
import math

import pyxivapi
from pyxivapi.models import Filter

# ADD YOUR API KEY HERE
API_KEY = ""

URL_PREFIX = "https://xivapi.com/i/"
async def fetch_example_results():
    client = pyxivapi.XIVAPIClient(api_key=API_KEY)
    action = await client.index_search(
            name="*", 
            indexes=["Action"], 
            columns=["Name", "IconHD"], 
            filters=[
                Filter("ClassJobLevel", "gte", 0)
            ],
            string_algo="match",
            per_page="1"
        )

    pages = math.ceil(action["Pagination"]["ResultsTotal"]/100)
    out_string = ""
    for i in range(pages):
        print(f'getting page {i+1}')
        loop_action = await client.index_search(
            name="*",
            indexes=["Action"], 
            columns=["Name", "IconHD"], 
            filters=[
                Filter("ClassJobLevel", "gte", 0)
            ],
            string_algo="match",
            per_page="100",
            page=i+1
        )
        for result in loop_action['Results']:
           print(f"![{result['Name']}]({result['IconHD'].replace('/i/', URL_PREFIX)})")
           out_string += "{"
           out_string += f"\"{result['Name']}\": \"{result['IconHD'].replace('/i/', URL_PREFIX)}\""
           out_string += "}"

    with open("test.json", 'w+') as f:
        f.write(out_string)
    await client.session.close()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s', datefmt='%H:%M')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(fetch_example_results())