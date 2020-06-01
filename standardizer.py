import sys
import os

def fileParser(path):
    file = open(path, 'r')
    line = file.readline()
    intermedList = []
    while line:
        intermedList.append(line.replace(' ', '_')[:-1])
        line = file.readline()
    file.close()
    return intermedList

def fastaParser(path):
    file = open(path, 'r')
    line = file.readline()
    speciesDict = dict()
    while line:
        if line[0] == '>':
            analyzedProtein = line[1:-1]
            speciesDict[analyzedProtein] = ''
        else:
            speciesDict[analyzedProtein] += line
        line = file.readline()
    file.close()
    return speciesDict

def fastaGenerator(speciesList, speciesDict):
    file = open('StandOut.fasta', 'w')
    for species in speciesList:
        for protein in speciesDict.keys():
            if species in protein:
                file.write('>' + protein + '\n' + speciesDict[protein])
    file.close()

def main():
    speciesList = []
    for fileName in sorted(os.listdir('Species')):
        speciesList.extend(fileParser('Species/' + fileName))
    fastaGenerator(speciesList, fastaParser('MSA.txt'))
    
main()

# !!! Write down species in out.fasta, but not in Species folder !!!
