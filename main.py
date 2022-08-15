from app.rank import Rank
import argparse


def main():
    # Create the parser
    my_parser = argparse.ArgumentParser(prog='Ranking',
                                        description='Ranks the table for a league',
                                        epilog='Enjoy the program! :)')

    # Add the arguments
    my_parser.add_argument('Rank', metavar='rank', help='ranks the table')
    my_parser.add_argument('-v', '--version',
                           action='version',
                           help='the version of the program',
                           version='%(prog)s 1.0')
    my_parser.add_argument('-o', '--output',
                           help='name of the file to write to ',
                           required=False)
    my_parser.add_argument('-i', '--input',
                           help='name of the file to read from',
                           required=False)

    # Execute the parse_args() method
    args = my_parser.parse_args()

    output_file = 'output file.txt'
    input_file = 'input file.txt'

    if args.output is not None:
        output_file = f'{args.output}'

    if args.input is not None:
        input_file = f'{args.input}'

    rank = Rank(input_file, output_file)
    rank.write_rank_data_to_output_file()


if __name__ == '__main__':
    main()
