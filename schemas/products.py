from pydantic import BaseModel

from database.model.product import Product


class AddProductSchema(BaseModel):
    """
    Defines how the adding structure \
    in the product database should be.
    """

    name: str = "Iphone 13"
    price: float = 8300.00
    supplier: str = "Apple"
    category: str = "Cell phone"
    description: str = (
        "One of the most popular and influential mobile devices in the world"
    )
    available_stock: int = 1


class MessageProductSchema(BaseModel):
    """
    Defines how the API response should be \
    for a successfully registered product.
    """

    message: str
    product: dict


class SingleMessageSchema(BaseModel):
    """
    Defines how the API response should be \
    when you want to send just one message.
    """

    message: str


class UpdateProductSchema(BaseModel):
    """
    Defines how the data informed \
    for stock update should be.
    """

    name: str = "Iphone 13"
    new_stock: int = 1


class ProductNameSchema(BaseModel):
    """
    Defines that a name must be informed \
    to execute the route
    """

    name: str


def format_product_response(product: Product) -> dict:
    """
    Format the API response for a added product.
    """
    response = {
        "name": product.name,
        "price": product.price,
        "supplier": product.supplier,
        "category": product.category,
        "description": product.description,
        "available_stock": product.available_stock,
    }

    return response


def format_update_product_response(name: str, old_stock: int, new_stock: int) -> dict:
    """
    Format the API response for a update product.
    """
    response = {
        "name": name,
        "old_available_stock": old_stock,
        "new_available_stock": new_stock,
    }

    return response
