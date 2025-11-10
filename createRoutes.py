from projectOneFunctions import solveTSPNN, tourLengthFromPoints
from kNearestCluster import kNearestCluster
import numpy as np

def createDronePaths(points , k):
    dronePadLabels, dronePads = kNearestCluster(points, k)
    totalDistance = 0
    completeRoute = []
    pointsArray = np.asarray(points, dtype = float)

    for i in range(k):
        cluster = pointsArray[dronePadLabels == i]
        route = solveTSPNN(cluster)                                #use code from P1    
        currentDistance = tourLengthFromPoints(route)
        totalDistance = totalDistance + currentDistance
        completeRoute.append({"DronePad": dronePads[i], "Size of Cluster": len(cluster),
                              "Distance": currentDistance, "Route": route})
        
    
    OFScore = np.sum((pointsArray - dronePads[dronePadLabels])**2)
        
    return totalDistance, completeRoute, OFScore