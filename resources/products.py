from urllib.parse import unquote
from flask_openapi3 import Tag

from app import app, database, log
from database.model.product import Product
from database.model.sales import Sales
from schemas.products import (
    AddProductSchema,
    MessageProductSchema,
    ProductNameSchema,
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
    log.add_message("Add_procuct route accessed")

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

        log.add_message(f"Checking if the {name} product exists")

        if len(registered_product) > 0:
            raise Exception("Product already registered")

        log.add_message(f"{name} product does not exist")

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

        log.add_message(f"{name} added")

        return_data = {
            "message": "Added Product",
            "product": formatted_response
        }

        log.add_message(f"Add_procuct response: {return_data}")
        log.add_message("Add_procuct status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Add_procuct response: {return_data}")
        log.add_message("Add_procuct status: 400")
        log.add_message("")

        return return_data, 400


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
    log.add_message("Update_stock route accessed")

    name = unquote(unquote(form.name)).strip().title()
    new_stock = form.new_stock

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        log.add_message(f"Checking if the {name} product exists")

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        log.add_message(f"{name} product exists")

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

        log.add_message(f"Updated {name} stock to {new_stock}")

        return_data = {
            "message": "Updated stock",
            "product": formatted_response
        }

        log.add_message(f"Update_stock response: {return_data}")
        log.add_message("Update_stock status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Update_stock response: {return_data}")
        log.add_message("Update_stock status: 400")
        log.add_message("")

        return return_data, 400


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
    log.add_message("Delete_product route accessed")

    name = unquote(unquote(form.name)).strip().title()

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        log.add_message(f"Checking if the {name} product exists")

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        log.add_message(f"{name} product exists")

        product_sold = database.select_value_table_parameter(
            column=Sales.name, filter_select={Sales.name: name}
        )

        log.add_message("Checking if the product has already been sold")

        if len(product_sold) > 0:
            raise Exception(
                f"{name} has already been sold, it's not possible to delete it"
            )

        log.add_message("The product has not yet been sold")

        database.delete_data_table(
            table=Product,
            filter_delete={Product.name: name},
        )

        log.add_message(f"{name} deleted")

        return_data = {"message": "Product deleted", "name": name}

        log.add_message(f"Delete_product response: {return_data}")
        log.add_message("Delete_product status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Delete_product response: {return_data}")
        log.add_message("Delete_product status: 400")
        log.add_message("")

        return return_data, 400


@app.get(
    "/get_product/",
    tags=[TAG_PRODUCTS],
    responses={
        "200": MessageProductSchema,
        "400": SingleMessageSchema,
    },
)
def get_product(query: ProductNameSchema):
    """Method to obtain data of registered products."""
    log.add_message("Get_product route accessed")

    name = unquote(unquote(query.name)).strip().title()

    try:
        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        log.add_message(f"Checking if the {name} product exists")

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        log.add_message(f"{name} product exists")

        product_data = database.select_data_table(
            table=Product,
            filter_select={Product.name: name},
        )[0]

        log.add_message("Products listed")

        formatted_response = format_product_response(product_data)

        return_data = {
            "message": "Product all data",
            "product": formatted_response
        }

        log.add_message(f"Get_product response: {return_data}")
        log.add_message("Get_product status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Get_product response: {return_data}")
        log.add_message("Get_product status: 400")
        log.add_message("")

        return return_data, 400
