import math
import numpy as np


class RandomNumberGeneration:
    a = 16807
    c = 0
    m = 2147483647
    x0 = 1234567

    def __init__(self, xi: int, lmbda: float):
        self.xi = xi
        self.lmbda = lmbda
        self.ri = -1.0

    def generateRandomServiceTime(self) -> float:
        self.__lcm()
        self.ri = self.xi / (self.m + 1)
        serviceTime = ((-1)/self.lmbda) * np.log(self.ri)
        return serviceTime

    def generateRandomNumberStreams(self, b: int, numBlocks: int):
        seeds = {}
        self.xi = self.x0
        seeds[0] = self.x0
        currJ = 0
        for i in range(numBlocks):
            for j in range(currJ, i*b):
                self.__lcm()
            currJ = i*b
            seeds[currJ] = self.xi
        return seeds

    def __lcm(self):
        self.xi = (self.a * self.xi + self.c) % self.m
