from urllib.parse import unquote

import requests
from flask_openapi3 import Tag

from app import app, database, log
from database.model.product import Product
from database.model.sales import Sales
from resources.products import update_stock
from schemas.products import UpdateProductSchema
from schemas.sales import (
    AddSalesSchema,
    CloseSaleSchema,
    MessageSalesSchema,
    SaleResponseSchema,
    SingleMessageSchema,
    format_add_sale_response,
)

TAG_SALES = Tag(name="SALES", description="Sales data control routes.")


@app.post(
    "/add_sale",
    tags=[TAG_SALES],
    responses={
        "200": MessageSalesSchema,
        "400": SingleMessageSchema,
    },
)
def add_sale(form: AddSalesSchema):
    """Add a new sale to the sales table."""
    log.add_message("Add_sale route accessed")

    name = unquote(unquote(form.name)).strip().title()
    quantity = form.quantity
    zip_code = unquote(unquote(form.zip_code))
    country = unquote(unquote(form.country)).strip().title()
    city = unquote(unquote(form.city)).strip().title()
    state = unquote(unquote(form.state)).strip().title()
    street = unquote(unquote(form.street)).strip().title()
    neighborhood = unquote(unquote(form.neighborhood)).strip().title()

    try:
        log.add_message("Checking if the country was informed")

        if len(country.strip()) == 0:
            raise Exception("Country name not given")

        log.add_message("Country informed")
        log.add_message(
            "Checking if the zip is Brazilian and if it is formatted correctly"
        )

        if (
            len(zip_code) not in [9, 10] or len(zip_code.split("-")) != 2
        ) and country in [
            "Brazil",
            "Brasil",
        ]:
            raise Exception(
                "Incorrect zip code, expected format: nnnnn-nnn or nnnnn-nnnn"
            )

        log.add_message("Zip code entered correctly")

        registered_product = database.select_value_table_parameter(
            column=Product.name, filter_select={Product.name: name}
        )

        log.add_message(f"Checking if the {name} product exists")

        if len(registered_product) == 0:
            raise Exception("The product does not exist")

        log.add_message(f"{name} product exists")

        available_stock = database.select_value_table_parameter(
            column=Product.available_stock, filter_select={Product.name: name}
        )

        log.add_message(f"Checking if there are {quantity} units in stock")

        if quantity > available_stock:
            raise Exception(
                f"There are only {available_stock} unit(s) available in stock"
            )

        log.add_message(f"Available stock is {available_stock} units")
        log.add_message("")

        new_stock = available_stock - quantity
        update_form = UpdateProductSchema(name=name, new_stock=new_stock)
        update_response = update_stock(update_form)[0]

        if update_response["message"] != "Updated stock":
            raise Exception("Error updating stock")

        price = database.select_value_table_parameter(
            column=Product.price, filter_select={Product.name: name}
        )
        value = round(price * quantity, 2)

        new_sale = Sales(
            name=name,
            quantity=quantity,
            value=value,
            zip_code=zip_code,
            country=country,
            city=city,
            state=state,
            street=street,
            neighborhood=neighborhood,
        )
        formatted_response = format_add_sale_response(sale=new_sale)
        database.insert_data_table(new_sale)

        log.add_message(f"{name} sale added")

        return_data = {"message": "Added Sale", "sale": formatted_response}

        log.add_message(f"Add_sale response: {return_data}")
        log.add_message("Add_sale status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Add_sale response: {return_data}")
        log.add_message("Add_sale status: 400")
        log.add_message("")

        return return_data, 400


