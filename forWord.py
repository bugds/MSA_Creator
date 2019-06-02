inFile = open('StandOut.fasta', 'r')
outFile = open('fW.txt', 'w')

fastaDict = dict()
line = inFile.readline()

while line:
    if line[0] == '>':
        species = line[:-1]
        while len(species) < 60:
            species += ' '
        fastaDict[species] = ''
        line = inFile.readline()
    if line[0] != '>':
        bigLine = ''
        while line:
            if line[0] != '>':
                bigLine += line[:-1]
            else:
                break
            line = inFile.readline()
        fastaDict[species] = bigLine

division = 6

for i in range(division):
    for key, value in fastaDict.items():
        outFile.write(key + value[i*len(value)//division:\
                                  (i+1)*len(value)//division] + '\n')
    outFile.write('\n***PAGE BREAK HERE***\n')

inFile.close()
outFile.close()
