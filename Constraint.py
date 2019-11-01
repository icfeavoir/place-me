class Constraint:
    def __init__(self, name):
        self.name = name
        self.concerned_seats = []

    def add_seat(self, line, cell):
        self.concerned_seats.append([line, cell])

    def set_concerned_seats(self, seats):
        self.concerned_seats = seats

    def is_allowed(self, line, cell):
        for seat in self.concerned_seats:
            if seat[0] == line and seat[1] == cell:
                return True

        return False
