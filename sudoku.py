initialState=[
[None,1   ,2   ,None,None,None,None,5   ,7   ],
[None,None,None,None,2   ,None,None,None,None],
[8   ,7   ,None,None,None,None,3   ,1   ,None],
[None,9   ,None,None,5   ,None,7   ,None,None],
[None,None,None,7   ,None,6   ,None,None,None],
[None,None,7   ,None,8   ,None,None,None,6   ],
[None,4   ,1   ,None,None,None,None,3   ,5   ],
[None,None,None,None,9   ,None,None,None,None],
[3   ,5   ,None,None,None,None,9   ,None,None]]

class Cell():
    def __init__(self,answer=None):
        self.groups = set()
        self.possible = {answer} if answer else set(range(1,10))
    def __repr__(self)->str:
        return str(self.answer()) if self.answer() else '_'
    def solved(self)->bool:
        'returns wheather the cell is solved'
        return len(self.possible) == 1
    def answer(self)->int:
        'returns the answer if it exists'
        return self.possible.copy().pop() if self.solved() else None
    def exclude(self,value:int):
        if value in self.possible:
            self.possible.discard(value)
            self.propagate()
    def propagate(self):
        'this propagates the reduction in possibilitys caused by the current cell becoming certain'
        if self.solved():
            answer = self.answer()
            for group in self.groups:
                for neighbor in group:
                    if not (neighbor is self):
                        neighbor.exclude(answer)
    def check_neighbors_for_answer(self):
        '''if the union of the possible values of the neighbors in
        a group excludes a value then this cell must have that value
        example: if all the other cells on a row can't be a 7 then the
        current cell must be a 7
        '''
        if self.solved():
            return
        for group in self.groups:
            groupLessSelf = set(group)
            groupLessSelf.remove(self)
            neighborsCanBe = set()
            for neighbor in groupLessSelf:
                neighborsCanBe.update(neighbor.possible)
            assert len(neighborsCanBe) == 8 or len(neighborsCanBe) == 9
            if len(neighborsCanBe) == 8:
                self.possible = set(range(1,10)).difference(neighborsCanBe)
                self.propagate()

def print_state(state):
    for row in state:
        for cell in row:
            print(cell,end='\t')
        print()
    print()
        
box = [[Cell(answer) for answer in row] for row in initialState]
# the top left corner is box[0][0]
# it is indexed as box[row][column]
# a group of cells is not allowed to share any digits

# 3x3 box restriction below
groups = set(frozenset(box[3*i+k][3*j+l] for k in range(3) for l in range(3)) for i in range(3) for j in range(3))

# row and column restriction below
for i in range(9):
    column = frozenset(box[y][i] for y in range(9))
    row = frozenset(box[i][x] for x in range(9))
    groups.add(row)
    groups.add(column)

for group in groups:
    for cell in group:
        cell.groups.add(group)

cells = frozenset(cell for row in box for cell in row)
# cells are not allowed to be their own neighbors
for cell in cells:
    cell.propagate() # propegate initial values
for i in range(10):
    print_state(box)
    for cell in cells:
        cell.check_neighbors_for_answer()
# this program is 89 lines long before optimiseation