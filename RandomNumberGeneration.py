import math


class RandomNumberGeneration:
    a = 16807
    c = 0
    m = 2147283647
    x0 = 1234567

    def __init__(self, xi: int, lmbda: float):
        self.xi = xi
        self.lmbda = lmbda
        self.ri = -1.0

    def generateRandomServiceTime(self, title) -> float:
        self.__lcm()
        print(title + " ri = " + str(self.ri))
        serviceTime = ((-1)/self.lmbda) * math.log(self.ri)
        return serviceTime

    def generateRandomNumberStreams(self, b: int, numBlocks: int):
        seeds = {}
        xj = self.x0
        seeds[0] = self.x0
        currJ = 0
        for i in range(numBlocks):
            for j in range(currJ, i*b):
                xj = self.__lcm(xj)
            currJ = i*b
            seeds[currJ] = xj
        return seeds

    def __lcm(self):
        self.xi = (self.a * self.ri + self.c) % self.m
        self.ri = self.xi / self.m
        return self.xi
