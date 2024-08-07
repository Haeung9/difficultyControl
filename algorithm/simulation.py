import numpy as np
import time
import math
from . import difficulty

def mineABlock(param: difficulty.Difficulty, rng, power = 1.0) -> int:
    difficultyRatio = float(param.currentDifficulty()) / float(param.difficulty[0])
    # expectedBGT = max(param.thresholdPeriod * 1.4 * difficultyRatio / power, 1.000001)
    expectedBGT = max(param.targetBGT * difficultyRatio / power, 1.000001)
    BGT = rng.geometric(1.0 / expectedBGT)
    # BGT = math.ceil(BGT)
    param.nextDifficulty(float(BGT), uncle=False)
    return float(BGT)

def runConstantPowerSimulation(param: difficulty.Difficulty, numSim = 2000):
    seed = int(time.time())
    rng = np.random.default_rng(seed)
    blockGenerationTime = []
    for i in range(numSim):
        blockGenerationTime.append(mineABlock(param, rng, power=1.0))
    powerTrend = generatePowerTrend(type="constant", numSim=numSim)
    return {"BGT": blockGenerationTime, "difficulty": param.difficulty[1:], "power": powerTrend}

def runVariablePowerSimulation(param: difficulty.Difficulty, powerTrend = np.ones(2000, dtype=float)):
    seed = int(time.time())
    rng = np.random.default_rng(seed)
    blockGenerationTime = []
    numSim = len(powerTrend)
    for i in range(numSim):
        blockGenerationTime.append(mineABlock(param, rng, power=powerTrend[i]))
    return {"BGT": blockGenerationTime, "difficulty": param.difficulty[1:], "power": powerTrend}

def generatePowerTrend(type = "perturbation", numSim = 2000) -> np.ndarray:
    seed = int(time.time())
    rng = np.random.default_rng(seed)
    maxPower = 10.0
    minPower = 0.1

    if type == "perturbation":
        powerTrend = rng.normal(loc = 1.0, scale = math.sqrt(0.01), size= numSim)
    elif type == "steady increase":
        powerTrend = np.linspace(start=1.0, stop=maxPower, num=numSim, dtype=float)
    elif type == "steady decrease":
        powerTrend = np.linspace(start=1.0, stop=minPower, num=numSim, dtype=float)
    elif type == "steep increase":
        transitionPoint = int(numSim * 0.4)
        left = np.ones(transitionPoint, dtype=float)
        right = np.ones(numSim-transitionPoint, dtype=float) * maxPower
        powerTrend = np.concatenate((left, right))
    elif type == "steep decrease":
        transitionPoint = int(numSim * 0.4)
        left = np.ones(transitionPoint, dtype=float)
        right = np.ones(numSim-transitionPoint, dtype=float) * minPower
        powerTrend = np.concatenate((left, right))
    elif type == "constant":
        powerTrend = np.ones(numSim, dtype=float)
    elif type == "hard increase":
        transitionStartPoint = int(numSim * 0.4)
        transitionEndPoint = int(numSim * 0.6)
        left = np.ones(transitionStartPoint, dtype=float)
        middle = np.linspace(1.0, 4.0*maxPower, transitionEndPoint-transitionStartPoint, dtype=float)
        right = np.ones(numSim-transitionEndPoint, dtype=float) * 4.0 * maxPower
        powerTrend = np.concatenate((np.concatenate((left, middle)), right))
    else:
        print("Warning: undetermined power type")
        powerTrend = np.zeros(numSim, dtype=float)
    
    return powerTrend