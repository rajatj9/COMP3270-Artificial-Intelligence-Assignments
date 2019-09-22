import random
import copy
from optparse import OptionParser
import util

class SolveEightQueens:
    def __init__(self, numberOfRuns, verbose, lectureExample):
        """
        Value 1 indicates the position of queen
        """
        self.numberOfRuns = numberOfRuns
        self.verbose = verbose
        self.lectureCase = [[]]
        if lectureExample:
            self.lectureCase = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 1, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 0, 0, 1, 0, 1],
            [0, 0, 1, 0, 0, 0, 1, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            ]
    def solve(self):
        solutionCounter = 0
        for i in range(self.numberOfRuns):
            if self.search(Board(self.lectureCase), self.verbose).getNumberOfAttacks() == 0:
                solutionCounter += 1
        print("Solved: %d/%d" % (solutionCounter, self.numberOfRuns))

    def search(self, board, verbose):
        """
        Hint: Modify the stop criterion in this function
        """
        newBoard = board
        i = 0 
        while True:
            if verbose:
                print("iteration %d" % i)
                print(newBoard.toString())
                print("# attacks: %s" % str(newBoard.getNumberOfAttacks()))
                print(newBoard.getCostBoard().toString(True))
            currentNumberOfAttacks = newBoard.getNumberOfAttacks()
            (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            i += 1
            # local_minima_flag = 0
            # if currentNumberOfAttacks == newNumberOfAttacks and local_minima_flag <= 100:
            #     (newBoard, newNumberOfAttacks, newRow, newCol) = newBoard.getBetterBoard()
            #     local_minima_flag += 1
            if currentNumberOfAttacks <= newNumberOfAttacks:
                break
        return newBoard

class Board:
    def __init__(self, squareArray = [[]]):
        if squareArray == [[]]:
            self.squareArray = self.initBoardWithRandomQueens()
        else:
            self.squareArray = squareArray

    @staticmethod
    def initBoardWithRandomQueens():
        tmpSquareArray = [[ 0 for i in range(8)] for j in range(8)]
        for i in range(8):
            tmpSquareArray[random.randint(0,7)][i] = 1
        return tmpSquareArray
          
    def toString(self, isCostBoard=False):
        """
        Transform the Array in Board or cost Board to printable string
        """
        s = ""
        for i in range(8):
            for j in range(8):
                if isCostBoard: # Cost board
                    cost = self.squareArray[i][j]
                    s = (s + "%3d" % cost) if cost < 9999 else (s + "  q")
                else: # Board
                    s = (s + ". ") if self.squareArray[i][j] == 0 else (s + "q ")
            s += "\n"
        return s 

    def getCostBoard(self):
        """
        First Initalize all the cost as 9999. 
        After filling, the position with 9999 cost indicating the position of queen.
        """
        costBoard = Board([[ 9999 for i in range(8)] for j in range(8)])
        for r in range(8):
            for c in range(8):
                if self.squareArray[r][c] == 1:
                    for rr in range(8):
                        if rr != r:
                            testboard = copy.deepcopy(self)
                            testboard.squareArray[r][c] = 0
                            testboard.squareArray[rr][c] = 1
                            costBoard.squareArray[rr][c] = testboard.getNumberOfAttacks()
        return costBoard

    def getBetterBoard(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return a tuple containing containing four values
        the new Board object, the new number of attacks, 
        the Column and Row of the new queen  
        For example:
            return (betterBoard, minNumOfAttack, newRow, newCol)
        The datatype of minNumOfAttack, newRow and newCol should be int
        """
        board_size = len(self.squareArray)
        min_attacks, newX, newY = board_size**2, 0, 0
        for col_index in range(board_size):
            queen_loc_x = 0
            for row_index in range(board_size):
                if self.squareArray[row_index][col_index] == 1:
                    queen_loc_x = row_index
                    break
            self.squareArray[queen_loc_x][col_index] = 0

            for row_index in range(board_size):
                self.squareArray[row_index][col_index] = 1
                attacks = self.getNumberOfAttacks()
                if attacks < min_attacks:
                    min_attacks = attacks
                    newX = row_index
                    newY = col_index
                self.squareArray[row_index][col_index] = 0

            self.squareArray[queen_loc_x][col_index] = 1

        better_board = copy.deepcopy(self)
        for i in range(board_size):
            better_board.squareArray[i][newY] = 0
        better_board.squareArray[newX][newY] = 1

        return (better_board, min_attacks, newX, newY)


    def getNumberOfAttacks(self):
        """
        "*** YOUR CODE HERE ***"
        This function should return the number of attacks of the current board
        The datatype of the return value should be int
        """
        num_attacks = 0
        board_size = len(self.squareArray)
        for queen_loc_y in range(board_size):
            queen_loc_x = 0
            for row_index in range(board_size):
                if self.squareArray[row_index][queen_loc_y] == 1:
                    queen_loc_x = row_index
                    break
            for col_index in range(queen_loc_y+1, board_size):
                if self.squareArray[queen_loc_x][col_index] == 1:
                    num_attacks += 1
            start_x, start_y = queen_loc_x, queen_loc_y
            while start_x > 0 and start_y < board_size - 1:
                start_y += 1
                start_x -= 1
                if self.squareArray[start_x][start_y] == 1:
                    num_attacks += 1
            start_x, start_y = queen_loc_x, queen_loc_y
            while start_x < board_size - 1 and start_y < board_size - 1:
                start_y += 1
                start_x += 1
                if self.squareArray[start_x][start_y] == 1:
                    num_attacks += 1
        return num_attacks

if __name__ == "__main__":
    #Enable the following line to generate the same random numbers (useful for debugging)
    random.seed(1)
    parser = OptionParser()
    parser.add_option("-q", dest="verbose", action="store_false", default=True)
    parser.add_option("-l", dest="lectureExample", action="store_true", default=False)
    parser.add_option("-n", dest="numberOfRuns", default=1, type="int")
    (options, args) = parser.parse_args()
    EightQueensAgent = SolveEightQueens(verbose=options.verbose, numberOfRuns=options.numberOfRuns, lectureExample=options.lectureExample)
    EightQueensAgent.solve()
