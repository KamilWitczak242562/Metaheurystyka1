class Customer:
    def __init__(self, cust_no, x_coord, y_coord, demand, ready_time, due_time, service_time):
        self.cust_no = cust_no
        self.x_coord = x_coord
        self.y_coord = y_coord
        self.demand = demand
        self.ready_time = ready_time
        self.due_time = due_time
        self.service_time = service_time
        self.visited = False

    def __str__(self):
        return f"CUST NO. {self.cust_no}  XCOORD. {self.x_coord}  YCOORD. {self.y_coord}  " \
               f"DEMAND {self.demand}  READY TIME {self.ready_time}  DUE DATE {self.due_time}  " \
               f"SERVICE TIME {self.service_time} VISITED {self.visited}"


def create_customers(data):
    customers = []

    for row in data:
        cust_no, x_coord, y_coord, demand, ready_time, due_date, service_time = map(float, row)
        customer = Customer(cust_no, x_coord, y_coord, demand, ready_time, due_date, service_time)
        customers.append(customer)

    return customers
