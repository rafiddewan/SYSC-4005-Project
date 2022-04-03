from RandomNumberGeneration import RandomNumberGeneration
from Simulation import Simulation
import csv

IS_ROUND_ROBIN = True

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

        filename = "RoundRobin_Production_Run.csv" if IS_ROUND_ROBIN else "Priority_Queue_Production_Run.csv"
        with open(filename, 'w', encoding='UTF8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.getHeaders())
            for x in range(self.numReplications):
                print(f"\n------------------------------------Replication {x + 1}------------------------------------")
                print(f"\nSeeds being used: " + str(seeds))
                sim = Simulation(seeds, IS_ROUND_ROBIN)

                sim.run()
                seeds = sim.getXis()
                replication = sim.getStatistics()
                self.replications.append(replication)
                replication.printStats()
                row = replication.getReplicationData()
                row.insert(0, str(x+1))
                writer.writerow(row)

    def getHeaders(self):
        return ['Replication #', 'Throughput', 'Workstation 1 Busy Prob', 'Workstation 2 Busy Prob', 'Workstation 3 Busy Prob',
         'Inspector 1 Blocked Prob', 'Inspector 2 Blocked Prob', 'Buffer 1 Occupancy Average','Buffer 2 Occupancy Average', 'Buffer 3 Occupancy Average',
         'Buffer 4 Occupancy Average', 'Buffer 5 Occupancy Average']
def main():
    per = Performance(20)
    per.run()


if __name__ == "__main__":
   main()