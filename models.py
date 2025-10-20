"""
Database Models for Pizza Ordering System

This module defines all database models and relationships for the pizza ordering application.
It includes models for menu items (pizzas, drinks, desserts), customers, orders, delivery persons,
ingredients, and discount codes.

The module uses SQLAlchemy ORM for database operations and includes a seed_data() function
to populate the database with initial test data.
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Numeric
from datetime import date, timedelta
from zoneinfo import ZoneInfo
from faker import Faker
import random

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class MenuItem(db.Model):
    """
    Represents a menu item in the pizza ordering system.
    
    This is a polymorphic model that can reference different types of items
    (pizza, drink, or dessert) through the item_type and item_ref_id fields.
    It acts as a unified interface for all orderable items.
    
    Attributes:
        item_id (int): Primary key
        item_type (str): Type of item - "pizza", "drink", or "dessert"
        item_ref_id (int): Foreign key reference to the specific item table
        order_items (list): Relationship to OrderItem entries
    """
    __tablename__ = "menu_item"
    item_id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(20), nullable=False)  # "pizza", "drink" of "dessert"
    item_ref_id = db.Column(db.Integer, nullable=False)   # points to pizza_id / drink_id / dessert_id

    # Relationships
    order_items = db.relationship("OrderItem", back_populates="menu_item")

    @property
    def name(self):
        """
        Get the name of the menu item by querying the appropriate table.
        
        Returns:
            str: Name of the pizza, drink, or dessert
        """
        if self.item_type == "pizza":
            return Pizza.query.get(self.item_ref_id).name
        elif self.item_type == "drink":
            return Drink.query.get(self.item_ref_id).name
        elif self.item_type == "dessert":
            return Dessert.query.get(self.item_ref_id).name
        else:
            return "[unknown]"

    @property
    def price(self):
        """
        Get the price of the menu item from the appropriate table.
        
        For pizzas, price is calculated dynamically based on ingredients.
        For drinks and desserts, price is stored directly in their tables.
        
        Returns:
            float: Price of the item in euros
        """
        if self.item_type == "pizza":
            return float(Pizza.query.get(self.item_ref_id).price)
        elif self.item_type == "drink":
            return float(Drink.query.get(self.item_ref_id).price)
        elif self.item_type == "dessert":
            return float(Dessert.query.get(self.item_ref_id).price)
        else: 
            return 0

class Pizza(db.Model):
    """
    Represents a pizza with its ingredients.
    
    Pizza prices are calculated dynamically based on ingredient costs,
    with a 40% markup and 9% tax applied. Dietary labels (vegan, vegetarian)
    are determined by the ingredients used.
    
    Attributes:
        pizza_id (int): Primary key
        name (str): Name of the pizza (e.g., "Margherita")
        ingredients (list): Many-to-many relationship with Ingredient
    """
    __tablename__ = "pizza"
    pizza_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    # Many-to-many relationship with ingredients
    ingredients = db.relationship(
        "Ingredient",
        secondary="pizza_ingredient",
        back_populates="pizzas"
    )

    @property
    def price(self):
        """
        Calculate pizza price based on ingredient costs.
        
        Formula: (sum of ingredient prices) * 1.4 (markup) * 1.09 (tax)
        
        Returns:
            float: Calculated price in euros
        """
        ingredient_cost = float(sum(ing.price for ing in self.ingredients))
        return float(ingredient_cost * 1.4 * 1.09)

    @property
    def label(self):
        """
        Determine dietary label based on ingredients.
        
        Returns:
            str: "vegan" if all ingredients are vegan,
                 "vegetarian" if all are vegetarian (but not vegan),
                 "non-vegetarian" otherwise
        """
        if all (ing.vegan for ing in self.ingredients):
            return "vegan"
        elif all (ing.vegetarian for ing in self.ingredients):
            return "vegetarian"
        return "non-vegetarian"
    
    def __repr__(self):
        return f"<Pizza {self.name} {self.price}>"


class Drink(db.Model):
    """
    Represents a drink item on the menu.
    
    Attributes:
        drink_id (int): Primary key
        name (str): Name of the drink (e.g., "Coca Cola")
        price (Numeric): Price in euros (must be positive)
    
    Constraints:
        - Price must be greater than 0
    """
    __tablename__ = "drink"
    drink_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)

    ## Database constraint: price must be positive
    __table_args__ = (
        db.CheckConstraint('price > 0', name='check_drink_price_positive'),
    )
    
    def __repr__(self):
        return f"<Drink {self.name} price {self.price}>"

class Dessert(db.Model):
    """
    Represents a dessert item on the menu.
    
    Attributes:
        dessert_id (int): Primary key
        name (str): Name of the dessert (e.g., "Tiramisu")
        price (Numeric): Price in euros

    Constraints:
        - Price must be greater than 0
    """
    __tablename__ = "dessert"
    dessert_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Numeric(8, 2), nullable=False)

    ## Database constraint: price must be positive
    __table_args__ = (
        db.CheckConstraint('price > 0', name='check_dessert_price_positive'),
    )

    def __repr__(self):
        return f"<Dessert {self.name} price {self.price}>"

class Ingredient(db.Model):
    """
    Represents an ingredient that can be used in pizzas.
    
    Each ingredient has dietary properties (vegetarian, vegan) and a price.
    Ingredients can be used in multiple pizzas through a many-to-many relationship.
    
    Attributes:
        ingredient_id (int): Primary key
        ingredient_name (str): Unique name of the ingredient
        price (Numeric): Cost per ingredient (must be positive)
        vegetarian (bool): Whether ingredient is vegetarian
        vegan (bool): Whether ingredient is vegan
        pizzas (list): Many-to-many relationship with Pizza
    
    Constraints:
        - ingredient_name must be unique
        - Price must be greater than 0
    """
    __tablename__ = "ingredient"
    ingredient_id = db.Column(db.Integer, primary_key=True)
    ingredient_name = db.Column(db.String(32), nullable=False, unique=True)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    vegetarian = db.Column(db.Boolean, nullable=False, default=False)
    vegan = db.Column(db.Boolean, nullable=False, default=False)
    
    # Database constraint: price must be positive
    __table_args__ = (
        db.CheckConstraint('price > 0', name='check_ingredient_price_positive'),
    )

    # Many-to-many relationship with pizzas
    pizzas = db.relationship("Pizza", secondary="pizza_ingredient", back_populates="ingredients")

    def __repr__(self):
        return f"<Ingredient {self.ingredient_id} {self.ingredient_name} ${self.price}>"

# Association table for Pizza-Ingredient many-to-many relationship
pizza_ingredient = db.Table('pizza_ingredient',
    db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.pizza_id'), primary_key=True),
    db.Column('ingredient_id', db.Integer, db.ForeignKey('ingredient.ingredient_id'), primary_key=True)
)

class Customer(db.Model):
    """
    Represents a customer in the pizza ordering system.
    
    Customers can place multiple orders and receive birthday discounts and
    loyalty rewards based on their order history.
    
    Attributes:
        customer_id (int): Primary key
        first_name (str): Customer's first name
        last_name (str): Customer's last name
        birthdate (date): Customer's date of birth
        address (str): Street address
        postal_code (str): 6-character postal code (e.g., "6222RT")
        phone_number (str): Unique phone number
        gender (int): Gender identifier (0=Female, 1=Male, 2=Other)
        orders (list): Relationship to customer's orders
    
    Properties:
        full_name: Concatenated first and last name
        birthday: Boolean indicating if today is customer's birthday
        total_pizzas_ordered: Count of all pizzas ordered by this customer
    """
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(32), nullable=False)
    last_name = db.Column(db.String(32), nullable=False)
    birthdate = db.Column(db.Date, nullable=False)
    address = db.Column(db.String(255))
    postal_code = db.Column(db.String(6), nullable=False) 
    phone_number = db.Column(db.String(32), nullable=False, unique=True)
    gender = db.Column(db.Integer)  # 0, 1, 2 for different gender options

    # Relationships - cascade delete means all orders are deleted when customer is deleted
    orders = db.relationship("Order", back_populates="customer", cascade="all, delete-orphan")

    @property
    def full_name(self):
        """Returns customer's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def birthday(self):
        """
        Check if today is the customer's birthday.
        
        Returns:
            bool: True if today matches birth month and day
        """
        if self.birthdate.month == date.today().month and self.birthdate.day == date.today().day:
            return True
        return False
    
    @property
    def total_pizzas_ordered(self):
        """
        Calculate total number of pizzas ordered by this customer.
        
        This is used for the "10 pizzas = 1 free" loyalty discount.
        
        Returns:
            int: Total count of pizzas across all orders
        """
        pizza_count = 0
        for order in self.orders:
            for item in order.order_items:
                # Ensure the item is a pizza
                if isinstance(item.menu_item, Pizza):
                    pizza_count += item.amount
        return pizza_count
    
    def __repr__(self):
        return f"<Customer {self.customer_id} {self.full_name}>"

