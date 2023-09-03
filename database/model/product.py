from sqlalchemy import Column, Float, Integer, String

from database.database import Database

BASE = Database().BASE


class Product(BASE):
    """Class for creating the product table"""

    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(30), unique=True)
    price = Column(Float)
    supplier = Column(String(100))
    category = Column(String(20))
    description = Column(String(500))

    def __init__(
        self,
        name: str,
        price: float,
        supplier: str,
        category: str,
        description: str,
    ):
        self.name = name
        self.price = price
        self.supplier = supplier
        self.category = category
        self.description = description
