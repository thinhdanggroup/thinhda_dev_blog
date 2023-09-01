from fastapi import FastAPI, Request
import time
import asyncio

app = FastAPI()

@app.get("/")
async def slow_endpoint(request: Request):
    x_request_id = request.headers.get('X-Request-ID', 'Not provided')
    print("Slow endpoint called",x_request_id)
    await asyncio.sleep(3)
    return {"message": "This is a slow endpoint", "X-Request-ID": x_request_id}
