from typing import List

import strawberry
from fastapi import FastAPI
from strawberry.asgi import GraphQL
import uvicorn


@strawberry.type
class User:
    id: int
    name: str
    age: int


Users: List[User] = [User(id=1, name="Patrick", age=100)]


@strawberry.type
class Query:
    @strawberry.field
    def user(self, id: int) -> User:
        for user in Users:
            if user.id == id:
                return user
        raise ValueError(f"User with id {id} not found")


@strawberry.type
class AddUserResult:
    user: User


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_user(self, name: str, age: int) -> AddUserResult:
        # add user to database
        user = User(id=len(Users) + 1, name=name, age=age)
        Users.append(user)
        print(f"Added user: {user}")
        return AddUserResult(user=user)


schema = strawberry.Schema(query=Query, mutation=Mutation)

graphql_app = GraphQL(schema)

app = FastAPI()
app.add_route("/graphql", graphql_app)
app.add_websocket_route("/graphql", graphql_app)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
