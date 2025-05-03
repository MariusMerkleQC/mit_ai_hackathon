# Optimization Problem: Traveling Salesman Problem with Utility and Distance Constraints

## Objective Function

$$max \sum_{i=1}^{n} u[i] \cdot x_{i} - 0.01 \cdot \sum_{i=1}^{n}\sum_{j=1}^{n} d[i][j] \cdot y_{i,j}$$

## Constraints

   - $\sum_{i=1}^{n}\sum_{j=1}^{n} d[i][j] \cdot y_{i,j} \leq D_{max}$  (The total distance covered must be less than or equal to $D_max$)

   - $\sum_{\forall j \neq i}^{n} y_{i,j} = x_{i} \quad \forall i \in \{1,2,...,n\}$ (flow constraints: For each visited node, there must be exactly one outgoing edge)

   - $\sum_{\forall j \neq i}^{n} y_{j,i} = x_{i} \quad \forall i \in \{1,2,...,n\}$ (flow constraints: For each visited node, there must be exactly one incoming edge)

   - $y_{i,i} = 0 \quad \forall i \in \{1,2,...,n\}$ (no self-loops)

   - $s_{i} - s_{j} + n \cdot y_{i,j} \leq n-1 \quad \forall i,j \in \{2,3,...,n\}, i \neq j$ (subtour elimination (MTZ Formulation))

   - $x_{startNode} = 1$ (the starting node must be visited)

   - $\sum_{\forall j \neq startNode}^{n} y_{startNode,j} = 1$ (exactly one edge leaving from starting node)

## Variables
- $x_{i}$ is 1 if location $i$ is visited, 0 otherwise.
- $y_{i,j}$ is 1 if path from $i$ to $j$ is used, 0 otherwise.
- $s_{i}$ are the subtour elimination helper variables.
- $n$ is the total number of nodes.
- $u[i]$ is the utility of node $i$.
- $d[i][j]$ is the distance from node $i$ to node $j$.
- $D_{max}$ is the maximum allowable total distance.
- $startNode$ is the pre-defined starting point of the tour.