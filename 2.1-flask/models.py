from sqlalchemy import Column, Integer, String, DateTime, func, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker


DSN = 'postgresql://postgres:postgres@127.0.0.1:5434/net_flask_4'

engine = create_engine(DSN)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Advt(Base):

    __tablename__ = 'advt'

    id = Column(Integer, primary_key=True)
    title = Column(String(300), nullable=False)
    description = Column(String, nullable=False)
    creation_time = Column(DateTime, server_default=func.now())
    author = Column(String, nullable=False)


Base.metadata.create_all(engine)
