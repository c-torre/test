from flask import Flask, render_template, request, session
import pandas as pd

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route("/")
def home():
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv("product_prices.csv")

    # Convert the DataFrame to a list of dictionaries
    products = df.to_dict("records")

    # Pass the data to the home.html template
    return render_template("home.html", products=products)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":
        selected_supermarket = request.form.get("supermarket")
        session["selected_supermarket"] = selected_supermarket

    else:
        selected_supermarket = session.get("selected_supermarket", "Masoutis")

    # Retrieve product information from the CSV file
    df = pd.read_csv("product_prices.csv")

    # Filter the products based on the selected supermarket
    checkout_products = df[["Product", selected_supermarket]]

    # Calculate the total price for the selected products
    total_price = checkout_products[selected_supermarket].sum()

    # Pass the data to the checkout.html template
    return render_template(
        "checkout.html",
        selected_supermarket=selected_supermarket,
        checkout_products=checkout_products,
        total_price=total_price,
    )


if __name__ == "__main__":
    app.run(debug=True)
