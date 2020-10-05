import requests
from bs4 import BeautifulSoup
from time import sleep
import parameters

params = parameters.params


def get_sudoku_board(p_link: str) -> str:
    """
        Returns a random Sudoku puzzle and solution, given puzzle link and solution

    :param p_link: string, The link of the website to download the puzzle from
    :return:String represents the number in each cell
    """
    req = requests.get(p_link)
    c = req.content
    soup = BeautifulSoup(c, 'html.parser')
    rows = soup.find_all('tr', {'class':'grid'})
    puzzle = []
    for row in rows:
        cols = row.find_all('td')
        for col in cols:
            txt = col.text
            if txt != '\xa0':
                puzzle.append(txt)
            else:
                puzzle.append('0')
    puzzle = ' '.join(puzzle)
    return puzzle

def try_get_puzzle(retries: int) -> str:
    """
        Trys to download the puzzles from the websites.

    :param retries:
    :return: None if fails to download over 20 times, the puzzle if succeed
    """
    # global curr_params
    size = 3
    no_puzzles = 1
    curr_params = params[size]
    no_puzzles = min(curr_params['max'], no_puzzles)

    if retries > 20:
        return
    try:
        i = 0
        while i <= no_puzzles:
            puzzle = get_sudoku_board(curr_params['puzzle'])
            i += 1
    except Exception as e:
        print(e)
        sleep(2)
        retries += 1
        try_get_puzzle(retries)
    return puzzle