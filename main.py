from copy import deepcopy

from script import load_from_csv
from customers import create_customers
import ant
from ant_colony import AntColony
import matplotlib.pyplot as plt


filename = "r201"

data = load_from_csv(filename + ".csv")
customers = create_customers(data)


def show_path(best_ant, alpha, beta, number, which):
    x1 = [point.x_coord for point in best_ant.path]
    y1 = [point.y_coord for point in best_ant.path]
    plt.figure(figsize=(8, 6))
    plt.plot(x1, y1, marker='o')
    plt.scatter(x1[0], y1[0], color='green', s=100, label='Start')
    plt.scatter(x1[-1], y1[-1], color='red', s=100, label='End')
    plt.title(f"Trasa przebyta przez mrówkę\nilość mrówek: {number} alpha: {alpha} beta: {beta}")
    plt.xlabel("Współrzędna X")
    plt.ylabel("Współrzędna Y")
    plt.legend()
    plt.grid()
    plt.savefig(f"wykresy/{filename}_{which}.png")
    plt.show()


if __name__ == "__main__":
    all_ants = []
    demand = 0
    cust2 = deepcopy(customers)
    index = 0
    all_demand = 0
    d = 0
    path = 0
    x = []
    y = []
    iter = 0
    for k in customers:
        d += k.demand
    while len(customers) > 1:
        iter += 1
        ant_colony = AntColony(customers)
        best_ant = ant.al(20, 0.2, 10, ant_colony, 1, 1, 200)
        all_ants.append(best_ant)

        x = [custo.x_coord for custo in customers]
        y = [custo.y_coord for custo in customers]
        show_path(best_ant, 1, 1, 10, iter)
        for element in cust2:
            if element.cust_no in [dupa.cust_no for dupa in best_ant.path[1:]]:
                for ele in customers:
                    if ele.cust_no == element.cust_no:
                        index = customers.index(ele)
                customers.pop(index)
            element.visited = False
        cust2 = deepcopy(customers)

    for ant in all_ants:
        for point in ant.path:
            print(point)
            demand += point.demand
        path += ant.get_traveled_path()
        print("Demand: ", demand)
        print("Distance: ", ant.get_traveled_path())
        all_demand += demand
        demand = 0
        print("\n")
    print(d)
    print(all_demand)
    print(path)
