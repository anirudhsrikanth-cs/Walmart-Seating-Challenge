# Movie Theatre Seating Challenge

### Question
Implement an algorithm for assigning seats within a movie theater to
fulfill reservation requests. Assume the movie theater has the seating
arrangement of 10 rows x 20 seats. For the purpose of public safety, assume that a buffer of three
seats and/or one row is required.

#### Input
An input file which would contain one line of input for each reservation request. The order of the lines in the file 
reflects the order in which the reservation requests were received. Each line in the file will be comprised of a 
reservation identifier, followed by a space, and then the number of seats requested. The reservation identifier will 
have the format: R####. Example: R001 2 R002 4 R003 4 R004 3

#### Output
The program should output a file containing the seating assignments for each request. Each row in the file should 
include the reservation number followed by a space, and then a comma-delimited list of the assigned seats. Example: 
R001 I1,I2 R002 F16,F17,F18,F19 R003 A1,A2,A3,A4 R004 J4,J5,J6

Please Note: The reservations that could not be accommodated in the theatre have 0 seats. 
Example: R005 No Seats Allocated represents the reservation cannot be fulfilled at this time.

#### Assumptions in the code

1) Cost of all the seats in the theatre are same.
2) Seats are reserved on the First come first serve basis.
3) Customers who reserve the seat first are offered better seats(seats that are far from the screen) 
than the customers who are reserve later.
4) After the theatre has few vacant seats the groups are split to adjust in the vacant seats.
5) Every booking wants to get the seats even if the seats allocated are in separate rows.
6) For customer safety, 3 buffer seats are allocated between every booking and only alternate rows
of the theatre are filled. Thus the number of total seats is half the maximum capacity. 

#### Instruction to Run the algorithm
1) In the directory of the project, make an inputFile.text which contains the reservation ID and the number of seats 
required
2) Open a terminal in the directory of the project
3) Run the command - ```python .\seat_booking.py .\inputFile.txt```
4) Open the output.txt file which is at the path displayed in the terminal output
5) Use the debug.log file to check for errors during the run


