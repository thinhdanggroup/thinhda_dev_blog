from fastapi.testclient import TestClient
from graphql_fastapi.graphql_fastapi.main import app

client = TestClient(app)


def test_get_user():
    response = client.post("/graphql", json={
        "query": """
            query($id: Int!) {
                user(id: $id) {
                    id
                    name
                    age
                }
            }
        """,
        "variables": {
            "id": 1
        }
    })

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "user": {
                "id": 1,
                "name": "Patrick",
                "age": 100
            }
        }
    }


def test_get_user_not_found():
    response = client.post("/graphql", json={
        "query": """
            query($id: Int!) {
                user(id: $id) {
                    id
                    name
                    age
                }
            }
        """,
        "variables": {
            "id": 100
        }
    })

    assert response.status_code == 200
    assert "errors" in response.json()
    assert response.json()["errors"][0]["message"] == "User with id 100 not found"


def test_add_user():
    response = client.post("/graphql", json={
        "query": """
            mutation($name: String!, $age: Int!) {
                addUser(name: $name, age: $age) {
                    user {
                        name
                        age
                    }
                }
            }
        """,
        "variables": {
            "name": "John",
            "age": 25
        }
    })

    assert response.status_code == 200
    assert response.json() == {
        "data": {
            "addUser": {
                "user": {
                    "name": "John",
                    "age": 25
                }
            }
        }
    }
