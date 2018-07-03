from __future__ import division
import csv
import numpy as np


# Going to store the graphs as dicts
# Keys: individuals
# Value: List of ordered pairs: (other individual, edge weight)

class ConversationGraph:
    def __init__(self, mat=None):
        # mat should be numpy array, square adjacency matrix
        if mat: self.mat = mat


    #Matrix foramt
    def loadGraphfromCSV(self, csvPath):
        with open(csvPath, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            header = next(reader)

            subjects = header[1:]

            for i, row in enumerate(reader):
                if (row[0] != subjects[i]):
                    print ("Data format must be square")
                    return False

                self.graph[row[0]] = [(header[x+1], row[x+1]) for x in range(0, len(subjects))]

            if ((i+1) != len(row)-1):
                print ("Size of data must be square")
                return False

            return True

    # Should be in format subID, partnerID, attr1, attr1, ... round
    # Should also be in order
    def loadGraphfromCSV2(self, csvPath, header=True, attrCol=2, roundNum=1, startingID=None):
        mat = []

        with open(csvPath, 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            if header: header = next(reader)

            if startingID: subID = startingID
            else: startingID = (roundNum - 1) * 20
            subRatings = []
            insertSelf = False

            for row in reader:
                # Only the right round
                if int(row[-1]) != roundNum:
                    continue

                # If found a new subject, reset the subID and list
                if int(row[0]) != subID:
                    mat.append(subRatings)
                    subID = int(row[0])
                    subRatings = []
                    insertSelf = False

                # Assuming in order, if looking at next subID, insert self first
                if int(row[1]) == (subID + 1) and insertSelf == False:
                    insertSelf = True
                    subRatings.append(0)

                # Otherwise append to row
                subRatings.append(int(row[attrCol]))

            subRatings.append(0)
            mat.append(subRatings)

        self.mat = np.array(mat)

    def getStochasticGraph(self, method='Proportion'):

        if (method == "Rank"):
            n = len(self.graph)
            N = (n*(n-1))/2

            for key, value in self.graph.items():
                tmp = []
                for i, other in enumerate(value.sort(key=lambda x: x[1])):
                    tmp.append((other[0], (n-i)/N))

                self.stochMat[key] = tmp.sort(key=lambda x: x[0])

        #Proportion of total score
        if (method == "Proportion"):
            self.stochMat = self.mat/self.mat.sum(axis=0)
