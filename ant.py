import copy
from time import sleep

from script import load_from_csv
from customers import create_customers, Customer
import numpy as np
import random
from copy import deepcopy


class Ant:
    def __init__(self, ant_colony, customers, alpha, beta, capacity):
        self.path = []
        self.alpha = alpha
        self.beta = beta
        self.capacity = capacity
        self.customers = customers
        self.distances = ant_colony.distances
        self.pheromones = ant_colony.pheromones
        self.starting_point()

    def starting_point(self):
        next_move = self.customers[0]
        self.path.append(next_move)

    def chose_next_place(self):
        current_place = self.path[-1]

        probabilities = []
        total = 0

        for place in self.customers:
            if (not place.visited) and place.demand != 0:
                pheromone = self.pheromones[self.customers.index(current_place)][self.customers.index(place)]
                distance = self.distances[self.customers.index(current_place)][self.customers.index(place)]

                heuristic = 1 / distance
                probability = (pheromone ** self.alpha) * (heuristic ** self.beta)
                probabilities.append((place, probability))
                total += probability

        if total > 0:
            probabilities = [(place, prob / total) for place, prob in probabilities]
            selected_place = np.random.choice([place for place, _ in probabilities],
                                              p=[prob for _, prob in probabilities])
            if self.capacity > selected_place.demand:
                self.path.append(selected_place)
                self.capacity -= selected_place.demand
                if self.capacity <= 0:
                    print(self.capacity)
            selected_place.visited = True

    def chose_next_place_randomly(self, point=0.3):
        if point > random.uniform(0, 1):
            try:
                next_move = random.choice([place for place in self.customers[1:] if not place.visited])
                if self.capacity > next_move.demand:
                    self.path.append(next_move)
                    self.customers[self.customers.index(next_move)].visited = True
                    self.capacity -= next_move.demand
                else:
                    self.chose_next_place()
            except:
                return False
            return True
        return False

    def leave_pheromones(self):
        for i in range(len(self.path) - 1):
            current_place = self.path[i]
            next_place = self.path[i + 1]

            self.pheromones[self.customers.index(current_place)][self.customers.index(next_place)] += 1 / self.get_traveled_path()
            self.pheromones[self.customers.index(next_place)][self.customers.index(current_place)] += 1 / self.get_traveled_path()

    def get_traveled_path(self):
        total_distance = 0
        for i in range(len(self.path) - 1):
            current_place = self.path[i]
            next_place = self.path[i + 1]
            distance = self.distances[self.customers.index(current_place)][self.customers.index(next_place)]
            total_distance += distance

        return total_distance


def get_best_ant(population_of_ants, previous_best_ant):
    best_ant = previous_best_ant

    if previous_best_ant is None:
        return min(population_of_ants, key=lambda ant: ant.get_traveled_path())

    for ant in population_of_ants:
        traveled_distance = ant.get_traveled_path()

        if traveled_distance < best_ant.get_traveled_path():
            best_ant = ant

    return best_ant


def al(iterations, evaporate, number_of_ants, ant_colony, alpha, beta, capacity):
    best_ant = None
    for i in range(iterations):
        ants = [Ant(ant_colony, deepcopy(ant_colony.customers), alpha, beta, capacity) for _ in range(number_of_ants)]
        for ant in ants:
            while not all([place.visited for place in ant.customers[1:]]):
                if not ant.chose_next_place_randomly():
                    ant.chose_next_place()
        ant_colony.evaporate_pheromones(evaporate)
        for ant in ants:
            ant.leave_pheromones()
        best_ant = get_best_ant(ants, best_ant)
        # print("Best path in ant (al) ", best_ant.path)
    print(best_ant.capacity)
    return best_ant
