"""
Pizza Ordering System - Main Application Module

This module serves as the entry point for the Flask-based pizza ordering application.
It initializes the Flask app, configures the database connection, registers all blueprints,
and starts the development server.

The application uses MySQL as the database backend and includes functionality for:
- Customer management
- Menu item management (pizzas, drinks, desserts)
- Order creation and tracking
- Ingredient listing
- Staff reporting and analytics

Authors: Lisa Ponsteen (i6397659) and Noortje van Maldegem (i6374487)
"""
from flask import Flask
from controllers import home_bp, customers_bp, menu_items_bp, orders_bp, ingredients_bp, create_order_bp, staff_reports_bp
from models import db, seed_data

def create_app():
    """
    Create and configure the Flask application.
    
    This factory function:
    1. Initializes a Flask application instance
    2. Configures the MySQL database connection
    3. Sets up the secret key for session management
    4. Initializes SQLAlchemy with the app
    5. Registers all application blueprints for different routes
    6. Creates database tables and seeds initial data
    
    Database Configuration:
        - Database: MySQL
        - Connection: mysql+pymysql://root:password@localhost/pizza_ordering
        - Driver: PyMySQL (pure Python MySQL client)
    
    Registered Blueprints:
        - home_bp: Home page route
        - customers_bp: Customer CRUD operations
        - menu_items_bp: Menu item management
        - orders_bp: Order listing and viewing
        - ingredients_bp: Ingredient management
        - create_order_bp: Order creation workflow
        - staff_reports_bp: Analytics and reporting
    
    Returns:
        Flask: Configured Flask application instance ready to run
    """
    app = Flask(__name__)
    
    # Configure MySQL database connection
    # Format: mysql+pymysql://username:password@host/database_name
    app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:password@localhost/pizza_ordering"
    
    # Disable modification tracking to improve performance
    # This feature is not needed for this application
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Set secret key for session management and CSRF protection
    app.secret_key = "dev-secret"

    # Initialize SQLAlchemy database with this Flask app
    db.init_app(app)

    # Register blueprints for different sections
    app.register_blueprint(home_bp)             # Home page
    app.register_blueprint(customers_bp)        # Customer management
    app.register_blueprint(menu_items_bp)       # Menu item management
    app.register_blueprint(orders_bp)           # Order listing and viewing
    app.register_blueprint(ingredients_bp)      # Ingredient management
    app.register_blueprint(create_order_bp)     # Order creation workflow
    app.register_blueprint(staff_reports_bp)    # Analytics and reporting

    # Create database tables and populate with initial data
    with app.app_context():
        db.create_all()    # Create all tables defined in models.py
        seed_data()        # Populate tables with data

    @app.route("/")
    def index():
        """
        Root route handler.
        
        Renders the home page of the application.
        
        Returns:
            str: Rendered HTML template for the home page
        """
        return render_template("index.html", title="Home")

    return app

if __name__ == "__main__":
    """
    Application entry point.
    
    When this script is run directly (not imported), it:
    1. Creates the Flask application
    2. Prints a startup message
    3. Runs the development server with debug mode enabled
    
    Debug Mode Features:
        - Automatic reloading on code changes
        - Detailed error pages with stack traces
        - Interactive debugger in the browser
    """
    app = create_app()
    print("Starting Pizza Ordering Flask app...")
    app.run(debug=True)