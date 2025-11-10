import numpy as np
import pandas as pd

def generateCirclePoints(xCenter, yCenter, radius, numPoints):
    angles = np.random.rand(numPoints) * 2 * np.pi
    x = radius * np.cos(angles) + xCenter
    y = radius * np.sin(angles) + yCenter
    return x, y

x1, y1 = generateCirclePoints(10, 5, 10, 64)   
x2, y2 = generateCirclePoints(45, 5, 10, 64)

circleGraphs = pd.DataFrame({
    'x': np.concatenate([x1, x2]),
    'y': np.concatenate([y1, y2])
})

circleGraphs.to_csv('testingSSE.txt', sep = '\t', index = False)       