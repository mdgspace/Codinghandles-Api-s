import aiohttp


async def graphql(query, variables, opertation):
    payload= {
        'query':query,
        'operationName': opertation,
        'variables': variables
    }
    async with aiohttp.ClientSession() as session:
        async with session.post('https://leetcode.com/graphql/', json=payload) as response:
            if response.status == 200:
                res= await response.json()
                return res["data"]
            return None
            

        
