import httpx
import asyncio
import time 
import uuid

async def fetch_data(client, request_id):
    headers = {'X-Request-ID': request_id}
    res = await client.get('http://localhost:8000/', headers=headers)
    print("Response: ", res.json())
    print(res.http_version)
    return res.json()

async def make_requests():
    async with httpx.AsyncClient(http2=True) as client:
        tasks = []
        for i in range(10):
            request_id = str(i)
            tasks.append(fetch_data(client, request_id))
        responses = await asyncio.gather(*tasks)
        # for i, response in enumerate(responses):
        #     print(f"Received response {i + 1}: {response}")
    

# Run the async function
asyncio.run(make_requests())