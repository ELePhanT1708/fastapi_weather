import json
import time
from typing import List, Optional, Union
import datetime as dt
import requests
from fastapi import Depends, HTTPException, status, Response
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

import tables
from db import get_session
from model import WeatherInCity, WeatherInCityBase
from settings import settings


class WeatherService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session
        self.base_url = r'https://api.openweathermap.org/data/2.5/weather'
        self.api_key = settings.key

    def _exists(self, city_name: str):
        city = self.session.query(tables.WeatherInCity) \
            .filter_by(city=city_name) \
            .first()
        # city_exists = self.session.query(tables.WeatherInCity.query.filter_by(city == city_name).exists()).scalar()
        # # raise HTTPException(404, f'{city}')
        if not city:
            return False
        return True

    def create(self, city_name: str) -> tables.WeatherInCity:
        city_name = city_name.replace(city_name[0], city_name[0].upper())
        # if self._exists(city_name):
        #     raise HTTPException(406, 'City exist in database !')
        response_dict = self.get_current_values_by_name(city_name)
        weather_data = {
            'city': city_name,
            'temperature': response_dict['temperature'],
            'pressure': response_dict['pressure'],
            'speed': response_dict['speed'],
            'timestamp': dt.datetime.utcnow()
        }

        weather_city_row = tables.WeatherInCity(**weather_data)
        self.session.add(weather_city_row)
        self.session.commit()
        return weather_city_row

    def kelvin_to_celcius(self, kelvin: float) -> float:
        celcius = kelvin - 273.15
        return round(celcius, 2)

    def get_current_values_by_name(self, city_name: str) -> float:
        params = f'?q={city_name}&appid={self.api_key}'
        url = self.base_url + params
        response = requests.get(url)
        if response.status_code == 404:
            raise HTTPException(404, detail='City not found!')
        res_data = response.json()
        print(res_data)
        kelvin = res_data['main']['temp']
        pressure = res_data['main']['pressure']
        speed = res_data['wind']['speed']

        res_dict = {
            'city_name': city_name,
            'temperature': self.kelvin_to_celcius(kelvin),
            'pressure': pressure,
            'speed': speed,
        }
        return res_dict

    def get_exists_lastinfo(self, search: Union[str, None] = None):
        if search:
            last_info = self.session.query(tables.WeatherInCity). \
                distinct(tables.WeatherInCity.city). \
                filter(tables.WeatherInCity.city.like(f"%{search}%")). \
                all()
        else:
            last_info = self.session.query(tables.WeatherInCity). \
                distinct(tables.WeatherInCity.city). \
                order_by(tables.WeatherInCity.city). \
                all()
        return last_info

    def get_statisitics_about_city(self, city_name: str):
        statistics_data = self.session.query(tables.WeatherInCity). \
            filter_by(city=city_name).all()
        avg_speed = self.session.query(func.avg(tables.WeatherInCity.speed)).\
            filter(tables.WeatherInCity.city == city_name).scalar()
        avg_temperature = self.session.query(func.avg(tables.WeatherInCity.temperature)). \
            filter(tables.WeatherInCity.city == city_name).scalar()
        avg_pressure = self.session.query(func.avg(tables.WeatherInCity.pressure)). \
            filter(tables.WeatherInCity.city == city_name).scalar()
        return {
            "Average":{
                'Speed': round(avg_speed, 2),
                'Temperature': round(avg_temperature, 2),
                'Pressure': round(avg_pressure, 2)
            },
            'All Data': statistics_data
        }



