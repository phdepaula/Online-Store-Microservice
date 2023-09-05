from datetime import datetime
from sqlalchemy import Column, Float, Integer, String

from database.database import Database

BASE = Database().BASE


class Sales(BASE):
    """Class created for sold products"""

    __tablename__ = "sales"

    sales_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30))
    quantity = Column(Integer)
    value = Column(Float)
    sale_status = Column(String(10), default="open")
    sale_date = Column(String(10), default=datetime.today())
    zip_code = Column(String(15))
    country = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    street = Column(String(50))
    neighborhood = Column(String(20))

    def __init__(
        self,
        name: str,
        quantity: int,
        value: float,
        zip_code: str,
        country: str,
        city: str,
        state: str,
        street: str,
        neighborhood: str,
    ):
        self.name = name
        self.quantity = quantity
        self.value = value
        self.zip_code = zip_code
        self.country = country
        self.city = city
        self.state = state
        self.street = street
        self.neighborhood = neighborhood
