import sys
import os

def fileParser(path):
    file = open(path, 'r')
    line = file.readline()
    intermedList = []
    while line:
        intermedList.append(line)
        line = file.readline()
    file.close()
    return intermedList

def fastaParser(path):
    file = open(path, 'r')
    line = file.readline()
    speciesDict = dict()
    while line:
        if line[0] == '>':
            analyzedSpecies = line.split('/')[0][1:] \
                + ' ' \
                + line.split(' ')[1][:-1]
            speciesDict[analyzedSpecies] = ''
        else:
            speciesDict[analyzedSpecies] += line
        line = file.readline()
    file.close()
    return speciesDict

def fastaGenerator(speciesList, speciesDict):
    file = open('./StandOut.fasta', 'w')
    for species in speciesList:
        try:
            file.write('>' + species + speciesDict[species[:-1]])
        except KeyError:
            pass
    file.close()

def main():
    speciesList = []
    for fileName in os.listdir('./Species'):
        speciesList.extend(fileParser('./Species/' + fileName))
    fastaGenerator(speciesList, fastaParser('./alignment.fasta'))
    
main()
