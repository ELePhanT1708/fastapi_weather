import asyncio
import aiohttp
from typing import List

import json
import requests
import time

start_time = time.time()


async def send_request_to_update(cities):
    async with aiohttp.ClientSession() as session:
        for city in cities:
            url = f'http://localhost:8000/weather/{city}'
            async with session.post(url) as resp:
                res = await resp.json()
    print("Update DONE! ")


def select_cities(quantity: int) -> List[str]:
    '''
    From city.list.json read exists city names from openweathermap
    with determined quantity city names to use
    '''
    with open('weather_api/city.list.json', 'r', encoding='utf-8') as json_cities:
        data = json.load(json_cities)
        list_citites = []
        for i in data[:quantity:]:
            list_citites.append(i['name'])
    return list_citites


async def send_to_db_via_api(city_names: List[str]) -> None:
    "/weather/{city_name}"
    base_url = r'http://localhost:8000/weather/'
    for city in city_names:
        return requests.post(url=base_url + city)

CITIES = select_cities(10)


if __name__ == "__main__":

    asyncio.run(send_request_to_update(CITIES))
    print("--- %s seconds ---" % (time.time() - start_time))
