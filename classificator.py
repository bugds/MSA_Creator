import os
import sys
from dBugFileWork import argumentCheck, filesCheck

class BlastResult:
    '''Object for storing properties of a single BLAST result

    .fasta is for aminoacid sequence
    .Evalue is for E-value
    '''
    def __init__(self, f, e):
        self.fasta = f
        self.Evalue = e

class BlastResultDataSet(dict):
    '''Object for storing all paralogs BLAST results

    A dictionary without the KeyError exception
    '''
    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            value = self[item] = type(self)()
            return value

    def fillingIn(path):
        '''Filling in the whole dataset
        '''
        

    def addFasta(path):
        '''Add fasta sequence for 1 result
        '''
        

    def addEvalue(path):
        '''Add E-value for 1 result
        '''
        

data = BlastResultDataSet()

def main():
    global data
    if argumentCheck(2):
        for fileName in filesCheck(sys.argv[1]):
            parser(fileName)
            if 'y' in input("Is " + fileName \
                    + " - the reference? " \
                    + "(y/not y) "):
                reference = fileName.split('.')[0]
        dictToFilter = data[reference]
        for p in data.pop(reference).keys():
            dictToFilter = comparator(dictToFilter, data[p])
        return dictToFilter

def parser(fileName):
    global data
    protein = fileName.split('.')[0]
    fastaFile = open(os.path.join(sys.argv[1], fileName), 'r')
    csvFile = open(os.path.join(sys.argv[1], fileName)\
               .replace('.*', '.csv'), 'r')
    fastaLine = fastaFile.readline()
    csvLine = ','
    while fastaLine:
        AN = fastaLine.split(' ')[0][1:]
        nextCsvLine = csvFile.readline()
        if nextCsvLine.split(',')[1] == csvLine.split(',')[1]:
            while nextCsvLine.split(',')[1] == csvLine.split(',')[1]:
                csvLine = csvFile.readline()
        else:
            csvLine = nextCsvLine
        if AN == csvLine.split(',')[1]:
            species = fastaLine.split('[')[1][:-2].replace(' ', '_')
            Evalue = float(csvLine.split(',')[-3])
            fasta = ''
            fastaLine = fastaFile.readline()
            while fastaLine and fastaLine[0] != '>':
                fasta += fastaLine
                fastaLine = fastaFile.readline()
                data[protein][species][AN]=BlastResult(fasta, Evalue)
        else:
            print(fastaLine + '\n' + csvLine)
            raise ValueError("Fasta and csv files do not match!")
    fastaFile.close()
    csvFile.close()

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
