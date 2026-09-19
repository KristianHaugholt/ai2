from typing import Any

class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        self.variables = variables
        self.domains = domains
        self.edges = edges
        
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # Here we add some backtracking statistics.                                                     #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        self.bt_calls = 0
        self.bt_failures = 0

        
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # Given all the possible pairings between two variables.                                        #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in self.edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

                        
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # We define a function to check if a binary constraint is violated or satisfied.                #
        # It returns True if assigning var1=x and var2=y does not violate a binary constraint. The way  #
        # the function check this is by looking through the possible variable-pairs, and checking if    #
        # the pair (x,y) violates a binary constraint. If does violate a constraint, then it returns    #
        # False.                                                                                        #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    def satisfies_constraint(self, var1, var2, x, y):
            if (var1, var2) in self.binary_constraints and (x, y) not in self.binary_constraints[(var1, var2)]:
                return False
            if (var2, var1) in self.binary_constraints and (y, x) not in self.binary_constraints[(var2, var1)]:
                return False
            return True
                        

            
#---#---#---#---#---#---#---#
# AC-3 Algorithm, start     #           
#---#---#---#---#---#---#---#           
    def ac_3(self) -> bool:    
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # This section constructs a dictionary consisting of all the neighbour-pairs.                   #
        # It iterates through every edge in given in the CSP. For every new variable, it makes an empty #
        # set. Then, every time a new "neighbour" is explored for a given variable, it will it that new #
        # neighbour to the set.                                                                         #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        neighbours= dict()
        for (var1, var2) in self.edges:
            if var1 not in neighbours:
                neighbours[var1] = set()
            neighbours[var1].add(var2)

            
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # The "revise"-function is defined in the psedocode for the AC-3 algorithm, and checks for every#
        # value x in the domain of a given variable1 if any value y from another variable2 satisfies a  #
        # binary constraint. If it does not violate any binary constraints (i.e. satisfies.constraints()#
        # = True), then it will break and return revised=False.                                         #
        # If there is no value y in the domain of variable2 that satisfies a constraint between varible1#
        # and variable2, then the value x is deleted from the domain of variable1. This removal happens #
        # after all the iterations, collected in "removed". Then it will return True.                   #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        def revise(var1, var2):
            revised = False
            removed = set()
            for x in self.domains[var1]:
                has_support = False
                for y in self.domains[var2]:
                    if self.satisfies_constraint(var1, var2, x, y) == True:
                        has_support = True
                        break
                if has_support == False:
                    removed.add(x)
            if removed:
                self.domains[var1] = set(self.domains[var1]) - removed
                revised = True
            return revised
        
        
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # This section constructs the initial queue.                                                    #
        # It begins with an empty list, and then iterates through all the variables and its neighbours. #
        # For every iteration, it adds the variable pair to the queue.                                  #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        queue = []
        for var1 in neighbours:
            for var2 in neighbours[var1]:
                queue.append((var1, var2))

                
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        # This section is taken straight from the psuedocode for the AC-3 algorithm. While the queue is #
        # not empty, it pops the first element (assigning var1, var2 the values of this first element in#
        # the queue) before it checks if var1, var2 violates a constraint. Note that in this "revise"-  #
        # function, it will remove elements from the domain of var1. In the event that the domain is    #
        # empty, the AC-3 function will return False (meaning that an inconsistency was found).         #
        # Otherwise, it returns True and succeeded.                                                     #
        #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
        
        while queue:
            var1, var2 = queue.pop(0)
            if revise(var1, var2) == True:
                if len(self.domains[var1]) == 0:   
                    return False                   # Returns False if an inconsistency is found
                for var in neighbours[var1]:
                    if var == var2:                # In the case where var=var2, then it just continues.
                        continue
                    queue.append((var, var1))

        return True
#---#---#---#---#---#---#---#
# AC-3 Algorithm, end       #           
#---#---#---#---#---#---#---#      
    
    
    
    
    
#---#---#---#---#---#---#---#
# Backtrack Algorithm, start#           
#---#---#---#---#---#---#---#
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    # This simply returns every variable who has not yet been assigned a value.                     #
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    def select_unassigned_variable(self, assignment):
        for var in self.variables:
            if var not in assignment:
                return var

    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    # This function checks if a value x for a variable satisfies the constraints given an assignment#
    # It iterates through all the assigned variables in "assignment" and returns False if it        #
    # violates a constraint.
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    def is_consistent(self, var1, x, assignment):
        for var2, y in assignment.items():
            if self.satisfies_constraint(var1, var2, x, y) == False:
                return False
        return True

    
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    # This section is the backtracking algorithm, and follows the psuedocode from the book.         #
    # It is a recursive function, so we have the "complete" measure in the beginning.               #
    # For every backtrack, it selects an unassigned variable.                                       #
    # Then it iterates through all of the domain, and if a value in the domain is consistent with   #
    # the assignment, then it assigns this value to the variable1 and begins the backtrack recursion#
    # If the backtrack results in inconsistency, it will return "Failure", and delete the assigned  #
    # value for variable1. This continues until every variable is assigned a value that satisfies   #
    # the constraints.                                                                              #
    #---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#
    def backtracking_search(self) -> None | dict[str, Any]:
        # reset counters
        self.bt_calls = 0
        self.bt_failures = 0

        def backtrack(assignment: dict[str, Any]):
            self.bt_calls += 1
            if len(assignment) == len(self.variables):         # If all variables have been assigned, then return assignment.
                return assignment

            var1 = self.select_unassigned_variable(assignment)  # Select unassigned variable.
            
            for x in self.domains[var1]:
                if self.is_consistent(var1, x, assignment):
                    assignment[var1] = x
                    result = backtrack(assignment)              # Backtrack
                    if result != "Failure":
                        return result
                    del assignment[var1]                        # Delete assigned variable if result is a "Failure"

            self.bt_failures += 1
            return "Failure"

        return backtrack({})
#---#---#---#---#---#---#---#
# Backtrack Algorithm, end  #           
#---#---#---#---#---#---#---#


def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]

