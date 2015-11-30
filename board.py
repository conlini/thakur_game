from enum import Enum
from random import choice, randint
import sys


class Inhabitant(Enum):
    THAKUR = "T",
    MAZDOOR = "M"


class Cell(object):
    def __init__(self, m, n, number):
        self.m = m
        self.n = n
        self.number = number
        self.next_cell = None
        self.current_occupant = None
        self.new_occupant = None

    def set_next_cell(self, next_cell):
        self.next_cell = next_cell

    def occupy(self, inhabitant):
        self.current_occupant = inhabitant

    def move(self):
        if self.current_occupant:
            if self.next_cell.current_occupant:
                if self.current_occupant == Inhabitant.MAZDOOR and \
                                self.next_cell.current_occupant == \
                                Inhabitant.THAKUR:
                    self.current_occupant = Inhabitant.THAKUR
                if self.current_occupant == Inhabitant.THAKUR and \
                                self.next_cell.current_occupant == \
                                Inhabitant.MAZDOOR:
                    self.current_occupant = None
                if self.current_occupant == self.next_cell.current_occupant \
                        and (self.current_occupant == Inhabitant.THAKUR or
                                     self.current_occupant == Inhabitant.MAZDOOR):
                    self.current_occupant = None
                    self.next_cell.current_occupant = None
            self.next_cell.new_occupant = self.current_occupant
            self.current_occupant = None

    def commit_move(self):
        self.current_occupant = self.new_occupant
        self.new_occupant = None

    def __repr__(self):
        if self.current_occupant:
            return self.current_occupant.value[0]
        else:
            return "_"
            # return "/".join((str(self.number), str(self.next_cell.number)))

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
                self.cells.append(Cell(i, j, i * m + j))
        self.assign_directions()
        self.populate_board(thakurs, mazdoors)

    def assign_directions(self):
        for i, cell in enumerate(self.cells):
            direction = choice(list(Board.Direction))
            cell_pos = self.__get_next_position(direction, i)
            cell.next_cell = self.cells[cell_pos]

    def __get_next_position(self, direction, i):
        if direction is Board.Direction.NORTH:
            if (i + self.n) >= (m * n):
                cell_pos = (i + self.n) - m * n
            else:
                cell_pos = i + self.n
        elif direction is Board.Direction.SOUTH:
            if (i - self.n) < 0:
                cell_pos = (i - self.n) + m * n
            else:
                cell_pos = i - self.n
        elif direction is Board.Direction.EAST:
            cell_pos = i - 1
            if cell_pos < 0:
                cell_pos = cell_pos + self.n
        else:
            cell_pos = i + 1
            if cell_pos >= m * n:
                cell_pos = cell_pos - self.n
        return cell_pos

    def __check_rules(self, possible_pos, inhabitant, isMove=False):
        neighbour_cells = {}
        for dir in list(Board.Direction):
            nieghbour = self.__get_next_position(dir, possible_pos)
            neighbour_cells[dir] = nieghbour

        for dir, cell in neighbour_cells.items():
            neigbouring_occupant = self.cells[nieghbour].current_occupant
            if neigbouring_occupant:
                if neigbouring_occupant == Inhabitant.THAKUR and inhabitant == Inhabitant.THAKUR:
                    return False
        if inhabitant == Inhabitant.MAZDOOR:
            north = self.cells[
                neighbour_cells[Board.Direction.NORTH]].current_occupant
            south = self.cells[
                neighbour_cells[Board.Direction.SOUTH]].current_occupant
            east = self.cells[
                neighbour_cells[Board.Direction.EAST]].current_occupant
            west = self.cells[
                neighbour_cells[Board.Direction.WEST]].current_occupant
            if (
                                north and south and north == south and north == Inhabitant.THAKUR) or (
                                east and west and east == west and east == Inhabitant.THAKUR):
                return False
            if isMove:
                if (north and north == Inhabitant.MAZDOOR) or\
                    (south and south == Inhabitant.MAZDOOR) or\
                        (east and east ==Inhabitant.MAZDOOR) or\
                        (west and west == Inhabitant.MAZDOOR):
                            if not north:
                                neighbour_cells[Board.Direction.NORTH].occupy(Inhabitant.MAZDOOR)
                            elif not south:
                                neighbour_cells[Board.Direction.SOUTH].occupy(Inhabitant.MAZDOOR)
                            elif not east:
                                neighbour_cells[Board.Direction.EAST].occupy(Inhabitant.MAZDOOR)
                            else:
                                neighbour_cells[Board.Direction.WEST].occupy(Inhabitant.MAZDOOR)

        return True

    def populate_board(self, thakurs, mazdoors):
        for i in range(thakurs):
            possible_pos = randint(0, m * n)
            while (self.cells[
                       possible_pos].current_occupant is not None and self.__check_rules(
                possible_pos, Inhabitant.THAKUR)):
                possible_pos = randint(0, m * n)
            self.cells[possible_pos].occupy(Inhabitant.THAKUR)
        for i in range(mazdoors):
            possible_pos = randint(0, (m * n) - 1)
            while (self.cells[
                       possible_pos].current_occupant is not None and self.__check_rules(
                possible_pos, Inhabitant.MAZDOOR)):
                possible_pos = randint(0, m * n)
            self.cells[possible_pos].occupy(Inhabitant.MAZDOOR)

    def move(self):
        for i, cell in enumerate(self.cells):
            cell.move()
            cell.commit_move()
        has_occupant = False
        for cell in self.cells:
            if cell.current_occupant:
                has_occupant = True
                if not self.__check_rules(i, cell.current_occupant):
                    return False


        return has_occupant

    def __repr__(self):
        answer = ""
        for i, cell in enumerate(self.cells):
            if i > 0 and (i % self.n) == 0:
                answer += "\n"
            answer += str(self.cells[i]) + "  "
        return answer

    def __str__(self):
        return self.__repr__()


if __name__ == "__main__":
    if len(sys.argv) == 5:
        m, n, thakurs, mazdoors = sys.argv[1:]
    else:
        m, n = [int(a) for a in input(
            "Enter m, n:").strip().split(",")]
        thakurs = int(.05 * m * n)
        mazdoors = int(.2 * m * n)
    board = Board(m, n, thakurs, mazdoors)
    print(board)
    # for i in range(iterations):
    #     board.move()
    #     print("================== ITERATION {} ==================".format(
    #         iterations))
    #     print(board)
    living = True
    iterations = 0
    while (living):
        living = board.move()
        iterations += 1
        if iterations % 20 == 0:
            board.assign_directions()
        print("================== ITERATION {} ==================".format(
            iterations))
        print(board)
    print("Gamed ended with {} iterations".format(iterations))
