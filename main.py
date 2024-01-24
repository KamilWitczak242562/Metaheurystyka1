from script import load_from_csv
from customers import create_customers, Customer
import ant
import ant_colony
import numpy as np

data = load_from_csv("r101.csv")
customers = create_customers(data)

if __name__ == "__main__":
    # best_ant = ant.al(100, 0.2, 50, customers, 1, 1, 200)
    all_ants = []
    # print(best_ant, best_ant.path, len(best_ant.path))
    # for customer in best_ant.path:
    #     print(customer)
    # print(len(set(best_ant.path)))
    # demand = 0
    # for customer in best_ant.path:
    #     demand += customer.demand
    # print(demand)
    demand = 0
    while customers:
        ant_colony = ant_colony.AntColony(customers)
        best_ant = ant.al(100, 0.2, 50, ant_colony, 1, 1, 200)
        all_ants.append(best_ant)
        for element in customers:
            if element in best_ant.path:
                customers.remove(element)

    for ant in all_ants:
        for point in ant:
            demand += point.demand
        print(ant.path)
        print(demand)
        demand = 0
