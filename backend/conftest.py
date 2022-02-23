import datetime

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database
from fastapi.testclient import TestClient
import typing as t

from app.core import config, security
from app.db.session import Base, get_db
from app.db import models
from app.main import app


def get_test_db_url() -> str:
    return f"{config.SQLALCHEMY_DATABASE_URI}_test"


@pytest.fixture
def test_db():
    """
    Modify the db session to automatically roll back after each test.
    This is to avoid tests affecting the database state of other tests.
    """
    # Connect to the test database
    engine = create_engine(
        get_test_db_url(),
    )

    connection = engine.connect()
    trans = connection.begin()

    # Run a parent transaction that can roll back all changes
    test_session_maker = sessionmaker(
        autocommit=False, autoflush=False, bind=engine
    )
    test_session = test_session_maker()
    test_session.begin_nested()

    @event.listens_for(test_session, "after_transaction_end")
    def restart_savepoint(s, transaction):
        if transaction.nested and not transaction._parent.nested:
            s.expire_all()
            s.begin_nested()

    yield test_session

    # Roll back the parent transaction after the test is complete
    test_session.close()
    trans.rollback()
    connection.close()


@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    """
    Create a test database and use it for the whole test session.
    """

    test_db_url = get_test_db_url()

    # Create the test database
    assert not database_exists(
        test_db_url
    ), "Test database already exists. Aborting tests."
    create_database(test_db_url)
    test_engine = create_engine(test_db_url)
    Base.metadata.create_all(test_engine)

    # Run the tests
    yield

    # Drop the test database
    drop_database(test_db_url)


@pytest.fixture
def client(test_db):
    """
    Get a TestClient instance that reads/write to the test database.
    """

    def get_test_db():
        yield test_db

    app.dependency_overrides[get_db] = get_test_db

    yield TestClient(app)


@pytest.fixture
def test_password() -> str:
    return "securepassword"


def get_password_hash() -> str:
    """
    Password hashing can be expensive so a mock will be much faster
    """
    return "supersecrethash"


@pytest.fixture
def test_user(test_db) -> models.User:
    """
    Make a test user in the database
    """

    user = models.User(
        email="fake@email.com",
        hashed_password=get_password_hash(),
        is_active=True,
    )
    test_db.add(user)
    test_db.commit()
    return user


@pytest.fixture
def test_superuser(test_db) -> models.User:
    """
    Superuser for testing
    """

    user = models.User(
        email="fakeadmin@email.com",
        hashed_password=get_password_hash(),
        is_superuser=True,
    )
    test_db.add(user)
    test_db.commit()
    return user


def verify_password_mock(first: str, second: str) -> bool:
    return True


@pytest.fixture
def user_token_headers(
    client: TestClient, test_user, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_user.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def superuser_token_headers(
    client: TestClient, test_superuser, test_password, monkeypatch
) -> t.Dict[str, str]:
    monkeypatch.setattr(security, "verify_password", verify_password_mock)

    login_data = {
        "username": test_superuser.email,
        "password": test_password,
    }
    r = client.post("/api/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


@pytest.fixture
def test_categories(test_db, test_superuser) -> models.Categories:
    """
    Categories for testing
    """

    categories = models.Categories(
        color="black",
        name="test_category",
        user_id=test_superuser.id,
        category_id=None,
        selected=0,
        created_at='2022-02-21 14:00:17.961523',
        updated_at='2022-02-21 14:00:17.961523',
    )
    test_db.add(categories)
    test_db.commit()
    return categories


@pytest.fixture
def test_posts(test_db, test_superuser) -> models.Posts:
    """
    Post for testing
    """

    posts = models.Posts(
        type="test_type",
        text="test_text",
        user_id=test_superuser.id,
        # files='3fa85f64-5717-4562-b3fc-2c963f66afa6',
        # categories='3fa85f64-5717-4562-b3fc-2c963f66afa6',
        created_at='2022-02-21 14:00:17.961523',
        updated_at='2022-02-21 14:00:17.961523',
    )
    test_db.add(posts)
    test_db.commit()
    return posts


@pytest.fixture
def test_files(test_db, test_posts, test_superuser) -> models.Files:
    """
    Files for testing
    """

    files = models.Files(
        width=50,
        height=50,
        path="test_path",
        public_path="test_path",
        post_id=test_posts.id,
        created_at='2022-02-21 14:00:17.961523',
        updated_at='2022-02-21 14:00:17.961523',
    )
    test_db.add(files)
    test_db.commit()
    return files


@pytest.fixture
def test_images(test_db, test_superuser) -> models.Images:
    """
    Images for testing
    """

    images = models.Images(
        path="test_path",
        public_path="test_path",
        created_at='2022-02-21 14:00:17.961523',
        updated_at='2022-02-21 14:00:17.961523',
    )
    test_db.add(images)
    test_db.commit()
    return images
