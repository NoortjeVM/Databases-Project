from flask import Flask
from controllers import customers_bp, menu_items_bp, orders_bp, ingredients_bp, create_order_bp, staff_reports_bp
from models import db, seed_data

def create_app():
    app = Flask(__name__)
    
    # Use MySQL connection instead of SQLite
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/pizza_ordering"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.secret_key = "dev-secret"

    db.init_app(app)

    # Register blueprints for different sections
    app.register_blueprint(customers_bp)
    app.register_blueprint(menu_items_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(ingredients_bp)
    app.register_blueprint(create_order_bp)
    app.register_blueprint(staff_reports_bp)

    with app.app_context():
        db.create_all()
        seed_data()

    @app.route("/")
    def index():
        return (
            "<h3>Pizza Ordering System</h3>"
            '<p>Navigate to: <a href="/customers">/customers</a>, '
            '<a href="/menu-items">/menu-items</a>, '
            '<a href="/orders">/orders</a>, '
            '<a href="/ingredients">/ingredients</a>, '
            '<a href="/create_order">/create_order</a>, '
            '<a href="/staff_reports">/staff_reports</a>'
        )

    return app

if __name__ == "__main__":
    app = create_app()
    print("Starting Pizza Ordering Flask app...")
    app.run(debug=True)