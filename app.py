from flask import Flask, render_template, request, redirect
import requests

app = Flask(__name__)
app.secret_key = "shopsphere"

# TEMP CART STORAGE

cart_items = []

# HOME PAGE

@app.route('/')
def home():

    search = request.args.get('search')

    # FETCH PRODUCTS FROM API

    response = requests.get(
        'https://fakestoreapi.com/products'
    )

    products = response.json()

    # SEARCH FILTER

    if search:

        filtered_products = []

        for product in products:

            if search.lower() in product['title'].lower():

                filtered_products.append(product)

        products = filtered_products

    return render_template(
        'index.html',
        products=products
    )

# ADD TO CART

@app.route('/add-to-cart/<int:id>')
def add_to_cart(id):

    response = requests.get(
        f'https://fakestoreapi.com/products/{id}'
    )

    product = response.json()

    cart_items.append(product)

    return redirect('/cart')

# CART PAGE

@app.route('/cart')
def cart():

    total = 0

    for item in cart_items:

        total += item['price']

    return render_template(
        'cart.html',
        cart_items=cart_items,
        total=round(total,2)
    )

# REMOVE ITEM

@app.route('/remove/<int:index>')
def remove(index):

    cart_items.pop(index)

    return redirect('/cart')

# CHECKOUT

@app.route('/checkout')
def checkout():

    return render_template('checkout.html')

# SUCCESS PAGE

@app.route('/success')
def success():

    cart_items.clear()

    return render_template('successful.html')

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)