#!/usr/bin/python3

import sys
import os

def fastaParser(path):
        file = open(path, 'r')
        line = '#'
        speciesDict = dict()
        analyzedSpecies = ''
        sequenceToSave = False
        while line:
                if line[0] == '>':
                        sequenceToSave = False
                        analyzedSpecies = ''
                        if line.split('[')[1][:-2].replace(' ', '_') \
                        not in speciesDict:
                                analyzedSpecies = \
                                line.split('[')[1][:-2].replace(' ', '_')
                                speciesDict[analyzedSpecies] = ''
                                sequenceToSave = True
                elif sequenceToSave:
                        speciesDict[analyzedSpecies] += line
                line = file.readline()
        file.close()
        return speciesDict

def comparator(dictToFilter, dictFilter):
        intersect = dict()
        for key, value in dictToFilter.items():
                try:
                        if dictFilter[key] != value:
                                intersect[key] = value
                except KeyError:
                        pass
        return intersect

def main():
        dataArray = []
        if len(sys.argv) == 1:
                print("Please, write the directory with BLAST results" + \
                      "in FASTA format as arguments.")
        else:
                for fileName in os.listdir(sys.argv[1]):
                        with open(os.path.join(sys.argv[1], fileName)) as file:
                                firstLine = file.readline()
                        file.close()
                        if firstLine[0] == '>':
                                print("Processing " + fileName)
                                dataArray.append(fastaParser \
                                        (os.path.join(sys.argv[1], fileName)))
                                print("Is " + fileName + " - the reference?")
                                if 'y' in input():
                                        dataArray[0], dataArray[-1] = \
                                        dataArray[-1], dataArray[0]
                        else:
                                print(fileName + " will not be processed")
                dictToFilter = dataArray[0]
                for dictFilter in dataArray[1:]:
                        dictToFilter = comparator(dictToFilter, dictFilter)
        return dictToFilter

file = open('out.txt', 'w')
result = main()
for key, value in result.items():
        file.write('>' + key + '\n' + value)
file.close()
