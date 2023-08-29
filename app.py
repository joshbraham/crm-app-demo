""" Flask Web App with MS SQL """

from platform import platform
from flask import Flask, render_template, request
from config import *
import pyodbc

app = Flask(__name__)

if platform().startswith("mac"):
    connection_string = f"\
        DRIVER={DRIVER};\
        SERVER={SERVER};\
        DATABASE={DATABASE};\
        UID={USERNAME};\
        PWD={PASSWORD};"
else:
    connection_string = f"\
        DRIVER={DRIVER};\
        SERVER={SERVER};\
        DATABASE={DATABASE};\
        TRUSTED_CONNECTION={TRUSTED_CONNECTION}"


def execute_query(query, params=None, method="GET"):
    """Define a helper function to execute SQL queries"""
    try:
        with pyodbc.connect(connection_string, timeout=TIMEOUT) as conn:
            try:
                with conn.cursor() as cursor:
                    if params:
                        cursor.execute(query, params)
                    else:
                        cursor.execute(query)
                    if method != "GET":
                        conn.commit()
                        cursor.execute(
                            """
                            SELECT TOP 1 CustomerID FROM Customers ORDER BY CustomerID DESC
                        """
                        )
                        get_id = cursor.fetchall()
                        return get_id[0][0]
                    return cursor.fetchall()
            except Exception as e:
                return e
    except Exception as e:
        return e


@app.route("/")
def index():
    """Define Index route"""
    return render_template("index.html")


@app.route("/customers", methods=["GET", "POST"])
def customers():
    """Define /customres route"""
    if request.method == "GET":
        # Get all rows from the table
        rows = execute_query("SELECT * FROM customers")
        if not isinstance(rows, list):
            return render_template("error.html", type=type(rows).__name__, message=rows)
        return render_template("customers.html", rows=rows)

    # Create a new row in the table
    customer_name = request.form["CustomerName"]
    contact_name = request.form["ContactName"]
    address = request.form["Address"]
    city = request.form["City"]
    postal_code = request.form["PostalCode"]
    country = request.form["Country"]
    customer_id = execute_query(
        f"""
        INSERT INTO 
            Customers 
        (CustomerName, ContactName, Address, City, PostalCode, Country) 
        VALUES
            ('{customer_name}', '{contact_name}',
            '{address}', '{city}',
            '{postal_code}', '{country}')
        """,
        method="INSERT",
    )
    if not isinstance(customer_id, int):
        return render_template(
            "error.html", type=type(customer_id).__name__, message=customer_id
        )
    return render_template(
        "customer-success.html", customer_id=customer_id, data=request.form
    )


@app.route("/suppliers", methods=["GET", "POST"])
def suppliers():
    """Define /proucts route"""
    if request.method == "GET":
        # Get all rows from the table
        rows = execute_query("SELECT * FROM suppliers")
        if not isinstance(rows, list):
            return render_template("error.html", type=type(rows).__name__, message=rows)
        return render_template("suppliers.html", rows=rows)

    # Create a new row in the table
    supplier_name = request.form["SupplierName"]
    contact_name = request.form["ContactName"]
    address = request.form["Address"]
    city = request.form["City"]
    postal_code = request.form["PostalCode"]
    country = request.form["Country"]
    phone = request.form["Phone"]
    supplier_id = execute_query(
        f"""
        INSERT INTO 
            Suppliers 
        (SupplierName, ContactName, Address, City, PostalCode, Country, Phone) 
        VALUES
            ('{supplier_name}', '{contact_name}',
            '{address}', '{city}',
            '{postal_code}', '{country}', '{phone}')
        """,
        method="INSERT",
    )
    if not isinstance(supplier_id, int):
        return render_template(
            "error.html", type=type(supplier_id).__name__, message=supplier_id
        )
    return render_template(
        "supplier-success.html", supplier_id=supplier_id, data=request.form
    )


# Run the app
if __name__ == "__main__":
    app.run()
