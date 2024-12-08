from .database import engine, Base

# just importing all the models is enough to have them created
# flake8: noqa
from .item.models.sql_model import SQLAlchemyItem
from .user.models.sql_model import SQLAlchemyCartItem, SQLAlchemyUser


def create_db_schema():
    Base.metadata.create_all(bind=engine)
