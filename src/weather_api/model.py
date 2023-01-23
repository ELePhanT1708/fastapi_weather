import datetime as dt

from pydantic import BaseModel


class WeatherInCityBase(BaseModel):
    city: str = 'Moscow'
    temperature: float = 15.00
    pressure: float = 0.0
    speed: float = 0.0
    timestamp: dt.datetime = dt.datetime.utcnow()


class WeatherInCity(WeatherInCityBase):
    id: int

    class Config:
        orm_mode = True
