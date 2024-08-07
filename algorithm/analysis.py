import os
import pandas as pd
import matplotlib.pyplot as plt

def main(sensitivities: list, powerTypes: list, dir: os.PathLike):
    fig_difficulty, ax_difficulty = plt.subplots()
    plt.title("Difficulty")
    plt.xlabel("block")
    plt.ylabel("difficulty")
    fig_power, ax_power = plt.subplots()
    plt.title("Computing Power")
    plt.xlabel("block")
    plt.ylabel("computing power (ratio to initial power)")
    legendSTR = []
    lineColors = ['lightgray', 'springgreen', 'orange', 'royalblue', 'gray', 'yellow', 'red', 'blue']
    lineColors = ['tab:blue']
    for i in range(len(sensitivities)):
        fileName = os.path.join(dir, "result_"+ str(1.0/sensitivities[i]) + "_" + powerTypes[i] + ".csv")
        try:
            df = pd.read_csv(fileName)
        except:
            print("Warning: cannot find file")
            continue
        lineColor = lineColors[i%len(lineColors)]
        plt.figure()
        df["BGT"].hist(bins=range(int(df["BGT"].max())))
        titleSTR = "BGT Histogram (sensitivity = 1/" + str(int(1.0/sensitivities[i])) + ", power type: " + powerTypes[i] + ")"
        plt.title(titleSTR)
        ax_power.plot(df["power"], color=lineColor)
        ax_difficulty.plot(df["difficulty"], color=lineColor)
        legendSTR.append("sensitivity = 1/" + str(int(1.0/sensitivities[i])))
        transitionPoint = int(len(df) * 0.4)
        steadyPoint = int(len(df) * 0.6)
        print("BGT statistics for sensitivity = 1/" + str(int(1.0/sensitivities[i])) + ", power type: " + powerTypes[i] + ")")
        print("    mean BGT: " + str(df["BGT"].mean()))        
        print("    mean BGT (before transition point): " + str(df["BGT"].loc[0:transitionPoint].mean()))
        print("    mean BGT (after transition end): " + str(df["BGT"].loc[steadyPoint:].mean()))
        print("    maximum BGT: " + str(df["BGT"].max()))
        print("    variance BGT: " + str(df["BGT"].var()))
        print("    variance BGT (before transition point): " + str(df["BGT"].loc[0:transitionPoint].var()))
        print("    variance BGT (after transition end): " + str(df["BGT"].loc[steadyPoint:].var()))
        print("Difficulty statistics for sensitivity = 1/" + str(int(1.0/sensitivities[i])) + ", power type: " + powerTypes[i] + ")")
        print("    mean difficulty: " + str(df["difficulty"].mean()))
        print("    maximum difficulty: " + str(df["difficulty"].max()))
        print("    minimum difficulty: " + str(df["difficulty"].min()))
        print("    mean difficulty (before transition point): " + str(df["difficulty"].loc[0:transitionPoint].mean()))
        print("    mean difficulty (after transition end): " + str(df["difficulty"].loc[steadyPoint:].mean()))
        print("    variance difficulty: " + str(df["difficulty"].var()))
        print("    variance difficulty (before transition point): " + str(df["difficulty"].loc[0:transitionPoint].var()))
        print("    variance difficulty (after transition end): " + str(df["difficulty"].loc[steadyPoint:].var()))
        

    fig_difficulty.legend(legendSTR)
    fig_power.legend(legendSTR)

if __name__ == "__main__":
    sensitivities = [1.0/64.0]
    powerTypes = ["steep decrease" for i in range(len(sensitivities))] # "constant" "perturbation" "steady increase" "steep increase" "steady decrease" "steep decrease"
    # dir = os.path.join(os.getcwd(), "data")
    dir = os.getcwd()
    main(sensitivities, powerTypes, dir)
    plt.show()