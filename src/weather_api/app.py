import asyncio
import time
from typing import List, Union
from fastapi_utils.tasks import repeat_every
from fastapi import FastAPI, Depends
import logging
import datetime
# import scrapy

import tables
from db import engine, Session, get_session
from service import WeatherService
from model import WeatherInCity, WeatherInCityBase
from city_spider import CITIES, send_request_to_update

logger = logging.getLogger(__name__)
tables.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='Weather API',
    description='Погода в городах',
    version='1.0.0',
)


# app.include_router(user_router)
# app.include_router(post_router)
# app.include_router(likes_router)
# app.include_router(dislikes_router)
# app.include_router(ui_router)


@app.on_event("startup")
@repeat_every(seconds=60)
def update_info():
    asyncio.run(send_request_to_update(CITIES))



@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/weather/{city_name}", response_model=WeatherInCity)
async def add_city(city_name: str,
                   service: WeatherService = Depends()):
    return service.create(city_name)



    # start_time = time.time()
    # cities = select_cities(10)
    # asyncio.run(main(cities))
    # print("--- %s seconds ---" % (time.time() - start_time))


@app.get("/last_weather")
async def get_last_info(
        search: Union[str, None] = None,
        service: WeatherService = Depends()):
    return service.get_exists_lastinfo(search)


@app.get("/city_stats")
async def get_statisitics_about_city(
        city_name: str,
        service: WeatherService = Depends()):
    return service.get_statisitics_about_city(city_name)