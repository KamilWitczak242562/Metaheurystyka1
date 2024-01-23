from script import load_from_csv
from customers import create_customers, Customer
import ant

data = load_from_csv("r101.csv")



if __name__ == "__main__":
    customers = create_customers(data)
    # for customer in customers:
    #     print(customer)
    best_ant = ant.al(500, 0.2, 50, customers, 1, 1, 200)

    print(best_ant, best_ant.path, len(best_ant.path))
    for customer in best_ant.path:
        print(customer)
    print(len(set(best_ant.path)))