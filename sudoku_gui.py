import pygame
import time
from threading import *
import getPuzzle
pygame.init()
pygame.font.init()
img = pygame.image.load("plain.jpg")
img = pygame.transform.scale(img, (540, 540))


class Cube:
    def __init__(self, val, row, col, width, height):
        self.val = val
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.is_seleced = False

class Timer(Thread):
    """
    Timer class for the stopwatch running on screen. Runs as seperate thread.
    """

    def __init__(self,screen):
        Thread.__init__(self)
        self.time = "00:00"
        self.running = True
        self.screen = screen
        self.seconds = 0
        self.minutes = 0
        self.pause_drawing = False

    def run(self) -> None:
        """
        Runs the timer.
        :return: None
        """
        while self.running:
            self.seconds += 1
            if 60 > self.seconds > 9:
                str_seconds = str(self.seconds)
            elif self.seconds == 60:
                self.seconds = 0
                self.minutes += 1
                str_seconds = "00"
            else:
                str_seconds = "0{}".format(self.seconds)
            if 60 > self.minutes > 9:
                str_minutes = str(self.minutes)
            elif self.minutes == 60:
                self.minutes = 0
            else:
                str_minutes = "0{}".format(self.minutes)
            self.time = "{}:{}".format(str_minutes, str_seconds)
            time.sleep(1)

    def stop(self) -> None:
        """
        Stops the timer by changing the while loop condition in run().

        :return: None
        """
        self.running = False

    def reset(self) -> None:
        """
        Resets the time to 00:00.
        :return:
        """
        self.seconds = 0
        self.minutes = 0
        self.running = True

    def draw_time(self) -> None:
        """Draws the timer on the board.

        :return: None
        """

        time_fnt = pygame.font.SysFont("Comic Sans MS", 30)
        time_surf = time_fnt.render(
            "Time - {}".format(self.time), True, (0, 0, 0)
        )
        rect_width = time_surf.get_width()
        rect_hegiht =  time_surf.get_height()
        pygame.draw.rect(self.screen, (255, 255, 255), (pygame.display.get_surface().get_width() - rect_width,  pygame.display.get_surface().get_height() - rect_hegiht, rect_width, rect_hegiht), 0)
        self.screen.blit(
            time_surf,
            (
                pygame.display.get_surface().get_width() - 176,
                pygame.display.get_surface().get_height() - 43,
            ),
        )

    def draw_total_calc_time(self,start_time: str) -> None:
        """Calculates the "time" took the program to solve (include ןntentional delay)
            and draw it on the board.

        :param start_time: string, the time that the automatic solve was activated.
        :return: None
        """
        start_minutes,start_seconds = start_time.rsplit(':')
        end_seconds = self.seconds - int(start_seconds)
        if end_seconds < 10:
            end_seconds = str('0{}'.format(end_seconds))
        end_minutes = self.minutes - int(start_minutes)
        pygame.draw.rect(self.screen, (255, 255, 255), (170, 550, 360, 80), 0)
        time_fnt1 = pygame.font.SysFont("Comic Sans MS", 20,bold=True)
        time_surf1 = time_fnt1.render("Done! Took me 0{}:{} seconds.".format(end_minutes,end_seconds), True, (0, 0, 0))
        self.screen.blit(time_surf1,(210,575))
        time_surf2 = time_fnt1.render("Think you can do better?",True,(0,0,0))
        self.screen.blit(time_surf2,(215,598))
        time_surf3 = time_fnt1.render("Hit 'Restart'",True,(0,0,0))
        self.screen.blit(time_surf3,(245,620))


        pygame.display.update()

