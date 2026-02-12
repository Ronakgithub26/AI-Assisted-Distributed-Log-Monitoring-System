from flask import Flask, render_template, session, redirect, url_for, request
from agent_sdk import Agent
from agent_sdk.network import monitored_request
import random
import time

app = Flask(__name__)
app.secret_key = "secret123"

# -------------------------
# AGENT INIT
# -------------------------
Agent.init(
    api_key="demo-client-key-123",
    endpoint="http://localhost:8000/api/logs/collect",
    project="ecommerce-demo-client",
    environment="development",
    framework="flask",
    app=app
)

# -------------------------
# BUG ENGINE (Hidden)
# -------------------------
BUGS = {
    "slow_mode": False,
    "payment_fail": True,   # turn on intentionally
    "random_crash": False
}

# -------------------------
# FAKE PRODUCT DATABASE
# -------------------------
PRODUCTS = {
    1: {"name": "Wireless Headphones", "price": 2999},
    2: {"name": "Smart Watch", "price": 4999},
    3: {"name": "Gaming Mouse", "price": 1499},
    4: {"name": "Bluetooth Speaker", "price": 1999},
}

# -------------------------
# ROUTES
# -------------------------

@app.route("/")
def home():
    if BUGS["slow_mode"]:
        time.sleep(2)
    return render_template("home.html", products=PRODUCTS)


@app.route("/product/<int:id>")
def product(id):
    if BUGS["random_crash"] and random.randint(1,5) == 3:
        raise Exception("Random product crash")

    product = PRODUCTS.get(id)
    if not product:
        raise ValueError("Product not found")

    return render_template("product.html", product=product, id=id)


@app.route("/add-to-cart/<int:id>")
def add_to_cart(id):
    cart = session.get("cart", [])
    cart.append(id)
    session["cart"] = cart
    return redirect(url_for("cart"))


@app.route("/cart")
def cart():
    cart_ids = session.get("cart", [])
    items = [PRODUCTS[i] for i in cart_ids if i in PRODUCTS]
    total = sum(item["price"] for item in items)
    return render_template("cart.html", items=items, total=total)


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    if request.method == "POST":

        if BUGS["payment_fail"]:
            monitored_request(
                "POST",
                "https://fake-payment-gateway-xyz.com/pay"
            )

        session["cart"] = []
        return redirect(url_for("home"))

    return render_template("checkout.html")


@app.errorhandler(Exception)
def handle_error(e):
    return render_template("error.html"), 500


if __name__ == "__main__":
    app.run(debug=True, port=3000)
