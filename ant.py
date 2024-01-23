from script import load_from_csv
from customers import create_customers, Customer
import numpy as np
import random


def euclidean_distance(point1, point2):
    distance = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)
    return distance if distance != 0 else 1


def create_distance_matrix(points):
    size = len(points)
    distance_matrix = np.zeros((size, size))

    for i in range(size):
        for j in range(size):
            distance_matrix[i][j] = euclidean_distance(points[i], points[j])

    return distance_matrix


def create_pheromone_matrix(size):
    return np.ones((size, size)) - np.eye(size)


data = load_from_csv("r101.csv")
customers = create_customers(data)

pheromones = create_pheromone_matrix(len(customers))

distances = create_distance_matrix([[x.x_coord, x.y_coord] for x in customers])


class Ant:
    def __init__(self, customers, alpha, beta, capacity):
        self.path = []
        self.customers = customers
        self.alpha = alpha
        self.beta = beta
        self.capacity = capacity
        self.starting_point()

    def starting_point(self):
        next_move = self.customers[0]
        self.path.append(next_move)

    def chose_next_place(self):
        current_place = self.path[-1]

        probabilities = []
        total = 0

        for place in self.customers:
            if (not place.visited) and self.capacity > place.demand != 0:
                pheromone = pheromones[self.customers.index(current_place)][self.customers.index(place)]
                distance = distances[self.customers.index(current_place)][self.customers.index(place)]

                heuristic = 1 / distance
                probability = (pheromone ** self.alpha) * (heuristic ** self.beta)
                probabilities.append((place, probability))
                total += probability

        if total > 0:
            probabilities = [(place, prob / total) for place, prob in probabilities]
            selected_place = np.random.choice([place for place, _ in probabilities],
                                              p=[prob for _, prob in probabilities])
            self.path.append(selected_place)
            self.capacity -= selected_place.demand
            selected_place.visited = True

    def chose_next_place_randomly(self, point=0.3):
        if point > random.uniform(0, 1):
            try:
                next_move = random.choice([place for place in self.customers[1:] if not place.visited])
                if self.capacity > next_move.demand:
                    self.path.append(next_move)
                    self.customers[self.customers.index(next_move)].visited = True
                else:
                    self.chose_next_place_randomly()
            except:
                return False
            return True
        return False

    def leave_pheromones(self):
        for i in range(len(self.path) - 1):
            current_place = self.path[i]
            next_place = self.path[i + 1]

            pheromones[self.customers.index(current_place)][self.customers.index(next_place)] += 1 / self.get_traveled_path()
            pheromones[self.customers.index(next_place)][self.customers.index(current_place)] += 1 / self.get_traveled_path()

    def get_traveled_path(self):
        total_distance = 0
        for i in range(len(self.path) - 1):
            current_place = self.path[i]
            next_place = self.path[i + 1]
            distance = distances[self.customers.index(current_place)][self.customers.index(next_place)]
            total_distance += distance

        return total_distance


def evaporate_pheromones(evaporation_rate):
    for i in range(len(pheromones)):
        for j in range(len(pheromones[i])):
            pheromones[i][j] *= (1 - evaporation_rate)


def get_best_ant(population_of_ants, previous_best_ant):
    best_ant = previous_best_ant

    if previous_best_ant is None:
        return min(population_of_ants, key=lambda ant: ant.get_traveled_path())

    for ant in population_of_ants:
        traveled_distance = ant.get_traveled_path()

        if traveled_distance < best_ant.get_traveled_path():
            best_ant = ant

    return best_ant


def al(iterations, evaporate, number_of_ants, attractions, alpha, beta, capacity):
    best_ant = None
    for i in range(iterations):
        for p in attractions:
            p.visited = False
        ants = [Ant(attractions, alpha, beta, capacity) for _ in range(number_of_ants)]
        # for ant in ants:
        #     ant.starting_point()
        # for j in attractions:
        while not all([place.visited for place in attractions[1:]]):
            # if all([place.visited for place in attractions]):
            #     print("Wszystko")
            #     return best_ant
            for ant in ants:
                if not ant.chose_next_place_randomly():
                    ant.chose_next_place()
        evaporate_pheromones(evaporate)
        for ant in ants:
            ant.leave_pheromones()
        best_ant = get_best_ant(ants, best_ant)
    return best_ant