class DiscountCode(db.Model):
    """
    Represents a discount code that can be applied to orders.
    
    Each discount code can only be used once per customer.
    
    Attributes:
        discount_id (int): Primary key
        percentage (int): Discount percentage (e.g., 10 for 10% off)
        discount_code (str): Unique code string (e.g., "WELCOME10")
        orders (list): Relationship to orders that used this code
    """
    __tablename__ = "discount_code"
    discount_id = db.Column(db.Integer, primary_key=True)
    percentage = db.Column(db.Integer, nullable=False)
    discount_code = db.Column(db.String(32), nullable=False, unique=True)
    
    # Relationships
    orders = db.relationship("Order", back_populates="discount_code")
    
    def __repr__(self):
        return f"<DiscountCode {self.discount_id} {self.discount_code} {self.percentage}%>"


class DeliveryPerson(db.Model):
    """
    Represents a delivery person who delivers orders.
    
    Each delivery person is assigned to a specific postal code and has
    availability tracking to manage delivery schedules.
    
    Attributes:
        delivery_person_id (int): Primary key
        delivery_person_first_name (str): First name
        delivery_person_last_name (str): Last name
        postal_code (str): Postal code this person delivers to
        next_available_time (datetime): When they'll be available next
        orders (list): Relationship to orders assigned to this person
    
    Properties:
        full_name: Concatenated first and last name
        is_available_now: Whether currently available for delivery
        minutes_until_available: Minutes until next availability
        next_available_time_aware: Timezone-aware availability time
    """
    __tablename__ = "delivery_person"
    delivery_person_id = db.Column(db.Integer, primary_key=True)
    delivery_person_first_name = db.Column(db.String(32), nullable=False)
    delivery_person_last_name = db.Column(db.String(32), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    next_available_time = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Amsterdam")), nullable=False)
    
    # Relationships
    orders = db.relationship("Order", back_populates="delivery_person")
    
    @property
    def full_name(self):
        """Returns delivery person's full name."""
        return f"{self.delivery_person_first_name} {self.delivery_person_last_name}"
    
    @property
    def is_available_now(self):
        """
        Check if delivery person is currently available.
        
        Returns:
            bool: True if current time >= next_available_time
        """
        # Get current time in Dutch timezone
        now_dutch = datetime.now(ZoneInfo("Europe/Amsterdam"))

        # Make next_available_time timezone-aware if it isn't already
        if self.next_available_time.tzinfo is None:
            next_available = self.next_available_time.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        else:
            next_available = self.next_available_time

        # Check if delivery person is currently available
        return now_dutch >= next_available
    
    @property
    def minutes_until_available(self):
        """
        Calculate minutes until delivery person is available.
        
        Returns:
            int: Minutes until available (0 if currently available)
        """
        # Calculate minutes until delivery person is available
        if self.is_available_now:
            return 0
        delta = self.next_available_time - datetime.now(ZoneInfo("Europe/Amsterdam"))
        return int(delta.total_seconds() / 60)
    
    @property
    def next_available_time_aware(self):
        """
        Returns next_available_time as a timezone-aware datetime.
        
        This ensures proper time comparisons by adding timezone info
        if the stored datetime is naive.
        
        Returns:
            datetime: Timezone-aware datetime in Europe/Amsterdam timezone
        """
        if self.next_available_time.tzinfo is None:
            return self.next_available_time.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        return self.next_available_time
    
    def __repr__(self):
        return f"<DeliveryPerson {self.delivery_person_id} {self.full_name}>"

class Order(db.Model):
    """
    Represents a customer order.
    
    Orders contain multiple items, have delivery information, and track
    order status through timestamps (order_time, pickup_time, expected_delivery_time).
    
    Attributes:
        order_id (int): Primary key
        customer_id (int): Foreign key to Customer
        discount_id (int): Optional foreign key to DiscountCode
        delivery_person_id (int): Foreign key to DeliveryPerson
        order_time (datetime): When order was placed
        delivery_address (str): Delivery street address
        postal_code (str): Delivery postal code
        pickup_time (datetime): When delivery person picks up order
        total_price (Numeric): Final price after discounts (must be positive)
        customer (Customer): Relationship to customer
        discount_code (DiscountCode): Relationship to discount code (if used)
        delivery_person (DeliveryPerson): Relationship to delivery person
        order_items (list): Relationship to ordered items
    
    Properties:
        expected_delivery_time: Pickup time + 30 minutes
        item_count: Total number of items in order
        raw_price: Price before discounts
        status: Current order status (pending/out_for_delivery/delivered)
        status_display: Human-readable status with icon
    
    Constraints:
        - total_price must be greater than 0
    """
    __tablename__ = "order"
    order_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"), nullable=False)
    discount_id = db.Column(db.Integer, db.ForeignKey("discount_code.discount_id"), nullable=True)
    delivery_person_id = db.Column(db.Integer, db.ForeignKey("delivery_person.delivery_person_id"), nullable=False)
    order_time = db.Column(db.DateTime, default=lambda: datetime.now(ZoneInfo("Europe/Amsterdam")), nullable=False)
    delivery_address = db.Column(db.String(255), nullable=False)
    postal_code = db.Column(db.String(6), nullable=False)
    pickup_time = db.Column(db.DateTime, nullable=False) 
    total_price = db.Column(db.Numeric(8,2), nullable=False)
    
    # Database constraint: total price must be positive
    __table_args__ = (
        db.CheckConstraint('total_price > 0', name='check_order_total_price_positive'),
    )

    # Relationships
    customer = db.relationship("Customer", back_populates="orders")
    discount_code = db.relationship("DiscountCode", back_populates="orders")
    delivery_person = db.relationship("DeliveryPerson", back_populates="orders")
    order_items = db.relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    @property
    def expected_delivery_time(self):
        """
        Calculate expected delivery time (pickup + 30 minutes).
        
        Returns:
            datetime: Expected delivery time
        """
        return self.pickup_time + timedelta(minutes=30)
    
    @property
    def item_count(self):
        """
        Get total number of items in the order.
        
        Returns:
            int: Sum of all item amounts
        """
        return sum(item.amount for item in self.order_items)
    
    @property
    def raw_price(self):
        """
        Calculate order price before any discounts.
        
        Returns:
            float: Sum of (item_price * quantity) for all items
        """
        subtotal = 0.0
        for item in self.order_items:
                item_total = item.amount * item.menu_item.price
                subtotal += item_total
        return subtotal
    
    @property
    def status(self):
        """
        Determine current order status based on timestamps.
        
        Status logic:
        - "pending": Order placed, waiting for pickup
        - "out_for_delivery": Picked up, in transit
        - "delivered": Past expected delivery time
        
        Returns:
            str: One of 'pending', 'out_for_delivery', or 'delivered'
        """
        now = datetime.now(ZoneInfo("Europe/Amsterdam"))
        
        # Make datetime values timezone-aware if they aren't already
        expected_delivery = self.pickup_time + timedelta(minutes=30)
        if expected_delivery.tzinfo is None:
            expected_delivery = expected_delivery.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        
        pickup = self.pickup_time
        if pickup.tzinfo is None:
            pickup = pickup.replace(tzinfo=ZoneInfo("Europe/Amsterdam"))
        
        if now >= expected_delivery:
            return 'delivered'
        elif now >= pickup:
            return 'out_for_delivery'
        else:
            return 'pending'
    
    @property
    def status_display(self):
        """
        Get human-readable status with emoji icon.
        
        Returns:
            str: Formatted status string with icon
        """
        status = self.status
        if status == 'delivered':
            return '✓ Delivered'
        elif status == 'out_for_delivery':
            return '🚚 Out for Delivery'
        else:
            return '⏳ Pending'
        
    def __repr__(self):
        return f"<Order {self.order_id} customer={self.customer_id} total=${self.total_price}>"

class OrderItem(db.Model):
    """
    Represents a single item within an order (junction table).
    
    Links orders to menu items with a quantity.
    
    Attributes:
        order_id (int): Primary key, foreign key to Order
        item_id (int): Primary key, foreign key to MenuItem
        amount (int): Quantity of this item in the order
        order (Order): Relationship to parent order
        menu_item (MenuItem): Relationship to menu item
    """
    __tablename__ = "order_item"

    # Composite primary key
    order_id = db.Column(db.Integer, db.ForeignKey("order.order_id"), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey("menu_item.item_id"), primary_key=True)
    amount = db.Column(db.Integer, default=1, nullable=False)
    
    # Relationships
    order = db.relationship("Order", back_populates="order_items")
    menu_item = db.relationship("MenuItem", back_populates="order_items")
    
    def __repr__(self):
        return f"<OrderItem order={self.order_id} item={self.item_id} amount={self.amount}>"


def seed_data():
    """
    Populate the database with initial test data.
    
    This function:
    1. Drops all existing tables and recreates them
    2. Creates 10 random customers using Faker
    3. Creates 3 delivery persons for different postal codes
    4. Creates ingredients with dietary properties
    5. Creates 10 pizzas with various ingredient combinations
    6. Creates drinks and desserts
    7. Creates menu items for all products
    8. Creates discount codes
    9. Generates 20 random orders from the past month
    
    Uses Faker library with Dutch locale for realistic test data.
    """

    db.drop_all()
    db.create_all()

    fake = Faker("nl_NL")
    postal_codes = ['6221AX', '6211RZ', '6215PD']

    # Create customers
    if Customer.query.count() == 0:
        for _ in range(10):
            c = Customer(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birthdate=fake.date_of_birth(minimum_age=18, maximum_age=60),
                address=f'{fake.street_name()} {random.randint(1,200)}',
                postal_code = random.choice(postal_codes),
                phone_number=fake.unique.phone_number(),
                gender=random.choice([0, 1, 2])
            )
            db.session.add(c)
        db.session.flush()

    # Create delivery persons (one per postal code)
    if DeliveryPerson.query.count() == 0:
        for i in range(3):
            d = DeliveryPerson(
                delivery_person_first_name=fake.first_name(),
                delivery_person_last_name=fake.last_name(),
                postal_code=postal_codes[i],
                next_available_time=datetime.now(ZoneInfo("Europe/Amsterdam"))
            )
            db.session.add(d)
        db.session.flush()

    # Create igredients
    if Ingredient.query.count() == 0:
        db.session.add_all([
            Ingredient(ingredient_name="Tomato Sauce", price=1.50, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Mozzarella", price=2.00, vegetarian=True, vegan=False),
            Ingredient(ingredient_name="Vegan Mozzarella", price=3.00, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Pepperoni", price=2.50, vegetarian=False, vegan=False),
            Ingredient(ingredient_name="Mushrooms", price=1.75, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Bell Peppers", price=1.25, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Onions", price=1.00, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Olives", price=1.50, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Ham", price=2.75, vegetarian=False, vegan=False),
            Ingredient(ingredient_name="Pineapple", price=1.80, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Basil", price=0.75, vegetarian=True, vegan=True),
            Ingredient(ingredient_name="Parmesan", price=2.20, vegetarian=True, vegan=False),
            Ingredient(ingredient_name="Gorgonzola", price=2.30, vegetarian=True, vegan=False),
        ])
    db.session.flush()  # so ingredient IDs exist

    # Create pizzas with ingredient combinations
    if Pizza.query.count() == 0:
        # Fetch ingredients for pizza creation
        tomato = Ingredient.query.filter_by(ingredient_name="Tomato Sauce").first()
        mozzarella = Ingredient.query.filter_by(ingredient_name="Mozzarella").first()
        pepperoni = Ingredient.query.filter_by(ingredient_name="Pepperoni").first()
        mushrooms = Ingredient.query.filter_by(ingredient_name="Mushrooms").first()
        peppers = Ingredient.query.filter_by(ingredient_name="Bell Peppers").first()
        onions = Ingredient.query.filter_by(ingredient_name="Onions").first()
        olives = Ingredient.query.filter_by(ingredient_name="Olives").first()
        ham = Ingredient.query.filter_by(ingredient_name="Ham").first()
        pineapple = Ingredient.query.filter_by(ingredient_name="Pineapple").first()
        basil = Ingredient.query.filter_by(ingredient_name="Basil").first()
        parmesan = Ingredient.query.filter_by(ingredient_name="Parmesan").first()
        gorgonzola = Ingredient.query.filter_by(ingredient_name="Gorgonzola").first()
        vegan_mozzarella = Ingredient.query.filter_by(ingredient_name="Vegan Mozzarella").first()

        pizzas = [
            Pizza(name="Margherita", ingredients=[tomato, mozzarella, basil]),
            Pizza(name="Vegan Margherita", ingredients=[tomato, vegan_mozzarella, basil]),
            Pizza(name="Pepperoni", ingredients=[tomato, mozzarella, pepperoni]),
            Pizza(name="Veggie Deluxe", ingredients=[tomato, mozzarella, mushrooms, peppers, onions, olives]),
            Pizza(name="Vegan Deluxe", ingredients=[tomato, vegan_mozzarella, mushrooms, peppers, onions, olives]),
            Pizza(name="Hawaiian", ingredients=[tomato, mozzarella, ham, pineapple]),
            Pizza(name="Four Cheese", ingredients=[tomato, mozzarella, parmesan, gorgonzola]),
            Pizza(name="Meat Feast", ingredients=[tomato, mozzarella, ham, pepperoni]),
            Pizza(name="Capricciosa", ingredients=[tomato, mozzarella, ham, mushrooms, olives]),
            Pizza(name="Funghi", ingredients=[tomato, mozzarella, mushrooms]),
        ]
        db.session.add_all(pizzas)
        db.session.flush()

    # Create drinks
    if Drink.query.count() == 0:
        drinks = [
            Drink(name="Coca Cola", price=2.00),
            Drink(name="Sprite", price=2.00),
            Drink(name="Ice Tea", price=2.50),
            Drink(name="Beer", price=3.50),
        ]
        db.session.add_all(drinks)
        db.session.flush()

    # Create desserts
    if Dessert.query.count() == 0:
        desserts = [
            Dessert(name="Tiramisu", price=4.00),
            Dessert(name="Panna Cotta", price=3.50),
            Dessert(name="Brownie", price=2.50)
        ]
        db.session.add_all(desserts)
        db.session.flush()

    # Create menu items for all pizzas, drinks, and desserts
    for p in Pizza.query.all():
        if not MenuItem.query.filter_by(item_type="pizza", item_ref_id=p.pizza_id).first():
            db.session.add(MenuItem(item_type="pizza", item_ref_id=p.pizza_id))

    for d in Drink.query.all():
        if not MenuItem.query.filter_by(item_type="drink", item_ref_id=d.drink_id).first():
            db.session.add(MenuItem(item_type="drink", item_ref_id=d.drink_id))

    for ds in Dessert.query.all():
        if not MenuItem.query.filter_by(item_type="dessert", item_ref_id=ds.dessert_id).first():
            db.session.add(MenuItem(item_type="dessert", item_ref_id=ds.dessert_id))


    # Create discount codes
    if DiscountCode.query.count() == 0:
        db.session.add_all([
            DiscountCode(percentage=10, discount_code="WELCOME10"),
            DiscountCode(percentage=15, discount_code="STUDENT15"),
            DiscountCode(percentage=20, discount_code="VIP20"),
        ])
        db.session.flush()


    # Generate random orders from the past month.
    if Order.query.count() == 0:
        customers = Customer.query.all()
        delivery_people = DeliveryPerson.query.all()
        menu_pizzas = MenuItem.query.filter_by(item_type="pizza").all()
        menu_drinks = MenuItem.query.filter_by(item_type="drink").all()
        menu_desserts = MenuItem.query.filter_by(item_type="dessert").all()

        base_date = datetime.now(ZoneInfo("Europe/Amsterdam"))

        # Create 20 random orders
        for _ in range(20):
            customer = random.choice(customers)
            delivery_person = random.choice(delivery_people)

            # Place orders randomly in the past month
            order_time = base_date - timedelta(
                days=random.randint(0, 30), 
                hours=random.randint(0, 10), 
                minutes=random.randint(0, 59)
            )
            pickup_time = order_time + timedelta(minutes=random.randint(0, 60))

            # Create order with placeholder price (will be updated)
            order = Order(
                customer_id=customer.customer_id,
                delivery_person_id=delivery_person.delivery_person_id,
                order_time=order_time,
                pickup_time=pickup_time,
                delivery_address=fake.street_address(),
                postal_code=customer.postal_code,
                total_price=1.0,
            )
            db.session.add(order)
            db.session.flush()

            # Add order items
            subtotal = 0
            added_item_ids = set()

            # Add 1 to 4 pizzas
            for _ in range(random.randint(1, 4)):
                pizza_item = random.choice(menu_pizzas)
                if pizza_item.item_id in added_item_ids:
                    continue  # skip if we already have this pizza in the orderitems
                qty = random.randint(1, 3)
                db.session.add(OrderItem(order_id=order.order_id, item_id=pizza_item.item_id, amount=qty))
                subtotal += pizza_item.price * qty
                added_item_ids.add(pizza_item.item_id)

            # 60% chance to add drinks
            if random.random() < 0.6:
                drink_item = random.choice(menu_drinks)
                if drink_item.item_id in added_item_ids:
                    continue  # skip if its already added
                qty = random.randint(1, 2)
                db.session.add(OrderItem(order_id=order.order_id, item_id=drink_item.item_id, amount=qty))
                subtotal += drink_item.price * qty
                added_item_ids.add(drink_item.item_id)

            # 30% chance to add a dessert
            if random.random() < 0.3:
                dessert_item = random.choice(menu_desserts)
                if dessert_item.item_id in added_item_ids:
                    continue
                qty = 1
                db.session.add(OrderItem(order_id=order.order_id, item_id=dessert_item.item_id, amount=qty))
                subtotal += dessert_item.price * qty
                added_item_ids.add(dessert_item.item_id)

            # Update order with calculated total price
            order.total_price = round(subtotal, 2)

        # Commit all changes to the database
        db.session.commit()
