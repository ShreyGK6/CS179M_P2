import numpy as np
import pandas as pd

def generateCirclePoints(x_center, y_center, radius, num_points):
    angles = np.random.rand(num_points) * 2 * np.pi
    x = radius * np.cos(angles) + x_center
    y = radius * np.sin(angles) + y_center
    return x, y

x1, y1 = generateCirclePoints(10, 5, 10, 64)   
x2, y2 = generateCirclePoints(45, 5, 10, 64)

circleGraphs = pd.DataFrame({
    'x': np.concatenate([x1, x2]),
    'y': np.concatenate([y1, y2])
})

circleGraphs.to_csv('testingSSE.txt', sep = '\t', index = False)       