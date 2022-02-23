import datetime
import json

from app.db import models


def test_get_categories(client, test_categories, superuser_token_headers):
    response = client.get("/api/v1/categories", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(test_categories.id),
            "color": test_categories.color,
            "name": test_categories.name,
            "user_id": str(test_categories.user_id),
            "image": test_categories.image_id,
            "category_id": test_categories.category_id,
            "selected": test_categories.selected,
            "created_at": '2022-02-21T14:00:17.961523',
            "updated_at": '2022-02-21T14:00:17.961523',

        }
    ]


def test_category_not_belongs_to_user(client, test_categories, user_token_headers):
    response = client.delete(
        f"/api/v1/categories/{test_categories.id}", headers=user_token_headers
    )
    assert response.status_code == 404


def test_delete_category(client, test_categories, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/categories/{test_categories.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Categories).all() == []


def test_delete_category_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/categories/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_category(client, test_categories, test_superuser, superuser_token_headers):
    new_categories = {
        "color": "white",
        "name": "test_category2",
        "user_id": str(test_superuser.id),
        "category_id": None,
        "selected": 0,
        "created_at": '2022-02-21T14:00:17.961523',
    }

    response = client.put(
        f"/api/v1/categories/{str(test_categories.id)}",
        json=new_categories,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_categories["id"] = str(test_categories.id)
    new_categories["image"] = None
    dict_data = dict(response.json())
    dict_data.pop('updated_at')

    assert dict_data == new_categories


def test_edit_category_not_found(client, test_db, test_superuser, superuser_token_headers):
    new_categories = {
       "color": "white",
       "name": "test_category2",
       "user_id": str(test_superuser.id),
       "category_id": None,
       "selected": 0,
       "created_at": '2022-02-21T14:00:17.961523',
    }
    response = client.put(
        "/api/v1/categories/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", json=new_categories, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_category(client, test_categories, superuser_token_headers,):
    response = client.get(
        f"/api/v1/categories/{str(test_categories.id)}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_categories.id),
        "color": test_categories.color,
        "name": test_categories.name,
        "user_id": str(test_categories.user_id),
        "image": test_categories.image_id,
        "category_id": test_categories.category_id,
        "selected": test_categories.selected,
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523',
    }


def test_category_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/categories/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers)
    assert response.status_code == 404


def test_authenticated_user_me(client, test_categories, superuser_token_headers):
    response = client.get("/api/v1/categories/my/", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [{
        "id": str(test_categories.id),
        "color": test_categories.color,
        "name": test_categories.name,
        "user_id": str(test_categories.user_id),
        "image": test_categories.image_id,
        "category_id": test_categories.category_id,
        "selected": test_categories.selected,
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523',
    }]


def test_create_categories(client, test_categories, test_images, test_superuser, superuser_token_headers):
    data = {
        "name": "new_name",
        "color": "new_color",
        "image_id": str(test_images.id)
    }

    new = json.dumps(data)
    response = client.post("/api/v1/categories", data=new, headers={'Content-Type': 'application/json', 'Authorization': superuser_token_headers.get('Authorization')})
    assert response.status_code == 200

    data["category_id"] = None
    data["selected"] = None
    data["user_id"] = str(test_superuser.id)
    data.pop("image_id")

    data["image"] = {
        "id": str(test_images.id),
        "path": test_images.path,
        "public_path": test_images.public_path,
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523'
    }
    dict_data = dict(response.json())
    dict_data.pop('id')
    dict_data.pop('created_at')
    dict_data.pop('updated_at')

    assert dict_data == data


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/categories/my")
    assert response.status_code == 401
    response = client.get("/api/v1/categories")
    assert response.status_code == 401
    response = client.post("/api/v1/categories")
    assert response.status_code == 401
    response = client.get("/api/v1/categories/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
    response = client.put("/api/v1/categories/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
    response = client.delete("/api/v1/categories/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
