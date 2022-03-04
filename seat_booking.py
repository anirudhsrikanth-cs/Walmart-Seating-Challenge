import logging
import os
import sys

from inputFileParser import inputParser
from booking_class import BookingTheatre

logging.basicConfig(filename='debug.log', level=logging.DEBUG)


def seatBooking():
    """
        Takes the input file from the command line as input and returns the output as a path of the output.txt file
    """
    try:
        FilePath = sys.argv[1]
    except FileNotFoundError as err:
        print(err)
    data = inputParser(FilePath)
    Arrangement = BookingTheatre()
    not_inserted = []

    for eachReservation in data:  # allocating group seats in same row
        if Arrangement.seatsAvailable == 0:
            logging.info("Theatre is full no vacant seat available")
            break
        if not Arrangement.verify_seats(eachReservation[1], str(eachReservation[0])):
            not_inserted.append(eachReservation)
    more_inserted = []
    import pdb; pdb.set_trace()
    sorted_not_inserted_bookings = (sorted(not_inserted, key=lambda x: x[1]))

    for eachReservation in sorted_not_inserted_bookings:  # allocating remaining seats by splitting groups to utilize
        # theater
        if Arrangement.seatsAvailable == 0:
            break
        elif eachReservation[1] > Arrangement.seatsAvailable:
            continue
        else:
            more_inserted.append(eachReservation)
            Arrangement.split_insert(eachReservation[1], str(eachReservation[0]))

    output = Arrangement.get_output()
    Arrangement.writing_output(data, output)

    # printing the putput file path.....>
    outputFilePath = os.getcwd() + '/' + 'outfile.txt'
    print('{} {} {}\n'.format('\n', 'Output file location:', outputFilePath))
    logging.info("Check the terminal to fetch Output File path")


seatBooking()