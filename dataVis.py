import os
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so
import matplotlib.pyplot as plt

def visAllDronePaths(points, completeRoute):

    minSidePix = 1920
    dpi = 200

    points = np.asarray(points, dtype=float)
    ptsDf = pd.DataFrame(points, columns=['x','y'])

    routeRows = []
    padRows = []

    for routeIdx, info in enumerate(completeRoute,start=1):
        route = np.asarray(info["Route"], dtype=float)
        for order, (x,y) in enumerate(route):
            routeRows.append({"routeId": f"Route {routeIdx}", "order": order, "x": x, "y": y})
        px, py = map(float,info["DronePad"])
        padRows.append({"routeId": f"Route {routeIdx}", "x": px, "y": py})
    routesDf = pd.DataFrame(routeRows)
    padsDf = pd.DataFrame(padRows)

    xAll = np.concatenate([ptsDf["x"].values, routesDf["x"].values, padsDf["x"].values])
    yAll = np.concatenate([ptsDf["y"].values, routesDf["y"].values, padsDf["y"].values])
    
    xMin, xMax = float(xAll.min()), float(xAll.max())
    yMin, yMax = float(yAll.min()), float(yAll.max())

    xRange = xMax - xMin
    yRange = yMax - yMin
    span = max(xRange, yRange)
    # 2% data padding per slides
    pad = 0.02 * span

    cx = (xMin + xMax) / 2.0
    cy = (yMin + yMax) / 2.0
    xLim = (cx - span / 2 - pad, cx + span / 2 + pad)
    yLim = (cy - span / 2 - pad, cy + span / 2 + pad)

    slideIn = float(minSidePix) / float(dpi)

    palette = sns.color_palette("colorblind", len(completeRoute))


    p = (
        so.Plot()
        # background points
        .add(so.Dot(alpha=.6, pointsize=9, color="#9aa0a6"),
             data=ptsDf, x="x", y="y")
        # paths per route
        .add(so.Path(linewidth=2.5),
             data=routesDf, x="x", y="y", color="routeId")
        # landing pads "stroke" (bigger black dot)
        .add(so.Dot(pointsize=7, color="black"),
             data=padsDf, x="x", y="y")
        # landing pads foreground (colored dot)
        .add(so.Dot(pointsize=4),
             data=padsDf, x="x", y="y", color="routeId")
        .scale(color=palette)
        .limit(x=xLim, y=yLim)  # keeps axes equal since limits share same span
        .label(x="X (meters)", y="Y (meters)",
               title=f"Overall Solution (K = {len(completeRoute)})")
        .theme({"figure.facecolor": "white","axes.facecolor": "white"})
    )

    movePlotToDesktop(p,"Andersons_OVERALL_SOLUTION",slideIn,dpi=dpi)
    print("[SUCCESS] Visualization saved to Desktop/visualizationRouteFolder")

    return None

def visTimeDroneTradeOff(all_results):
    setupMinPerDrone = 2.0
    sns.set_theme(style="whitegrid")

    ks = sorted(all_results)
    totalDistance = np.array([all_results[k][0] for k in ks], dtype=float)
    setupTime = np.array(ks, dtype=float) * setupMinPerDrone
    totalWithSetup = totalDistance + setupTime

    bestIdx = int(np.argmin(totalWithSetup))
    bestK = ks[bestIdx]
    bestY = totalWithSetup[bestIdx]

    # Prepare dataframe for seaborn
    df = pd.DataFrame({
        "DronesUsed": ks,
        "TotalDistance": totalDistance,
        "SetupTime": setupTime,
        "TotalWithSetup": totalWithSetup
    })

    dfMelted = df.melt(
        id_vars="DronesUsed",
        value_vars=["TotalDistance", "SetupTime", "TotalWithSetup"],
        var_name="Category",
        value_name="Value"
    )

    # Seaborn visualization
    linePlot = sns.lineplot(
        data=dfMelted,
        x="DronesUsed",
        y="Value",
        hue="Category",
        marker="o"
    )

    sns.scatterplot(x=[bestK], y=[bestY], color="black", s=80, zorder=5)
    linePlot.text(bestK + 0.1, bestY, f"Best tradeoff: {bestK} drones", fontsize=10)

    linePlot.set_xticks(ks)
    linePlot.set_xlabel("Number of Drones Used")
    linePlot.set_ylabel("Meters + Setup Time (2 min/drone)")
    linePlot.set_title("Drone Count vs Total Distance + Setup Time Tradeoff")

    plt.show()
    return None

def movePlotToDesktop(plotObj,filename,slideIn,dpi):
    desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
    folderPath = os.path.join(desktopPath, "visualizationRouteFolder")
    os.makedirs(folderPath, exist_ok=True)

    if not filename.lower().endswith(".jpeg"):
        filename += ".jpeg"


    outPath = os.path.join(folderPath, filename)

    # plotObj.save(outPath, width=slideIn,height=slideIn,dpi=dpi)
    plotObj.save(outPath, dpi=dpi, format="jpeg", facecolor="white")
    return None