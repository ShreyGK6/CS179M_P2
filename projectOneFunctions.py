from __future__ import annotations
import math
import random
import numpy as np

# Computes the distance between points and returns it
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

# Compares the original Points and Best Route Points and gives their indicies as a return as an array
def displayRouteIndicies(originalPoints,bestRoutPoints):
    originalPoints = np.asarray(originalPoints, dtype=float)
    bestRoutPoints = np.asarray(bestRoutPoints, dtype=float)

    indexMap = {}
    for i, p in enumerate(originalPoints, start=1):
        key = (float(p[0]), float(p[1]))
        indexMap.setdefault(key, []).append(i)

    # Convert best_route coordinates to their original indices
    routeIndicies = []
    for p in bestRoutPoints:
        key = (float(p[0]), float(p[1]))
        if key in indexMap and indexMap[key]:
            routeIndicies.append(indexMap[key].pop(0))
    
    # Adding the start point again at the end to show it is a closed TSP problem
    if routeIndicies:
        routeIndicies.append(routeIndicies[0])
    
    return routeIndicies


def nearestNeigborOrderRand(points=None,distanceMatrix=None):

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

    cur = 0
    order[0] = cur
    visited[cur] = True

    # Iterating over all the nodes
    for i in range(1, totalRows):
        # Finding the distance from current point to rest of the point and if 
        # visited then we set it to infinity to ignore it
        drow = np.where(visited, np.inf, distanceMatrix[cur])

        # Calculating the number of univisted points left
        remainingNodes = totalRows - np.sum(visited)
        # Random selection done between 10 or fewer nodes left
        # Bigger the random select number more exploration aka 10+ and smaller then more deterministic ex 3-5
        numNodeRandSelect = min(10, remainingNodes)
        # Partially rearranging the 3 closest nodes and returning it without fully sorting all the distances
        candIdx = np.argpartition(drow, numNodeRandSelect-1)[:numNodeRandSelect]

        actualDistance = drow[candIdx].astype(float)
        # Calculating the inverse distance weights aka higher weight means closer
        w = 1.0/ (actualDistance + 1.e-12)
        # Setting the visited infinity nodes weights to 0
        w[np.isinf(w)] = 0.0
        # Softening the weights to increase the exploration of the algorithm to reduce crossovers
        # Keep it between (0.6 for more exploration 0.8 for more greediness)
        w = w ** 0.7
        # Calculating the total weight
        totalWeight = w.sum()

        # If total weight is 0 then we fall back to uniform random choice
        if totalWeight == 0.0:
            w = np.ones_like(w) / len(w)
        else:
            # Normalizing the weights to sum to 1
            w = w / totalWeight

        # Randomly chooses one next point from the candidates.
        nxt = int(random.choices(list(candIdx), weights=list(w), k=1)[0])
        order[i] = nxt
        visited[nxt] = True
        cur = nxt

    return order

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

def solveTSPNNRand(points):
    # Convert input points to a NumPy float array for consistency
    points = np.asarray(points, dtype=float)
    # Build the distance matrix between every pair of points
    distanceMatrix = buildDistanceMatrix(points)

     # Compute the visiting order using the randomized nearest neighbor approach
    order = nearestNeigborOrderRand(distanceMatrix=distanceMatrix)

    # Close the route by returning to the starting point
    order_closed = np.concatenate([order, order[:1]])

    # Return the ordered coordinates of the full route
    return points[order_closed]