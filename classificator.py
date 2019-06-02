import os
import sys

data = {}
reference = ''

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
				parser(os.path.join(sys.argv[1], fileName))
				if 'y' in input("Is " + fileName +\
				" - the reference? "):
					reference = fileName.split('.')[0]
		print(reference)
		dictToFilter = data[reference]
		for filter in data.keys():
			if filter != reference:
	                        dictToFilter = comparator(dictToFilter,\
					filter)
		return dictToFilter

def parser(path):
	global data
	protein = path.split('/')[-1].split('.')[0]
	data[protein] = {}
	fastaFile = open(path, 'r')
	csvFile = open(path.split('.')[0] + '.csv', 'r')
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

def comparator(dictToFilter, filter):
	for species in dictToFilter.keys():
		minInDictToFilter = min(float(dictToFilter[species].items()))
		minInFilter = min(float(dictToFilter[species].items()))
		if minInDictToFilter > minInFilter:
			dictToFilter.pop(species)
main()
