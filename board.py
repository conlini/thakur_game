from enum import Enum
from random import choice, randint
import sys


class Inhabitant(Enum):
    THAKUR = "T",
    MAZDOOR = "M"


class Cell(object):
    def __init__(self, m, n):
        self.m = m
        self.n = n
        self.next_cell = None
        self.current_occupant = None
        self.new_occupant = None

    def set_next_cell(self, next_cell):
        self.next_cell = next_cell

    def occupy(self, inhabitant):
        self.current_occupant = inhabitant

    def move(self):
        self.next_cell.new_occupant = self.current_occupant
        print("moved from {} x {} to {} x {}".format(self.m, self.n , self.next_cell.m, self.next_cell.n))
        self.current_occupant = None

    def commit_move(self):
        self.current_occupant = self.new_occupant
        self.new_occupant = None

    def __repr__(self):
        if self.current_occupant:
            return self.current_occupant.value[0]
        else:
            return "_"

    def __str__(self):
        return self.__repr__()

class Board(object):
    class Direction(Enum):
        NORTH = (0, 1),
        SOUTH = (0, -1),
        EAST = (-1, 0),
        WEST = (1, 0)

    def __init__(self, m, n, thakurs, mazdoors):
        if m * n < 40:
            raise Exception("board basic criteria not met")
        self.n = n
        self.m = m
        self.cells = []
        for i in range(m):
            for j in range(n):
                self.cells.append(Cell(i, j))
        self.assign_directions()
        self.populate_board(thakurs, mazdoors)

    def assign_directions(self):
        for i, cell in enumerate(self.cells):
            direction = choice(list(Board.Direction))
            if direction is Board.Direction.NORTH:
                if (i + self.n) >= (m*n):
                    cell_pos = (i + self.n) - m*n
                else:
                    cell_pos = i + self.n
                cell.next_cell = self.cells[cell_pos]
            elif direction is Board.Direction.SOUTH:
                if (i - self.n) < 0:
                    cell_pos = (i - self.n) + m*n
                else:
                    cell_pos = i - self.n
                cell.next_cell = self.cells[cell_pos]
            elif direction is Board.Direction.EAST:
                cell_pos = i-1
                if cell_pos < 0:
                    cell_pos = cell_pos + self.n
                cell.next_cell = self.cells[cell_pos]
            else:
                cell_pos = i+ 1
                if cell_pos >= m*n:
                    cell_pos = cell_pos - self.n
                cell.next_cell = self.cells[cell_pos]

    def __check_rules(self):
        pass

    def populate_board(self, thakurs, mazdoors):
        for i in range(thakurs):
            possible_pos = randint(0, m * n)
            while (self.cells[possible_pos].current_occupant is not None):
                possible_pos = randint(0, m * n)
            self.cells[possible_pos].occupy(Inhabitant.THAKUR)
        for i in range(mazdoors):
            possible_pos = randint(0, (m * n)-1)
            while (self.cells[possible_pos].current_occupant is not None):
                possible_pos = randint(0, m * n)
            self.cells[possible_pos].occupy(Inhabitant.MAZDOOR)

    def move(self):
        for cell in self.cells:
            cell.move()
            cell.commit_move()
        return True

    def __repr__(self):
        answer = ""
        for i,cell in enumerate(self.cells):
            answer += str(self.cells[i])
            if (i % self.n) ==0:
                answer += "\n"
        return answer

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    if len(sys.argv) == 5:
        m, n, thakurs, mazdoors = sys.argv[1:]
    else:
        m, n, thakurs, mazdoors = [int(a) for a in input("Enter m, n, thakurs, mazdoors:").strip().split(",")]
    board = Board(m, n, thakurs, mazdoors)
    board.move()
    print(board)
    # living = True
    # iterations = 0
    # while (living):
    #     living = board.move()
    #     iterations += 1
    #     if iterations % 20 == 0:
    #         board.assign_directions()
    #     print("================== ITERATION {} ==================".format(iterations))
    #     print(board)
    # print("Gamed ended with {} iterations".format(iterations))
