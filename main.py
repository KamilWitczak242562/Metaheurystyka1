from script import load_from_csv
from customers import create_customers, Customer

data = load_from_csv("r101.csv")


if __name__ == "__main__":
    customers = create_customers(data)
    for customer in customers:
        print(customer)
