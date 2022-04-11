from app.db import models


def test_get_files(client, test_files, superuser_token_headers):
    response = client.get("/api/v1/files", headers=superuser_token_headers)
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": str(test_files.id),
            "width": test_files.width,
            "height": test_files.height,
            "path": str(test_files.path),
            "public_path": test_files.public_path,
            "post_id": str(test_files.post_id),
            "created_at": '2022-02-21T14:00:17.961523',
            "updated_at": '2022-02-21T14:00:17.961523',

        }
    ]


def test_file_not_belongs_to_user(client, test_files, user_token_headers):
    response = client.delete(
        f"/api/v1/files/{test_files.id}", headers=user_token_headers
    )
    assert response.status_code == 404


def test_delete_file(client, test_files, test_db, superuser_token_headers):
    response = client.delete(
        f"/api/v1/files/{test_files.id}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert test_db.query(models.Files).all() == []


def test_delete_file_not_found(client, superuser_token_headers):
    response = client.delete(
        "/api/v1/files/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers
    )
    assert response.status_code == 404


def test_get_post(client, test_files, superuser_token_headers,):
    response = client.get(
        f"/api/v1/files/{str(test_files.id)}", headers=superuser_token_headers
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": str(test_files.id),
        "width": test_files.width,
        "height": test_files.height,
        "path": str(test_files.path),
        "public_path": test_files.public_path,
        "post_id": str(test_files.post_id),
        "created_at": '2022-02-21T14:00:17.961523',
        "updated_at": '2022-02-21T14:00:17.961523',

    }


def test_post_not_found(client, superuser_token_headers):
    response = client.get("/api/v1/files/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b", headers=superuser_token_headers)
    assert response.status_code == 404


def test_create_file(client, test_posts, test_superuser, superuser_token_headers):
    response = client.post(f"/api/v1/upload_file/{str(test_posts.id)}",
                           headers=superuser_token_headers,
                           files={"file": ("filename", open('app/api/api_v1/routers/tests/image/image.png', "rb"),
                                           "image/jpeg")})
    assert response.status_code == 200

    assert 'AWSAccessKeyId' in response.json()
    assert 'policy' in response.json()
    assert 'signature' in response.json()


def test_unauthenticated_routes(client):
    response = client.get("/api/v1/files")
    assert response.status_code == 401
    response = client.get("/api/v1/files/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
    response = client.delete("/api/v1/files/4f58bd00-5bc1-4aea-9c4b-8ddb23b6016b")
    assert response.status_code == 401
