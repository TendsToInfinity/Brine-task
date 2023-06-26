import unittest
import pandas as pd
from io import StringIO
from task import calculate_revenues

class TestRevenueCalculations(unittest.TestCase):
    def setUp(self):
        # This function is called before each test case
        # We'll create a small DataFrame that simulates the CSV file
        csv_data = StringIO("""
order_id,customer_id,order_date,product_id,product_name,product_price,quantity
1,1,2023-06-01,1,Product1,100,1
2,2,2023-06-01,2,Product2,200,1
3,1,2023-06-02,1,Product1,100,2
4,1,2023-07-01,2,Product2,200,1
        """)
        self.df = pd.read_csv(csv_data, parse_dates=['order_date'])

    def test_calculate_revenues(self):
        monthly_revenue, product_revenue, customer_revenue, top_10_customers = calculate_revenues(self.df)

        expected_monthly_revenue = pd.Series({
            pd.to_datetime('2023-06-01'): 500,
            pd.to_datetime('2023-07-01'): 200
        })
        expected_product_revenue = pd.Series({
            'Product1': 300,
            'Product2': 400
        })
        expected_customer_revenue = pd.Series({
            1: 500,
            2: 200
        })

        pd.testing.assert_series_equal(monthly_revenue, expected_monthly_revenue)
        pd.testing.assert_series_equal(product_revenue, expected_product_revenue)
        pd.testing.assert_series_equal(customer_revenue, expected_customer_revenue)
        self.assertEqual(list(top_10_customers.index), [1])  # There's only one customer

if __name__ == '__main__':
    unittest.main()
