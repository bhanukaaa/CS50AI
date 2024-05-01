import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }


    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters


    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()


    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox(
                            (0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)


    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())


    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # loop over each variable
        for v in self.domains:
            remove = set()

            # loop over each word in the variable's domain
            for word in self.domains[v]:
                # if length isnt not correct
                if len(word) != v.length:
                    # remove
                    remove.add(word)

            # remove appropriate words
            for r in remove:
                self.domains[v].remove(r)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revised = False
        remove = set()

        # looping over each Word in X's domain
        for xWord in self.domains[x]:
            haveY = False

            if self.crossword.overlaps[x, y]:
                # getting overlapping indexes
                xOverlap, yOverlap = self.crossword.overlaps[x, y]

                # looping over each Word in Y's domain
                for yWord in self.domains[y]:
                    if xWord[xOverlap] == yWord[yOverlap]:
                        haveY = True

                if not haveY:
                    # revise
                    remove.add(xWord)
                    revised = True

        # remove the appropriate words
        for r in remove:
            self.domains[x].remove(r)

        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # establish proper queue
        if arcs:
            queue = arcs
        else:
            # even if arcs were not provided
            queue = []
            for v1 in self.crossword.variables:
                for v2 in self.crossword.variables:
                    if v1 != v2:
                        queue.append((v1, v2))

        # while queue is not empty
        while queue:
            # dequeue
            x, y = queue.pop()

            # if revised
            if self.revise(x, y):
                # if size of X.domain == 0
                if len(self.domains[x]) == 0:
                    return False

                # for each Z in X.neighbors - {Y}:
                for z in self.crossword.neighbors(x) - {y}:
                    # enqueue
                    queue.append((z, x))

        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # check if every variable has been assigned to something
        for v in self.domains:
            if v not in assignment:
                return False

        return True


    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        existingWords = []

        # loop over each assigment
        for x, word in assignment.items():
            
            # check if word already used
            if word in existingWords:
                return False
            existingWords.append(word)

            # check if word has correct length
            if len(word) != x.length:
                return False

            # check if overlaps clash or not
            for y in self.crossword.neighbors(x):
                if y in assignment:
                    if self.crossword.overlaps[x, y]:
                        xOverlap, yOverlap = self.crossword.overlaps[x, y]

                        if word[xOverlap] != assignment[y][yOverlap]:
                            return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        heuristic = {value: 0 for value in self.domains[var]}

        # loop over each word
        for val in heuristic:
            for varY in self.crossword.neighbors(var):
                for valY in self.domains[varY]:
                    if self.crossword.overlaps[var, varY]:
                        xOverlap, yOverlap = self.crossword.overlaps[var, varY]

                        # if ruled out add to heuristic
                        if val[xOverlap] != valY[yOverlap]:
                            heuristic[val] += 1
        
        # return the sorted heuristic
        return sorted([x for x in heuristic], key = lambda x: heuristic[x])
      

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # create list of unassigned variables
        unassigned = []
        for v in self.domains:
            if v not in assignment.keys():
                unassigned.append(v)

        # initialize values
        minRem = float('inf')
        out = None

        # loop over each unassigned variable
        for var in unassigned:
            # if it has fewer words in domain, select that
            if len(self.domains[var]) < minRem:
                minRem = len(self.domains[var])
                out = var

            # if it has the same length of domain
            elif len(self.domains[var]) == minRem:
                # check if it has more neighbours and select that
                if len(self.crossword.neighbors(var)) > len(self.crossword.neighbors(out)):
                    out = var

        return out


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # check if assignment complete
        if self.assignment_complete(assignment):
            return assignment

        var = self.select_unassigned_variable(assignment)

        for value in self.order_domain_values(var, assignment):
            assignment[var] = value
            # if value is consistent with assignment
            if self.consistent(assignment):
                # recursively call backtrack
                result = self.backtrack(assignment)

                if result:
                    return result

                # remove var from assignment
                del assignment[var]

        # return failure
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
