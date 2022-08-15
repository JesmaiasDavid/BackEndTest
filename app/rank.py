import errno
import os
import logging

class Rank:
    """
    A class that represents the ranking of a league
    """

    def __init__(self, input_file_name, output_file_name):
        """
        Constructs the necessary attributes for the Rank object.
        :param input_file_name: str
        :param output_file_name: str
        """
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.teams = {}
        logging.basicConfig(filename='files/log.txt', filemode='w', level=logging.INFO, format='[%(asctime)s] [%(module)s]  [%('
                                                                          'levelname)s]  %(message)s')

    def read_data_from_input_file(self):
        """
        Reads the data from the input file and append it to a list.
        :return: all_games: [] -> list with all the games result
        """

        if self.input_file_name.split(".")[-1]:
            if self.input_file_name.split(".")[-1].lower() != 'txt':
                logging.error(RuntimeError("Input file extension has to be of type txt.").__str__())
                raise RuntimeError("Input file extension has to be of type txt.")

        file_path = os.path.join(os.getcwd(), "files", self.input_file_name)
        raw_data_list = None

        logging.info(f'About to read the data from \'{self.input_file_name}\' file.')
        try:
            with open(file_path, "r") as file_data:
                # splits the string for every new line (home team and away team data per line)
                raw_data_list = file_data.read().split("\n")
        except IOError as e:
            if e.errno == errno.EACCES:
                logging.error(PermissionError(errno.EACCES, os.strerror(errno.EACCES), file_path).__str__())
                raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), file_path)
            elif e.errno == errno.ENOENT:
                logging.error(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path).__str__())
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)

        logging.info(f'Data successfully read.')
        all_games = []
        for raw_data in raw_data_list:
            team_data = raw_data.split(", ")  # splits the string into a list of 2 (home team data and away team data)
            teams_to_compare = []
            for data in team_data:
                team_clean_data = data.rsplit(" ", 1)  # splits the team data into a list of 2(team name and team score)
                team = {team_clean_data[0]: int(team_clean_data[1])}
                teams_to_compare.append(team)
            all_games.append(teams_to_compare)

        return all_games

    def calculate_points_by_team(self):
        """
        calculates the sum of the points per team for all the games.
        :return: None
        """
        all_games = self.read_data_from_input_file()
        logging.info('About to calculate the points for each team')
        for data in all_games:

            home_team_score = list(data[0].values())[0]
            away_team_score = list(data[1].values())[0]
            home_team_name = list(data[0].keys())[0]
            away_team_name = list(data[1].keys())[0]

            logging.info(f'{home_team_name} vs {away_team_name} - {home_team_score} : {away_team_score}')
            if home_team_score > away_team_score:
                self.add_points_to_team(home_team_name, 3)
                self.add_points_to_team(away_team_name, 0)
            elif home_team_score < away_team_score:
                self.add_points_to_team(home_team_name, 0)
                self.add_points_to_team(away_team_name, 3)
            else:
                self.add_points_to_team(home_team_name, 1)
                self.add_points_to_team(away_team_name, 1)


    def add_points_to_team(self, team_name, team_points):
        """
        Adds points to a team based on the game result.
        :param team_name: str
        :param team_points: int
        :return: None
        """
        points = 'pts'
        if team_points == 1:
            points = 'pt'

        logging.info(f"{team_name}: {team_points} {points}")
        if team_name in self.teams:  # if the team already played a game
            previous_point = self.teams[team_name]  # old points
            current_point = team_points     # points for the current game
            sum_points = previous_point + current_point

            self.teams[team_name] = sum_points
        else:
            self.teams[team_name] = team_points

    def write_rank_data_to_output_file(self):
        """
        Writes to a file, the final ranking of the league starting from the team with most points to the least.
        :return: None
        """

        self.calculate_points_by_team()
        list_of_text_to_write = []
        position = 1
        next_position = 1
        previous_point = None

        rank_sorted = sorted(self.teams.items(), key=lambda x: x[1], reverse=True)  # sort by points
        for i in range(len(rank_sorted)):
            for j in range(len(rank_sorted) - i - 1):
                if rank_sorted[j][1] == rank_sorted[j + 1][1]: # checks if teams have the same ranking
                    if rank_sorted[j][0] > rank_sorted[j + 1][0]:
                        rank_sorted[j], rank_sorted[j + 1] = rank_sorted[j + 1], rank_sorted[j] # sorts alphabetically if teams have the same rank

        logging.info("Ranking the teams")
        for data in rank_sorted:
            team_point = data[1]
            team_name = data[0]

            points_txt = "pts"
            if team_point == 1:
                points_txt = "pt"

            if team_point == previous_point:
                text_to_write = f"{position}. {team_name}, {team_point} {points_txt}"
                list_of_text_to_write.append(text_to_write)
                logging.info(text_to_write)
                print(text_to_write)
                next_position += 1
            else:
                text_to_write = f"{next_position}. {team_name}, {team_point} {points_txt}"
                list_of_text_to_write.append(text_to_write)
                logging.info(text_to_write)
                print(text_to_write)
                position = next_position
                next_position += 1

            previous_point = team_point

        file_path = os.path.join(os.getcwd(), "files", self.output_file_name)

        if self.output_file_name.split(".")[-1]:
            if self.output_file_name.split(".")[-1].lower() != 'txt':
                logging.error(RuntimeError("Output file extension has to be of type txt.").__str__())
                raise RuntimeError("Output file extension has to be of type txt.")

        logging.info(f'About to write the ranking to the \'{self.output_file_name}\' file')
        try:
            with open(file_path, 'w') as f:
                for line in list_of_text_to_write:
                    f.write(line)
                    f.write('\n')
        except IOError as e:
            if e.errno == errno.EACCES:
                logging.error(PermissionError(errno.EACCES, os.strerror(errno.EACCES), file_path).__str__())
                raise PermissionError(errno.EACCES, os.strerror(errno.EACCES), file_path)
            elif e.errno == errno.ENOENT:
                logging.error(FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path).__str__())
                raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), file_path)
        logging.info(f'The data was successfully written.')