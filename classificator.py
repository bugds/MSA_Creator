import os
import sys

data = {}
reference = 'MeCP2_1'

class BlastResult:
	def __init__(self, f, e):
		self.fasta = f
		self.Evalue = e

#class BlastResultDataSet(dict):
#       def __init__:
#               self.addSpecies
#               self.addProteins
#       def addSpecies(pathToBlastResults) - get species
#       def addProteins(pathToBlastResults) - get AN and fasta

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
				print("Processing " + fileName + " and " \
						+ fileName.split('.')[0] \
						+ ".csv")
				parser(fileName)
				if 'y' in input("Is " + fileName \
						+ " - the reference? " \
						+ "(y/not y) "):
					reference = fileName.split('.')[0]
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
			Evalue = float(csvLine.split(',')[-3])
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
			for AN in list(dictToFilter[species]):
				try:
					referenceE = \
					dictToFilter[species][AN].Evalue
					testingE = \
					dictFilter[species][AN].Evalue
					if referenceE > testingE:
						dictToFilter[species].pop(AN)
				except KeyError:
					pass
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
