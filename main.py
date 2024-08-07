from algorithm import difficulty, simulation, analysis
import os
import pandas as pd
import matplotlib.pyplot as plt

def main(numSim, cwd, sensitivities, powerTypes):

    for i in range(len(sensitivities)):
        param = difficulty.Difficulty(sensitivity=sensitivities[i], thresholdPeriod=7.0)
        fileName = os.path.join(cwd, "result_"+ str(1.0/sensitivities[i]) + "_" + powerTypes[i] + ".csv")
        if powerTypes[i] == "constant":
            result = simulation.runConstantPowerSimulation(param, numSim)
        else:
            powerTrend = simulation.generatePowerTrend(type=powerTypes[i], numSim=numSim)
            result = simulation.runVariablePowerSimulation(param, powerTrend)
        df = pd.DataFrame(data=result)
        df.to_csv(fileName)

if __name__ == "__main__":
    numSim = 20000
    cwd = os.getcwd()
    sensitivities = [1.0/64.0]
    powerTypes = ["steep decrease" for i in range(len(sensitivities))] # "constant" "perturbation" "steady increase" "steep increase" "steady decrease" "steep decrease" "hard increase"

    main(numSim, cwd, sensitivities, powerTypes)
    analysis.main(sensitivities, powerTypes, cwd)

    plt.show()
