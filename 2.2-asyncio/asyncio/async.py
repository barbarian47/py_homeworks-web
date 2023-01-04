import re
import asyncio
import datetime
import more_itertools
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String


PG_DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5431/net_asyncio'
engine = create_async_engine(PG_DSN)
Base = declarative_base(bind=engine)
Session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

CHUNCK_SIZE = 10


class People(Base):
    __tablename__ = 'SW_People'

    id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    name = Column(String)
    birth_year = Column(String(10))
    eye_color = Column(String(100))
    gender = Column(String)
    hair_color = Column(String(100))
    height = Column(String(15))
    mass = Column(String(15))
    skin_color = Column(String(100))
    homeworld = Column(String)
    species = Column(String)
    starships = Column(String)
    vehicles = Column(String)
    films = Column(String)


async def get_people(people_id, session):
    api_url = f'https://swapi.dev/api/people/{people_id}'
    async with session.get(api_url) as response:
        return await response.json()


async def get_homeworld(url, session):
    async with session.get(url) as response:
        data = await response.json()

        return data['name']


async def get_details(title):
    result_list = []
    for url in title:
        async with ClientSession() as session:
            response = await session.get(url)
        result = await response.json()
        result_list.append(result)

    return result_list


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()

    async with ClientSession() as http_session:
        count = 1
        tasks = (asyncio.create_task(get_people(i, http_session)) for i in range(1, 101))
        for task_chunck in more_itertools.chunked(tasks, CHUNCK_SIZE):
            async with Session() as db_session:
                for task in task_chunck:
                    result = await task
                    try:
                        print(count, '-', result['name'], result['url'])
                        count += 1
                        db_session.add(People(
                                    api_id=int(''.join(re.findall(r'\d+', result['url']))),
                                    name=result['name'],
                                    birth_year=result['birth_year'],
                                    eye_color=result['eye_color'],
                                    gender=result['gender'],
                                    hair_color=result['hair_color'],
                                    height=result['height'],
                                    mass=result['mass'],
                                    skin_color=result['skin_color'],
                                    homeworld=await get_homeworld(result['homeworld'], http_session),
                                    species=', '.join([i['name'] for i in await get_details(result['species'])]),
                                    starships=', '.join([i['name'] for i in await get_details(result['starships'])]),
                                    vehicles=', '.join([i['name'] for i in await get_details(result['vehicles'])]),
                                    films=', '.join([i['title'] for i in await get_details(result['films'])])
                        ))
                    except KeyError:
                        print(result)
                        count += 1
                await db_session.commit()


start = datetime.datetime.now()
asyncio.run(main())
finish = datetime.datetime.now()
print(finish - start)
