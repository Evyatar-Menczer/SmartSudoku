import pygame
import time
from threading import *
import sys

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

    def __init__(self, rows, cols, width, height, screen, timer):
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
        self.start_board = [[self.b[i][j] for j in range(cols)] for i in range(rows)]
        self.timer = timer
        self.status = None

    def draw_grid(self) -> None:
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

    def draw_buttons(self, restart_color: tuple=(200, 200, 0), check_color: tuple=(200, 200, 0)) -> None:
        restart_button = (60, 560, 100, 50)
        restart_fnt = pygame.font.SysFont("Comic Sans MS", 20)
        pygame.draw.rect(self.screen, restart_color, restart_button, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), restart_button, 2)
        restart_surf = restart_fnt.render("Restart", True, (0, 0, 0))

        check_button = (60, 620, 100, 50)
        check_fnt = pygame.font.SysFont("Comic Sans MS", 20)

        pygame.draw.rect(self.screen, check_color, check_button, 0)
        pygame.draw.rect(self.screen, (0, 0, 0), check_button, 2)
        check_surf = check_fnt.render("Check", True, (0, 0, 0))

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

    def draw_time(self) -> None:
        time_fnt = pygame.font.SysFont("Comic Sans MS", 30)
        time_surf = time_fnt.render(
            "Time - {}".format(self.timer.time), True, (0, 0, 0)
        )
        self.screen.blit(
            time_surf,
            (
                pygame.display.get_surface().get_width() - time_surf.get_width(),
                pygame.display.get_surface().get_height() - time_surf.get_height(),
            ),
        )

    def draw_text(self):
        text_pos = (200, 560)
        text_fnt = pygame.font.SysFont("Comic Sans MS", 20)
        if self.status is None:
            text_surf = text_fnt.render("Press Space if you give up",True,(0,0,0))
            self.screen.blit(text_surf,text_pos)
        elif self.status:
            text_surf = text_fnt.render("Now wait untill I solve for you...",True,(0,0,0))
            self.screen.blit(text_surf,text_pos)
        else:
            text_surf = text_fnt.render("Done! Press 'Restart' to try again", True, (0, 0, 0))
            self.screen.blit(text_surf, text_pos)
        pygame.display.update()

    def draw_change(self, num: int, row: int=None, col: int=None) -> None:

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
                            self.cubes[i][j].is_seleced = False
                            self.redraw()

    def redraw(self) -> None:
        self.screen.fill((255, 255, 255))
        self.draw_grid()
        self.draw_buttons()
        self.draw_time()
        self.draw_text()

    def update_board(self) -> None:
        for i in range(self.rows):
            for j in range(self.cols):
                self.cubes[i][j].val == self.board[i][j]

    def if_mouse_on_button(self) -> None:
        pos = pygame.mouse.get_pos()

        light_yellow = (255, 255, 0)
        dark_yellow = (200, 200, 0)
        if 160 > pos[0] > 60 and 610 > pos[1] > 560:
            restart_color = light_yellow
        else:
            restart_color = dark_yellow

        if 160 > pos[0] > 60 and 670 > pos[1] > 620:
            check_color = light_yellow
        else:
            check_color = dark_yellow
        self.draw_buttons(restart_color, check_color)

    def clicked(self, pos: tuple) -> None:
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
        self.selected.val = 0
        self.update_board()
        self.redraw()

    def check_solution(self) -> bool:
        for i in range(self.rows):
            if sum(x for x in self.board[i]) != 45:
                return False
        for j in range(self.cols):
            if sum(self.board[i][j] for i in range(self.cols)) != 45:
                return False

    def valid_placement(self, row: int, col: int, num: int) -> None:
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
        for x in range(i, 9):
            for y in range(0, 9):
                if self.board[x][y] == 0:
                    return x, y
        return -1, -1
    def solve_with_gui(self, row=0, col=0) -> bool:
        ""
        row, col = self.next_cell_to_fill(row)
        if row == -1:
            return True
        self.cubes[row][col].is_seleced = True
        for val in range(1, 10):
            if self.valid_placement(row, col, val):
                self.board[row][col] = val
                self.cubes[row][col].val = val
                self.draw_change(val, row, col)
                pygame.time.delay(100)
                pygame.display.update()
                if self.solve_with_gui(row, col):
                    return True
                self.cubes[row][col].is_seleced = False
                self.cubes[row][col].val = 0
                self.board[row][col] = 0
        return False


class Timer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.time = "00:00"
        self.running = True

    def run(self):
        seconds = 0
        str_seconds = "00"
        minutes = 0
        str_minutes = "00"
        while self.running:
            seconds += 1
            if 60 > seconds > 9:
                str_seconds = str(seconds)
            elif seconds == 60:
                seconds = 0
                minutes += 1
                str_seconds = "00"
            else:
                str_seconds = "0{}".format(seconds)
            if 60 > minutes > 9:
                str_minutes = str(minutes)
            elif minutes == 60:
                minutes = 0
            else:
                str_minutes = "0{}".format(minutes)
            self.time = "{}:{}".format(str_minutes, str_seconds)
            time.sleep(1)

    def exit(self):
        self.running = False

def main():
    screen = pygame.display.set_mode((540, 700))
    screen.fill((255, 255, 255))
    pygame.display.set_caption("Sudoku")
    timer = Timer()
    timer.start()

    board = Board(9, 9, 540, 540, screen, timer)
    board.redraw()
    is_running = True

    while is_running:
        board.if_mouse_on_button()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
                timer.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                print(pos)
                if pos[0] > board.width or pos[1] > board.height:
                    pass
                else:
                    board.clicked(pos)

                #restart button
                if 160 > pos[0] > 60 and 610 > pos[1] > 560:
                    board.status = None

                    board.board = [
                        [board.start_board[i][j] for j in range(board.cols)]
                        for i in range(board.rows)
                    ]
                    board.redraw()
                #check button
                if 160 > pos[0] > 60 and 670 > pos[1] > 620:
                    pass
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
                    board.delete()
                elif event.key == pygame.K_SPACE:
                    board.status = True
                    board.solve_with_gui()
                    board.status = False
                    board.redraw()
                if key is not None:
                    board.draw_change(key)
        pygame.display.update()


if __name__ == "__main__":
    main()
