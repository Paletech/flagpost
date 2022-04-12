import json

from app.db import models


def test_get_posts(client, test_posts, superuser_token_headers):
    response = client.get("/api/v1/posts", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(test_posts.id),
            "type": test_posts.type,
            "text": test_posts.text,
            "user_id": str(test_posts.user_id),
            "files": test_posts.files,
            "categories": test_posts.categories,
            "created_at": '2022-02-21T14:00:17.961523',
            "updated_at": '2022-02-21T14:00:17.961523',

        }
    ]


def test_post_not_belongs_to_user(client, test_posts, user_token_headers):
    response = client.delete(
        f"/api/v1/posts/{test_posts.id}", headers=user_token_headers
    )
    assert response.status_code == 404


def test_delete_post(client, test_posts, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/posts/{test_posts.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Posts).all() == []


def test_delete_post_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/posts/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_edit_post(client, test_posts, test_superuser, superuser_token_headers):
    new_post = {
        "type": "new_type",
        "text": "new_text",
        "user_id": str(test_superuser.id),
        "created_at": '2022-02-21T14:00:17.961523',
    }

    response = client.put(
        f"/api/v1/posts/{str(test_posts.id)}",
        json=new_post,
        headers=superuser_token_headers,
    )
    assert response.status_code == 200
    new_post["id"] = str(test_posts.id)
    new_post["files"] = []
    new_post["categories"] = []
    dict_data = dict(response.json())
    dict_data.pop('updated_at')

    assert dict_data == new_post


def test_edit_post_not_found(client, test_db, test_superuser, superuser_token_headers):
    new_post = {
        "type": "new_type",
        "text": "new_text",
        "user_id": str(test_superuser.id),
        "created_at": '2022-02-21T14:00:17.961523',
    }

    response = client.put(
        "/api/v1/posts/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", json=new_post, headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_post(client, test_posts, superuser_token_headers,):
    response = client.get(
        f"/api/v1/posts/{str(test_posts.id)}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_posts.id),
        "type": test_posts.type,
        "text": test_posts.text,
        "user_id": str(test_posts.user_id),
        "files": [],
        "categories": [],
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523',
    }


def test_create_post(client, test_categories, test_files, test_superuser, superuser_token_headers):
    data = {
        "type": "new_type",
        "text": "new_text",
        "categories": [str(test_categories.id)],
        "files": [str(test_files.id)]
    }

    json_data = json.dumps(data)
    response = client.post("/api/v1/posts", data=json_data, headers={
        'Content-Type': 'application/json',
        'Authorization': superuser_token_headers.get('Authorization')
    })
    assert response.status_code == 200

    data["user_id"] = str(test_superuser.id)

    data["categories"] = [{
        "id": str(test_categories.id),
        "category_id": None,
        "color": test_categories.color,
        "image": test_categories.image,
        "name": test_categories.name,
        "selected": test_categories.selected,
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523',
        "user_id": str(test_categories.user_id)
    }]

    data["files"] = [{
        "id": str(test_files.id),
        "height": test_files.height,
        "width": test_files.height,
        "path": test_files.path,
        "post_id": str(test_files.post_id),
        "public_path": test_files.public_path,
        "created_at": '2022-02-21T14:00:17.961523',
        # "updated_at": '2022-02-21T14:00:17.961523',

    }]

    dict_data = dict(response.json())
    dict_data.pop('id')
    dict_data.pop('created_at')
    dict_data.pop('updated_at')
    dict_data.get('files')[0].pop('updated_at')
    assert dict_data == data


def test_post_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/posts/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers)
    assert response.status_code == 404


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/posts/my")
    assert response.status_code == 401
    response = client.get("/api/v1/posts")
    assert response.status_code == 401
    response = client.get("/api/v1/posts/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
    response = client.put("/api/v1/posts/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
    response = client.delete("/api/v1/posts/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
