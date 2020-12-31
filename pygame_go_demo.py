# coding: utf8

import pygame
from pygame.locals import *
from enum import IntEnum

from test_pyq.common.color import Color

class PieceState(IntEnum):
    NULL = 0
    BLACK = 1
    WHITE = 2

class GameGui:

    def __init__(self, col_count: int = 19, col_size: int = 30):
        pygame.init()
        self.window_size = (col_count * col_size + 150, col_count * col_size + 50)
        self.col_size = col_size
        self.col_count = col_count
        self.piece_size = int(col_size * 0.45)
        self.screen = pygame.display.set_mode(self.window_size)
        # 星位
        self.star_index = [3, self.col_count - 4] if col_count > 12 else ([2, self.col_count - 3] if col_count > 7 else [])
        if self.col_count % 2 == 1:
            self.star_index.append(self.col_count // 2)

        self.game_state = PieceState.NULL

    def base_window(self):
        self._draw_go_board()
        pygame.display.update()

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    exit(0)
                if event.type == MOUSEBUTTONUP:
                    x,y = pygame.mouse.get_pos()
                    x,y = self._convert_position(x, y)
                    if x != -1:
                        self.game_state = PieceState.WHITE if self.game_state == PieceState.BLACK else PieceState.BLACK
                        self.draw_go_piece(x, y, self.game_state)
                pygame.display.update()

    def _draw_go_board(self):
        self.screen.fill(Color.white)
        self.screen.fill(Color.cyan, (30, 30, self.col_count * self.col_size, self.col_count * self.col_size))
        # draw go board line
        for i in range(self.col_count):
            x1, y1 = self._position_convert(i, 0)
            x2, y2 = self._position_convert(i, self.col_count-1)

            pygame.draw.line(self.screen, Color.black, (x1, y1), (x2, y2))
            pygame.draw.line(self.screen, Color.black, (y1, x1), (y2, x2))

        index_list = self.star_index
        for x,y in [(x, y) for x in index_list for y in index_list]:
            x1, y1 = self._position_convert(x, y)
            pygame.draw.circle(self.screen, Color.black, (x1, y1), self.col_size / 5)

    def draw_go_piece(self, x:int, y:int, piece_color):
        x1, y1 = self._position_convert(x, y)
        color = Color.black if piece_color == PieceState.BLACK else Color.white
        pygame.draw.circle(self.screen, color, (x1, y1), self.piece_size)

    def _draw_remove_piece(self, x:int, y:int):
        x1, y1 = self._position_convert(x, y)
        color = Color.cyan
        pygame.draw.circle(self.screen, color, (x1, y1), self.piece_size)
        # draw +
        x2, y2 = self._position_convert(x-1, y)
        x3, y3 = self._position_convert(x+1, y)
        pygame.draw.line(self.screen, Color.black, (x2, y2), (x3, y3))

        x2, y2 = self._position_convert(x, y-1)
        x3, y3 = self._position_convert(x, y+1)
        pygame.draw.line(self.screen, Color.black, (x2, y2), (x3, y3))

        if x in self.star_index and y in self.star_index:
            pygame.draw.circle(self.screen, Color.black, (x1, y1), self.col_size / 5)

    def _position_convert(self, x: int, y: int):
        x1 = 0 if x < 0 else (x if x < self.col_count else self.col_count - 1)
        y1 = 0 if y < 0 else (y if y < self.col_count else self.col_count - 1)
        return (self.col_size / 2 + 30 + x1 * self.col_size, self.col_size / 2 + 30 + y1 * self.col_size)

    def _convert_position(self, x: float, y:float):
        if not 30 < x < self.col_count * self.col_size + 30:
            return (-1, -1)
        if not 30 < y < self.col_count * self.col_size + 30:
            return (-1, -1)
        return int((x-30)/self.col_size), int((y-30)/self.col_size)


if __name__ == '__main__':
    game_gui = GameGui(col_count=12, col_size=30)
    game_gui.base_window()
    game_gui.start()
