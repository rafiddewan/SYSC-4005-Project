from RandomNumberGeneration import RandomNumberGeneration
from Simulation import Simulation
import csv


class Performance:
    def __init__(self, numReplications):
        self.replications = []
        self.numReplications = numReplications

    def writeStatsToCsv(self, filename):
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            headers = ['Batch Number', 'Throughput']
            for key in (self.replications[0]).getProbabilityWorkstationBusy().keys():
                headers.append("Workstation " + str(key) + " Busy %")

            for key in self.replications[0].getProbabilityInspectorBlocked().keys():
                headers.append("Inspector " + str(key) + " Blocked %")

            for key in self.replications[0].getAvgBufferOccupancy().keys():
                headers.append("Buffer " + str(key) + " Occupancy Average")
            
            writer.writerow(headers)



    def run(self):
        g1 = RandomNumberGeneration(0, 0.0)
        seeds = g1.generateRandomNumberStreams(100000, 6)
        filename = "Replication_Stats.csv"
        
        for x in range(self.numReplications):
            print(f"\n------------------------------------Replication {x + 1}------------------------------------")
            print(f"\nSeeds being used: " + str(seeds))
            sim = Simulation(seeds)

            sim.run()
            seeds = sim.getXis()
            replication = sim.getStatistics()
            self.replications.append(replication)

        self.writeStatsToCsv(filename)
        for replication in self.replications:
            replication.printStats()
            replication.writeStatsToCsv(filename)


def main():
    per = Performance(10)
    per.run()


if __name__ == "__main__":
   main()