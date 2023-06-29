# Django E-commerce Website
This project is an e-commerce website built with Django. It allows users to browse products, add items to a cart, and checkout. Authentication is provided, enabling users to sign up, log in, and view their order history.

## Features
- User Authentication: Users can sign up, log in, and log out. User sessions are managed securely using Django's built-in authentication.
- Product Browsing: All products are listed in the store. Users can view individual product details by clicking on a product.
- Shopping Cart: Users can add products to a cart. The cart updates in real time as items are added or removed.
- Checkout Process: Users can checkout. Orders are associated with the user account and can be viewed later.
- Search: Users can search for products by name or description from the store page.

## Directory Structure
- store: This directory contains the main application.
- views.py: Contains the views for login, signup, store, cart, checkout, updating items, processing orders, viewing items, and home.
- urls.py: Contains URL mappings for the aforementioned views.
- forms.py: Contains forms for user creation and product ordering.
- utils.py: Contains utility functions used across the application.
- models.py: Contains the models for Customer, Product, Order, OrderItem, and ShippingAddress.
- templates/store: Contains the HTML templates for the application, including main.html, cart.html, store.html, view_item.html, login.html, signup.html, and home.html.
- static: This directory contains static files such as CSS, JavaScript, and images used across the application.
- css: Contains CSS files.
- images: Contains image files.
- js: Contains JavaScript files.
- ecommerce: This directory contains the settings for the Django project.
- settings.py: Contains Django project settings.
- urls.py: Contains project-level URL mappings.

## Installation

### Clone this repository:

git clone https://github.com/username/projectname.git

### Install the required packages:

pip install -r requirements.txt

### Make migrations:

'python manage.py makemigrations

### Migrate the database:

'python manage.py migrate'

### Run the server:

python manage.py runserver

The server will start at localhost:8000.

## Contributing
Please submit issues if you find any bugs. Feel free to fork and submit pull requests for any features you think would be useful.

## License
This project is licensed under the MIT License. See LICENSE for more details.

Please replace username and projectname in the git clone command with your actual GitHub username and repository name. Add further details to the sections as needed to provide more information about your project. If you plan to license your project under the MIT License or another license, ensure you include a LICENSE file in your project.
