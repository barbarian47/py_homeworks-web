import asyncio
import aiohttp


async def main():
    async with aiohttp.ClientSession() as session:
        async with session.post('http://127.0.0.1:8080/advt/',
                         json={
                             'title': 'ADVT #1',
                             'author': 'user1',
                             'description': 'sell old elephant'
                               }) as resp:
            print(resp.status)
            print(await resp.json())

        async with session.get('http://127.0.0.1:8080/advt/1', ) as resp:
            print(resp.status)
            print(await resp.json())

        async with session.patch('http://127.0.0.1:8080/advt/1', json={'author': 'patched'}) as resp:
            print(resp.status)
            print(await resp.json())

        async with session.delete('http://127.0.0.1:8080/advt/1') as resp:
            print(resp.status)
            print(await resp.json())

        async with session.get('http://127.0.0.1:8080/advt/1', ) as resp:
            print(resp.status)
            print(await resp.json())


asyncio.run(main())
