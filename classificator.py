import os
import sys
from dBugFileWork import argumentCheck, filesCheck

class BlastResult:
    '''Object for storing properties of a single BLAST result

    .fasta is for aminoacid sequence
    .Evalue is for E-value
    '''
    def __init__(self, f='', e=''):
        self.fasta = f
        self.Evalue = e

class BlastResultDataSet(dict):
    '''Object for storing all paralogs BLAST results

    A dictionary without the KeyError exception
    '''
    def __init__(self, fastaList):
        for fastaFile in fastaList:
            self[fastaFile.split('.')[0]] = {}

    def fillingIn(self, resultPath):
        '''Filling in the whole dataset
        '''
        protein = os.path.split(resultPath)[-1].split('.')[0]
        fastaFile = open(resultPath, 'r')
        csvFile = open(os.path.splitext(resultPath)[0] + '.csv', 'r')
        fastaLine = fastaFile.readline()
        csvLine = csvFile.readline()
        while fastaLine:
            AN = fastaLine.split(' ')[0][1:]
            species = fastaLine.split('[')[1][:-2].replace(' ', '_')
            if AN == csvLine.split(',')[1]:
                self.addSpecies(protein, species, AN, fastaLine)
                self.addEvalue(protein, species, AN, csvLine)
                fastaBlock = ''
                fastaLine = fastaFile.readline()
                while fastaLine and (not '>' in fastaLine):
                    fastaBlock += fastaLine
                    fastaLine = fastaFile.readline()
                self.addFasta(protein, species, AN, fastaBlock)
            else:
                csvLine = csvFile.readline()
        fastaFile.close()
        csvFile.close()

    def addSpecies(self, protein, species, AN, fastaLine):
        '''Add species information, create BlastResult object
        '''
        if not (species in self[protein]):
            self[protein][species] = {}
        self[protein][species][AN] = BlastResult()

    def addFasta(self, protein, species, AN, fastaBlock):
        '''Add fasta sequence for 1 result
        '''
        self[protein][species][AN].fasta = fastaBlock

    def addEvalue(self, protein, species, AN, csvLine):
        '''Add E-value for 1 result
        '''
        self[protein][species][AN].Evalue = float(csvLine.split(',')[-3])

def main():
    argumentCheck(2)
    fastaList = filesCheck(sys.argv[1])
    data = BlastResultDataSet(fastaList)
    for fastaFile in fastaList:
        data.fillingIn(os.path.join(sys.argv[1], fastaFile))
        if 'y' in input("Is " + fastaFile + " - the reference (y/not y) "):
                reference = fastaFile.split('.')[0]
    dictToFilter = data[reference]
    data.pop(reference)
    for p in data.keys():
        dictToFilter = comparator(dictToFilter, data[p])
    return dictToFilter

def comparator(dictToFilter, dictFilter):
    for species in list(dictToFilter):
        try:
            for AN in list(dictToFilter[species]):
                if AN in dictFilter[species].keys():
                    referenceE = dictToFilter[species][AN].Evalue
                    testingE = dictFilter[species][AN].Evalue
                    if referenceE > testingE:
                        dictToFilter[species].pop(AN)
        except KeyError:
            pass
    return dictToFilter

result = main()

output = open('out.fasta', 'w')

maximum = float(1e-10)
for key, value in result.items():
    AN = ''
    fasta = ''
    for k,v in value.items():
        if maximum > v.Evalue:
            AN = k
            fasta = v.fasta
            output.write('>' + AN + ':' + key + '\n')
            output.write(fasta)
output.close()
