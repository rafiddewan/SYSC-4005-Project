from RandomNumberGeneration import RandomNumberGeneration
from Simulation import Simulation


class Performance:
    def __init__(self, numReplications):
        self.replications = []
        self.numReplications = numReplications

    def run(self):
        g1 = RandomNumberGeneration(0, 0.0)
        seeds = g1.generateRandomNumberStreams(100000, 6)
        for x in range(self.numReplications):
            print(f"\n------------------------------------Replication {x + 1}------------------------------------")
            print(f"\nSeeds being used: " + str(seeds))
            sim = Simulation(seeds)

            sim.run()
            seeds = sim.getXis()
            replication = sim.getStatistics()
            self.replications.append(replication)
            replication.printStats()


def main():
    per = Performance(10)
    per.run()


if __name__ == "__main__":
   main()