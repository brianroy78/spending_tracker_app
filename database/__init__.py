import glob
import os
from os.path import dirname, basename, isfile, join, exists
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.orm import declarative_base
from configparser import ConfigParser

Base = declarative_base()

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")]


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
    set_settings(_get_settings()["DEFAULT"]["sqlalchemy.url"])


def connect_get_session():
    connect()
    return get_session()


def create_database():
    connect()
    Base.metadata.create_all(Data.ENGINE)
    print("Database created!")


def remove_sqlite_db():
    path = _get_settings()["DEFAULT"]["sqlalchemy.url"].split("/")[-1]
    if exists(path):
        os.remove(path)
        print(f"{path} database deleted!")


def _get_settings():
    config = ConfigParser()
    config.read("settings.ini")
    return config
