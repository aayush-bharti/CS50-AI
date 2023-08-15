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
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
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
        
        #loops through each variable and value in the domain to check if the length of the word is the same as the length of the variable
        for variable in self.domains:
            for value in self.domains[variable].copy():
                #if the length is not the same, remove the value from the domain
                if variable.length != len(value):
                    self.domains[variable].remove(value)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        #creates 2 boolean variables, one to be returned
        revised = False
        overlap = False

        if self.crossword.overlaps[x,y]:
            x_index, y_index = self.crossword.overlaps[x,y]
            #loops through the domain of x to see if the overlap is satisfied
            for x_variable in self.domains[x].copy():
                for y_variable in self.domains[y]:
                    if x_variable[x_index] == y_variable[y_index]:
                        overlap = True
                #if not satisfied, remove the value from the domain of x 
                #changes the revised boolean to true, since the domain was changed
                if not overlap:
                    self.domains[x].remove(x_variable)
                    revised = True
        
        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """

        #if arcs is empty, fill it up with all of the arcs
        if arcs is None:
            arcs = []
            for i in self.domains:
                for j in self.domains:
                    if i != j:
                        arcs.append((i, j))

        #as long as there is something in arcs, run the loop
        while len(arcs) != 0:
            #dequeues or pops the last item in the queue
            x, y = arcs.pop()
            if self.revise(x, y):
                #if the domain is empty, that means that cannot work and returns false
                if len(self.domains[x]) == 0:
                    return False
                #checks if all of the neighbors of x except y are still consistent and adds them to the arc queue
                for z in self.crossword.neighbors(x) - {y}:
                    arcs.append((z, x))

        return True    
        
        
    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        
        #checks if each variable is assigned to a value, if not return false
        for variable in self.domains:
            if variable not in assignment:
                return False
            
        return True

       
    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        
        #loops through each variable object in assignment
        for variable in assignment:
            #checks if all the values are different, if not return false
            for var in assignment:
                if variable != var:
                    if assignment[variable] == assignment[var]:
                        return False
            
            #checks if every value is the correct length, if not return false
            if variable.length != len(assignment[variable]):
                return False
            
            #checks for any conflicts with neighbors
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment.keys():
                    i, j = self.crossword.overlaps[variable, neighbor]
                    #if the neighbor values are not the same, return false
                    if neighbor in assignment:
                        if assignment[variable][i] != assignment[neighbor][j]:
                            return False
                            
        return True
        

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        values = {}
        
        #loops through all the values in the domain
        for value in self.domains[var]:
            count = 0
            for neighbor in self.crossword.neighbors(var):
                #makes sure the value isn't in the assignment so its not counted
                if value not in assignment:
                    #increase the ruled out count by one if value is in the domain of the neighbor
                    if value in self.domains[neighbor]:
                        count += 1
                    values[value] = count
        
        #returns the sorted list
        return sorted(values, key = lambda val: values[val])


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        unassigned = []
        #adds in all the unassigned variables
        for variable in self.domains.keys():
            if variable not in assignment:
                unassigned.append(variable)
        
        #sorts the list based on the minimum remaining value heuristic and the degree heuristic
        return sorted(unassigned, key = lambda var: (len(self.domains[var]), -len(self.crossword.neighbors(var))))[0]


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        
        #if the assignment is complete return it
        if self.assignment_complete(assignment):
            return assignment
        
        variable = self.select_unassigned_variable(assignment)
        
        #takes the unassigned variables and tests them out on the assignment
        for value in self.order_domain_values(variable, assignment):
            assignment[variable] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                #if the result did not fail, return the result
                if result is not None:
                    return result
            #delete the variable after testing if it failed
            del assignment[variable]
            
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
