import unittest
from io import StringIO
from unittest.mock import patch
import graded_ex_1 as gex



class TestShoppingProgram(unittest.TestCase):

    def setUp(self):
        self.cart = []

    # def test_name_validation(self):
    #     self.assertTrue(gex.validate_name("John Doe"))
    #     self.assertFalse(gex.validate_name("JohnDoe"))
    #     self.assertFalse(gex.validate_name("John 123"))


    # def test_email_validation(self):
    #     self.assertTrue(gex.validate_email("john.doe@example.com"))
    #     self.assertFalse(gex.validate_email("johndoe.com"))
    #     self.assertTrue(gex.validate_email("john@doe"))
    #     self.assertFalse(gex.validate_email(" "))


    @patch('builtins.input', side_effect=['1'])
    def test_valid_category_selection(self, mock_input):
        category_index = gex.display_categories()
        self.assertEqual(category_index, 0)

    @patch('builtins.input', side_effect=['5'])
    def test_invalid_category_selection(self, mock_input):
        category_index = gex.display_categories()
        self.assertTrue(category_index is None or category_index >= len(gex.products))  


    @patch('builtins.input', side_effect=['abc'])
    def test_non_numeric_category_selection(self, mock_input):
        category_index = gex.display_categories()
        self.assertIsNone(category_index)  

    
    def test_valid_product_selection(self):
        products_list = [("Laptop", 1000), ("Smartphone", 600)]
        product_choice = "1"
        product_index = int(product_choice) - 1
        self.assertEqual(product_index, 0)  

    def test_invalid_product_selection(self):
        products_list = [("Laptop", 1000), ("Smartphone", 600)]
        product_choice = "10"  
        product_index = int(product_choice) - 1
        self.assertNotIn(product_index, range(len(products_list)))  

    
    def test_valid_quantity(self):
        quantity = "3"
        self.assertTrue(quantity.isdigit() and int(quantity) > 0)  

    def test_invalid_quantity_zero(self):
        quantity = "0"
        self.assertFalse(int(quantity) > 0)  

    def test_invalid_quantity_non_numeric(self):
        quantity = "abc"
        self.assertFalse(quantity.isdigit())  

    # Test Sorting Products
    def test_sort_ascending(self):
        products_list = [("Laptop", 1000), ("Smartphone", 600), ("USB Drive", 15)]
        sorted_list = gex.display_sorted_products(products_list, "asc")
        expected_list = [("USB Drive", 15), ("Smartphone", 600), ("Laptop", 1000)]
        self.assertEqual(sorted_list, expected_list)  

    def test_sort_descending(self):
        products_list = [("Laptop", 1000), ("Smartphone", 600), ("USB Drive", 15)]
        sorted_list = gex.display_sorted_products(products_list, "desc")
        expected_list = [("Laptop", 1000), ("Smartphone", 600), ("USB Drive", 15)]
        self.assertEqual(sorted_list, expected_list)  

    
    def test_add_to_cart(self):
        product = ("Laptop", 1000)
        quantity = 2
        gex.add_to_cart(self.cart, product, quantity)
        self.assertIn(("Laptop", 1000, 2), self.cart)  

    def test_display_cart(self):
        cart = [("Laptop", 1000, 2), ("Smartphone", 600, 1)]
        expected_output = "Laptop - $1000 x 2 = $2000\nSmartphone - $600 x 1 = $600\nTotal cost: $2600"
        with patch('sys.stdout', new=StringIO()) as fake_out:
            gex.display_cart(cart)
            self.assertIn(expected_output, fake_out.getvalue().strip())  

    
    @patch('builtins.input', side_effect=['3'])  
    def test_back_to_categories(self, mock_input):
        action_choice = '3'
        self.assertEqual(action_choice, '3')  

    
    @patch('builtins.input', side_effect=['4'])  
    def test_finish_shopping(self, mock_input):
        finish_shopping = True
        self.assertTrue(finish_shopping)  

    
    """ def test_receipt_generation(self):
        cart = [("Laptop", 1000, 2), ("Smartphone", 600, 1)]
        total_cost = 2600
        name = "John Doe"
        email = "john.doe@example.com"
        address = "1234 Elm St, Springfield"
        expected_output = (
            "Customer: John Doe\n"
            "Email: john.doe@example.com\n"
            "Items Purchased:\n"
            "2 x Laptop - $1000 = $2000\n"
            "1 x Smartphone - $600 = $600\n"
            "Total: $2600\n"
            "Delivery Address: 1234 Elm St, Springfield\n"
            "Your items will be delivered in 3 days.\n"
            "Payment will be accepted upon delivery."
        )
        with patch('sys.stdout', new=StringIO()) as fake_out:
            gex.generate_receipt(name, email, cart, total_cost, address)
            self.assertIn(expected_output, fake_out.getvalue().strip())  # Check receipt output """


if __name__ == '__main__':
    unittest.main()
