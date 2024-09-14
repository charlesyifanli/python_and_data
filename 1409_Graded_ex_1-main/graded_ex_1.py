# Available products by category

products = {
    "IT Products": [
        ("Laptop", 1000),
        ("Smartphone", 600),
        ("Headphones", 150),
        ("Keyboard", 50),
        ("Monitor", 300),
        ("Mouse", 25),
        ("Printer", 120),
        ("USB Drive", 15)
    ],
    "Electronics": [
        ("Smart TV", 800),
        ("Bluetooth Speaker", 120),
        ("Camera", 500),
        ("Smartwatch", 200),
        ("Home Theater", 700),
        ("Gaming Console", 450)
    ],
    "Groceries": [
        ("Milk", 2),
        ("Bread", 1.5),
        ("Eggs", 3),
        ("Rice", 10),
        ("Chicken", 12),
        ("Fruits", 6),
        ("Vegetables", 5),
        ("Snacks", 8)
    ]
}


def display_sorted_products(products_list, sort_order):
    reverse_order = sort_order.lower() == 'desc'
    return sorted(products_list, key=lambda x: x[1], reverse=reverse_order)


def display_products(products_list):
    for i, (product, price) in enumerate(products_list, start=1):
        print(f'{i}. {product}: ${price}')


def display_categories():
    print('The following are the categories:')
    for i, category in enumerate(products.keys(), start=1):
        print(f'{i}. {category}')


def add_to_cart(cart, product, quantity):
    cart.append((*product, quantity))
    print('Product added to the cart.')


def display_cart(cart):
    if not cart:
        print('Your cart is empty.')
        return 0

    total_cost = 0
    for name, price, quantity in cart:
        total = price * quantity
        total_cost += total
        print(f'{name} - ${price} x {quantity} = ${total}')

    print(f'Total cost: ${total_cost}')
    return total_cost


def generate_receipt(name, email, cart, total_cost, address):
    print(f'Username: {name}\nEmail: {email}')
    print('Cart items:')
    display_cart(cart)
    print(f'Delivery Address: {address}')
    print(f'Total Cost: ${total_cost}')


def validate_name(name):
    if ' ' not in name or not all(part.isalpha() for part in name.split()):
        print('Invalid Name')
        return False
    return True


def validate_email(email):
    if '@' not in email:
        print('Invalid Email')
        return False
    return True


def get_category_by_number(category_num):
    category_list = list(products.keys())
    if 1 <= category_num <= len(category_list):
        return category_list[category_num - 1]
    return None


def get_user_input(prompt, validation_fn=None):
    user_input = input(prompt)
    while validation_fn and not validation_fn(user_input):
        user_input = input(prompt)
    return user_input


def main():
    # Get username
    username = get_user_input(prompt='Please enter your full name >> ', validation_fn=validate_name)

    # Get email
    user_email = get_user_input(prompt='Please enter your email >> ', validation_fn=validate_email)

    cart = []

    while True:
        # Display categories
        display_categories()
        category_num = int(get_user_input('Enter the number of the category >> ', str.isdigit))
        category_name = get_category_by_number(category_num)

        if not category_name:
            print('Invalid category. Try again.')
            continue

        while True:
            # Display products in the selected category
            display_products(products[category_name])

            print('\nYou have 4 choices:')
            print('1. Select a product to buy')
            print('2. Sort the products by price')
            print('3. Go back to category selection')
            print('4. Finish shopping')

            choice = get_user_input('Please enter your choice >> ', str.isdigit)
            choice = int(choice)

            if choice == 1:
                # Select a product and quantity
                product_id = int(get_user_input('Enter the product number >> ', str.isdigit))
                quantity = int(get_user_input('Enter the quantity >> ', str.isdigit))
                if 1 <= product_id <= len(products[category_name]):
                    product = products[category_name][product_id - 1]
                    add_to_cart(cart, product, quantity)
                else:
                    print('Invalid product number.')

            elif choice == 2:
                # Sort products by price
                sort_order = get_user_input('Enter "asc" for ascending or "desc" for descending >> ').lower()
                sorted_products = display_sorted_products(products[category_name], sort_order)
                display_products(sorted_products)

            elif choice == 3:
                # Go back to category selection
                break

            elif choice == 4:
                # Finish shopping
                if not cart:
                    print('No items in the cart. Goodbye!')
                    return

                total_cost = display_cart(cart)
                delivery_address = input('Please enter your delivery address >> ')
                generate_receipt(username, user_email, cart, total_cost, delivery_address)
                return


if __name__ == "__main__":
    main()
