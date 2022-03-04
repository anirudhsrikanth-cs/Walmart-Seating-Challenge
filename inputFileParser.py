import os


def inputParser(inpFile):
    """
    :param inpFile:
    :return: List with reservation ID and number of seats
    """
    if os.path.exists(inpFile):
        reservationList = []
        inputFile = open(inpFile, 'r')
        totalSeats = 100
        for line in inputFile:
            if totalSeats >= 0:
                line = line.split()
                reservationList.append([line[0], int(line[1])])
                totalSeats -= 1
            else:
                break
        return reservationList
    else:
        raise Exception("File Not Found Error")