class Board:
    b = [
        [7, 8, 0, 4, 0, 0, 1, 2, 0],
        [6, 0, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 0, 6, 0, 1, 0, 7, 8],
        [0, 0, 7, 0, 4, 0, 2, 6, 0],
        [0, 0, 1, 0, 5, 0, 9, 3, 0],
        [9, 0, 4, 0, 6, 0, 0, 0, 5],
        [0, 7, 0, 3, 0, 0, 0, 1, 2],
        [1, 2, 0, 0, 0, 7, 4, 0, 0],
        [0, 4, 9, 2, 0, 6, 0, 0, 7],
    ]

    def __init__(self, rows, cols, width, height, screen):
        self.rows = rows
        self.cols = cols
        self.cubes = [
            [Cube(self.b[i][j], i, j, width, height) for j in range(cols)]
            for i in range(rows)
        ]
        self.width = width
        self.height = height
        self.selected = None
        self.screen = screen
        self.board = self.b
        self.start_board = [[self.board[i][j] for j in range(cols)] for i in range(rows)]
        self.running_status = None

    def draw_grid(self) -> None:
        """Draws the grid (clean sudoku board).

        :return: None
        """
        self.screen.blit(img, (0, 0))
        gap = self.width / 9
        for i in range(self.cols + 1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(
                self.screen, (0, 0, 0), (0, i * gap), (self.width, i * gap), thick
            )
            pygame.draw.line(
                self.screen, (0, 0, 0), (i * gap, 0), (i * gap, self.height), thick
            )

        # Fill grid with values
        fnt = pygame.font.SysFont("Comic Sans MS", 20)
        for i in range(self.rows):
            for j in range(self.cols):
                if self.board[i][j] == 0:
                    text_surface = fnt.render("", True, (0, 0, 0))
                else:
                    text_surface = fnt.render(str(self.board[i][j]), True, (0, 0, 0))
                self.screen.blit(
                    text_surface,
                    (
                        j * gap + (gap // 2 - text_surface.get_width() // 2),
                        i * gap + (gap // 2 - text_surface.get_height() // 2),
                    ),
                )

    def draw_buttons(self, restart_color=(200, 200, 0), check_color=(200, 200, 0),mix_color=(0, 200, 0)) -> None:
        """Draws all the buttons on the board.

        :param mix_color:
        :param restart_color: tuple, color of the button. changes if the cursor on it
        :param check_color: tuple, color of the button. changes if the cursor on it
        :return: None
        """
        restart_button = (30, 560, 100, 50)
        restart_fnt = pygame.font.SysFont("Comic Sans MS", 20)
        restart_surf = restart_fnt.render("Restart", True, (0, 0, 0))
        pygame.draw.rect(self.screen, restart_color, restart_button, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), restart_button, 2)

        check_button = (30, 620, 100, 50)
        check_fnt = pygame.font.SysFont("Comic Sans MS", 20)
        check_surf = check_fnt.render("Check", True, (0, 0, 0))
        pygame.draw.rect(self.screen, check_color, check_button, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), check_button, 2)

        mix_button = (135, 560, 50, 110)
        mix_fnt = pygame.font.SysFont("Comic Sans MS", 20)
        mix_surf = mix_fnt.render("Generate", True, (0,0,0))
        mix_surf = pygame.transform.rotate(mix_surf, 90)
        pygame.draw.rect(self.screen, mix_color, mix_button, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), mix_button, 2)



        self.screen.blit(
            restart_surf,
            (
                restart_button[0]
                + (restart_button[2] / 2 - restart_surf.get_width() // 2),
                restart_button[1]
                + (restart_button[3] / 2)
                - restart_surf.get_height() // 2,
            ),
        )
        self.screen.blit(
            check_surf,
            (
                check_button[0] + (check_button[2] / 2 - check_surf.get_width() // 2),
                check_button[1] + (check_button[3] / 2) - check_surf.get_height() // 2,
            ),
        )
        self.screen.blit(
            mix_surf,
            (
                mix_button[0]
                + (mix_button[2] / 2 - mix_surf.get_width() // 2),
                mix_button[1]
                + (mix_button[3] / 2)
                - mix_surf.get_height() // 2,
            ),
        )

    def draw_text(self) -> None:
        """Draws all the text elements.

        :return: None
        """
        text_pos = (200, 560)
        text_fnt = pygame.font.SysFont("Comic Sans MS", 20,bold=True)
        if self.running_status is None:
            text_surf = text_fnt.render("Press Space if you give up",True,(0,0,0))
            self.screen.blit(text_surf,text_pos)
        elif self.running_status:
            text_surf = text_fnt.render("Now wait untill I solve for you.",True,(0,0,0))
            self.screen.blit(text_surf,text_pos)
            text_surf = text_fnt.render("Im backtracking...",True,(0,0,0))
            self.screen.blit(text_surf,(text_pos[0],text_pos[1] + 23))

        pygame.display.update()

    def draw_change(self, num: int, row: int=None, col: int=None) -> None:
        """Draws the given number in the given row-col.

        :param num: int, number to change
        :param row: int, number of row
        :param col: int, number of col
        :return: None
        """
        if row is not None and col is not None:
            self.cubes[row][col].val = num
            self.redraw()
        else:
            for i in range(self.rows):
                for j in range(self.cols):
                    if self.cubes[i][j].is_seleced:
                            self.cubes[i][j].val = num
                            self.board[i][j] = num
                            self.update_board()
                            self.redraw()

    def redraw(self) -> None:
        """Redraws all the board elements.

        :return: None
        """
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_buttons()
        self.draw_text()

    def update_board(self) -> None:
        """Updates the cubes values from the board

        :return: None
        """
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].val == self.board[i][j]

    def generate_board(self):
        new_board = getPuzzle.try_get_puzzle(0)
        new_board = new_board.rsplit(' ')
        self.board = [[int(new_board[j+9*i]) for j in range(self.cols)] for i in range(self.rows)]
        self.start_board = [[int(new_board[j+9*i]) for j in range(self.cols)] for i in range(self.rows)]
        self.update_board()
        self.redraw()

    def if_mouse_on_button(self) -> None:
        """Check if the cursor is on one of the buttons, if so, chenges the color of the button.

        :return: None
        """
        pos = pygame.mouse.get_pos()

        light_yellow = (255, 255, 0)
        dark_yellow = (200, 200, 0)
        light_green = (0, 255, 0)
        dark_green = (0, 200, 0)

        #if mouse on restart button
        if 130 > pos[0] > 30 and 610 > pos[1] > 560:
            restart_color = light_yellow
        else:
            restart_color = dark_yellow

        #if mouse on check button
        if 130 > pos[0] > 30 and 670 > pos[1] > 620:
            check_color = light_yellow
        else:
            check_color = dark_yellow

        #if mouse on generate button
        if 185 > pos[0] > 135 and 670 > pos[1] > 560:
            mix_color = light_green
        else:
            mix_color = dark_green

        self.draw_buttons(restart_color, check_color,mix_color)

    def cell_clicked(self, pos: tuple) -> None:
        """Draws rectangle on the clicked square on board.

        :param pos: tuple, conatins x and y value on board
        :return: None
        """
        # Return the value of the previous selected cube to False
        if self.selected is not None:
            self.selected.is_seleced = False

        self.redraw()
        gap = self.width // 9
        x = (pos[0] // gap) * gap
        y = (pos[1] // gap) * gap

        # In Board, takes the place of the selected cube and mark the cube as selected
        self.selected = self.cubes[pos[1] // gap][pos[0] // gap]
        self.selected.is_seleced = True

        pygame.draw.rect(self.screen, (0, 255, 0), (x, y, gap, gap), 3)

    def delete(self) -> None:
        """Deletes number from board

        :return: None
        """
        self.selected.val = 0
        self.update_board()
        self.redraw()

    def checking(self) -> None:
        """Draws the text 'Checking' with effect of calculating.

        :return: None
        """
        text_fnt = pygame.font.SysFont("Comic Sans MS", 35)
        pygame.draw.rect(self.screen, (255, 255, 255), (190, 550, 350, 150), 0)
        for i in range(4):
            for j in range(1,5):
                text_surf = text_fnt.render("Checking" + "."*j,True,(0,0,0))
                pygame.draw.rect(self.screen, (255, 255, 255), (250,600,text_surf.get_width(), text_surf.get_height()), 0)
                self.screen.blit(text_surf,(250,590))
                pygame.time.delay(300)
                pygame.display.update()
            pygame.draw.rect(self.screen, (255, 255, 255), (396, 620, 35, 20), 0)
            pygame.display.update()

    def done_checking(self,is_valid: bool) -> None:
        """Draws the answer of the computer after hecking the board.

        :param is_valid: bool, points if the solution is valid or not
        :return: None
        """
        text_fnt1 = pygame.font.SysFont("Comic Sans MS", 25,bold=True)
        text_fnt2 = pygame.font.SysFont("Comic Sans MS", 25, bold=True)
        text_fnt3 = pygame.font.SysFont("Comic Sans MS", 25, bold=True)
        pygame.draw.rect(self.screen, (255, 255, 255), (170, 550, 350, 90), 0)
        if is_valid:
            text_surf1 = text_fnt1.render("Done. Correct answer!",True,(0,255,0))
            text_surf2 = text_fnt2.render("Press 'Restart'",True,(0,255,0))
            text_surf3 = text_fnt3.render("to play again",True,(0,255,0))

            pygame.draw.rect(self.screen, (255, 255, 255), (200, 590, text_surf1.get_width(), text_surf1.get_height()*2), 0)
            self.screen.blit(text_surf1, (210, 565))
            self.screen.blit(text_surf2, (240, 590))
            self.screen.blit(text_surf3,(250,615))
        else:
            text_surf1 = text_fnt1.render("Wrong answer. try again!",True,(255,0,0))
            pygame.draw.rect(self.screen, (255, 255, 255), (200, 600, text_surf1.get_width(), text_surf1.get_height()), 0)
            self.screen.blit(text_surf1, (200, 600))

    def check_solution(self) -> bool:
        self.checking()
        for i in range(self.rows):
            if sum(x for x in self.board[i]) != 45:
                return False
        for j in range(self.cols):
            if sum(self.board[i][j] for i in range(self.cols)) != 45:
                return False
        for i in range(0,9,3):
            for j in range(0,9,3):
                sum_grid = 0
                for k in range(i, i +3)  :
                    for m in range(j, j+3):
                        sum_grid += self.board[k][m]
                if sum_grid != 45:
                    return False

        return True

    def restart_board(self) -> None:
        """Sets the values of the board back the the initial values.

        :return: None
        """
        self.board = [
            [self.start_board[i][j] for j in range(self.cols)]
            for i in range(self.rows)
        ]

    def valid_placement(self, row: int, col: int, num: int) -> None:
        """Checks if the number is valid in the sudoku.

        :param row:int, the number of the row
        :param col:int, the number of the col
        :param num:int, the number that given tu put in the row,col
        :return: True or False
        """
        row_valid = all([num != self.board[row][j] for j in range(9)])
        if row_valid:
            col_valid = all([num != self.board[i][col] for i in range(9)])
            if col_valid:
                grid_col = int(col / 3) * 3
                grid_row = int(row / 3) * 3
                for i in range(self.rows):
                    if i % 3 == 0 and i != 0:
                        grid_row += 1
                        grid_col = int(col / 3) * 3
                    if self.board[grid_row][grid_col] == num:
                        return False
                    grid_col += 1
                return True
        return False

    def next_cell_to_fill(self, i: int) -> int:
        """Finds the next cell to fill with values - (empty one)

        :param i: int, the number of the row to start looking from
        :return: tuple, row,col where it finds the nect cell to fill
        """
        for x in range(i, 9):
            for y in range(0, 9):
                if self.board[x][y] == 0:
                    return x, y
        return -1, -1

    def generating(self):
        text_fnt = pygame.font.SysFont("Comic Sans MS", 35)
        pygame.draw.rect(self.screen, (255, 255, 255), (190, 550, 350, 150), 0)
        for i in range(2):
            for j in range(1,5):
                text_surf = text_fnt.render("Generating" + "."*j,True,(0,0,0))
                pygame.draw.rect(self.screen, (255, 255, 255), (250,600,text_surf.get_width(), text_surf.get_height()), 0)
                self.screen.blit(text_surf,(250,590))
                pygame.time.delay(300)
                pygame.display.update()
            pygame.draw.rect(self.screen, (255, 255, 255), (427, 620, 35, 20), 0)
            pygame.display.update()

    def solve_with_gui(self, row=0, col=0) -> bool:
        """Solves the puzzle recursively.

        :param row: int, number of the row to start looking from
        :param col: int, number of the col to start looking from
        :return: None
        """
        row, col = self.next_cell_to_fill(row)
        if row == -1:
            return True
        self.cubes[row][col].is_seleced = True
        for val in range(1, 10):
            if self.valid_placement(row, col, val):
                self.board[row][col] = val
                self.cubes[row][col].val = val
                self.draw_change(val, row, col)
                # pygame.time.delay(100)
                pygame.display.update()
                self.cubes[row][col].is_seleced = False
                if self.solve_with_gui(row, col):
                    return True
                self.cubes[row][col].val = 0
                self.board[row][col] = 0
        return False



def main():
    screen = pygame.display.set_mode((540, 700))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku")
    timer = Timer(screen)
    timer.start()
    game = Board(9, 9, 540, 540, screen)
    game.redraw()
    is_running = True

    while is_running:
        game.if_mouse_on_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                timer.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                if pos[0] > game.width or pos[1] > game.height:
                    pass
                else:
                    game.cell_clicked(pos)

                #if restart button clicked
                if 130 > pos[0] > 30 and 610 > pos[1] > 560:
                    game.running_status = None
                    game.restart_board()
                    timer.reset()
                    timer.pause_drawing = False
                    game.redraw()

                #if check button clicked
                if 130 > pos[0] > 30 and 670 > pos[1] > 620:
                    timer.pause_drawing = True
                    if game.check_solution():
                        game.done_checking(True)
                        timer.draw_time()
                    else:
                        game.done_checking(False)
                        timer.pause_drawing = False

                if 185 > pos[0] > 135 and 670 > pos[1] > 560:
                    game.generating()
                    game.generate_board()
                    timer.reset()
                    timer.pause_drawing = False

            if event.type == pygame.KEYDOWN:
                key = None
                if event.key == pygame.K_1:
                    key = 1
                elif event.key == pygame.K_2:
                    key = 2
                elif event.key == pygame.K_3:
                    key = 3
                elif event.key == pygame.K_4:
                    key = 4
                elif event.key == pygame.K_5:
                    key = 5
                elif event.key == pygame.K_6:
                    key = 6
                elif event.key == pygame.K_7:
                    key = 7
                elif event.key == pygame.K_8:
                    key = 8
                elif event.key == pygame.K_9:
                    key = 9
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    game.delete()
                elif event.key == pygame.K_SPACE:
                    start_calc_time = timer.time
                    game.running_status = True
                    game.restart_board()
                    game.solve_with_gui()
                    timer.draw_total_calc_time(start_calc_time)
                    timer.pause_drawing = True
                    game.running_status = False
                if key is not None:
                    game.draw_change(key)
        if timer.pause_drawing:
            pass
        else:
            timer.draw_time()
        pygame.display.update()


if __name__ == "__main__":
    main()
