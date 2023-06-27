import pandas as pd
import unittest
from io import StringIO
from pandas._testing import assert_frame_equal, assert_series_equal

# Main function
def calculate_revenues(df):
    # Create a new column for the total cost of each order
    df['total_cost'] = df['product_price'] * df['quantity']

    # Convert order_date to datetime format
    df['order_date'] = pd.to_datetime(df['order_date'])

    # Set order_date as the index of the DataFrame to use resample
    df.set_index('order_date', inplace=True)

    # Calculate total revenue per month
    monthly_revenue = df.resample('MS')['total_cost'].sum()


    # Calculate total revenue per product
    product_revenue = df.groupby('product_name')['total_cost'].sum()

    # Calculate total revenue per customer
    customer_revenue = df.groupby('customer_id')['total_cost'].sum()

    # Get the top 10 customers by revenue
    top_10_customers = customer_revenue.nlargest(10)

    return monthly_revenue, product_revenue, customer_revenue, top_10_customers

# Test cases
class TestRevenueCalculations(unittest.TestCase):
    results = {}  # Store results here
    def setUp(self):
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
# Store the results
    self.__class__.results['monthly_revenue'] = monthly_revenue
    self.__class__.results['product_revenue'] = product_revenue
    self.__class__.results['customer_revenue'] = customer_revenue
    self.__class__.results['top_10_customers'] = top_10_customers
    expected_monthly_revenue = pd.Series({
    pd.to_datetime('2023-06-01'): 500,
    pd.to_datetime('2023-07-01'): 200
    }, name='total_cost')

    expected_monthly_revenue.index.name = 'order_date'
    monthly_revenue.index.freq = None  # remove frequency before comparison

    expected_product_revenue = pd.Series({
        'Product1': 300,
        'Product2': 400
    }, name='total_cost')
    expected_product_revenue.index.name = 'product_name'

    # Expected revenues
    expected_customer_revenue = pd.Series({
    1: 700,
    }, name='total_cost')
    expected_customer_revenue.index.name = 'customer_id'

    assert_series_equal(monthly_revenue, expected_monthly_revenue)
    assert_series_equal(product_revenue, expected_product_revenue)
    assert_series_equal(customer_revenue, expected_customer_revenue)
    self.assertEqual(list(top_10_customers.index), [1])  # There's only one customer

# Execute tests if the script is run directly
if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

