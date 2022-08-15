# League Ranking

## Description
This a command-line application that calculates the ranking table for a league. It gets the data from an input file in a 
specific format, calculates the ranking and writes the data to an output file. The ranking is in ascending order
where the 1st is the team with the most points and the last team is the one with the least points. If two or more teams
have the same number of points, they will have the same rank and will be ordered alphabetically.

## Setup
This application requires python 3.9.
You must have a **files** folder in the root directory, and the folder must contain at least one file that will be used
as the **input file**.

### Install
Install the necessary packages by running the command:

**pip install -r requirements.txt**.

##  How To Run
To run this code you have to use the following command:

**python main.py rank**

This command will use the **input file.txt** as the input file and will create the **output file.txt** file which will 
contain the league ranking.
**input file.txt** and **output file.txt** are the default names for the files, but you can use the **optional parameters** to 
pass any name.

### Optional Parameters
`-o , --output` : name of the output file [must be used with the positional parameter **rank**]

`-i, --input` : name for the input file [must be used with the positional parameter **rank**]

`-h, --help` : shows the help message

`-v, --version` : shows the version of the application

#### Example of commands:
**python main.py rank --output myoutput.txt --input myinput.txt**

**python main.py -h**

### Testing

To test you can run the one of the following commands:

**pytest test** -> runs the tests inside the **test/** directory

**pytest test/test_rank.py** -> runs the specific that contains the tests
