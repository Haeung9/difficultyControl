import math
class Difficulty:
    def __init__(self, sensitivity = (1.0/8.0), minDifficulty = 1024, initDifficulty = (2**28), thresholdPeriod = 7.0):
        self.sensitivity = sensitivity
        self.minDifficulty = minDifficulty
        self.thresholdPeriod = float(thresholdPeriod)
        # self.targetBGT = 9.8668 # for threshold period = 7.0
        if self.thresholdPeriod == 7.0:
            self.targetBGT = 9.8668
        elif self.thresholdPeriod == 8.0:
            self.targetBGT = 11.3114
        elif self.thresholdPeriod == 9.0:
            self.targetBGT = 12.755
        elif self.thresholdPeriod == 10.0:
            self.targetBGT = 14.1978
        else:
            self.targetBGT = (self.thresholdPeriod / math.log(2.0)) + 0.5 - (0.5/math.log(2.0))
            print("warning: unexpected threshold. Target BGT can be inaccurate.")
        
        self.difficulty = [initDifficulty]
        self.uncle = [False]

    def currentDifficulty(self) -> int:
        return self.difficulty[-1]
    
    def nextDifficulty(self, blockGenerationTime: float, uncle = False) -> int:
        currentDifficulty = self.currentDifficulty()
        numerator = 1.0 - math.floor((blockGenerationTime)/ self.thresholdPeriod)
        numerator = numerator + 1.0 if self.uncle[-1] else numerator
        nextDifficulty = int(float(currentDifficulty) * (1.0 + (numerator * self.sensitivity)))
        nextDifficulty = max(nextDifficulty, self.minDifficulty)
        self.difficulty.append(nextDifficulty)
        self.uncle.append(uncle)
        return nextDifficulty

