from fastapi.testclient import TestClient
from hello_world.app import app as hello_world_app
from item.app import app as item_app
import json

hello_world_app = TestClient(hello_world_app)
item_client = TestClient(item_app)

def test_root():
    response = hello_world_app.get("/hello")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello SAM World"}

def test_get_item():
    response = item_client.get("/item?id=ABC")
    assert response.status_code == 200
    assert response.json() == {"id": "ABC", "name": "get_item+ABC","description":"get_item+ABC","price":100.0}

def test_poset_item():
    response = item_client.post(
        "/item",
        json={"name": "post_item","description":"post_item","price":200.0}
    )
    del_id_res = response.json()
    del del_id_res["id"]
    assert response.status_code == 201
    assert del_id_res == {"name": "post_item","description":"post_item","price":200.0}

def test_put_item():
    response = response = item_client.put(
        "/item/9"
    )
    assert response.status_code == 201
    assert response.json() == {"id": "9", "name": "put_item+9","description":"put_item+9","price":300.0}
