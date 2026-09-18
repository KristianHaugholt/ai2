from typing import Any
from queue import Queue
from collections import defaultdict


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
        q: Queue[tuple[str, str]] = Queue()
        for xi in neighbors:
            for xj in neighbors[xi]:
                q.put((xi, xj))

        def allowed(xi: str, vi: Any, xj: str, vj: Any) -> bool:
            # Return True if assigning xi=vi and xj=vj does NOT violate a binary constraint
            if (xi, xj) in self.binary_constraints:
                return (vi, vj) in self.binary_constraints[(xi, xj)]
            if (xj, xi) in self.binary_constraints:
                return (vi, vj) in self.binary_constraints[(xj, xi)]
            # No constraint between xi and xj
            return True

        def revise(xi: str, xj: str) -> bool:
            revised = False
            to_remove = set()
            for vi in set(self.domains[xi]):
                # if no value vj in domain[xj] allows (xi=vi, xj=vj), remove vi
                if not any(allowed(xi, vi, xj, vj) for vj in self.domains[xj]):
                    to_remove.add(vi)
            if to_remove:
                self.domains[xi] = set(self.domains[xi]) - to_remove
                revised = True
            return revised

        # AC-3 main loop
        while not q.empty():
            xi, xj = q.get()
            if revise(xi, xj):
                if len(self.domains[xi]) == 0:
                    return False
                for xk in neighbors[xi]:
                    if xk == xj:
                        continue
                    q.put((xk, xi))
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
    
    def is_consistent(self, var: str, val: Any, assignment: dict[str, Any]) -> bool:
        """Checks if assigning var = val is consistent with the current assignment.
        
        Parameters
        ----------
        var : str"""
        # Check assigned neighbors for consistency
        for other_var, other_val in assignment.items():
            if other_var == var:
                continue
            # If there is a binary constraint between var and other_var,
            # ensure (val, other_val) is allowed.
            if (var, other_var) in self.binary_constraints:
                if (val, other_val) not in self.binary_constraints[(var, other_var)]:
                    return False
            elif (other_var, var) in self.binary_constraints:
                if (val, other_val) not in self.binary_constraints[(other_var, var)]:
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
