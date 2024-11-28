import uuid

from fastapi import FastAPI
from mangum import Mangum
from pydantic import BaseModel


class RequestItem(BaseModel):
    name: str
    description: str | None
    price: float


class ResponseItem(BaseModel):
    id: str
    name: str
    description: str | None
    price: float


app = FastAPI()


@app.get("/item", status_code=200, response_model=ResponseItem)
async def read_item(id: str):
    return {"id": str(id), "name": "get_item+" + str(id), "description": "get_item+" + str(id), "price": 100.0}


@app.post("/item", status_code=201, response_model=ResponseItem)
async def create_item(item: RequestItem):
    create_item = {"id": str(uuid.uuid4())}
    create_item.update(item)
    return create_item


@app.put("/item/{id}", status_code=201, response_model=ResponseItem)
async def update_item(id: str):
    return {"id": id, "name": "put_item+" + str(id), "description": "put_item+" + str(id), "price": 300.0}


lambda_handler = Mangum(app)
