from app.db import models


def test_get_images(client, test_images, superuser_token_headers):
    response = client.get("/api/v1/images")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(test_images.id),
            "path": str(test_images.path),
            "public_path": test_images.public_path,
            "created_at": '2022-02-21T14:00:17.961523',
            "updated_at": '2022-02-21T14:00:17.961523',

        }
    ]


def test_delete_image(client, test_images, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/images/{test_images.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Images).all() == []


def test_delete_image_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/images/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_image(client, test_images, superuser_token_headers,):
    response = client.get(
        f"/api/v1/images/{str(test_images.id)}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_images.id),
        "path": str(test_images.path),
        "public_path": test_images.public_path,
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523',
    }

# def test_create_image(client, test_posts, test_superuser, superuser_token_headers):
#
#     with open("app/api/api_v1/routers/tests/image/image.png", "rb") as image_file:
#         encoded_string = base64.b64encode(image_file.read())
#
#     data = {"pictures": encoded_string}
#     # new = json.dumps(data)
#
#     response = client.post(f"/api/v1/images", headers={'Content-Type': 'application/json',
#                                                        'Authorization': superuser_token_headers.get('Authorization')},
#                            data=data)
#     assert response.status_code == 200


def test_post_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/images/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers)
    assert response.status_code == 404


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/images/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
    response = client.delete("/api/v1/images/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
