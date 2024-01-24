import numpy as np

class AntColony:
    def __init__(self, customers):
        self.customers = customers
        self.distances = self.create_distance_matrix([[x.x_coord, x.y_coord] for x in self.customers])
        self.pheromones = self.create_pheromone_matrix(len(self.customers))

    def euclidean_distance(self, point1, point2):
        distance = np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)
        return distance if distance != 0 else 1

    def create_distance_matrix(self, points):
        size = len(points)
        distance_matrix = np.zeros((size, size))

        for i in range(size):
            for j in range(size):
                distance_matrix[i][j] = self.euclidean_distance(points[i], points[j])

        return distance_matrix

    def create_pheromone_matrix(self, size):
        return np.ones((size, size)) - np.eye(size)

    def evaporate_pheromones(self, evaporation_rate):
        for i in range(len(self.pheromones)):
            for j in range(len(self.pheromones[i])):
                self.pheromones[i][j] *= (1 - evaporation_rate)
