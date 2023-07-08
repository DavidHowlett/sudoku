"""
In 2015, I wrote this sudoku solver on a train while I was newish to python. It worked but it was not beautiful.
I came back to it in 2023 with the benefit of better tooling and more experience. The text file full of puzzles came
from: http://www2.warwick.ac.uk/fac/sci/moac/people/students/peter_cock/python/sudoku/
"""


initialState = [
    [None, 1, 2, None, None, None, None, 5, 7],
    [None, None, None, None, 2, None, None, None, None],
    [8, 7, None, None, None, None, 3, 1, None],
    [None, 9, None, None, 5, None, 7, None, None],
    [None, None, None, 7, None, 6, None, None, None],
    [None, None, 7, None, 8, None, None, None, 6],
    [None, 4, 1, None, None, None, None, 3, 5],
    [None, None, None, None, 9, None, None, None, None],
    [3, 5, None, None, None, None, 9, None, None],
]


class Cell:
    """This represents a single cell in the sudoku puzzle."""

    def __init__(self, answer=None):
        self.groups = set()
        self.possible = {answer} if answer else set(range(1, 10))

    def __repr__(self) -> str:
        return str(self.answer()) if self.answer() else "_"

    def solved(self) -> bool:
        """Returns whether the cell is solved."""
        return len(self.possible) == 1

    def answer(self) -> int:
        """Returns the answer if it exists."""
        return self.possible.copy().pop() if self.solved() else None

    def exclude(self, value: int):
        """Remove a value from the set of allowed possibilities for the cell."""
        if value in self.possible:
            self.possible.discard(value)
            if self.solved():
                self.propagate()

    def propagate(self):
        """Call this after the cell becomes certain, it propagates the
        reduction in possibilities in neighbors."""
        answer = self.answer()
        assert answer
        for group in self.groups:
            for neighbor in group:
                if neighbor is not self:
                    neighbor.exclude(answer)

    def check_neighbors_for_answer(self):
        """If the union of the possible values of the neighbors in
        a group excludes a value then this cell must have that value
        example: if all the other cells on a row can't be a 7 then the
        current cell must be a 7
        """
        if self.solved():
            return
        for group in self.groups:
            group_less_self = set(group)
            group_less_self.remove(self)
            neighbors_can_be = set()
            for neighbor in group_less_self:
                neighbors_can_be.update(neighbor.possible)
            assert len(neighbors_can_be) == 8 or len(neighbors_can_be) == 9
            if len(neighbors_can_be) == 8:
                self.possible = set(range(1, 10)).difference(neighbors_can_be)
                self.propagate()


def print_state(state):
    """Pretty print the current state of the puzzle."""
    for row in state:
        for cell in row:
            print(cell, end="\t")
        print()
    print()


def solve(state):
    """Given a sudoku puzzle, return the solution."""
    box = [[Cell(answer) for answer in row] for row in state]
    # the top left corner is box[0][0]
    # it is indexed as box[row][column]
    # a group of cells is not allowed to share any digits

    # 3x3 box restriction
    groups = {
        frozenset(box[3 * i + k][3 * j + l] for k in range(3) for l in range(3))  # noqa
        for i in range(3)
        for j in range(3)
    }

    # row and column restriction
    for i in range(9):
        column = frozenset(box[y][i] for y in range(9))
        row = frozenset(box[i][x] for x in range(9))
        groups.add(row)
        groups.add(column)

    for group in groups:
        for cell in group:
            cell.groups.add(group)

    cells = frozenset(cell for row in box for cell in row)

    for cell in cells:
        if cell.solved():
            cell.propagate()  # propagate initial values

    for _ in range(5):
        for cell in cells:
            cell.check_neighbors_for_answer()

    return box


if __name__ == "__main__":
    print_state(solve(initialState))
