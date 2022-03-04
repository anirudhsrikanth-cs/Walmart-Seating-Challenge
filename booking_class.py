import logging
from row_nodes import NilNode, RowNode
from constants import SEATS

seats = SEATS
NIL_NODE = NilNode(seats)


class BookingTheatre:  # Linked List to find the correct row and seats
    def __init__(self):
        self.totalNodes = 10
        self.root = NIL_NODE
        self.lastinsert = None
        self.totalSeats = 20
        self.seatsAvailable = (self.totalNodes * self.totalSeats)/2
        self.output = {}

    def lookup(self, seatRequested):  # finding if any back row still vacant
        """
        :param seatRequested:
        Checks if any row exists in our theatre
        """
        if self.root != NIL_NODE:
            logging.debug("Root node already present")
            return self.__lookup(self.root, seatRequested)

    def __lookup(self, tnode, seatRequested):  # recursive function to look for seats with empty seats
        logging.debug(
            "Current Node is: {} and vacant seat are {} and seat requested are {}".format(tnode.name, tnode.seatsEmpty,
                                                                                          seatRequested))

        if tnode.seatsEmpty >= seatRequested:
            return tnode
        else:
            sub = tnode.subs[1]
            if sub is not None:
                logging.debug("Current Node is {} with vacant seats {}".format(tnode.name, tnode.seatsEmpty))
                logging.debug("Trying to find better match in other nodes.....")
                return self.__lookup(sub, seatRequested)
            else:
                logging.debug("No existing vacant node found, creating a new node.....!")
                return None

    def insert(self, seatRequested, reservationID, seats):
        """
        Inserts a new row into our linked list
        :param seatRequested:
        :param reservationID:
        :param seats:
        """
        if self.root != NIL_NODE:  # we are not an empty tree
            self.lastinsert = self.__insert_node(self.root, seatRequested, self.totalNodes, reservationID)
            self.delete(self.lastinsert)
        else:  # adding the first node to the List
            logging.info("Adding new root row to the List")
            name = chr(self.totalNodes + 64)
            self.root = RowNode(name, seats, seatRequested, reservationID, None)
            self.totalNodes -= 2
            self.lastinsert = self.root
            self.substract_seats(seatRequested, self.root)

    def __insert_node(self, currentNode, seatRequested, totalNodes, reservationID):
        if seatRequested <= currentNode.seatsEmpty:  # key exists, update value
            currentNode.seatsOccupied = currentNode.seats_reserved(seatRequested, reservationID)
            currentNode.seatsEmpty = currentNode.vacant_seat(seats)
            self.substract_seats(seatRequested, currentNode)
        elif seatRequested > currentNode.seatsEmpty:  # lookup to find best place to add new node
            if currentNode.subs[1]:
                return self.__insert_node(currentNode.subs[1], seatRequested, totalNodes, reservationID)
            elif currentNode.subs[1] is None and totalNodes > 0:  # adding a new node (row) to the linked list
                self.substract_seats(seatRequested, currentNode)
                name = chr(self.totalNodes + 64)
                currentNode.subs[1] = RowNode(name, seats, seatRequested, reservationID, currentNode)
                logging.info("Addign new row {} to the List".format(name))
                self.totalNodes -= 2
        return currentNode.subs[1]

    def verify_seats(self, seatRequested,
                     reservationID):  # checking if any back row with seats exists else call insert function
        """
        Checks if the seats can be allocated
        :param seatRequested:
        :param reservationID:
        :return:
        """
        logging.debug("Reservation ID: {} Seat Requested : {} ".format(reservationID, seatRequested))
        can_insert_continous_seats = False
        if seatRequested > 20:
            return can_insert_continous_seats
        tnode = self.lookup(seatRequested)
        if tnode is None and self.totalNodes > 0:
            self.insert(seatRequested, reservationID, seats)
            can_insert_continous_seats = True
        elif tnode is not None:
            logging.debug("No need to add a new node reservation can be accomodated in {}".format(tnode.name))
            self.substract_seats(seatRequested, tnode)
            tnode.seats_reserved(seatRequested, reservationID)
            self.output = tnode.get_output()
            tnode.seatsEmpty = tnode.vacant_seat(seats)
            parent = self.delete(tnode)
            can_insert_continous_seats = True
        elif self.totalNodes is 0:
            return can_insert_continous_seats

        return can_insert_continous_seats

    def substract_seats(self, seatsRequested, tnode):  # finding total seats available
        """
        Calculates the number of seats available in the theatre after every allocation
        :param seatsRequested:
        :param tnode:
        """
        self.seatsAvailable -= (seatsRequested + tnode.buffer)

    def split_insert(self, seatsRequested, reservationID):  # spliting the later bookings to utilise the theater
        """
        Handles inserting of non sequential seats
        :param seatsRequested:
        :param reservationID:
        """
        logging.info("splitting the booking")
        self.substract_seats(seatsRequested, self.root)
        currentNode = self.root
        while currentNode is not None and seatsRequested != 0:
            if currentNode.seatsEmpty <= seatsRequested:
                logging.debug('current node name:{} empty seats:{} current seat requested: {}'.format(currentNode.name,
                                                                                                      str(currentNode.seatsEmpty),
                                                                                                      str(seatsRequested)))
                currentNode.seats_reserved(currentNode.seatsEmpty, reservationID)
                self.output = currentNode.get_output()
                seatsRequested -= currentNode.seatsEmpty
                currentNode.seatsEmpty = currentNode.vacant_seat(seats)
                currentNode = currentNode.subs[1]
                if currentNode is not None:
                    self.delete(currentNode.parent)
            else:
                logging.debug('current node name {} empty seats:{} seats requested: {}'.format(currentNode.name,
                                                                                               str(currentNode.seatsEmpty),
                                                                                               str(seatsRequested)))
                currentNode.seats_reserved(seatsRequested, reservationID)
                self.output = currentNode.get_output()
                currentNode.seatsEmpty = currentNode.vacant_seat(seats)
                seatsRequested -= seatsRequested
                self.delete(currentNode)

    def delete(self, currentNode):  # deleting the nodes(row) from the list for efficient search
        """
        Deletes the row from the linkedlist once it becomes full
        :param currentNode:
        :return:
        """
        if currentNode.seatsEmpty == 0:
            logging.debug("deleted node {}".format(currentNode.name))
            if currentNode == self.root and currentNode.subs[1] is not None:
                currentNode.subs[1].parent = None
                self.root = currentNode.subs[1]
                return self.root
            elif currentNode != self.root:
                currentNode.parent.subs[1] = currentNode.subs[1]
                if currentNode.subs[1] != None:
                    currentNode.subs[1].parent = currentNode.parent
                    return currentNode.parent
            else:
                self.root = NIL_NODE
                return self.root

    def writing_output(self, data, output):  # writing the output to the file
        logging.info("Program Finished....Writing seats allocated to the file")
        outfile = open("outfile.txt", 'w+')
        for eachReservation in data:
            if eachReservation[0] in output:
                outfile.write('{} {}\n'.format(eachReservation[0], output[eachReservation[0]]))
            else:
                outfile.write('{} {}\n'.format(eachReservation[0], "No Seats Allocated"))

    def get_output(self):
        return self.output
