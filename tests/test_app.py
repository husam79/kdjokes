from main import get_random_joke
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from main import app, get_session
from sqlmodel.pool import StaticPool
import pytest
from joke import Joke

@pytest.fixture(name="session")  
def session_fixture():  
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session  

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_joke(client: TestClient):
    response = client.post("/", json={"content": "My long joke is here my dear!!", "source": "manual"})
    data = response.json()

    assert response.status_code == 200
    assert data["content"] == "My long joke is here my dear!!"
    assert data["source"] == "manual"
    assert data["id"] is not None

def test_joke_length(client: TestClient, session: Session):
    session.add(
        Joke(
            content="This is my new long joke to test this requirements of the test",
            source="manual"
        )
    )
    client = TestClient(app)
    response = client.get("/text/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) > 40

def test_joke_word_count(client: TestClient, session: Session):
    session.add(
        Joke(
            content="This is my new long joke to test this requirements of the test",
            source="manual"
        )
    )
    client = TestClient(app)
    response = client.get("/text/")
    data = response.json()

    assert response.status_code == 200
    assert len(data.split(' ')) > 5
