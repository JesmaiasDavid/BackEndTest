import pytest
import os
from app.rank import Rank


def current_working_directory():
    """Sets cwd to the root directory"""
    os.chdir("..")


@pytest.fixture
def rank_with_valid_input_file():
    """ Returns a Rank instance with valid input file name"""
    return Rank("input file.txt", "")


@pytest.fixture
def rank_with_invalid_input_file():
    """ Returns a Rank instance with invalid input file name"""
    return Rank("invalid input file.txt", "")


@pytest.fixture
def rank_with_valid_output_file():
    """ Returns a Rank instance with valid output file name"""
    return Rank("input file.txt", "vvvv ")


@pytest.fixture
def rank_with_invalid_output_file():
    """ Returns a Rank instance with invalid output file name"""
    return Rank("input file.txt", "invalid output file.zds")


def test_read_data_from_input_file_success(rank_with_valid_input_file):
    """Test that reading data from a valid file name in the files folder is successful"""
    current_working_directory()
    rank = rank_with_valid_input_file
    input_file = rank.input_file_name

    file_path = os.path.join(os.getcwd(), "files", input_file)
    file_exists = os.path.exists(file_path)

    assert file_exists == True
    assert len(rank.read_data_from_input_file()) > 0


def test_read_data_from_input_file_not_in_files_folder(rank_with_invalid_input_file):
    """Test that reading data from a file not in the files folder fails"""
    current_working_directory()
    rank = rank_with_invalid_input_file
    input_file = rank.input_file_name

    file_path = os.path.join(os.getcwd(), "files", input_file)
    file_exists = os.path.exists(file_path)

    assert file_exists == False
    with pytest.raises(FileNotFoundError):
        assert rank.read_data_from_input_file()


def test_write_data_to_output_file_success(rank_with_valid_output_file):
    """Test that writing data to a valid file is successful"""
    current_working_directory()
    rank = rank_with_valid_output_file
    output_file = rank.output_file_name

    rank.write_rank_data_to_output_file()
    file_path = os.path.join(os.getcwd(), "files", output_file)
    file_exists = os.path.exists(file_path)

    assert file_exists == True


def test_write_data_to_output_file_with_wrong_extension(rank_with_invalid_output_file):
    """Test that reading data from a invalid file name is unsuccessful"""
    current_working_directory()
    rank = rank_with_invalid_output_file
    output_file = rank.output_file_name

    file_path = os.path.join(os.getcwd(), "files", output_file)
    print(file_path)
    file_exists = os.path.exists(file_path)
    assert file_exists == False
    with pytest.raises(RuntimeError):
        assert rank.write_rank_data_to_output_file()

def test_add_points_to_a_team():
    """Test that points are added to a specific team"""
    rank = Rank("input file.txt", "output file.txt")
    rank.add_points_to_team("Lions", 2)
    rank.add_points_to_team("Snakes", 5)
    rank.add_points_to_team("Lions", 3)

    assert rank.teams["Lions"]==5
    assert rank.teams["Snakes"]==5

