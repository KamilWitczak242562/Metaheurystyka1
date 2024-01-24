from copy import deepcopy

from script import load_from_csv
from customers import create_customers
import ant
from ant_colony import AntColony

data = load_from_csv("r101.csv")
customers = create_customers(data)

if __name__ == "__main__":
    all_ants = []
    demand = 0
    cust2 = deepcopy(customers)
    index = 0
    all_demand = 0
    d = 0
    for k in customers:
        d += k.demand
    while len(customers) > 1:
        # print("C1", " ", customers)
        ant_colony = AntColony(customers)
        best_ant = ant.al(20, 0.2, 10, ant_colony, 1, 1, 200)
        all_ants.append(best_ant)
        # print("Best ant path in main: ", best_ant.path)

        for element in cust2:
            if element.cust_no in [dupa.cust_no for dupa in best_ant.path[1:]]:
                # print("usunieto")
                for ele in customers:
                    if ele.cust_no == element.cust_no:
                        index = customers.index(ele)
                customers.pop(index)
            element.visited = False
        cust2 = deepcopy(customers)
        # print("C2", " ", customers)

    for ant in all_ants:
        for point in ant.path:
            print(point)
            demand += point.demand
        print(demand)
        all_demand += demand
        demand = 0
        print("\n")
    print(d)
    print(all_demand)
