# Supreme Slices Pizza Management System

## Description
The Supreme Slices Pizza Management System is a web application designed to streamline the management of pizzas and toppings in a restaurant setting. It provides features for Chefs to create, update, and delete pizzas, as well as Owners to manage toppings. Access to both the Chef and Owner dashboards are user-authenticated and therefore prevent non-management users from accessing and editing the system.

## User Stories

### Manage Toppings
As a pizza store owner, I should be able to manage the toppings available for my pizza chefs.

- It should allow me to see a list of available toppings.
- It should allow me to add a new topping.
- It should allow me to delete an existing topping.
- It should allow me to update an existing topping.
- It should not allow me to enter duplicate toppings.

### Manage Pizzas
As a pizza chef, I should be able to create new pizza masterpieces.

- It should allow me to see a list of existing pizzas and their toppings.
- It should allow me to create a new pizza and add toppings to it.
- It should allow me to delete an existing pizza.
- It should allow me to update an existing pizza.
- It should allow me to update toppings on an existing pizza.
- It should not allow me to enter duplicate pizzas.

## Table of Contents
- [User Stories](#user-stories)
- [Installation](#installation)
- [Usage](#usage)
- [Login Information](#login-information)
- [Running Tests](#running-tests)
- [Author](#author)
- [License](#license)

## Installation
To install the Pizza Management System locally, follow these steps:

1. **Clone the repository to your local machine:**
   ```bash
   git clone https://github.com/your-username/pizza-management.git
2. **Navigate to the project directory:**
   ```bash
   cd pizza-management
3. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
4. **Activate the virtual environment:**
     - On Windows:
       ```bash
       venv\Scripts\activate
     - On macOS and Linux:
       ```bash
       source venv/bin/activate
5. Install the project dependencies:
   ```bash
   pip install -r requirements.txt
6. Apply the database migrations:
   ```bash
   python manage.py migrate

 ## Usage
To run the Pizza Management System locally, execute the following command making sure you are in the project's root directory:
```bash
python manage.py runserver
```
Then, access the application in your web browser at http://localhost:8000.

## Login Information
To access the Chef and Owner dashboards, use the following credentials to log in:
- **Chef**
  - **Username:** Chef
  - **Password:** SupremeSlicesChef
- **Owner:**
  - **Username:** Owner
  - **Password:** SupremeSlicesOwner

If you do not log in, you will not be able to access the dashboards.

## Running Tests
To run tests for the Pizza Management System locally, use the following commands:
> Make sure you are in the project's root directory and virtual environment. \path\to\full-stack-developer\pizzaManagement\
- Run Chef Dashboard Tests
  ```bash
  python manage.py test Chef
  ```
- Run Owner Dashboard Tests
  ```bash
  python manage.py test Owner
  ```
  These commands will execute all the tests within the respective Chef and Owner apps in the project and display the results in the terminal.
  
## Author
This project was created by **Sami Tanquary**. It is intended for use by **StrongMind** as a part of the Full Stack Developer technical interview.

## License
This project is licensed under the MIT License.
