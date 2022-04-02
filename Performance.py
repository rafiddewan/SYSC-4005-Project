from RandomNumberGeneration import RandomNumberGeneration
from Simulation import Simulation
import csv


class Performance:
    def __init__(self, numReplications):
        self.replications = []
        self.numReplications = numReplications

    def run(self):
        """
        Run the specified number of replications and keep track of each one
        Returns: None

        """
        g1 = RandomNumberGeneration(0, 0.0)
        seeds = g1.generateRandomNumberStreams(100000, 7)
        filename = "Replication_Output.csv"
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.getHeaders())
            for x in range(self.numReplications):
                print(f"\n------------------------------------Replication {x + 1}------------------------------------")
                print(f"\nSeeds being used: " + str(seeds))
                sim = Simulation(seeds)

                sim.run()
                seeds = sim.getXis()
                replication = sim.getStatistics()
                self.replications.append(replication)
                replication.printStats()
                row = replication.getReplicationData()
                row.insert(0,str(x+1))
                writer.writerow(row)

    def getHeaders(self):
        return ['Replication #', 'Throughput', 'Workstation 1 Busy %', 'Workstation 2 Busy %', 'Workstation 3 Busy %',
         'Inspector 1 Blocked %', 'Inspector 2 Blocked %', 'Buffer 1 Occupancy Average','Buffer 2 Occupancy Average', 'Buffer 3 Occupancy Average',
         'Buffer 4 Occupancy Average', 'Buffer 5 Occupancy Average']
def main():
    per = Performance(20)
    per.run()


if __name__ == "__main__":
   main()