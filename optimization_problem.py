import gurobipy as gp
from gurobipy import GRB
from dataclasses import dataclass


@dataclass
class OptimalPath:
    visited: list
    tour: list
    total_utility: float
    total_distance: float

def maximize_utility_with_distance_constraint(utilities: list[float], distance_matrix: list[list[float]], D_max: float, start_node: int) -> OptimalPath | None:
    n = len(utilities)
    
    model = gp.Model('UtilityMaximizationWithStart')

    # Decision variables
    x = model.addVars(n, vtype=GRB.BINARY, name='x')           # 1 if location i is visited
    y = model.addVars(n, n, vtype=GRB.BINARY, name='y')         # 1 if path from i to j is used

    # Subtour elimination helper variables (MTZ formulation)
    s = model.addVars(n, vtype=GRB.CONTINUOUS, lb=0, ub=n-1, name='s')

    # Objective: maximize total utility
    model.setObjective(gp.quicksum(utilities[i] * x[i] for i in range(n)) - gp.quicksum(0.01*distance_matrix[i][j]*y[i, j] for i in range(n) for j in range(n)), GRB.MAXIMIZE)

    # Constraint: total distance must be within D_max
    model.addConstr(gp.quicksum(distance_matrix[i][j] * y[i,j] for i in range(n) for j in range(n)) <= D_max, 'DistanceConstraint')

    # Flow constraints: each visited node must have exactly one incoming and one outgoing edge
    for i in range(n):
        model.addConstr(gp.quicksum(y[i,j] for j in range(n) if j != i) == x[i], f'Outflow_{i}')
        model.addConstr(gp.quicksum(y[j,i] for j in range(n) if j != i) == x[i], f'Inflow_{i}')

    # No self-loops
    for i in range(n):
        model.addConstr(y[i,i] == 0, f'NoSelfLoop_{i}')

    # Subtour elimination (MTZ formulation)
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                model.addConstr(s[i] - s[j] + n * y[i,j] <= n-1, f'SubtourElimination_{i}_{j}')

    # Force starting node to be visited
    model.addConstr(x[start_node] == 1, 'StartNodeVisited')

    # Force exactly one outgoing edge from starting node
    model.addConstr(gp.quicksum(y[start_node, j] for j in range(n) if j != start_node) == 1, 'StartNodeOutflow')

    # Optimize
    model.optimize()

    if model.status == GRB.OPTIMAL:
        # Reconstruct the path order
        successor = {}
        for i in range(n):
            for j in range(n):
                if y[i, j].X > 0.5:
                    successor[i] = j

        # Now walk from start_node following the successors
        path_ordered = [start_node]
        current = start_node
        while True:
            if current not in successor:
                break
            next_node = successor[current]
            if next_node == start_node:
                break  # If we return to start, stop here
            path_ordered.append(next_node)
            current = next_node


        total_utility = sum(utilities[i] for i in path_ordered)
        total_distance = sum(distance_matrix[path_ordered[i]][path_ordered[i+1]] for i in range(len(path_ordered) - 1))
        
        return OptimalPath(path_ordered, list(successor.items()), total_utility, total_distance)
    else:
        print('No feasible solution found')
        return None



if __name__ == "__main__":
    ## Example usage:
    utilities = [10, 20, 30, 40]
    distances = [[0, 5, 9, 10],
                [5, 0, 6, 4],
                [9, 6, 0, 8],
                [10, 4, 8, 0]]
    D_max = 15
    start_node = 0
    optimal_path = maximize_utility_with_distance_constraint(utilities, distances, D_max, start_node)
    if optimal_path:
        print(f"Visited nodes: {optimal_path.visited}")
        print(f"Tour: {optimal_path.tour}")
        print(f"Total utility: {optimal_path.total_utility}")
        print(f"Total distance: {optimal_path.total_distance}")
