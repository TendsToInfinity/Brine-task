import unittest
import pandas as pd
from main import calculate_revenues
from pandas.testing import assert_series_equal

class TestRevenueCalculations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Test Data here
        data = {
            'order_id': [1, 2, 3, 4, 5],
            'customer_id': [1, 1, 2, 2, 3],
            'order_date': ['2023-06-01', '2023-06-02', '2023-07-01', '2023-07-02', '2023-07-03'],
            'product_id': [1, 2, 1, 2, 1],
            'product_name': ['Product1', 'Product2', 'Product1', 'Product2', 'Product1'],
            'product_price': [100, 200, 100, 200, 100],
            'quantity': [1, 1, 2, 1, 3]
        }
        cls.df = pd.DataFrame(data)
        cls.df['order_date'] = pd.to_datetime(cls.df['order_date'])  # convert to datetime
        cls.results = {}

    def test_calculate_revenues(self):
        monthly_revenue, product_revenue, customer_revenue, top_10_customers = calculate_revenues(self.__class__.df)
        
        # Store the results
        self.__class__.results['monthly_revenue'] = monthly_revenue
        self.__class__.results['product_revenue'] = product_revenue
        self.__class__.results['customer_revenue'] = customer_revenue
        self.__class__.results['top_10_customers'] = top_10_customers

        # Define your expected results here
        expected_monthly_revenue = pd.Series({
            pd.to_datetime('2023-06-01'): 300,
            pd.to_datetime('2023-07-01'): 700
        }, name='total_cost')
        expected_monthly_revenue.index.name = 'order_date'
        monthly_revenue.index.freq = None  # remove frequency before comparison

        expected_product_revenue = pd.Series({
            'Product1': 600,
            'Product2': 400
        }, name='total_cost')
        expected_product_revenue.index.name = 'product_name'

        expected_customer_revenue = pd.Series({
            1: 300,
            2: 400,
            3: 300
        }, name='total_cost')
        expected_customer_revenue.index.name = 'customer_id'

        # Assert if the results match expected results
        assert_series_equal(monthly_revenue, expected_monthly_revenue)
        assert_series_equal(product_revenue, expected_product_revenue)
        assert_series_equal(customer_revenue, expected_customer_revenue)
        self.assertEqual(list(top_10_customers.index), [1, 2, 3])  # There's only one customer

# Execute tests if the script is run directly
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
