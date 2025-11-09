import os
import numpy as np
import pandas as pd
import seaborn as sns
import seaborn.objects as so

def visAllDronePaths():
    sns.set_theme()
    sns.lineplot(x="Number of Drones Used", y="Minutes")
    return None

def visTimeDroneTradeOff(all_results):
    sns.set_theme()
    # sns.lineplot(x="Number of Drones Used", y="Minutes")
    return None

def movePlotToDesktop():
    return None