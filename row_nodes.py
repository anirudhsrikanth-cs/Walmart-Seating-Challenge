from constants import SEATS

output = {}
seats = SEATS


class NilNode:  # Nil Node
    """
        Class for the first row to be inserted into our list
    """
    def __init__(self, seats):
        self.level = 0
        self.name = None
        self.seatsPresent = [0 * seats]
        self.seatsEmpty = None
        self.subs = [None, None]
        self.seatsOccupied = [0 for i in range(seats)]
        self.parent = None


class RowNode:  # Creates New Node
    """
        Class defines every row in the movie theatre
    """
    def __init__(self, name, seats, seatRequested, reservationID, currentNode):
        self.isFull = False
        self.name = name
        self.totalSeats = 20
        self.subs = [None, None]
        self.seatsOccupied = [0 for i in range(seats)]
        self.buffer = 0
        self.seats_reserved(seatRequested, reservationID)
        self.seatsEmpty = self.vacant_seat(seats)
        self.parent = currentNode
        self.output = output

    def vacant_seat(self, seats):  # estimating number of vacant seats
        """
        :param seats:
        :return: count of seats
        """
        count = 0
        for i in range(seats):
            if self.seatsOccupied[i] == 0:
                count += 1
        return count

    def seats_reserved(self, seatRequested, reservationID):  # adding the reservation ID to the reserved seats
        """
        :param seatRequested:
        :param reservationID:
        :return: number of seats occupied
        """

        global buffer_count
        seats_assigned = []
        for i in range(len(self.seatsOccupied)):
            if seatRequested != 0:
                if self.seatsOccupied[i] == 0:
                    self.seatsOccupied[i] = reservationID
                    seatRequested -= 1
                    seats_assigned.append(self.name + str(i + 1))
            else:
                if i+2 < seats:
                    self.seatsOccupied[i], self.seatsOccupied[i+1], self.seatsOccupied[i+2] = -1, -1, -1
                    buffer_count = 3
                    break
                else:
                    buffer_count = 0
                    while i < seats:
                        self.seatsOccupied[i] = -1
                        i += 1
                        buffer_count += 1
                    break

        self.buffer = buffer_count

        if reservationID not in output:
            output[reservationID] = ",".join(seats_assigned)
        else:
            output[reservationID] += "," + ",".join(seats_assigned)
        return self.seatsOccupied

    def get_output(self):
        """
        :return: output
        """
        return self.output

