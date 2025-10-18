# Database Project - Pizza Ordering System

A comprehensive web-based pizza ordering and management system built with Flask and MySQL.

Made by:
- Lisa Ponsteen (i6397659)
- Noortje van Maldegem (i6374487)

## Table of Contents
- [Features](#features)
- [Setup Instructions](#setup-instructions)
- [Running the Application](#running-the-application)
- [Business Logic & Rules](#business-logic--rules)
- [Project Structure](#project-structure)
- [Technologies Used](#technologies-used)

---

## Features

- **Customer displaying and new customer creation**: Create and manage customer profiles with personal information. New customers can be added.
- **Menu**: Menu shows the pizza's, drinks and desserts. For the pizza's, the ingredients are shown, as well as whether a pizza is vegetarian, vegan, or non-vegetarian.
- **Order Processing**: Create orders with automatic pricing and discount calculations.
- **Delivery System**: Automatic delivery person assignment based on postal codes.
- **Staff Reports**: Analytics including top-selling pizzas, undelivered orders, and monthly earnings. There is one customer report with the top 3 of best selling pizza's, one report that displays undelivered orders, and one report that shows monthly earnings. In the monthly earnings report, you can filter on month, year, gender, age or postal code. You can use all the filters, a combination of them, one single filter, or no filter.
- **Discount System**: Birthday discounts, loyalty rewards, and promotional codes.

---

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- MySQL Server
- pip (Python package manager)

### 1. Clone the Repository
```bash
git clone https://gitlab.maastrichtuniversity.nl/I6374487/databases-project.git
cd databases-project
```

### 2. Create Virtual Environment
```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install flask flask-sqlalchemy pymysql
```

### 4. Configure MySQL Database

1. Start your MySQL server
2. Create a database:
```sql
CREATE DATABASE pizza_ordering;
```

3. Update database credentials in `app.py`:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://username:password@localhost/pizza_ordering"
```
Replace `username` and `password` with your MySQL username and password.

### 5. Initialize Database
The database tables will be created automatically when you first run the application. Sample data will also be seeded automatically, using Fake for e.g. customer names and adresses. The sample menu items and ingredients where generated using ChatGPT (since fake can't generate realistic data for for instance pizza names).

---

## Running the Application

1. **Activate the virtual environment** (if not already activated):
```bash
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

2. **Run the Flask application**:
```bash
python app.py
```

3. **Access the application**:
Open your web browser and navigate to:
```
http://localhost:5000
```

4. **Available Routes**:
- `/` - Home page
- `/customers` - Customer management
- `/menu-items` - Menu display
- `/list_orders` - View all orders
- `/ingredients` - Ingredient management
- `/create_order` - Create new orders
- `/staff_reports` - Analytics and reports

---

## Sample Data

The application automatically seeds sample data on first run:
- 3 delivery persons covering 3 different postal codes in Maastricht
- 11 customers that live in those postal codes 
- 13 ingredients (including vegan options)
- 10 pizzas with different ingredient combinations
- 4 drinks
- 3 desserts
- 3 discount codes
- 20 orders

This seed data can be found in at the bottom of the file [models.py](models.py)

---

## Business Logic & Rules

### Pricing System

#### Pizza Pricing
- Pizza prices are **calculated dynamically** based on their ingredients
- Each ingredient has an individual price
- Total pizza price = ((sum of all ingredient prices) * 1.40) * 1.09 (This means that a 40% margin and a 9% VAT are added to the cost price of the pizza.)

#### Fixed Pricing
- Drinks and desserts have fixed prices set in the system

### Discount Rules

#### 1. Birthday Discount
- **Eligibility**: Automatically applied on customer's birthday
- **Benefit**: One free pizza (cheapest) + one free drink (cheapest)
- **Limitation**: Only valid for the first order placed on birthday
- **Logic**: System checks if customer's birthdate matches current date and if they haven't placed an order yet today

#### 2. Loyalty Discount (10-Pizza Rule)
- **Eligibility**: Automatically applied based on total pizzas ordered
- **Benefit**: Every 10th pizza is free
- **Calculation**: Tracks cumulative pizza orders across all previous orders
- **Example**: 
  - Customer has ordered 18 pizzas previously
  - New order contains 5 pizzas
  - Total becomes 23 pizzas
  - Customer receives 1 free pizza (and the counting towards the next 10 starts again at pizza 21)
  - The cheapest pizza in the current order is discounted

#### 3. Discount Codes
- **Types**: Percentage-based discounts (e.g., WELCOME10, STUDENT15, VIP20)
- **Limitation**: One-time use per customer per code
- **Validation**: System checks if customer has already used the specific code
- **Application**: Applied to the subtotal after free pizza/drink discounts

### Order Constraints

#### Minimum Order Requirements
- **Every order must contain at least 1 pizza**
- Orders with only drinks or desserts are not allowed
- System validates this before order creation

### Delivery System

#### Delivery Person Assignment
- **Automatic assignment** based on postal code
- Each delivery person is assigned to specific postal codes
- System finds available delivery person for the order's postal code
- If there is no delivery person for the order's postal code, the system notifies the customer about this before the order gets placed.

#### Timing Calculations
- **Pickup Time**: Maximum of current time or delivery person's next available time
- **Expected Delivery Time**: Pickup time + 30 minutes
- **Availability Update**: Delivery person becomes available again for a new order after expected delivery time

#### Order Status
Orders have three statuses that are automatically calculated:
1. **Pending**: Order placed, waiting for pickup time
2. **Out for Delivery**: Past pickup time, before expected delivery time
3. **Delivered**: Past expected delivery time

### Dietary Information

#### Pizza Classification
Pizzas are automatically labeled based on their ingredients:
- **Vegan**: All ingredients are vegan
- **Vegetarian**: All ingredients are vegetarian (but not vegan)
- **Non-vegetarian**: Contains at least one non-vegetarian ingredient

#### Ingredient Properties
Each ingredient is marked as:
- Vegan (true/false)
- Vegetarian (true/false)

### Staff Reports

#### Top Pizzas Report
- Shows top 3 best-selling pizzas from the last 30 days
- Based on total quantity sold

#### Undelivered Orders Report
- Lists all orders with status "pending" or "out_for_delivery"
- Shows expected delivery times and assigned delivery persons

#### Monthly Earnings Report
- Filter by specific month and year
- Optional filters: gender, age range (min/max), postal code
- Shows total earnings and breakdown per customer
- Age is calculated dynamically from birthdate

---

## Project Structure

```
pizza-ordering-system/
├── app.py                 # Main Flask application
├── models.py              # Database models and relationships
├── controllers.py         # Route handlers and business logic
├── templates/             # HTML templates
│   ├── index.html
│   ├── layout.html
│   ├── customers.html
│   ├── customer_form.html
│   ├── menu_items.html
│   ├── menu_item_form.html
│   ├── orders.html
│   ├── order_form.html
│   ├── ingredients.html
│   └── staff_reports.html
└── README.md
```

### Key Files

- **app.py**: Application initialization, database configuration, and blueprint registration
- **models.py**: SQLAlchemy models for all database tables (Customer, Order, MenuItem, Pizza, Ingredient, etc.)
- **controllers.py**: All route handlers organized into blueprints with business logic
- **templates/**: HTML templates for the user interface

---

## Technologies Used

- **Backend Framework**: Flask 3.x
- **Database**: MySQL with SQLAlchemy ORM
- **Database Driver**: PyMySQL
- **Templating**: Jinja2 (Flask default)
- **CSS**: Custom inline styles
- **Timezone**: zoneinfo (Europe/Amsterdam)

---

## HTML Templates

**Note**: The HTML templates in the `templates/` directory were generated with the help of AI (Claude and ChatGPT).

---

# License

This project is created by Lisa Ponsteen (i6397659) and Noortje van Maldegem (i6374487)
---