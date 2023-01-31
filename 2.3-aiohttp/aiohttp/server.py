import json

from aiohttp import web
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy import Column, String, Integer, DateTime, func
from sqlalchemy.exc import IntegrityError
import pydantic
from typing import Optional


PG_DSN = 'postgresql+asyncpg://postgres:postgres@127.0.0.1:5435/net_aiohttp'
engine = create_async_engine(PG_DSN)
Session = sessionmaker(class_=AsyncSession, bind=engine, expire_on_commit=False)


class ApiError(web.HTTPException):

    def __init__(self, error_message: str | dict):
        message = json.dumps({'status': 'error', 'description': error_message})
        super(ApiError, self).__init__(text=message, content_type='application/json')


class NotFound(ApiError):
    status_code = 404


class BadRequest(ApiError):
    status_code = 400


Base = declarative_base()


class Advt(Base):
    __tablename__ = 'advt'

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    author = Column(String, nullable=False)


async def get_advt(advt_id: int, session: Session):
    advt = await session.get(Advt, advt_id)
    if advt is None:
        raise NotFound(error_message='advt not found')

    return advt

app = web.Application()


class CreateAdvtSchema(pydantic.BaseModel):
    title: str
    description: str
    author: str

    @pydantic.validator('description')
    def len_advt(cls, value):
        if len(value) <= 10:
            raise ValueError('Advertisement is too short')
        return value


class PatchAdvtSchema(pydantic.BaseModel):
    title: Optional[str]
    description: Optional[str]
    author: Optional[str]

    @pydantic.validator('description')
    def len_advt(cls, value):
        if len(value) <= 10:
            raise ValueError('Advertisement is too short')
        return value


class AdvtView(web.View):

    async def get(self):
        advt_id = int(self.request.match_info['advt_id'])
        async with Session() as session:
            advt = await get_advt(advt_id, session)

            return web.json_response({
                'id': advt.id,
                'author': advt.author,
                'title': advt.title,
                'description': advt.description,
                'creation_time': int(advt.creation_time.timestamp())
            })

    async def post(self):
        json_data = await self.request.json()
        json_data_validate = CreateAdvtSchema(**json_data).dict()
        async with Session() as session:
            new_advt = Advt(**json_data_validate)
            try:
                session.add(new_advt)
                await session.commit()
            except IntegrityError:
                raise BadRequest(error_message='advt already exists')
            return web.json_response({'title': new_advt.title})

    async def patch(self):
        advt_id = int(self.request.match_info['advt_id'])
        json_data = await self.request.json()
        json_data_validate = PatchAdvtSchema(**json_data).dict(exclude_none=True)
        async with Session() as session:
            advt = await get_advt(advt_id, session)
            for key, value in json_data_validate.items():
                setattr(advt, key, value)
            session.add(advt)
            await session.commit()
            return web.json_response({
                            'status': 'success',
                            'id': advt.id,
                            'author': advt.author,
                            'title': advt.title,
                            'description': advt.description
                            })

    async def delete(self):
        advt_id = int(self.request.match_info['advt_id'])
        async with Session() as session:
            advt = await get_advt(advt_id, session)
            await session.delete(advt)
            await session.commit()
            return web.json_response({'status': 'success'})


async def init_orm(app):
    print('START')
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await conn.commit()
    yield
    await engine.dispose()
    print('SHUT DOWN')


app.router.add_route('GET', '/advt/{advt_id:\d+}', AdvtView)
app.router.add_route('POST', '/advt/', AdvtView)
app.router.add_route('DELETE', '/advt/{advt_id:\d+}', AdvtView)
app.router.add_route('PATCH', '/advt/{advt_id:\d+}', AdvtView)
app.cleanup_ctx.append(init_orm)
web.run_app(app)
