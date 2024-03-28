import aiohttp

async def fetch_url(url):
    async with aiohttp.ClientSession() as session:
        response = await session.get( url)
        return await response.text()

