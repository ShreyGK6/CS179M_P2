from __future__ import annotations
import numpy as np

def buildDistanceMatrix(points):
    # Converting the input points into a numpy array as float points
    pointsArr = np.asarray(points, dtype=float)
    # Computing the full pairwise Euclidean distance matrix between all points using NumPy broadcasting
    return np.linalg.norm(pointsArr[:,None,:] - pointsArr[None,:,:], axis = 2)

# Computing the total distance of a closed tour path directly from the coordinates that returns to the start point always
def tourLengthFromPoints(route_points):
    # Represents the coordinate differences between each consecutive leg of the tour
    diffs = np.diff(route_points, axis=0)
    # Returning the calculation of the Euclidean distance for each leg of the tour
    return float(np.sum(np.linalg.norm(diffs, axis=1)))

def nearestNeigborOrder(points=None, distanceMatrix=None):
    
    # Checking if one input is atleast given which is points or the distanceMatrix 
    if (points is None) == (distanceMatrix is None):
        raise ValueError("Provide exactly one of points= or distanceMatrix=.")
    
    # Computes the distance between points if we dont have one
    if distanceMatrix is None:
        distanceMatrix = buildDistanceMatrix(points)
    else:
        distanceMatrix = np.asarray(distanceMatrix, dtype=float)

    # Getting the total number of points we have from the file
    totalRows = distanceMatrix.shape[0]
    # Initalizing arrays to track the order of points and visited nodes
    order = np.empty(totalRows, dtype=int)
    visited = np.zeros(totalRows, dtype=bool)

    # Setting a variable that allows the algorithm to find the next start index for the node that we 
    # computed or if not it defaults back to the start node if nothing was made
    start_offset = getattr(nearestNeigborOrder, "_start_offset", 0)
    cur = int(start_offset) % totalRows
    order[0] = cur
    visited[cur] = True

    # Iterating over all the nodes
    for i in range(1, totalRows):
        # Finding the distance from current point to rest of the point and if 
        # visited then we set it to infinity to ignore it
        drow = np.where(visited, np.inf, distanceMatrix[cur])

        # Pick the closest unvisited node
        nxt = int(np.argmin(drow))

        order[i] = nxt
        visited[nxt] = True
        cur = nxt

    # To find the new offset and use it as the new starting node.
    nearestNeigborOrder._start_offset = (start_offset + 1) % totalRows

    return order

def solveTSPNN(points):
    # Convert input points to a NumPy float array for consistency
    points = np.asarray(points, dtype=float)
    # Build the distance matrix between every pair of points
    distanceMatrix = buildDistanceMatrix(points)

     # Compute the visiting order using the randomized nearest neighbor approach
    order = nearestNeigborOrder(distanceMatrix=distanceMatrix)

    # Close the route by returning to the starting point
    order_closed = np.concatenate([order, order[:1]])

    # Return the ordered coordinates of the full route
    return points[order_closed]