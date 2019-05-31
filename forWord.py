inFile = open('in.fasta', 'r')
outFile = open('out.fasta', 'w')

fastaDict = dict()
line = inFile.readline()

while line:
    if line[0] == '>':
        spec = line.split('[')[1][:-2].replace(' ', '_')
        spec += '_(' + line.split(' ')[0][1:] + ')'
        while len(spec) < 50:
            spec += ' '
        fastaDict[spec] = ''
        line = inFile.readline()
    if line[0] != '>':
        bigLine = ''
        while line:
            if line[0] != '>':
                bigLine += line[:-1]
            else:
                break
            line = inFile.readline()
        fastaDict[spec] = bigLine

for key, value in fastaDict.items():
    outFile.write(key + value[:len(value)//2] + '\n')
outFile.write('\n')
for key, value in fastaDict.items():
    outFile.write(key + value[len(value)//2:] + '\n')

'''
for key, value in fastaDict.items():
    outFile.write(key + value[:len(value)//3] + '\n')
outFile.write('\n')
for key, value in fastaDict.items():
    outFile.write(key + value[len(value)//3:2*len(value)//3] + '\n')
outFile.write('\n')
for key, value in fastaDict.items():
    outFile.write(key + value[2*len(value)//3:] + '\n')
'''

inFile.close()
outFile.close()
