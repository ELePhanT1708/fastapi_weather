import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class WeatherInCity(Base):
    __tablename__ = 'WeatherInCity'
    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    city = sa.Column(sa.String)
    temperature = sa.Column(sa.Float)
    pressure = sa.Column(sa.Float)
    speed = sa.Column(sa.Float)
    timestamp = sa.Column(sa.TIMESTAMP)
