from fastapi import APIRouter, Depends, Response, status

from api.depends import get_db
from .data import Callback
from api.create_tables import MODELS

router = APIRouter(tags=['callback'])


#ToDo: Make auth for rpc server
@router.post('/', dependencies=[Depends(get_db)], name='callback')
def callback(data: Callback):
    """
    ## Callback CRUD

    Calback url for db operations from another services

    **usage**
    ```python
    def test_rpc_method():
        requests.post('https://{API_DOMAIN}/callback', {
            "entry": "DBUser",
            "id": "72a61c9012564c7d819c3bcf41ef1c3e",
            "action": "update",
            "data": {"is_active": True}
        })

    aiohttp_rpc.rpc_server.add_methods([
        test_rpc_method
    ])
    ```
    """
    model = next(filter(lambda model: model.__name__ == data.entry, MODELS), None)
    if model:
        query = getattr(model, data.action)(**data.data)
        if data.id:
            query = query.where(model.id == data.id)
        query.execute()

    return Response(status_code=status.HTTP_200_OK)