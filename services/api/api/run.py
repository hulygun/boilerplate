from fastapi import FastAPI, Depends

from .create_tables import create
from .depends import locale
from .services import load_services

create()

app = FastAPI(dependencies=[Depends(locale)])
load_services(app)
sleep_time = 10
