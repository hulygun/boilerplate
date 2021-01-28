from fastapi import FastAPI

from .create_tables import create
from .services import load_services

create()

app = FastAPI()
load_services(app)
sleep_time = 10
