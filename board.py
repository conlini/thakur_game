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
        self.new_occupant = []

    def set_next_cell(self, next_cell):
        self.next_cell = next_cell

    def occupy(self, inhabitant):
        '''
        initial occupation
        :param inhabitant:
        :return:
        '''
        self.current_occupant = inhabitant

    def stage(self, new_occupant):
        '''
        stage the next set of folks interested in moving to this cell
        :param new_occupant:
        :return:
        '''
        self.new_occupant.append(new_occupant)

    def move(self):
        '''
        Moves this cells occupants to the next cell
        :return:
        '''
        if self.current_occupant:
            self.next_cell.stage(self.current_occupant)
            # self.current_occupant = None

    def commit_move(self):
        '''
        finalize the move of this iteration
        :return:
        '''
        if self.new_occupant:
            self.current_occupant = self.new_occupant[0]
        self.new_occupant.clear()

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
        '''
        assigna one random direction to each cell for its next cell
        :return:
        '''
        for i, cell in enumerate(self.cells):
            direction = choice(list(Board.Direction))
            cell_pos = self.__get_next_position(direction, i)
            cell.next_cell = self.cells[cell_pos]

    def __get_next_position(self, direction, i):
        '''
        Given a cell and direction, defines the 4 possible locaton that its is surrounded by
        :param direction:
        :param i:
        :return:
        '''
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
            if (i) % n == 0:
                cell_pos = i + n -1
            if cell_pos < 0:
                cell_pos = cell_pos + self.n
        else:
            cell_pos = i + 1
            if(i + 1) % n == 0:
                cell_pos = i - n + 1
            if cell_pos >= m * n:
                cell_pos = cell_pos - self.n
        return cell_pos

    def __check_rules(self, possible_pos, inhabitant, isMove=False):
        neighbour_cells = {}
        for dir in list(Board.Direction):
            nieghbour = self.__get_next_position(dir, possible_pos)
            neighbour_cells[dir] = nieghbour
        # print(possible_pos, neighbour_cells)

        for dir, cell in neighbour_cells.items():
            neigbouring_occupant = self.cells[cell].current_occupant
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
                print(
                    "Ending world as 2 Thakurs sperated by Mazdoor at {}".format(
                        possible_pos))
                return False
        return True

    def __check_first_placement(self, possible_pos, inhabitant):
        neighbour_cells = {}
        for dir in list(Board.Direction):
            nieghbour = self.__get_next_position(dir, possible_pos)
            neighbour_cells[dir] = nieghbour
        print(possible_pos, neighbour_cells)

    def populate_board(self, thakurs, mazdoors):
        '''
        Put folks on the board initally
        :param thakurs:
        :param mazdoors:
        :return:
        '''
        for i in range(thakurs):
            possible_pos = self.__get_next_random_empty_cell(Inhabitant.THAKUR)
            self.cells[possible_pos].occupy(Inhabitant.THAKUR)
        for i in range(mazdoors):
            possible_pos = self.__get_next_random_empty_cell(Inhabitant.MAZDOOR)
            self.cells[possible_pos].occupy(Inhabitant.MAZDOOR)

    def __get_next_random_empty_cell(self, type):
        '''
        Given a type gives a possible random cell to place a inhabitant
        :param type:
        :return:
        '''
        possible_pos = 0
        can_occupy = False
        while (not can_occupy):
            possible_pos = randint(0, (m * n) - 1)
            if self.cells[possible_pos].current_occupant:
                can_occupy = False
                continue
            else:
                can_occupy = self.__check_rules(possible_pos, type)

        # while (self.cells[
        #            possible_pos].current_occupant is not None and self.__check_first_placement(
        #     possible_pos, type)):
        #     possible_pos = randint(0, m * n)
        return possible_pos

    def move(self):
        for i, cell in enumerate(self.cells):
            cell.move()
            cell.commit_move()
        has_occupant = False
        pop = 0
        for cell in self.cells:
            if cell.current_occupant:
                has_occupant = True
                pop += 1
                if not self.__check_rules(i, cell.current_occupant,
                                          isMove=True):
                    print("Ending world")
                    return False
        # print(pop)
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
    print(sys.argv)
    if len(sys.argv) == 3:
        m = int(sys.argv[1])
        n = int(sys.argv[2])
    else:
        m, n = [int(a) for a in input(
            "Enter m, n:").strip().split(",")]
    thakurs = int(.05 * m * n)
    mazdoors = int(.2 * m * n)
    print(thakurs, mazdoors)
    board = Board(m, n, thakurs, mazdoors)
    living = True
    iterations = 1
    print(board)
    while (living):
        print("================== ITERATION {} ==================".format(
            iterations))
        print(board)
        living = board.move()
        iterations += 1
        board.assign_directions()

    print("Gamed ended with {} iterations".format(iterations))
