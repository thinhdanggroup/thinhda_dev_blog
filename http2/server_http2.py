from quart import make_response, Quart, render_template, url_for, request
import asyncio

app = Quart(__name__)



@app.route('/')
async def slow_endpoint():
    # x_request_id = request.headers.get('X-Request-ID', 'Not provided')
    x_request_id = request.headers.get("X-Request-ID'","Not provided")
    print("Slow endpoint called",x_request_id)
    await asyncio.sleep(3)
    return {"message": "This is a slow endpoint", "X-Request-ID": x_request_id}


if __name__ == '__main__':
    app.run(
        host='localhost', 
        port=8000, 
        certfile='cert.pem', 
        keyfile='key.pem',
    )
