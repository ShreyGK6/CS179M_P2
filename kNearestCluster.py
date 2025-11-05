import numpy as np
from projectOneFunctions import solveTSPNN, tourLengthFromPoints

def kNearestCluster(points, k):
    np.random.seed(42)                                 #seed for kmeans algorithm
    pointsArray = np.asarray(points, dtype = float)
    dronePadIndex = np.random.choice(len(pointsArray), k, replace = False)
    dronePads = pointsArray[dronePadIndex]
    dronePads = np.asarray(dronePads, dtype = float)

    #to make sure that we reach the end, it will iterate 100 times
    for _ in range(100):
        distance = np.linalg.norm(pointsArray[:,None,:] - dronePads[None,:,:], axis = 2)  #calculate distance and create labels
        dronePadLabels = np.argmin(distance, axis = 1)
        newPads = []
        for i in range(k):
            clusteredPoints = pointsArray[i == dronePadLabels]
            if len(clusteredPoints) > 0:       #calculate the mean of the cluster points
                meanDronePads = clusteredPoints.mean(axis = 0)
            else:
                meanDronePads = dronePads[i]
            newPads.append(meanDronePads)
        newPads = np.asarray(newPads, dtype = float)

        #compare newPads with the dronePads to see if they are the same

        if np.allclose(dronePads, newPads):
            break

        #if the two are not equal yet, then replace dronePads with newPads
        dronePads = newPads

    return dronePadLabels, dronePads


def createDronePaths(points , k):
    dronePadLabels, dronePads = kNearestCluster(points, k)
    totalDistance = 0
    completeRoute = []

    for i in range(k):
        cluster = points[i == dronePadLabels]
        route = solveTSPNN(cluster)                                #use code from P1    
        currentDistance = tourLengthFromPoints(route)
        totalDistance = totalDistance + currentDistance
        completeRoute.append({"DronePad": dronePads[i], "Size of Cluster": len(cluster),
                              "Distance": currentDistance, "Route": route})
        
    return totalDistance, completeRoute