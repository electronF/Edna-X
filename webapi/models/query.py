# Built-in modules
from datetime import datetime

# External modules
from sqlalchemy import (
    Integer,
    String, 
    DateTime
)

from sqlalchemy.orm import (
    mapped_column,
)

from marshmallow_sqlalchemy import auto_field

#Local modules
from configs import database, marsmallow


class Query(database.Model):
    __tablename__ = "documents"
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String, nullable=False)
    email = mapped_column(String)
    query = mapped_column(String, nullable=False)
    query_response = mapped_column(String)
    user_id = mapped_column(String, nullable=False)
    sended_at = mapped_column(DateTime)
    received_at = mapped_column(
        DateTime, 
        default=datetime.utcnow, 
        onupdate=datetime.utcnow
    )
    replyed_at = mapped_column(DateTime)
    
    def __repr__(self) -> str:
        return """Query(id={}, query='{}', query_response='{}' username='{}', email='{}' user_id='{}', sended_at='{}', received_at='{}' replyed_at='{}')""".format(
            self.id,
            self.query[:25],
            self.query_response[:25],
            self.username,
            self.email,
            self.user_id,
            self.sended_at,
            self.received_at,
            self.replyed_at
        )


class QuerySchema(marsmallow.SQLAlchemySchema):
    class Meta:
        model = Query
        load_instance = True
    id = auto_field()
    username = auto_field()
    email = auto_field()
    query = auto_field()
    query_response = auto_field()
    user_id = auto_field()
    sended_at = auto_field()
    received_at = auto_field()
    replyed_at = auto_field()
