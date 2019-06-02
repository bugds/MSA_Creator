import os
import sys

data = {}
reference = 'MeCP2_1'

class BlastResult:
	def __init__(self, f, e):
		self.fasta = f
		self.Evalue = e

def main():
	global data
	if len(sys.argv) == 1:
		print("Please, write the directory with BLAST results " + \
			      "(fasta and csv) as an argument.")
		print("Restart manually")
	else:
		for fileName in os.listdir(sys.argv[1]):
			with open(os.path.join(sys.argv[1], fileName)) as file:
				firstLine = file.readline()
			file.close()
			if firstLine[0] == '>':
				print("Processing " + fileName + " and " +\
					fileName.split('.')[0] + ".csv")
				parser(fileName)
				#if 'y' in input("Is " + fileName +\
				#" - the reference? "):
				#	reference = fileName.split('.')[0]
		dictToFilter = data[reference]
		for p in data.keys():
			if p != reference:
				dictToFilter = comparator(dictToFilter,\
					data[p])
		return dictToFilter

def parser(fileName):
	global data
	protein = fileName.split('.')[0]
	data[protein] = {}
	fastaFile = open(os.path.join(sys.argv[1], fileName), 'r')
	csvFile = open(os.path.join(sys.argv[1], fileName)\
		       .replace('.txt', '.csv'), 'r')
	fastaLine = fastaFile.readline()
	csvLine = ','
	while fastaLine:
		AN = fastaLine.split(' ')[0][1:]
		nextCsvLine = csvFile.readline()
		if nextCsvLine.split(',')[1] == csvLine.split(',')[1]:
			while nextCsvLine.split(',')[1] ==\
			csvLine.split(',')[1]:
				csvLine = csvFile.readline()
		else:
			csvLine = nextCsvLine
		if AN == csvLine.split(',')[1]:
			species = fastaLine.split('[')[1][:-2]\
					   .replace(' ', '_')
			Evalue = csvLine.split(',')[-3]
			fasta = ''
			fastaLine = fastaFile.readline()
			while fastaLine and fastaLine[0] != '>':
				fasta += fastaLine
				fastaLine = fastaFile.readline()
			try:
				data[protein][species][AN]=BlastResult(\
				fasta, Evalue)
			except KeyError:
				data[protein][species] = {AN:BlastResult(\
				fasta, Evalue)}
		else:
			print(fastaLine + '\n' + csvLine)
			raise ValueError("Fasta and csv files do not match!")
	fastaFile.close()
	csvFile.close()

def comparator(dictToFilter, dictFilter):
	for species in list(dictToFilter):
                try:
                        minDictToFilter = min([float(item[1].Evalue) for item\
					in dictToFilter[species].items()])
                        minDictFilter = min([float(item[1].Evalue) for item\
					in dictFilter[species].items()])
                        if minDictToFilter > minDictFilter:
                                dictToFilter.pop(species)
                except KeyError:
                        print('y')
                        pass
	return dictToFilter

for key, item in main().items():
        minimum = 10
        AN = ''
        fasta = ''
        for i in item.items():
                if minimum > float(i[1].Evalue):
                        minimum = float(i[1].Evalue)
                        AN = i[0]
                        fasta = i[1].fasta
        print('>' + key + ':_(' + AN + ')')
        print(fasta)
