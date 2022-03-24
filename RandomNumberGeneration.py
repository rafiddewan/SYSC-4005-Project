import random
from Buffer import Buffer
from Event import Event
from EventType import EventType
from InspectorEvent import InspectorEvent
from Component import Component
from WorkstationEvent import WorkstationEvent
import numpy as np


class RandomNumberGeneration:
    a = 16807
    c = 0
    m = 2147283647
    x0 = 1234567

    def generateRandomNumberStreams(self, b: long, numBlocks: int):
        seeds = {}
        xj = self.x0
        seeds[0] = self.x0
        currJ = 0
        for i in range(numBlocks):
            for j in range(currJ, i*b):
                xj = self.__lcm(xj)
            currJ = i*b
            print(currJ)
            seeds[currJ] = xj
        return seeds

    def lcm(self, xi):
        return (self.a * xi + self.c) % self.m

    def generateRandomServiceTime(self, lmda, ri):
        return (-1)/lmda * numpy.log(ri)
