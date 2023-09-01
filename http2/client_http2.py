import requests 
import httpx
import asyncio
import time 
import uuid
import aiohttp
import concurrent.futures


async def fetch_data(client, request_id):
    headers = {'X-Request-ID': request_id}
    res = await client.get('https://127.0.0.1:8000',headers=headers,verify=False,timeout=10)
    # print("Response: ", res.json())
    # print(res.http_version)
    print(res.status_code)
    print(res.json())
    return res

async def make_requests():
    session = requests.Session()

    tasks = []
    for i in range(10):
        request_id = str(i)

        tasks.append(fetch_data(session, request_id))

    responses = await asyncio.gather(*tasks)

    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:

        loop = asyncio.get_event_loop()
        futures = [
            loop.run_in_executor(
                executor, 
                fetch_data, 
                session,
                request_id
            )
            for i in range(20)
        ]
        for response in await asyncio.gather(*futures):
            pass
        # for i, response in enumerate(responses):
        #     print(f"Received response {i + 1}: {response}")
    

# Run the async function
asyncio.run(make_requests())