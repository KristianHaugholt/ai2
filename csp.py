from typing import Any
from collections import defaultdict, deque


class CSP:
    def __init__(
        self,
        variables: list[str],
        domains: dict[str, set],
        edges: list[tuple[str, str]],
    ):
        """Constructs a CSP instance with the given variables, domains and edges.
        
        Parameters
        ----------
        variables : list[str]
            The variables for the CSP
        domains : dict[str, set]
            The domains of the variables
        edges : list[tuple[str, str]]
            Pairs of variables that must not be assigned the same value
        """
        self.variables = variables
        self.domains = domains

        # Binary constraints as a dictionary mapping variable pairs to a set of value pairs.
        #
        # To check if variable1=value1, variable2=value2 is in violation of a binary constraint:
        # if (
        #     (variable1, variable2) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        # ) or (
        #     (variable2, variable1) in self.binary_constraints and
        #     (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        # ):
        #     Violates a binary constraint
        self.binary_constraints: dict[tuple[str, str], set] = {}
        for variable1, variable2 in edges:
            self.binary_constraints[(variable1, variable2)] = set()
            for value1 in self.domains[variable1]:
                for value2 in self.domains[variable2]:
                    if value1 != value2:
                        self.binary_constraints[(variable1, variable2)].add((value1, value2))
                        self.binary_constraints[(variable1, variable2)].add((value2, value1))

    def ac_3(self) -> bool:
        """Performs AC-3 on the CSP.
        Meant to be run prior to calling backtracking_search() to reduce the search for some problems.
        
        Returns
        -------
        bool
            False if a domain becomes empty, otherwise True
        """
        # Build neighbor mapping from binary constraints
        neighbors: dict[str, set[str]] = defaultdict(set)
        for (xi, xj) in self.binary_constraints.keys():
            neighbors[xi].add(xj)
            neighbors[xj].add(xi)

        # Initialize queue with all arcs (xi, xj)
        q: deque[tuple[str, str]] = deque()
        for xi in neighbors:
            for xj in neighbors[xi]:
                q.append((xi, xj))

        def revise(xi: str, xj: str) -> bool:       #returns true iff domain of xi is revised
            revised = False                         #revised <= false
            to_remove = set()
            for vi in set(self.domains[xi]):        #for each x vi in di do
                # if no value vj in domain[xj] allows (xi=vi, xj=vj), remove vi from domain[xi]
                if not any(self.constraint_allows(xi, vi, xj, vj) for vj in self.domains[xj]):
                    to_remove.add(vi)
            if to_remove:
                self.domains[xi] = set(self.domains[xi]) - to_remove
                revised = True
            return revised

                                                # AC-3 main loop
        while q:                                #while q is not empty
            xi, xj = q.popleft()                #xi, xj = pop(q) 
            if revise(xi, xj):                  #if revise(xi, xj) then
                if len(self.domains[xi]) == 0:  #if size of di = 0 then return false
                    return False
                for xk in neighbors[xi]:        #for each xk in xi.neighbors - xj do
                    if xk == xj:
                        continue
                    q.append((xk, xi))          #add (xk, xi) to q
        return True

    def constraint_allows(self, variable1: str, value1: Any, variable2: str, value2: Any) -> bool:
        """Return True if the pair (variable1=value1, variable2=value2) does not violate a constraint.

        Uses the same variable1/variable2 structure and or-condition checks as other methods.
        """
        if (
            (variable1, variable2) in self.binary_constraints and
            (value1, value2) not in self.binary_constraints[(variable1, variable2)]
        ) or (
            (variable2, variable1) in self.binary_constraints and
            (value1, value2) not in self.binary_constraints[(variable2, variable1)]
        ):
            return False
        return True

    def backtracking_search(self) -> None | dict[str, Any]:
        """Performs backtracking search on the CSP.
        
        Returns
        -------
        None | dict[str, Any]
            A solution if any exists, otherwise None
        """
        def backtrack(assignment: dict[str, Any]):
            # YOUR CODE HERE (and remove the assertion below)
            if len(assignment) == len(self.variables):
                return assignment
            
            var = self.select_unassigned_variable(assignment)

            # Try each value in the domain of the selected variable
            for val in self.domains[var]:
                # Check if assigning var = val is consistent with current assignment
                if self.is_consistent(var, val, assignment):
                    # Make assignment
                    assignment[var] = val
                    
                    # Recursively search for a solution
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                    
                    # Backtrack: remove assignment if it did not lead to a solution
                    del assignment[var]

            # No valid assignment found for this branch
            return None

        return backtrack({})
    
    def select_unassigned_variable(self, assignment: dict[str, Any]) -> str:
        """Selects an unassigned variable from the CSP.
        
        Parameters
        ----------
        assignment : dict[str, Any]
            The current assignment of variables to values

        Returns
        -------
        str
            An unassigned variable
        """
        for var in self.variables:
            if var not in assignment:
                return var
        raise ValueError("All variables are assigned")
    
    def is_consistent(self, variable1: str, value1: Any, assignment: dict[str, Any]) -> bool:
        """Checks if assigning var = val is consistent with the current assignment.
        
        Parameters
        ----------
        var : str"""
        # Check assigned neighbors for consistency
        for variable2, value2 in assignment.items():
            if not self.constraint_allows(variable1, value1, variable2, value2):
                return False
        return True



def alldiff(variables: list[str]) -> list[tuple[str, str]]:
    """Returns a list of edges interconnecting all of the input variables

    Parameters
    ----------
    variables : list[str]
        The variables that all must be different

    Returns
    -------
    list[tuple[str, str]]
        List of edges in the form (a, b)
    """
    return [(variables[i], variables[j]) for i in range(len(variables) - 1) for j in range(i + 1, len(variables))]
