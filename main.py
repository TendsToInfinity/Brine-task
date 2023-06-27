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

# Create a DataFrame for testing
data = {
    'order_id': [1, 2, 3, 4, 5],
    'customer_id': [1, 1, 2, 2, 3],
    'order_date': ['2023-06-01', '2023-06-02', '2023-07-01', '2023-07-02', '2023-07-03'],
    'product_id': [1, 2, 1, 2, 1],
    'product_name': ['Product1', 'Product2', 'Product1', 'Product2', 'Product1'],
    'product_price': [100, 200, 100, 200, 100],
    'quantity': [1, 1, 2, 1, 3]
}

df = pd.DataFrame(data)
df['order_date'] = pd.to_datetime(df['order_date'])  # convert to datetime

# Call calculate_revenues and print the results
monthly_revenue, product_revenue, customer_revenue, top_10_customers = calculate_revenues(df)

print("Monthly revenue:\n", monthly_revenue)
print("\nProduct revenue:\n", product_revenue)
print("\nCustomer revenue:\n", customer_revenue)
print("\nTop 10 customers by revenue:\n", top_10_customers)


