from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///inventory.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(100), unique=True, nullable=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


@app.route("/")
def home():

    search = request.args.get("search", "").strip()

    if search:

        products = Product.query.filter(
            db.or_(
                Product.name.ilike(f"%{search}%"),
                Product.category.ilike(f"%{search}%"),
                Product.barcode.ilike(f"%{search}%")
            )
        ).all()

    else:

        products = Product.query.all()

    all_products = Product.query.all()

    total_products = len(all_products)

    low_stock = Product.query.filter(
        Product.quantity > 0,
        Product.quantity <= 5
    ).count()

    out_of_stock = Product.query.filter(
        Product.quantity == 0
    ).count()

    total_value = sum(
        product.price * product.quantity
        for product in all_products
    )

    return render_template(
        "index.html",
        products=products,
        total_products=total_products,
        low_stock=low_stock,
        out_of_stock=out_of_stock,
        total_value=total_value,
        search=search
    )


@app.route("/view-product/<int:product_id>")
def view_product(product_id):

    product = Product.query.get_or_404(product_id)

    total_value = product.price * product.quantity

    return render_template(
        "view_product.html",
        product=product,
        total_value=total_value
    )


@app.route("/add-product", methods=["GET", "POST"])
def add_product():

    if request.method == "POST":

        name = request.form["name"]
        category = request.form["category"]
        barcode = request.form["barcode"].strip()
        price = float(request.form["price"])
        quantity = int(request.form["quantity"])

        product = Product(
            name=name,
            category=category,
            barcode=barcode if barcode else None,
            price=price,
            quantity=quantity
        )

        db.session.add(product)
        db.session.commit()

        return redirect("/")

    return render_template("add_product.html")


@app.route("/edit-product/<int:product_id>", methods=["GET", "POST"])
def edit_product(product_id):

    product = Product.query.get_or_404(product_id)

    if request.method == "POST":

        product.name = request.form["name"]
        product.category = request.form["category"]

        barcode = request.form["barcode"].strip()

        product.barcode = barcode if barcode else None

        product.price = float(request.form["price"])
        product.quantity = int(request.form["quantity"])

        db.session.commit()

        return redirect("/")

    return render_template(
        "edit_product.html",
        product=product
    )


@app.route("/delete-product/<int:product_id>")
def delete_product(product_id):

    product = Product.query.get_or_404(product_id)

    db.session.delete(product)
    db.session.commit()

    return redirect("/")


@app.route("/reports")
def reports():

    products = Product.query.all()

    total_products = len(products)

    total_quantity = sum(
        product.quantity
        for product in products
    )

    total_value = sum(
        product.price * product.quantity
        for product in products
    )

    low_stock_products = [
        product
        for product in products
        if 0 < product.quantity <= 5
    ]

    out_of_stock_products = [
        product
        for product in products
        if product.quantity == 0
    ]

    categories = {}

    for product in products:

        if product.category not in categories:

            categories[product.category] = {
                "products": 0,
                "quantity": 0,
                "value": 0
            }

        categories[product.category]["products"] += 1

        categories[product.category]["quantity"] += product.quantity

        categories[product.category]["value"] += (
            product.price * product.quantity
        )

    return render_template(
        "reports.html",
        products=products,
        total_products=total_products,
        total_quantity=total_quantity,
        total_value=total_value,
        low_stock_products=low_stock_products,
        out_of_stock_products=out_of_stock_products,
        categories=categories
    )


with app.app_context():

    db.create_all()

    if Product.query.count() == 0:

        sample_products = [

            Product(
                name="Rice",
                category="Grains",
                barcode="8901234567890",
                price=60,
                quantity=25
            ),

            Product(
                name="Milk",
                category="Dairy",
                barcode="8901234567891",
                price=30,
                quantity=4
            ),

            Product(
                name="Bread",
                category="Bakery",
                barcode="8901234567892",
                price=40,
                quantity=0
            ),

            Product(
                name="Sugar",
                category="Groceries",
                barcode="8901234567893",
                price=50,
                quantity=15
            )
        ]

        db.session.add_all(sample_products)

        db.session.commit()


if __name__ == "__main__":
    app.run(debug=True)