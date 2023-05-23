import glob
import os
from os.path import dirname, basename, isfile, join
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base
from configparser import ConfigParser

Base = declarative_base()

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


class Data:
    URL: str
    ENGINE: Optional[Engine]
    SESSION_MAKER: Optional[sessionmaker]


def set_settings(url: str):
    Data.URL = url
    Data.ENGINE = create_engine(url)
    Data.SESSION_MAKER = sessionmaker(bind=Data.ENGINE)


def get_session() -> Session:
    return Data.SESSION_MAKER()


def connect():
    config = ConfigParser()
    config.read('settings.ini')
    set_settings(config['DEFAULT']['sqlalchemy.url'])

def connect_get_session():
    connect()
    return get_session()


def create_database():
    config = ConfigParser()
    config.read('settings.ini')
    set_settings(config['DEFAULT']['sqlalchemy.url'])
    Base.metadata.create_all(Data.ENGINE)


def remove_sqlite_db():
    config = ConfigParser()
    config.read('settings.ini')
    os.remove(config['DEFAULT']['sqlalchemy.url'].split('/')[-1])