@app.put(
    "/close_sale",
    tags=[TAG_SALES],
    responses={
        "200": SingleMessageSchema,
        "400": SingleMessageSchema,
    },
)
def close_sale(form: CloseSaleSchema):
    """Closes a sale from the sales table."""
    log.add_message("Close_sale route accessed")

    sales_id = form.sales_id

    try:
        registered_sale = database.select_value_table_parameter(
            column=Sales.sales_id, filter_select={Sales.sales_id: sales_id}
        )

        log.add_message(f"Checking if the sale {sales_id} exists")

        if not registered_sale:
            raise Exception(f"The sale {sales_id} does not exist")

        log.add_message("The sale exists")

        sale_status = database.select_value_table_parameter(
            column=Sales.sale_status, filter_select={Sales.sales_id: sales_id}
        )

        log.add_message(f"Checking if sale {sales_id} is closed")

        if sale_status == "Closed":
            raise Exception(f"The sale {sales_id} is already closed")

        log.add_message("The sale is open")

        new_sale_status = "Closed"
        database.update_data_table(
            table=Sales,
            filter_update={Sales.sales_id: sales_id},
            new_data={Sales.sale_status: new_sale_status},
        )

        log.add_message(f"Sale {sales_id} closed")

        return_data = {"message": f"Sale {sales_id} closed successfully"}

        log.add_message(f"Close_sale response: {return_data}")
        log.add_message("Close_sale status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Close_sale response: {return_data}")
        log.add_message("Close_sale status: 400")
        log.add_message("")

        return return_data, 400


@app.get(
    "/get_sales",
    tags=[TAG_SALES],
    responses={
        "200": SaleResponseSchema,
        "400": SingleMessageSchema,
    },
)
def get_sales():
    """Method to get all open sales data."""
    log.add_message("Get_sales route accessed")

    try:
        status_open = "Open"
        open_sales = database.select_data_table(
            table=Sales,
            filter_select={Sales.sale_status: status_open},
        )

        log.add_message("Checking if there are open sales")

        if len(open_sales) == 0:
            raise Exception("There are no open sales")

        log.add_message(f"There are {len(open_sales)} open sales")
        log.add_message("")

        full_content = []

        for sale in open_sales:
            sale_product_data = {}

            sales_id = sale.sales_id
            sale_product_data["sales_id"] = sales_id

            sale_date = sale.sale_date
            sale_product_data["sale_date"] = sale_date

            other_sale_data = format_add_sale_response(sale)
            sale_product_data.update(other_sale_data)

            get_product_url = "http://127.0.0.1:5000/get_product/?name="
            name = sale_product_data.get("name")
            response_get_product = requests.get(f"{get_product_url}{name}")

            if response_get_product.status_code == 200:
                product_data = response_get_product.json()["product"]
                sale_product_data.update(product_data)

            full_content.append(sale_product_data)

        return_data = {
            "message": "Open sales consulted",
            "sales": full_content
        }

        log.add_message(f"Get_sales response: {return_data}")
        log.add_message("Get_sales status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Get_sales response: {return_data}")
        log.add_message("Get_sales status: 400")
        log.add_message("")

        return return_data, 400


@app.delete(
    "/delete_sale",
    tags=[TAG_SALES],
    responses={
        "200": SingleMessageSchema,
        "400": SingleMessageSchema,
    },
)
def delete_sale(form: CloseSaleSchema):
    """Deletes an open sale from the sales table."""
    log.add_message("Delete_sale route accessed")

    sales_id = form.sales_id

    try:
        registered_sale = database.select_value_table_parameter(
            column=Sales.sale_status, filter_select={Sales.sales_id: sales_id}
        )

        log.add_message(f"Checking if the sale {sales_id} exists")

        if not registered_sale:
            raise Exception(f"The sale {sales_id} does not exist")

        log.add_message("The sale exists")

        sale_status = database.select_value_table_parameter(
            column=Sales.sale_status, filter_select={Sales.sales_id: sales_id}
        )

        log.add_message(f"Checking if sale {sales_id} is closed")

        if sale_status == "Closed":
            raise Exception(
                f"The sale {sales_id} is closed, it is not possible to delete"
            )

        log.add_message("The sale is open")

        database.delete_data_table(
            table=Sales,
            filter_delete={Sales.sales_id: sales_id},
        )

        log.add_message(f"Sale {sales_id} deleted")

        return_data = {"message": f"Sale {sales_id} deleted successfully"}

        log.add_message(f"Delete_sale response: {return_data}")
        log.add_message("Delete_sale status: 200")
        log.add_message("")

        return return_data, 200
    except Exception as error:
        return_data = {"message": f"Error: {error}"}

        log.add_message(f"Delete_sale response: {return_data}")
        log.add_message("Delete_sale status: 400")
        log.add_message("")

        return return_data, 400
