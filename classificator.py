import os
import sys

class BlastResult:
	def __init__(self, f, e):
		self.fasta = f
		self.Evalue = e

class BlastResultDataSet(dict):
	def __getitem__(self, item):
		try:
			return dict.__getitem__(self, item)
		except KeyError:
			value = self[item] = type(self)()
			return value

	#def addProteins(path):

	#def addProteins(path):
		

data = BlastResultDataSet()

def filesCheck(path):
	fastaList = []
	for fileName in os.listdir(path):
		with open(os.path.join(path, fileName)) as file:
			firstLine = file.readline()
		file.close()
		csv = fileName.split('.')[0] + ".csv"
		if (firstLine[0] == '>') and \
		(csv in os.listdir(path)):
			print("Processing " + fileName\
				+ " and " \
				+ csv)
			fastaList.append(fileName)
	return fastaList

def main():
	global data
	if len(sys.argv) == 1:
		print("Please, write the directory with BLAST results " + \
			      "(fasta and csv) as an argument.")
		print("Restart manually")
	else:
		fastaList = filesCheck(sys.argv[1])
		for fileName in fastaList:
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
				data[protein][species][AN]=BlastResult(\
				fasta, Evalue)
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
					referenceE = \
					dictToFilter[species][AN].Evalue
					testingE = \
					dictFilter[species][AN].Evalue
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
