from sqlalchemy import Column, Float, Integer, String
from datetime import datetime

from database.database import Database

BASE = Database().BASE


class Sales(BASE):
    """Class created for sold products"""

    __tablename__ = "sales"

    sales_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    quantity = Column(Integer)
    price = Column(Float)
    sale_status = Column(String(10), default = "open")
    sale_date = Column(String(10), default = datetime.today())
    zip_code = Column(String(9))
    country = Column(String(50))
    city = Column(String(50))
    state = Column(String(50))
    street = Column(String(50))
    neighborhood = Column(String(20))

    def __init__(
        self,
        name: str,
        quantity: int,
        price: float,
        sale_status: str,
        sale_date: datetime,
        zip_cod: str,
        country: str,
        city: str,
        state: str,
        street: str,
        neighborhood: str
    ):
        self.name = name
        self.quantity = quantity
        self.price = price
        self.sale_status = sale_status
        self.sale_date = sale_date
        self.zip_cod = zip_cod
        self.country = country
        self.city = city
        self.state = state
        self.street = street
        self.neighborhood = neighborhood
