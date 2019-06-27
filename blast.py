from Bio.Blast import NCBIWWW, NCBIXML

class SingleBlastResult:
    '''Object for storing properties of a single BLAST result

    .fasta is for aminoacid sequence
    .eValue is for E-value
    .queryCover is for query cover
    '''
    def __init__(self, f=None, e=None, c=None, i=None):
        self.fasta = f
        self.eValue = e
        self.queryCover = c
        self.ident = i

class BlastResultDataSet(dict):
    '''Object for storing all BLAST results
    '''
    def __init__(self, result):
        for alignment in result.alignments:
            species = alignment.title.split('[')[1].split(']')[0]
            for hsp in alignment.hsps:
                if hsp.expect < 10e-10:
                    accession = alignment.accession
                    if species not in self:
                        self[species] = {}
                    if accession not in self[species]:
                        self[species][accession] = \
                        SingleBlastResult(e=hsp.expect)
                    elif self[species][accession].eValue > hsp.expect:
                        print(">1 hsps!! on " + accession)
def blastSearch():
    accession = input("Query: ")
    if "y" in input("Limit search to Homo sapiens? "):
        entrez = 'Homo Sapiens'
        hitlist = 5
    else:
        entrez = None
        hitlist = 50
    result = NCBIXML.read(NCBIWWW.qblast(
                              'blastp',\
                              'refseq_protein',\
                              accession,\
                              entrez_query = entrez,\
                              hitlist_size = hitlist
                              ))
    dataSet = BlastResultDataSet(result)
    for species in dataSet.keys():
        print(species)
        for accession in dataSet[species].keys():
            print(accession)

blastSearch()
