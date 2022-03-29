import math
import numpy as np


class RandomNumberGeneration:
    ## These values were chosen from Deliverable 2 and have been tested to make sure they are not correlated and uniform
    a = 16807
    c = 0
    m = 2147483647
    x0 = 1234567

    def __init__(self, xi: int, lmbda: float):
        """
        Initialize the random number generator
        Args:
            xi: The initial seed value
            lmbda: The lambda value for this exponential number generator
        """
        self.xi = xi
        self.lmbda = lmbda
        self.ri = -1.0

    def generateRandomServiceTime(self) -> float:
        """
        Generates a random number to use as a service time. This uses the inverse transform technique for an exponential
        distribution
        Returns: A random number that follows the exponential distribution

        """
        self.__lcm()
        self.ri = self.xi / (self.m + 1)
        serviceTime = ((-1)/self.lmbda) * np.log(self.ri)
        return serviceTime

    def generateRandomNumberStreams(self, b: int, numBlocks: int):
        """
        Generate streams of random digits using the lowest congruential method
        Args:
            b: How far each stream should be
            numBlocks: The number of blocksyou'd like

        Returns: A dictionary with the i value of where the stream starts at and the according xi value
        The xi value should be used as the seed for that specific stream

        """
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
        """
        Lowest congruential method to generate random numbers
        Returns: A random number

        """
        self.xi = (self.a * self.xi + self.c) % self.m
