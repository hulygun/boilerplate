from fastapi import APIRouter, Depends, Response

from api.depends import get_db
from .data import Callback
from api.create_tables import MODELS

router = APIRouter(tags=['callback'])


#ToDo: Make auth for rpc server
@router.post('/', dependencies=[Depends(get_db)])
def callback(data: Callback):
    """
    Docstring with markup support
    **item** item
    """
    model = next(filter(lambda model: model.__name__ == data.entry, MODELS), None)
    if model:
        query = getattr(model, data.action)(**data.data)
        if data.id:
            query = query.where(model.id == data.id)
        query.execute()

    return Response()