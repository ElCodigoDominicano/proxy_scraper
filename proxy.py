"""A simple proxy scrapper, smaller part of a bigger project
currently working on.

Author: ElCodigoDominicano
Date: 09/02/2024"""

import time
import logging
import asyncio

from aiohttp import ClientSession, ClientResponse, ClientConnectionError

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class CheckYourConnection(BaseException):
    ...


async def connection(url: str) -> BeautifulSoup:
    """ Attempts to make a connection to a url
    asynchronously, and RETURNS json response."""
    async with ClientSession() as session:
        try:
            async with session.get(url) as response:
                return await response.json()
        except ClientConnectionError:
            raise CheckYourConnection("Connection Failure")
    
async def get_json_responses() -> list[ClientResponse]:
    """Returns a list containing 13 client responses..
    granted thats if everything went well.."""
    urls = [f"""
        https://proxylist.geonode.com/api/proxy-list?\
        limit=500&page={x}&sort_by=responseTime&sort_type=asc"""
        for x in range(13)]
    json_responses = await asyncio.gather(*[
        connection(url)
        for url in urls
    ])
    return json_responses

async def main():
    """Await for a list of responses, enumerates that list
    assigns a number to be used for a filename, writes those
    responses to a .json file is a list containing a 
    dictionaries"""
    logger.info("Welcome! Plese wait while we set things up.")
    list_of_responses = await get_json_responses()
    
    logger.info("Going to loop into a list of responses.")
    for x, response in enumerate(list_of_responses):
        file_num = x + 1
        with open(f"proxy_pages/geonode-page-{file_num}.json", "w") as json_file:
            logger.info(f"Going to attempt to write json file -> {file_num}")
            json_file.writelines(response)
            logger.info(f"Wrote Json -> {file_num}")

if __name__ == "__main__":
    start = time.time()
    asyncio.run(main())

    logger.info(f"Program took -> {time.time() - start}.")
