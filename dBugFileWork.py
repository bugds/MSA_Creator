import os
import sys

def argumentCheck(numberOfArguments):
    if len(sys.argv) < numberOfArguments:
        print("Please, write the directory with BLAST results " + \
                  "(fasta and csv) as an argument.")
        print("Restart manually")
        raise Exception("Wrong arguments")
    return True

def filesCheck(path, twoFiles = 1):
    fastaList = []
    for fileName in os.listdir(path):
        with open(os.path.join(path, fileName)) as file:
            firstLine = file.readline()
        file.close()
        if firstLine[0] == '>':
            if twoFiles:
                secondFile = fileName.split('.')[0] + ".csv"
                # Or any other checking condition
                if secondFile in os.listdir(path):
                    print("Processing " + fileName\
                    + " and " + secondFile)
                else:
                    raise Exception("Additional file not found")
            else:
                print("Processing " + fileName)
            fastaList.append(fileName)
        else:
            print(fileName + " is not fasta")
    return fastaList
