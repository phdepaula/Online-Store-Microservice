from pydantic import BaseModel

from database.model.sales import Sales


class AddSalesSchema(BaseModel):
    """
    Defines how the adding structure \
    in the sales database should be.
    """

    name: str = "Iphone 13"
    quantity: int = 1
    zip_code: str = "01025-020"
    country: str = "Brazil"
    city: str = "São Paulo"
    state: str = "SP"
    street: str = "Avenida do Estado"
    neighborhood = ""


class MessageSalesSchema(BaseModel):
    """
    Defines how the API response should be \
    for a successfully registered sale.
    """

    message: str
    sale: dict


class SingleMessageSchema(BaseModel):
    """
    Defines how the API response should be \
    when you want to send just one message.
    """

    message: str


class CloseSaleSchema(BaseModel):
    """
    Defines how the close sale structure \
    should be.
    """

    sales_id: int = 1


class SaleResponseSchema(BaseModel):
    """
    Defines how the response should be \
    when querying a sale.
    """

    message: str
    data: list


def format_add_sale_response(sale: Sales) -> dict:
    """
    Format the API response for a added sale.
    """
    response = {
        "name": sale.name,
        "quantity": sale.quantity,
        "value": sale.value,
        "zip_code": sale.zip_code,
        "country": sale.country,
        "city": sale.city,
        "state": sale.state,
        "street": sale.street,
        "neighborhood": sale.neighborhood,
    }

    return response
