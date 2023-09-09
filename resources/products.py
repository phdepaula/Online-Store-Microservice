from urllib.parse import unquote
from flask_openapi3 import Tag

from app import app, database
from database.model.product import Product
from database.model.sales import Sales
from schemas.products import (
    AddProductSchema,
    ProductNameSchema,
    MessageProductSchema,
    SingleMessageSchema,
    UpdateProductSchema,
    format_product_response,
    format_update_product_response,
)

TAG_PRODUCTS = Tag(name="Product", description="Product data control routes.")


@app.post(
    "/add_product",
    tags=[TAG_PRODUCTS],
    responses={
        "200": MessageProductSchema,
        "400": SingleMessageSchema,
    },
)
def add_product(form: AddProductSchema):
    """Add a new product to the product table."""
    name = unquote(unquote(form.name)).strip().title()
    price = round(form.price, 2)
    supplier = unquote(unquote(form.supplier)).strip().title()
    category = unquote(unquote(form.category)).strip().title()
    description = unquote(unquote(form.description)).strip()
    available_stock = form.available_stock

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        if len(registered_product) > 0:
            raise Exception("Product already registered")

        new_product = Product(
            name=name,
            price=price,
            supplier=supplier,
            category=category,
            description=description,
            available_stock=available_stock,
        )
        formatted_response = format_product_response(product=new_product)
        database.insert_data_table(new_product)

        return {"message": "Added Product", "product": formatted_response}, 200
    except Exception as error:
        return {"message": f"Error: {error}"}, 400


@app.put(
    "/update_stock",
    tags=[TAG_PRODUCTS],
    responses={
        "200": MessageProductSchema,
        "400": SingleMessageSchema,
    },
)
def update_stock(form: UpdateProductSchema):
    """Updates the available stock of the specified product."""
    name = unquote(unquote(form.name)).strip().title()
    new_stock = form.new_stock

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        old_stock = database.select_value_table_parameter(
            column=Product.available_stock, filter_select={Product.name: name}
        )
        formatted_response = format_update_product_response(
            name=name, old_stock=old_stock, new_stock=new_stock
        )

        database.update_data_table(
            table=Product,
            filter_update={Product.name: name},
            new_data={Product.available_stock: new_stock},
        )

        return {"message": "Updated stock", "product": formatted_response}, 200
    except Exception as error:
        return {"message": f"Error: {error}"}, 400


@app.delete(
    "/delete_product",
    tags=[TAG_PRODUCTS],
    responses={
        "200": MessageProductSchema,
        "400": SingleMessageSchema,
    },
)
def delete_product(form: ProductNameSchema):
    """Delete a product from the product table."""
    name = unquote(unquote(form.name)).strip().title()

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        product_sold = database.select_value_table_parameter(
            column=Sales.name, filter_select={Sales.name: name}
        )

        if len(product_sold) > 0:
            raise Exception(
                f"{name} has already been sold, it's not possible to delete it"
            )

        database.delete_data_table(
            table=Product,
            filter_delete={Product.name: name},
        )

        return {"message": "Product deleted", "name": name}, 200
    except Exception as error:
        return {"message": f"Error: {error}"}, 400


@app.get(
    "/get_product/<string:name>",
    tags=[TAG_PRODUCTS],
    responses={
        "200": MessageProductSchema,
        "400": SingleMessageSchema,
    },
)
def get_product(query: ProductNameSchema):
    """Method to obtain data of registered products."""
    name = unquote(unquote(query.name)).strip().title()

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        product_data = database.select_data_table(
            table=Product,
            filter_select={Product.name: name},
        )[0]

        formatted_response = format_product_response(product_data)

        return {"message": "Product all data", "product": formatted_response}, 200
    except Exception as error:
        return {"message": f"Error: {error}"}, 400
