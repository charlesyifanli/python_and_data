# Products available in the store by category
from Demos.win32ts_logoff_disconnected import username

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
    judge = False if sort_order == 1 else True
    return sorted(products_list, key=lambda x: x[1], reverse=judge)


def display_products(products_list):
    i = 0
    for product, price in products_list:
        i += 1
        print(f'{i}. {product}:{price}')


def display_categories():
    i = 0
    for key in products.keys():
        i += 1
        print(f'{i}. {key}')


def add_to_cart(cart, product, quantity):
    category_ = product[0]
    product_name, product_price = products[category_][product[1] - 1]
    if not cart.get(product_name):
        cart[product_name] = [product_price, quantity]
    else:
        cart[product_name][quantity] += quantity
    print('Your product has already been added')


def display_cart(cart):
    cost = 0
    print('Product Name :: Price :: Quantity')
    for product_name, list_ in cart.items():
        cost += list_[0] * list_[1]
        print(f'{product_name} :: {list_[0]} :: {list_[1]}')
    return cost


def generate_receipt(name, email, cart, total_cost, address):
    print(f'Username:{name}\n'
          f'Email:{email}\n'
          f'Cart:{cart}\n'
          f'Total Cost:{total_cost}\n'
          f'Address:{address}')


def validate_name(name: str) -> bool:
    if ' ' not in name:
        print('Invalid name')
        return False
    res = True
    first, last = name.split(' ')
    if not first.isalpha() or not last.isalpha():
        print('Invalid')
        res = False
    return res


def validate_email(email: str) -> bool:
    if '@' not in email:
        print('Invalid email')
        return False
    else:
        return True


def get_category(num: int) -> str:
    i = 0
    for key in products.keys():
        i += 1
        if num == i:
            return key
    return ''


def main():
    # name
    username = ''
    while True:
        username = input('Please enter your firstname and lastname seperated by blank with only alphabets >> ')
        if validate_name(username):
            break
    # email
    user_email = ''
    while True:
        user_email = input('Please enter your email >> ')
        if validate_email(user_email):
            break
    # show categories
    display_categories()
    category_chosen = get_category(int(input('Please enter your number corresponding with category >> ')))
    # show products
    display_products(products[category_chosen])
    # process choice
    cart = dict()
    while True:
        print('1. Select a product to buy\n'
              '2. Sort the products according to the price.\n'
              '3. Go back to the category selection.\n'
              '4. Finish shopping')
        choice = int(input('Please enter your choice >> '))
        if choice == 1:
            product_id = int(input('Please enter the id >> '))
            quantity = int(input('Please enter the number >> '))
            add_to_cart(cart=cart, product=[category_chosen, product_id], quantity=quantity)
            continue
        elif choice == 2:
            print('1. Ascending\n'
                  '2. Descending')
            print(display_sorted_products(products[category_chosen], int(input('Please enter the number'))))
            continue
        elif choice == 3:
            display_categories()
            category_chosen = get_category(int(input('Please enter your number corresponding with category >> ')))
            # show products
            display_products(products[category_chosen])
            continue
        elif choice == 4:
            if not cart:
                print('Thank you for using our portal. '
                      'Hope you buy something from us next time. Have a nice day')
                break
            else:
                cost = display_cart(cart)
                print(f'Totally cost: {cost}')
                # delivery
                address = input('Please enter your delivery address')
                generate_receipt(name=username, email=user_email, cart=cart, total_cost=cost, address=address)
                break


""" The following block makes sure that the main() function is called when the program is run. 
It also checks that this is the module that's being run directly, and not being used as a module in some other program. 
In that case, only the part that's needed will be executed and not the entire program """
if __name__ == "__main__":
    main()
