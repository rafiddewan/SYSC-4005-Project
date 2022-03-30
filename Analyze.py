import csv


def main():
    rows = []
    with open('Replication_Stats.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rows.append(row)

    batches = [[0] * 10 for i in range(200)]
    for i in range(1,len(rows)):
        row = rows[i]
        batches[int(row[0]) - 1][((i-1) % 10)] = row

    with open("Analyzed.csv",'w', newline='') as outputF:
        writer = csv.writer(outputF)
        headers = ['Batch Number', 'avgThroughput', 'WK1', 'WK2', 'wk3', 'ins1', 'ins2', 'bf1', 'bf2','bf3', 'bf4', 'bf5']
        
        writer.writerow(headers)

        for batch in batches:
            averageThroughput = 0
            workstation1 = 0
            workstation2 = 0
            workstation3 = 0
            inspector1 = 0
            inspector2 = 0
            buffer1 = 0
            buffer2 = 0
            buffer3 = 0
            buffer4 = 0
            buffer5 = 0
            for run in batch:
                averageThroughput += float(run[1])
                workstation1 += float(run[2])
                workstation2 += float(run[3])
                workstation3 += float(run[4])
                inspector1 += float(run[5])
                inspector2 += float(run[6])
                buffer1 += float(run[7])
                buffer2 += float(run[8])
                buffer3 += float(run[9])
                buffer4 += float(run[10])
                buffer5 += float(run[11])
            averageThroughput = averageThroughput/len(batch)
            workstation1 = (workstation1/len(batch))/100
            workstation2 = (workstation2/len(batch))/100
            workstation3 = (workstation3/len(batch))/100
            inspector1 = (inspector1/len(batch))/100
            inspector2 = (inspector2/len(batch))/100
            buffer1 = buffer1/len(batch)
            buffer2 = buffer2/len(batch)
            buffer3 = buffer3/len(batch)
            buffer4 = buffer4/len(batch)
            buffer5 = buffer5/len(batch)
            newRow = [batch[0][0], averageThroughput, workstation1, workstation2, workstation3, inspector1, inspector2, buffer1,buffer2,buffer3,buffer4, buffer5] 
            writer.writerow(newRow)
        

    



if __name__ == "__main__":
    main()