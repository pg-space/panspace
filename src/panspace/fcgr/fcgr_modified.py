"""
same class FCGR than here https://github.com/AlgoLab/complexCGR/blob/master/complexcgr/fcgr.py
but when the class FCGR is initialized, kmer2pixel dictionary is loaded (already precomputed
"""

from complexcgr import FCGR 
# from .precomputed_encodings import (
#     _6mer2pixel,
#     _7mer2pixel,
#     _8mer2pixel,
#     # _9mer2pixel,
# )

class FCGRmodified(FCGR):

    def __init__(self, k: int, use_canonical_kmers: bool = False , bits: int = 8):
        super().__init__(k, use_canonical_kmers)
        self.k = k # k-mer representation
        self.use_canonical_kmers = use_canonical_kmers
        # self.kmers = list("".join(kmer) for kmer in product("ACGT", repeat=self.k))

        if use_canonical_kmers is True:
            self.kmer2pixel = self._kmer2pixel_canonical_kmers()        
        else:
            self.kmer2pixel = self.kmer2pixel_position()
    
        self.bits = bits
        self.max_color = 2**bits-1    

    def kmer2pixel_position(self,):        
        kmer2pixel = KMER2PIXEL #eval(f"_{self.k}mer2pixel")
        return kmer2pixel
    

KMER2PIXEL={
    "AAAAAA": [
        1,
        64
    ],
    "AAAAAC": [
        1,
        32
    ],
    "AAAAAG": [
        33,
        32
    ],
    "AAAAAT": [
        33,
        64
    ],
    "AAAACA": [
        1,
        48
    ],
    "AAAACC": [
        1,
        16
    ],
    "AAAACG": [
        33,
        16
    ],
    "AAAACT": [
        33,
        48
    ],
    "AAAAGA": [
        17,
        48
    ],
    "AAAAGC": [
        17,
        16
    ],
    "AAAAGG": [
        49,
        16
    ],
    "AAAAGT": [
        49,
        48
    ],
    "AAAATA": [
        17,
        64
    ],
    "AAAATC": [
        17,
        32
    ],
    "AAAATG": [
        49,
        32
    ],
    "AAAATT": [
        49,
        64
    ],
    "AAACAA": [
        1,
        56
    ],
    "AAACAC": [
        1,
        24
    ],
    "AAACAG": [
        33,
        24
    ],
    "AAACAT": [
        33,
        56
    ],
    "AAACCA": [
        1,
        40
    ],
    "AAACCC": [
        1,
        8
    ],
    "AAACCG": [
        33,
        8
    ],
    "AAACCT": [
        33,
        40
    ],
    "AAACGA": [
        17,
        40
    ],
    "AAACGC": [
        17,
        8
    ],
    "AAACGG": [
        49,
        8
    ],
    "AAACGT": [
        49,
        40
    ],
    "AAACTA": [
        17,
        56
    ],
    "AAACTC": [
        17,
        24
    ],
    "AAACTG": [
        49,
        24
    ],
    "AAACTT": [
        49,
        56
    ],
    "AAAGAA": [
        9,
        56
    ],
    "AAAGAC": [
        9,
        24
    ],
    "AAAGAG": [
        41,
        24
    ],
    "AAAGAT": [
        41,
        56
    ],
    "AAAGCA": [
        9,
        40
    ],
    "AAAGCC": [
        9,
        8
    ],
    "AAAGCG": [
        41,
        8
    ],
    "AAAGCT": [
        41,
        40
    ],
    "AAAGGA": [
        25,
        40
    ],
    "AAAGGC": [
        25,
        8
    ],
    "AAAGGG": [
        57,
        8
    ],
    "AAAGGT": [
        57,
        40
    ],
    "AAAGTA": [
        25,
        56
    ],
    "AAAGTC": [
        25,
        24
    ],
    "AAAGTG": [
        57,
        24
    ],
    "AAAGTT": [
        57,
        56
    ],
    "AAATAA": [
        9,
        64
    ],
    "AAATAC": [
        9,
        32
    ],
    "AAATAG": [
        41,
        32
    ],
    "AAATAT": [
        41,
        64
    ],
    "AAATCA": [
        9,
        48
    ],
    "AAATCC": [
        9,
        16
    ],
    "AAATCG": [
        41,
        16
    ],
    "AAATCT": [
        41,
        48
    ],
    "AAATGA": [
        25,
        48
    ],
    "AAATGC": [
        25,
        16
    ],
    "AAATGG": [
        57,
        16
    ],
    "AAATGT": [
        57,
        48
    ],
    "AAATTA": [
        25,
        64
    ],
    "AAATTC": [
        25,
        32
    ],
    "AAATTG": [
        57,
        32
    ],
    "AAATTT": [
        57,
        64
    ],
    "AACAAA": [
        1,
        60
    ],
    "AACAAC": [
        1,
        28
    ],
    "AACAAG": [
        33,
        28
    ],
    "AACAAT": [
        33,
        60
    ],
    "AACACA": [
        1,
        44
    ],
    "AACACC": [
        1,
        12
    ],
    "AACACG": [
        33,
        12
    ],
    "AACACT": [
        33,
        44
    ],
    "AACAGA": [
        17,
        44
    ],
    "AACAGC": [
        17,
        12
    ],
    "AACAGG": [
        49,
        12
    ],
    "AACAGT": [
        49,
        44
    ],
    "AACATA": [
        17,
        60
    ],
    "AACATC": [
        17,
        28
    ],
    "AACATG": [
        49,
        28
    ],
    "AACATT": [
        49,
        60
    ],
    "AACCAA": [
        1,
        52
    ],
    "AACCAC": [
        1,
        20
    ],
    "AACCAG": [
        33,
        20
    ],
    "AACCAT": [
        33,
        52
    ],
    "AACCCA": [
        1,
        36
    ],
    "AACCCC": [
        1,
        4
    ],
    "AACCCG": [
        33,
        4
    ],
    "AACCCT": [
        33,
        36
    ],
    "AACCGA": [
        17,
        36
    ],
    "AACCGC": [
        17,
        4
    ],
    "AACCGG": [
        49,
        4
    ],
    "AACCGT": [
        49,
        36
    ],
    "AACCTA": [
        17,
        52
    ],
    "AACCTC": [
        17,
        20
    ],
    "AACCTG": [
        49,
        20
    ],
    "AACCTT": [
        49,
        52
    ],
    "AACGAA": [
        9,
        52
    ],
    "AACGAC": [
        9,
        20
    ],
    "AACGAG": [
        41,
        20
    ],
    "AACGAT": [
        41,
        52
    ],
    "AACGCA": [
        9,
        36
    ],
    "AACGCC": [
        9,
        4
    ],
    "AACGCG": [
        41,
        4
    ],
    "AACGCT": [
        41,
        36
    ],
    "AACGGA": [
        25,
        36
    ],
    "AACGGC": [
        25,
        4
    ],
    "AACGGG": [
        57,
        4
    ],
    "AACGGT": [
        57,
        36
    ],
    "AACGTA": [
        25,
        52
    ],
    "AACGTC": [
        25,
        20
    ],
    "AACGTG": [
        57,
        20
    ],
    "AACGTT": [
        57,
        52
    ],
    "AACTAA": [
        9,
        60
    ],
    "AACTAC": [
        9,
        28
    ],
    "AACTAG": [
        41,
        28
    ],
    "AACTAT": [
        41,
        60
    ],
    "AACTCA": [
        9,
        44
    ],
    "AACTCC": [
        9,
        12
    ],
    "AACTCG": [
        41,
        12
    ],
    "AACTCT": [
        41,
        44
    ],
    "AACTGA": [
        25,
        44
    ],
    "AACTGC": [
        25,
        12
    ],
    "AACTGG": [
        57,
        12
    ],
    "AACTGT": [
        57,
        44
    ],
    "AACTTA": [
        25,
        60
    ],
    "AACTTC": [
        25,
        28
    ],
    "AACTTG": [
        57,
        28
    ],
    "AACTTT": [
        57,
        60
    ],
    "AAGAAA": [
        5,
        60
    ],
    "AAGAAC": [
        5,
        28
    ],
    "AAGAAG": [
        37,
        28
    ],
    "AAGAAT": [
        37,
        60
    ],
    "AAGACA": [
        5,
        44
    ],
    "AAGACC": [
        5,
        12
    ],
    "AAGACG": [
        37,
        12
    ],
    "AAGACT": [
        37,
        44
    ],
    "AAGAGA": [
        21,
        44
    ],
    "AAGAGC": [
        21,
        12
    ],
    "AAGAGG": [
        53,
        12
    ],
    "AAGAGT": [
        53,
        44
    ],
    "AAGATA": [
        21,
        60
    ],
    "AAGATC": [
        21,
        28
    ],
    "AAGATG": [
        53,
        28
    ],
    "AAGATT": [
        53,
        60
    ],
    "AAGCAA": [
        5,
        52
    ],
    "AAGCAC": [
        5,
        20
    ],
    "AAGCAG": [
        37,
        20
    ],
    "AAGCAT": [
        37,
        52
    ],
    "AAGCCA": [
        5,
        36
    ],
    "AAGCCC": [
        5,
        4
    ],
    "AAGCCG": [
        37,
        4
    ],
    "AAGCCT": [
        37,
        36
    ],
    "AAGCGA": [
        21,
        36
    ],
    "AAGCGC": [
        21,
        4
    ],
    "AAGCGG": [
        53,
        4
    ],
    "AAGCGT": [
        53,
        36
    ],
    "AAGCTA": [
        21,
        52
    ],
    "AAGCTC": [
        21,
        20
    ],
    "AAGCTG": [
        53,
        20
    ],
    "AAGCTT": [
        53,
        52
    ],
    "AAGGAA": [
        13,
        52
    ],
    "AAGGAC": [
        13,
        20
    ],
    "AAGGAG": [
        45,
        20
    ],
    "AAGGAT": [
        45,
        52
    ],
    "AAGGCA": [
        13,
        36
    ],
    "AAGGCC": [
        13,
        4
    ],
    "AAGGCG": [
        45,
        4
    ],
    "AAGGCT": [
        45,
        36
    ],
    "AAGGGA": [
        29,
        36
    ],
    "AAGGGC": [
        29,
        4
    ],
    "AAGGGG": [
        61,
        4
    ],
    "AAGGGT": [
        61,
        36
    ],
    "AAGGTA": [
        29,
        52
    ],
    "AAGGTC": [
        29,
        20
    ],
    "AAGGTG": [
        61,
        20
    ],
    "AAGGTT": [
        61,
        52
    ],
    "AAGTAA": [
        13,
        60
    ],
    "AAGTAC": [
        13,
        28
    ],
    "AAGTAG": [
        45,
        28
    ],
    "AAGTAT": [
        45,
        60
    ],
    "AAGTCA": [
        13,
        44
    ],
    "AAGTCC": [
        13,
        12
    ],
    "AAGTCG": [
        45,
        12
    ],
    "AAGTCT": [
        45,
        44
    ],
    "AAGTGA": [
        29,
        44
    ],
    "AAGTGC": [
        29,
        12
    ],
    "AAGTGG": [
        61,
        12
    ],
    "AAGTGT": [
        61,
        44
    ],
    "AAGTTA": [
        29,
        60
    ],
    "AAGTTC": [
        29,
        28
    ],
    "AAGTTG": [
        61,
        28
    ],
    "AAGTTT": [
        61,
        60
    ],
    "AATAAA": [
        5,
        64
    ],
    "AATAAC": [
        5,
        32
    ],
    "AATAAG": [
        37,
        32
    ],
    "AATAAT": [
        37,
        64
    ],
    "AATACA": [
        5,
        48
    ],
    "AATACC": [
        5,
        16
    ],
    "AATACG": [
        37,
        16
    ],
    "AATACT": [
        37,
        48
    ],
    "AATAGA": [
        21,
        48
    ],
    "AATAGC": [
        21,
        16
    ],
    "AATAGG": [
        53,
        16
    ],
    "AATAGT": [
        53,
        48
    ],
    "AATATA": [
        21,
        64
    ],
    "AATATC": [
        21,
        32
    ],
    "AATATG": [
        53,
        32
    ],
    "AATATT": [
        53,
        64
    ],
    "AATCAA": [
        5,
        56
    ],
    "AATCAC": [
        5,
        24
    ],
    "AATCAG": [
        37,
        24
    ],
    "AATCAT": [
        37,
        56
    ],
    "AATCCA": [
        5,
        40
    ],
    "AATCCC": [
        5,
        8
    ],
    "AATCCG": [
        37,
        8
    ],
    "AATCCT": [
        37,
        40
    ],
    "AATCGA": [
        21,
        40
    ],
    "AATCGC": [
        21,
        8
    ],
    "AATCGG": [
        53,
        8
    ],
    "AATCGT": [
        53,
        40
    ],
    "AATCTA": [
        21,
        56
    ],
    "AATCTC": [
        21,
        24
    ],
    "AATCTG": [
        53,
        24
    ],
    "AATCTT": [
        53,
        56
    ],
    "AATGAA": [
        13,
        56
    ],
    "AATGAC": [
        13,
        24
    ],
    "AATGAG": [
        45,
        24
    ],
    "AATGAT": [
        45,
        56
    ],
    "AATGCA": [
        13,
        40
    ],
    "AATGCC": [
        13,
        8
    ],
    "AATGCG": [
        45,
        8
    ],
    "AATGCT": [
        45,
        40
    ],
    "AATGGA": [
        29,
        40
    ],
    "AATGGC": [
        29,
        8
    ],
    "AATGGG": [
        61,
        8
    ],
    "AATGGT": [
        61,
        40
    ],
    "AATGTA": [
        29,
        56
    ],
    "AATGTC": [
        29,
        24
    ],
    "AATGTG": [
        61,
        24
    ],
    "AATGTT": [
        61,
        56
    ],
    "AATTAA": [
        13,
        64
    ],
    "AATTAC": [
        13,
        32
    ],
    "AATTAG": [
        45,
        32
    ],
    "AATTAT": [
        45,
        64
    ],
    "AATTCA": [
        13,
        48
    ],
    "AATTCC": [
        13,
        16
    ],
    "AATTCG": [
        45,
        16
    ],
    "AATTCT": [
        45,
        48
    ],
    "AATTGA": [
        29,
        48
    ],
    "AATTGC": [
        29,
        16
    ],
    "AATTGG": [
        61,
        16
    ],
    "AATTGT": [
        61,
        48
    ],
    "AATTTA": [
        29,
        64
    ],
    "AATTTC": [
        29,
        32
    ],
    "AATTTG": [
        61,
        32
    ],
    "AATTTT": [
        61,
        64
    ],
    "ACAAAA": [
        1,
        62
    ],
    "ACAAAC": [
        1,
        30
    ],
    "ACAAAG": [
        33,
        30
    ],
    "ACAAAT": [
        33,
        62
    ],
    "ACAACA": [
        1,
        46
    ],
    "ACAACC": [
        1,
        14
    ],
    "ACAACG": [
        33,
        14
    ],
    "ACAACT": [
        33,
        46
    ],
    "ACAAGA": [
        17,
        46
    ],
    "ACAAGC": [
        17,
        14
    ],
    "ACAAGG": [
        49,
        14
    ],
    "ACAAGT": [
        49,
        46
    ],
    "ACAATA": [
        17,
        62
    ],
    "ACAATC": [
        17,
        30
    ],
    "ACAATG": [
        49,
        30
    ],
    "ACAATT": [
        49,
        62
    ],
    "ACACAA": [
        1,
        54
    ],
    "ACACAC": [
        1,
        22
    ],
    "ACACAG": [
        33,
        22
    ],
    "ACACAT": [
        33,
        54
    ],
    "ACACCA": [
        1,
        38
    ],
    "ACACCC": [
        1,
        6
    ],
    "ACACCG": [
        33,
        6
    ],
    "ACACCT": [
        33,
        38
    ],
    "ACACGA": [
        17,
        38
    ],
    "ACACGC": [
        17,
        6
    ],
    "ACACGG": [
        49,
        6
    ],
    "ACACGT": [
        49,
        38
    ],
    "ACACTA": [
        17,
        54
    ],
    "ACACTC": [
        17,
        22
    ],
    "ACACTG": [
        49,
        22
    ],
    "ACACTT": [
        49,
        54
    ],
    "ACAGAA": [
        9,
        54
    ],
    "ACAGAC": [
        9,
        22
    ],
    "ACAGAG": [
        41,
        22
    ],
    "ACAGAT": [
        41,
        54
    ],
    "ACAGCA": [
        9,
        38
    ],
    "ACAGCC": [
        9,
        6
    ],
    "ACAGCG": [
        41,
        6
    ],
    "ACAGCT": [
        41,
        38
    ],
    "ACAGGA": [
        25,
        38
    ],
    "ACAGGC": [
        25,
        6
    ],
    "ACAGGG": [
        57,
        6
    ],
    "ACAGGT": [
        57,
        38
    ],
    "ACAGTA": [
        25,
        54
    ],
    "ACAGTC": [
        25,
        22
    ],
    "ACAGTG": [
        57,
        22
    ],
    "ACAGTT": [
        57,
        54
    ],
    "ACATAA": [
        9,
        62
    ],
    "ACATAC": [
        9,
        30
    ],
    "ACATAG": [
        41,
        30
    ],
    "ACATAT": [
        41,
        62
    ],
    "ACATCA": [
        9,
        46
    ],
    "ACATCC": [
        9,
        14
    ],
    "ACATCG": [
        41,
        14
    ],
    "ACATCT": [
        41,
        46
    ],
    "ACATGA": [
        25,
        46
    ],
    "ACATGC": [
        25,
        14
    ],
    "ACATGG": [
        57,
        14
    ],
    "ACATGT": [
        57,
        46
    ],
    "ACATTA": [
        25,
        62
    ],
    "ACATTC": [
        25,
        30
    ],
    "ACATTG": [
        57,
        30
    ],
    "ACATTT": [
        57,
        62
    ],
    "ACCAAA": [
        1,
        58
    ],
    "ACCAAC": [
        1,
        26
    ],
    "ACCAAG": [
        33,
        26
    ],
    "ACCAAT": [
        33,
        58
    ],
    "ACCACA": [
        1,
        42
    ],
    "ACCACC": [
        1,
        10
    ],
    "ACCACG": [
        33,
        10
    ],
    "ACCACT": [
        33,
        42
    ],
    "ACCAGA": [
        17,
        42
    ],
    "ACCAGC": [
        17,
        10
    ],
    "ACCAGG": [
        49,
        10
    ],
    "ACCAGT": [
        49,
        42
    ],
    "ACCATA": [
        17,
        58
    ],
    "ACCATC": [
        17,
        26
    ],
    "ACCATG": [
        49,
        26
    ],
    "ACCATT": [
        49,
        58
    ],
    "ACCCAA": [
        1,
        50
    ],
    "ACCCAC": [
        1,
        18
    ],
    "ACCCAG": [
        33,
        18
    ],
    "ACCCAT": [
        33,
        50
    ],
    "ACCCCA": [
        1,
        34
    ],
    "ACCCCC": [
        1,
        2
    ],
    "ACCCCG": [
        33,
        2
    ],
    "ACCCCT": [
        33,
        34
    ],
    "ACCCGA": [
        17,
        34
    ],
    "ACCCGC": [
        17,
        2
    ],
    "ACCCGG": [
        49,
        2
    ],
    "ACCCGT": [
        49,
        34
    ],
    "ACCCTA": [
        17,
        50
    ],
    "ACCCTC": [
        17,
        18
    ],
    "ACCCTG": [
        49,
        18
    ],
    "ACCCTT": [
        49,
        50
    ],
    "ACCGAA": [
        9,
        50
    ],
    "ACCGAC": [
        9,
        18
    ],
    "ACCGAG": [
        41,
        18
    ],
    "ACCGAT": [
        41,
        50
    ],
    "ACCGCA": [
        9,
        34
    ],
    "ACCGCC": [
        9,
        2
    ],
    "ACCGCG": [
        41,
        2
    ],
    "ACCGCT": [
        41,
        34
    ],
    "ACCGGA": [
        25,
        34
    ],
    "ACCGGC": [
        25,
        2
    ],
    "ACCGGG": [
        57,
        2
    ],
    "ACCGGT": [
        57,
        34
    ],
    "ACCGTA": [
        25,
        50
    ],
    "ACCGTC": [
        25,
        18
    ],
    "ACCGTG": [
        57,
        18
    ],
    "ACCGTT": [
        57,
        50
    ],
    "ACCTAA": [
        9,
        58
    ],
    "ACCTAC": [
        9,
        26
    ],
    "ACCTAG": [
        41,
        26
    ],
    "ACCTAT": [
        41,
        58
    ],
    "ACCTCA": [
        9,
        42
    ],
    "ACCTCC": [
        9,
        10
    ],
    "ACCTCG": [
        41,
        10
    ],
    "ACCTCT": [
        41,
        42
    ],
    "ACCTGA": [
        25,
        42
    ],
    "ACCTGC": [
        25,
        10
    ],
    "ACCTGG": [
        57,
        10
    ],
    "ACCTGT": [
        57,
        42
    ],
    "ACCTTA": [
        25,
        58
    ],
    "ACCTTC": [
        25,
        26
    ],
    "ACCTTG": [
        57,
        26
    ],
    "ACCTTT": [
        57,
        58
    ],
    "ACGAAA": [
        5,
        58
    ],
    "ACGAAC": [
        5,
        26
    ],
    "ACGAAG": [
        37,
        26
    ],
    "ACGAAT": [
        37,
        58
    ],
    "ACGACA": [
        5,
        42
    ],
    "ACGACC": [
        5,
        10
    ],
    "ACGACG": [
        37,
        10
    ],
    "ACGACT": [
        37,
        42
    ],
    "ACGAGA": [
        21,
        42
    ],
    "ACGAGC": [
        21,
        10
    ],
    "ACGAGG": [
        53,
        10
    ],
    "ACGAGT": [
        53,
        42
    ],
    "ACGATA": [
        21,
        58
    ],
    "ACGATC": [
        21,
        26
    ],
    "ACGATG": [
        53,
        26
    ],
    "ACGATT": [
        53,
        58
    ],
    "ACGCAA": [
        5,
        50
    ],
    "ACGCAC": [
        5,
        18
    ],
    "ACGCAG": [
        37,
        18
    ],
    "ACGCAT": [
        37,
        50
    ],
    "ACGCCA": [
        5,
        34
    ],
    "ACGCCC": [
        5,
        2
    ],
    "ACGCCG": [
        37,
        2
    ],
    "ACGCCT": [
        37,
        34
    ],
    "ACGCGA": [
        21,
        34
    ],
    "ACGCGC": [
        21,
        2
    ],
    "ACGCGG": [
        53,
        2
    ],
    "ACGCGT": [
        53,
        34
    ],
    "ACGCTA": [
        21,
        50
    ],
    "ACGCTC": [
        21,
        18
    ],
    "ACGCTG": [
        53,
        18
    ],
    "ACGCTT": [
        53,
        50
    ],
    "ACGGAA": [
        13,
        50
    ],
    "ACGGAC": [
        13,
        18
    ],
    "ACGGAG": [
        45,
        18
    ],
    "ACGGAT": [
        45,
        50
    ],
    "ACGGCA": [
        13,
        34
    ],
    "ACGGCC": [
        13,
        2
    ],
    "ACGGCG": [
        45,
        2
    ],
    "ACGGCT": [
        45,
        34
    ],
    "ACGGGA": [
        29,
        34
    ],
    "ACGGGC": [
        29,
        2
    ],
    "ACGGGG": [
        61,
        2
    ],
    "ACGGGT": [
        61,
        34
    ],
    "ACGGTA": [
        29,
        50
    ],
    "ACGGTC": [
        29,
        18
    ],
    "ACGGTG": [
        61,
        18
    ],
    "ACGGTT": [
        61,
        50
    ],
    "ACGTAA": [
        13,
        58
    ],
    "ACGTAC": [
        13,
        26
    ],
    "ACGTAG": [
        45,
        26
    ],
    "ACGTAT": [
        45,
        58
    ],
    "ACGTCA": [
        13,
        42
    ],
    "ACGTCC": [
        13,
        10
    ],
    "ACGTCG": [
        45,
        10
    ],
    "ACGTCT": [
        45,
        42
    ],
    "ACGTGA": [
        29,
        42
    ],
    "ACGTGC": [
        29,
        10
    ],
    "ACGTGG": [
        61,
        10
    ],
    "ACGTGT": [
        61,
        42
    ],
    "ACGTTA": [
        29,
        58
    ],
    "ACGTTC": [
        29,
        26
    ],
    "ACGTTG": [
        61,
        26
    ],
    "ACGTTT": [
        61,
        58
    ],
    "ACTAAA": [
        5,
        62
    ],
    "ACTAAC": [
        5,
        30
    ],
    "ACTAAG": [
        37,
        30
    ],
    "ACTAAT": [
        37,
        62
    ],
    "ACTACA": [
        5,
        46
    ],
    "ACTACC": [
        5,
        14
    ],
    "ACTACG": [
        37,
        14
    ],
    "ACTACT": [
        37,
        46
    ],
    "ACTAGA": [
        21,
        46
    ],
    "ACTAGC": [
        21,
        14
    ],
    "ACTAGG": [
        53,
        14
    ],
    "ACTAGT": [
        53,
        46
    ],
    "ACTATA": [
        21,
        62
    ],
    "ACTATC": [
        21,
        30
    ],
    "ACTATG": [
        53,
        30
    ],
    "ACTATT": [
        53,
        62
    ],
    "ACTCAA": [
        5,
        54
    ],
    "ACTCAC": [
        5,
        22
    ],
    "ACTCAG": [
        37,
        22
    ],
    "ACTCAT": [
        37,
        54
    ],
    "ACTCCA": [
        5,
        38
    ],
    "ACTCCC": [
        5,
        6
    ],
    "ACTCCG": [
        37,
        6
    ],
    "ACTCCT": [
        37,
        38
    ],
    "ACTCGA": [
        21,
        38
    ],
    "ACTCGC": [
        21,
        6
    ],
    "ACTCGG": [
        53,
        6
    ],
    "ACTCGT": [
        53,
        38
    ],
    "ACTCTA": [
        21,
        54
    ],
    "ACTCTC": [
        21,
        22
    ],
    "ACTCTG": [
        53,
        22
    ],
    "ACTCTT": [
        53,
        54
    ],
    "ACTGAA": [
        13,
        54
    ],
    "ACTGAC": [
        13,
        22
    ],
    "ACTGAG": [
        45,
        22
    ],
    "ACTGAT": [
        45,
        54
    ],
    "ACTGCA": [
        13,
        38
    ],
    "ACTGCC": [
        13,
        6
    ],
    "ACTGCG": [
        45,
        6
    ],
    "ACTGCT": [
        45,
        38
    ],
    "ACTGGA": [
        29,
        38
    ],
    "ACTGGC": [
        29,
        6
    ],
    "ACTGGG": [
        61,
        6
    ],
    "ACTGGT": [
        61,
        38
    ],
    "ACTGTA": [
        29,
        54
    ],
    "ACTGTC": [
        29,
        22
    ],
    "ACTGTG": [
        61,
        22
    ],
    "ACTGTT": [
        61,
        54
    ],
    "ACTTAA": [
        13,
        62
    ],
    "ACTTAC": [
        13,
        30
    ],
    "ACTTAG": [
        45,
        30
    ],
    "ACTTAT": [
        45,
        62
    ],
    "ACTTCA": [
        13,
        46
    ],
    "ACTTCC": [
        13,
        14
    ],
    "ACTTCG": [
        45,
        14
    ],
    "ACTTCT": [
        45,
        46
    ],
    "ACTTGA": [
        29,
        46
    ],
    "ACTTGC": [
        29,
        14
    ],
    "ACTTGG": [
        61,
        14
    ],
    "ACTTGT": [
        61,
        46
    ],
    "ACTTTA": [
        29,
        62
    ],
    "ACTTTC": [
        29,
        30
    ],
    "ACTTTG": [
        61,
        30
    ],
    "ACTTTT": [
        61,
        62
    ],
    "AGAAAA": [
        3,
        62
    ],
    "AGAAAC": [
        3,
        30
    ],
    "AGAAAG": [
        35,
        30
    ],
    "AGAAAT": [
        35,
        62
    ],
    "AGAACA": [
        3,
        46
    ],
    "AGAACC": [
        3,
        14
    ],
    "AGAACG": [
        35,
        14
    ],
    "AGAACT": [
        35,
        46
    ],
    "AGAAGA": [
        19,
        46
    ],
    "AGAAGC": [
        19,
        14
    ],
    "AGAAGG": [
        51,
        14
    ],
    "AGAAGT": [
        51,
        46
    ],
    "AGAATA": [
        19,
        62
    ],
    "AGAATC": [
        19,
        30
    ],
    "AGAATG": [
        51,
        30
    ],
    "AGAATT": [
        51,
        62
    ],
    "AGACAA": [
        3,
        54
    ],
    "AGACAC": [
        3,
        22
    ],
    "AGACAG": [
        35,
        22
    ],
    "AGACAT": [
        35,
        54
    ],
    "AGACCA": [
        3,
        38
    ],
    "AGACCC": [
        3,
        6
    ],
    "AGACCG": [
        35,
        6
    ],
    "AGACCT": [
        35,
        38
    ],
    "AGACGA": [
        19,
        38
    ],
    "AGACGC": [
        19,
        6
    ],
    "AGACGG": [
        51,
        6
    ],
    "AGACGT": [
        51,
        38
    ],
    "AGACTA": [
        19,
        54
    ],
    "AGACTC": [
        19,
        22
    ],
    "AGACTG": [
        51,
        22
    ],
    "AGACTT": [
        51,
        54
    ],
    "AGAGAA": [
        11,
        54
    ],
    "AGAGAC": [
        11,
        22
    ],
    "AGAGAG": [
        43,
        22
    ],
    "AGAGAT": [
        43,
        54
    ],
    "AGAGCA": [
        11,
        38
    ],
    "AGAGCC": [
        11,
        6
    ],
    "AGAGCG": [
        43,
        6
    ],
    "AGAGCT": [
        43,
        38
    ],
    "AGAGGA": [
        27,
        38
    ],
    "AGAGGC": [
        27,
        6
    ],
    "AGAGGG": [
        59,
        6
    ],
    "AGAGGT": [
        59,
        38
    ],
    "AGAGTA": [
        27,
        54
    ],
    "AGAGTC": [
        27,
        22
    ],
    "AGAGTG": [
        59,
        22
    ],
    "AGAGTT": [
        59,
        54
    ],
    "AGATAA": [
        11,
        62
    ],
    "AGATAC": [
        11,
        30
    ],
    "AGATAG": [
        43,
        30
    ],
    "AGATAT": [
        43,
        62
    ],
    "AGATCA": [
        11,
        46
    ],
    "AGATCC": [
        11,
        14
    ],
    "AGATCG": [
        43,
        14
    ],
    "AGATCT": [
        43,
        46
    ],
    "AGATGA": [
        27,
        46
    ],
    "AGATGC": [
        27,
        14
    ],
    "AGATGG": [
        59,
        14
    ],
    "AGATGT": [
        59,
        46
    ],
    "AGATTA": [
        27,
        62
    ],
    "AGATTC": [
        27,
        30
    ],
    "AGATTG": [
        59,
        30
    ],
    "AGATTT": [
        59,
        62
    ],
    "AGCAAA": [
        3,
        58
    ],
    "AGCAAC": [
        3,
        26
    ],
    "AGCAAG": [
        35,
        26
    ],
    "AGCAAT": [
        35,
        58
    ],
    "AGCACA": [
        3,
        42
    ],
    "AGCACC": [
        3,
        10
    ],
    "AGCACG": [
        35,
        10
    ],
    "AGCACT": [
        35,
        42
    ],
    "AGCAGA": [
        19,
        42
    ],
    "AGCAGC": [
        19,
        10
    ],
    "AGCAGG": [
        51,
        10
    ],
    "AGCAGT": [
        51,
        42
    ],
    "AGCATA": [
        19,
        58
    ],
    "AGCATC": [
        19,
        26
    ],
    "AGCATG": [
        51,
        26
    ],
    "AGCATT": [
        51,
        58
    ],
    "AGCCAA": [
        3,
        50
    ],
    "AGCCAC": [
        3,
        18
    ],
    "AGCCAG": [
        35,
        18
    ],
    "AGCCAT": [
        35,
        50
    ],
    "AGCCCA": [
        3,
        34
    ],
    "AGCCCC": [
        3,
        2
    ],
    "AGCCCG": [
        35,
        2
    ],
    "AGCCCT": [
        35,
        34
    ],
    "AGCCGA": [
        19,
        34
    ],
    "AGCCGC": [
        19,
        2
    ],
    "AGCCGG": [
        51,
        2
    ],
    "AGCCGT": [
        51,
        34
    ],
    "AGCCTA": [
        19,
        50
    ],
    "AGCCTC": [
        19,
        18
    ],
    "AGCCTG": [
        51,
        18
    ],
    "AGCCTT": [
        51,
        50
    ],
    "AGCGAA": [
        11,
        50
    ],
    "AGCGAC": [
        11,
        18
    ],
    "AGCGAG": [
        43,
        18
    ],
    "AGCGAT": [
        43,
        50
    ],
    "AGCGCA": [
        11,
        34
    ],
    "AGCGCC": [
        11,
        2
    ],
    "AGCGCG": [
        43,
        2
    ],
    "AGCGCT": [
        43,
        34
    ],
    "AGCGGA": [
        27,
        34
    ],
    "AGCGGC": [
        27,
        2
    ],
    "AGCGGG": [
        59,
        2
    ],
    "AGCGGT": [
        59,
        34
    ],
    "AGCGTA": [
        27,
        50
    ],
    "AGCGTC": [
        27,
        18
    ],
    "AGCGTG": [
        59,
        18
    ],
    "AGCGTT": [
        59,
        50
    ],
    "AGCTAA": [
        11,
        58
    ],
    "AGCTAC": [
        11,
        26
    ],
    "AGCTAG": [
        43,
        26
    ],
    "AGCTAT": [
        43,
        58
    ],
    "AGCTCA": [
        11,
        42
    ],
    "AGCTCC": [
        11,
        10
    ],
    "AGCTCG": [
        43,
        10
    ],
    "AGCTCT": [
        43,
        42
    ],
    "AGCTGA": [
        27,
        42
    ],
    "AGCTGC": [
        27,
        10
    ],
    "AGCTGG": [
        59,
        10
    ],
    "AGCTGT": [
        59,
        42
    ],
    "AGCTTA": [
        27,
        58
    ],
    "AGCTTC": [
        27,
        26
    ],
    "AGCTTG": [
        59,
        26
    ],
    "AGCTTT": [
        59,
        58
    ],
    "AGGAAA": [
        7,
        58
    ],
    "AGGAAC": [
        7,
        26
    ],
    "AGGAAG": [
        39,
        26
    ],
    "AGGAAT": [
        39,
        58
    ],
    "AGGACA": [
        7,
        42
    ],
    "AGGACC": [
        7,
        10
    ],
    "AGGACG": [
        39,
        10
    ],
    "AGGACT": [
        39,
        42
    ],
    "AGGAGA": [
        23,
        42
    ],
    "AGGAGC": [
        23,
        10
    ],
    "AGGAGG": [
        55,
        10
    ],
    "AGGAGT": [
        55,
        42
    ],
    "AGGATA": [
        23,
        58
    ],
    "AGGATC": [
        23,
        26
    ],
    "AGGATG": [
        55,
        26
    ],
    "AGGATT": [
        55,
        58
    ],
    "AGGCAA": [
        7,
        50
    ],
    "AGGCAC": [
        7,
        18
    ],
    "AGGCAG": [
        39,
        18
    ],
    "AGGCAT": [
        39,
        50
    ],
    "AGGCCA": [
        7,
        34
    ],
    "AGGCCC": [
        7,
        2
    ],
    "AGGCCG": [
        39,
        2
    ],
    "AGGCCT": [
        39,
        34
    ],
    "AGGCGA": [
        23,
        34
    ],
    "AGGCGC": [
        23,
        2
    ],
    "AGGCGG": [
        55,
        2
    ],
    "AGGCGT": [
        55,
        34
    ],
    "AGGCTA": [
        23,
        50
    ],
    "AGGCTC": [
        23,
        18
    ],
    "AGGCTG": [
        55,
        18
    ],
    "AGGCTT": [
        55,
        50
    ],
    "AGGGAA": [
        15,
        50
    ],
    "AGGGAC": [
        15,
        18
    ],
    "AGGGAG": [
        47,
        18
    ],
    "AGGGAT": [
        47,
        50
    ],
    "AGGGCA": [
        15,
        34
    ],
    "AGGGCC": [
        15,
        2
    ],
    "AGGGCG": [
        47,
        2
    ],
    "AGGGCT": [
        47,
        34
    ],
    "AGGGGA": [
        31,
        34
    ],
    "AGGGGC": [
        31,
        2
    ],
    "AGGGGG": [
        63,
        2
    ],
    "AGGGGT": [
        63,
        34
    ],
    "AGGGTA": [
        31,
        50
    ],
    "AGGGTC": [
        31,
        18
    ],
    "AGGGTG": [
        63,
        18
    ],
    "AGGGTT": [
        63,
        50
    ],
    "AGGTAA": [
        15,
        58
    ],
    "AGGTAC": [
        15,
        26
    ],
    "AGGTAG": [
        47,
        26
    ],
    "AGGTAT": [
        47,
        58
    ],
    "AGGTCA": [
        15,
        42
    ],
    "AGGTCC": [
        15,
        10
    ],
    "AGGTCG": [
        47,
        10
    ],
    "AGGTCT": [
        47,
        42
    ],
    "AGGTGA": [
        31,
        42
    ],
    "AGGTGC": [
        31,
        10
    ],
    "AGGTGG": [
        63,
        10
    ],
    "AGGTGT": [
        63,
        42
    ],
    "AGGTTA": [
        31,
        58
    ],
    "AGGTTC": [
        31,
        26
    ],
    "AGGTTG": [
        63,
        26
    ],
    "AGGTTT": [
        63,
        58
    ],
    "AGTAAA": [
        7,
        62
    ],
    "AGTAAC": [
        7,
        30
    ],
    "AGTAAG": [
        39,
        30
    ],
    "AGTAAT": [
        39,
        62
    ],
    "AGTACA": [
        7,
        46
    ],
    "AGTACC": [
        7,
        14
    ],
    "AGTACG": [
        39,
        14
    ],
    "AGTACT": [
        39,
        46
    ],
    "AGTAGA": [
        23,
        46
    ],
    "AGTAGC": [
        23,
        14
    ],
    "AGTAGG": [
        55,
        14
    ],
    "AGTAGT": [
        55,
        46
    ],
    "AGTATA": [
        23,
        62
    ],
    "AGTATC": [
        23,
        30
    ],
    "AGTATG": [
        55,
        30
    ],
    "AGTATT": [
        55,
        62
    ],
    "AGTCAA": [
        7,
        54
    ],
    "AGTCAC": [
        7,
        22
    ],
    "AGTCAG": [
        39,
        22
    ],
    "AGTCAT": [
        39,
        54
    ],
    "AGTCCA": [
        7,
        38
    ],
    "AGTCCC": [
        7,
        6
    ],
    "AGTCCG": [
        39,
        6
    ],
    "AGTCCT": [
        39,
        38
    ],
    "AGTCGA": [
        23,
        38
    ],
    "AGTCGC": [
        23,
        6
    ],
    "AGTCGG": [
        55,
        6
    ],
    "AGTCGT": [
        55,
        38
    ],
    "AGTCTA": [
        23,
        54
    ],
    "AGTCTC": [
        23,
        22
    ],
    "AGTCTG": [
        55,
        22
    ],
    "AGTCTT": [
        55,
        54
    ],
    "AGTGAA": [
        15,
        54
    ],
    "AGTGAC": [
        15,
        22
    ],
    "AGTGAG": [
        47,
        22
    ],
    "AGTGAT": [
        47,
        54
    ],
    "AGTGCA": [
        15,
        38
    ],
    "AGTGCC": [
        15,
        6
    ],
    "AGTGCG": [
        47,
        6
    ],
    "AGTGCT": [
        47,
        38
    ],
    "AGTGGA": [
        31,
        38
    ],
    "AGTGGC": [
        31,
        6
    ],
    "AGTGGG": [
        63,
        6
    ],
    "AGTGGT": [
        63,
        38
    ],
    "AGTGTA": [
        31,
        54
    ],
    "AGTGTC": [
        31,
        22
    ],
    "AGTGTG": [
        63,
        22
    ],
    "AGTGTT": [
        63,
        54
    ],
    "AGTTAA": [
        15,
        62
    ],
    "AGTTAC": [
        15,
        30
    ],
    "AGTTAG": [
        47,
        30
    ],
    "AGTTAT": [
        47,
        62
    ],
    "AGTTCA": [
        15,
        46
    ],
    "AGTTCC": [
        15,
        14
    ],
    "AGTTCG": [
        47,
        14
    ],
    "AGTTCT": [
        47,
        46
    ],
    "AGTTGA": [
        31,
        46
    ],
    "AGTTGC": [
        31,
        14
    ],
    "AGTTGG": [
        63,
        14
    ],
    "AGTTGT": [
        63,
        46
    ],
    "AGTTTA": [
        31,
        62
    ],
    "AGTTTC": [
        31,
        30
    ],
    "AGTTTG": [
        63,
        30
    ],
    "AGTTTT": [
        63,
        62
    ],
    "ATAAAA": [
        3,
        64
    ],
    "ATAAAC": [
        3,
        32
    ],
    "ATAAAG": [
        35,
        32
    ],
    "ATAAAT": [
        35,
        64
    ],
    "ATAACA": [
        3,
        48
    ],
    "ATAACC": [
        3,
        16
    ],
    "ATAACG": [
        35,
        16
    ],
    "ATAACT": [
        35,
        48
    ],
    "ATAAGA": [
        19,
        48
    ],
    "ATAAGC": [
        19,
        16
    ],
    "ATAAGG": [
        51,
        16
    ],
    "ATAAGT": [
        51,
        48
    ],
    "ATAATA": [
        19,
        64
    ],
    "ATAATC": [
        19,
        32
    ],
    "ATAATG": [
        51,
        32
    ],
    "ATAATT": [
        51,
        64
    ],
    "ATACAA": [
        3,
        56
    ],
    "ATACAC": [
        3,
        24
    ],
    "ATACAG": [
        35,
        24
    ],
    "ATACAT": [
        35,
        56
    ],
    "ATACCA": [
        3,
        40
    ],
    "ATACCC": [
        3,
        8
    ],
    "ATACCG": [
        35,
        8
    ],
    "ATACCT": [
        35,
        40
    ],
    "ATACGA": [
        19,
        40
    ],
    "ATACGC": [
        19,
        8
    ],
    "ATACGG": [
        51,
        8
    ],
    "ATACGT": [
        51,
        40
    ],
    "ATACTA": [
        19,
        56
    ],
    "ATACTC": [
        19,
        24
    ],
    "ATACTG": [
        51,
        24
    ],
    "ATACTT": [
        51,
        56
    ],
    "ATAGAA": [
        11,
        56
    ],
    "ATAGAC": [
        11,
        24
    ],
    "ATAGAG": [
        43,
        24
    ],
    "ATAGAT": [
        43,
        56
    ],
    "ATAGCA": [
        11,
        40
    ],
    "ATAGCC": [
        11,
        8
    ],
    "ATAGCG": [
        43,
        8
    ],
    "ATAGCT": [
        43,
        40
    ],
    "ATAGGA": [
        27,
        40
    ],
    "ATAGGC": [
        27,
        8
    ],
    "ATAGGG": [
        59,
        8
    ],
    "ATAGGT": [
        59,
        40
    ],
    "ATAGTA": [
        27,
        56
    ],
    "ATAGTC": [
        27,
        24
    ],
    "ATAGTG": [
        59,
        24
    ],
    "ATAGTT": [
        59,
        56
    ],
    "ATATAA": [
        11,
        64
    ],
    "ATATAC": [
        11,
        32
    ],
    "ATATAG": [
        43,
        32
    ],
    "ATATAT": [
        43,
        64
    ],
    "ATATCA": [
        11,
        48
    ],
    "ATATCC": [
        11,
        16
    ],
    "ATATCG": [
        43,
        16
    ],
    "ATATCT": [
        43,
        48
    ],
    "ATATGA": [
        27,
        48
    ],
    "ATATGC": [
        27,
        16
    ],
    "ATATGG": [
        59,
        16
    ],
    "ATATGT": [
        59,
        48
    ],
    "ATATTA": [
        27,
        64
    ],
    "ATATTC": [
        27,
        32
    ],
    "ATATTG": [
        59,
        32
    ],
    "ATATTT": [
        59,
        64
    ],
    "ATCAAA": [
        3,
        60
    ],
    "ATCAAC": [
        3,
        28
    ],
    "ATCAAG": [
        35,
        28
    ],
    "ATCAAT": [
        35,
        60
    ],
    "ATCACA": [
        3,
        44
    ],
    "ATCACC": [
        3,
        12
    ],
    "ATCACG": [
        35,
        12
    ],
    "ATCACT": [
        35,
        44
    ],
    "ATCAGA": [
        19,
        44
    ],
    "ATCAGC": [
        19,
        12
    ],
    "ATCAGG": [
        51,
        12
    ],
    "ATCAGT": [
        51,
        44
    ],
    "ATCATA": [
        19,
        60
    ],
    "ATCATC": [
        19,
        28
    ],
    "ATCATG": [
        51,
        28
    ],
    "ATCATT": [
        51,
        60
    ],
    "ATCCAA": [
        3,
        52
    ],
    "ATCCAC": [
        3,
        20
    ],
    "ATCCAG": [
        35,
        20
    ],
    "ATCCAT": [
        35,
        52
    ],
    "ATCCCA": [
        3,
        36
    ],
    "ATCCCC": [
        3,
        4
    ],
    "ATCCCG": [
        35,
        4
    ],
    "ATCCCT": [
        35,
        36
    ],
    "ATCCGA": [
        19,
        36
    ],
    "ATCCGC": [
        19,
        4
    ],
    "ATCCGG": [
        51,
        4
    ],
    "ATCCGT": [
        51,
        36
    ],
    "ATCCTA": [
        19,
        52
    ],
    "ATCCTC": [
        19,
        20
    ],
    "ATCCTG": [
        51,
        20
    ],
    "ATCCTT": [
        51,
        52
    ],
    "ATCGAA": [
        11,
        52
    ],
    "ATCGAC": [
        11,
        20
    ],
    "ATCGAG": [
        43,
        20
    ],
    "ATCGAT": [
        43,
        52
    ],
    "ATCGCA": [
        11,
        36
    ],
    "ATCGCC": [
        11,
        4
    ],
    "ATCGCG": [
        43,
        4
    ],
    "ATCGCT": [
        43,
        36
    ],
    "ATCGGA": [
        27,
        36
    ],
    "ATCGGC": [
        27,
        4
    ],
    "ATCGGG": [
        59,
        4
    ],
    "ATCGGT": [
        59,
        36
    ],
    "ATCGTA": [
        27,
        52
    ],
    "ATCGTC": [
        27,
        20
    ],
    "ATCGTG": [
        59,
        20
    ],
    "ATCGTT": [
        59,
        52
    ],
    "ATCTAA": [
        11,
        60
    ],
    "ATCTAC": [
        11,
        28
    ],
    "ATCTAG": [
        43,
        28
    ],
    "ATCTAT": [
        43,
        60
    ],
    "ATCTCA": [
        11,
        44
    ],
    "ATCTCC": [
        11,
        12
    ],
    "ATCTCG": [
        43,
        12
    ],
    "ATCTCT": [
        43,
        44
    ],
    "ATCTGA": [
        27,
        44
    ],
    "ATCTGC": [
        27,
        12
    ],
    "ATCTGG": [
        59,
        12
    ],
    "ATCTGT": [
        59,
        44
    ],
    "ATCTTA": [
        27,
        60
    ],
    "ATCTTC": [
        27,
        28
    ],
    "ATCTTG": [
        59,
        28
    ],
    "ATCTTT": [
        59,
        60
    ],
    "ATGAAA": [
        7,
        60
    ],
    "ATGAAC": [
        7,
        28
    ],
    "ATGAAG": [
        39,
        28
    ],
    "ATGAAT": [
        39,
        60
    ],
    "ATGACA": [
        7,
        44
    ],
    "ATGACC": [
        7,
        12
    ],
    "ATGACG": [
        39,
        12
    ],
    "ATGACT": [
        39,
        44
    ],
    "ATGAGA": [
        23,
        44
    ],
    "ATGAGC": [
        23,
        12
    ],
    "ATGAGG": [
        55,
        12
    ],
    "ATGAGT": [
        55,
        44
    ],
    "ATGATA": [
        23,
        60
    ],
    "ATGATC": [
        23,
        28
    ],
    "ATGATG": [
        55,
        28
    ],
    "ATGATT": [
        55,
        60
    ],
    "ATGCAA": [
        7,
        52
    ],
    "ATGCAC": [
        7,
        20
    ],
    "ATGCAG": [
        39,
        20
    ],
    "ATGCAT": [
        39,
        52
    ],
    "ATGCCA": [
        7,
        36
    ],
    "ATGCCC": [
        7,
        4
    ],
    "ATGCCG": [
        39,
        4
    ],
    "ATGCCT": [
        39,
        36
    ],
    "ATGCGA": [
        23,
        36
    ],
    "ATGCGC": [
        23,
        4
    ],
    "ATGCGG": [
        55,
        4
    ],
    "ATGCGT": [
        55,
        36
    ],
    "ATGCTA": [
        23,
        52
    ],
    "ATGCTC": [
        23,
        20
    ],
    "ATGCTG": [
        55,
        20
    ],
    "ATGCTT": [
        55,
        52
    ],
    "ATGGAA": [
        15,
        52
    ],
    "ATGGAC": [
        15,
        20
    ],
    "ATGGAG": [
        47,
        20
    ],
    "ATGGAT": [
        47,
        52
    ],
    "ATGGCA": [
        15,
        36
    ],
    "ATGGCC": [
        15,
        4
    ],
    "ATGGCG": [
        47,
        4
    ],
    "ATGGCT": [
        47,
        36
    ],
    "ATGGGA": [
        31,
        36
    ],
    "ATGGGC": [
        31,
        4
    ],
    "ATGGGG": [
        63,
        4
    ],
    "ATGGGT": [
        63,
        36
    ],
    "ATGGTA": [
        31,
        52
    ],
    "ATGGTC": [
        31,
        20
    ],
    "ATGGTG": [
        63,
        20
    ],
    "ATGGTT": [
        63,
        52
    ],
    "ATGTAA": [
        15,
        60
    ],
    "ATGTAC": [
        15,
        28
    ],
    "ATGTAG": [
        47,
        28
    ],
    "ATGTAT": [
        47,
        60
    ],
    "ATGTCA": [
        15,
        44
    ],
    "ATGTCC": [
        15,
        12
    ],
    "ATGTCG": [
        47,
        12
    ],
    "ATGTCT": [
        47,
        44
    ],
    "ATGTGA": [
        31,
        44
    ],
    "ATGTGC": [
        31,
        12
    ],
    "ATGTGG": [
        63,
        12
    ],
    "ATGTGT": [
        63,
        44
    ],
    "ATGTTA": [
        31,
        60
    ],
    "ATGTTC": [
        31,
        28
    ],
    "ATGTTG": [
        63,
        28
    ],
    "ATGTTT": [
        63,
        60
    ],
    "ATTAAA": [
        7,
        64
    ],
    "ATTAAC": [
        7,
        32
    ],
    "ATTAAG": [
        39,
        32
    ],
    "ATTAAT": [
        39,
        64
    ],
    "ATTACA": [
        7,
        48
    ],
    "ATTACC": [
        7,
        16
    ],
    "ATTACG": [
        39,
        16
    ],
    "ATTACT": [
        39,
        48
    ],
    "ATTAGA": [
        23,
        48
    ],
    "ATTAGC": [
        23,
        16
    ],
    "ATTAGG": [
        55,
        16
    ],
    "ATTAGT": [
        55,
        48
    ],
    "ATTATA": [
        23,
        64
    ],
    "ATTATC": [
        23,
        32
    ],
    "ATTATG": [
        55,
        32
    ],
    "ATTATT": [
        55,
        64
    ],
    "ATTCAA": [
        7,
        56
    ],
    "ATTCAC": [
        7,
        24
    ],
    "ATTCAG": [
        39,
        24
    ],
    "ATTCAT": [
        39,
        56
    ],
    "ATTCCA": [
        7,
        40
    ],
    "ATTCCC": [
        7,
        8
    ],
    "ATTCCG": [
        39,
        8
    ],
    "ATTCCT": [
        39,
        40
    ],
    "ATTCGA": [
        23,
        40
    ],
    "ATTCGC": [
        23,
        8
    ],
    "ATTCGG": [
        55,
        8
    ],
    "ATTCGT": [
        55,
        40
    ],
    "ATTCTA": [
        23,
        56
    ],
    "ATTCTC": [
        23,
        24
    ],
    "ATTCTG": [
        55,
        24
    ],
    "ATTCTT": [
        55,
        56
    ],
    "ATTGAA": [
        15,
        56
    ],
    "ATTGAC": [
        15,
        24
    ],
    "ATTGAG": [
        47,
        24
    ],
    "ATTGAT": [
        47,
        56
    ],
    "ATTGCA": [
        15,
        40
    ],
    "ATTGCC": [
        15,
        8
    ],
    "ATTGCG": [
        47,
        8
    ],
    "ATTGCT": [
        47,
        40
    ],
    "ATTGGA": [
        31,
        40
    ],
    "ATTGGC": [
        31,
        8
    ],
    "ATTGGG": [
        63,
        8
    ],
    "ATTGGT": [
        63,
        40
    ],
    "ATTGTA": [
        31,
        56
    ],
    "ATTGTC": [
        31,
        24
    ],
    "ATTGTG": [
        63,
        24
    ],
    "ATTGTT": [
        63,
        56
    ],
    "ATTTAA": [
        15,
        64
    ],
    "ATTTAC": [
        15,
        32
    ],
    "ATTTAG": [
        47,
        32
    ],
    "ATTTAT": [
        47,
        64
    ],
    "ATTTCA": [
        15,
        48
    ],
    "ATTTCC": [
        15,
        16
    ],
    "ATTTCG": [
        47,
        16
    ],
    "ATTTCT": [
        47,
        48
    ],
    "ATTTGA": [
        31,
        48
    ],
    "ATTTGC": [
        31,
        16
    ],
    "ATTTGG": [
        63,
        16
    ],
    "ATTTGT": [
        63,
        48
    ],
    "ATTTTA": [
        31,
        64
    ],
    "ATTTTC": [
        31,
        32
    ],
    "ATTTTG": [
        63,
        32
    ],
    "ATTTTT": [
        63,
        64
    ],
    "CAAAAA": [
        1,
        63
    ],
    "CAAAAC": [
        1,
        31
    ],
    "CAAAAG": [
        33,
        31
    ],
    "CAAAAT": [
        33,
        63
    ],
    "CAAACA": [
        1,
        47
    ],
    "CAAACC": [
        1,
        15
    ],
    "CAAACG": [
        33,
        15
    ],
    "CAAACT": [
        33,
        47
    ],
    "CAAAGA": [
        17,
        47
    ],
    "CAAAGC": [
        17,
        15
    ],
    "CAAAGG": [
        49,
        15
    ],
    "CAAAGT": [
        49,
        47
    ],
    "CAAATA": [
        17,
        63
    ],
    "CAAATC": [
        17,
        31
    ],
    "CAAATG": [
        49,
        31
    ],
    "CAAATT": [
        49,
        63
    ],
    "CAACAA": [
        1,
        55
    ],
    "CAACAC": [
        1,
        23
    ],
    "CAACAG": [
        33,
        23
    ],
    "CAACAT": [
        33,
        55
    ],
    "CAACCA": [
        1,
        39
    ],
    "CAACCC": [
        1,
        7
    ],
    "CAACCG": [
        33,
        7
    ],
    "CAACCT": [
        33,
        39
    ],
    "CAACGA": [
        17,
        39
    ],
    "CAACGC": [
        17,
        7
    ],
    "CAACGG": [
        49,
        7
    ],
    "CAACGT": [
        49,
        39
    ],
    "CAACTA": [
        17,
        55
    ],
    "CAACTC": [
        17,
        23
    ],
    "CAACTG": [
        49,
        23
    ],
    "CAACTT": [
        49,
        55
    ],
    "CAAGAA": [
        9,
        55
    ],
    "CAAGAC": [
        9,
        23
    ],
    "CAAGAG": [
        41,
        23
    ],
    "CAAGAT": [
        41,
        55
    ],
    "CAAGCA": [
        9,
        39
    ],
    "CAAGCC": [
        9,
        7
    ],
    "CAAGCG": [
        41,
        7
    ],
    "CAAGCT": [
        41,
        39
    ],
    "CAAGGA": [
        25,
        39
    ],
    "CAAGGC": [
        25,
        7
    ],
    "CAAGGG": [
        57,
        7
    ],
    "CAAGGT": [
        57,
        39
    ],
    "CAAGTA": [
        25,
        55
    ],
    "CAAGTC": [
        25,
        23
    ],
    "CAAGTG": [
        57,
        23
    ],
    "CAAGTT": [
        57,
        55
    ],
    "CAATAA": [
        9,
        63
    ],
    "CAATAC": [
        9,
        31
    ],
    "CAATAG": [
        41,
        31
    ],
    "CAATAT": [
        41,
        63
    ],
    "CAATCA": [
        9,
        47
    ],
    "CAATCC": [
        9,
        15
    ],
    "CAATCG": [
        41,
        15
    ],
    "CAATCT": [
        41,
        47
    ],
    "CAATGA": [
        25,
        47
    ],
    "CAATGC": [
        25,
        15
    ],
    "CAATGG": [
        57,
        15
    ],
    "CAATGT": [
        57,
        47
    ],
    "CAATTA": [
        25,
        63
    ],
    "CAATTC": [
        25,
        31
    ],
    "CAATTG": [
        57,
        31
    ],
    "CAATTT": [
        57,
        63
    ],
    "CACAAA": [
        1,
        59
    ],
    "CACAAC": [
        1,
        27
    ],
    "CACAAG": [
        33,
        27
    ],
    "CACAAT": [
        33,
        59
    ],
    "CACACA": [
        1,
        43
    ],
    "CACACC": [
        1,
        11
    ],
    "CACACG": [
        33,
        11
    ],
    "CACACT": [
        33,
        43
    ],
    "CACAGA": [
        17,
        43
    ],
    "CACAGC": [
        17,
        11
    ],
    "CACAGG": [
        49,
        11
    ],
    "CACAGT": [
        49,
        43
    ],
    "CACATA": [
        17,
        59
    ],
    "CACATC": [
        17,
        27
    ],
    "CACATG": [
        49,
        27
    ],
    "CACATT": [
        49,
        59
    ],
    "CACCAA": [
        1,
        51
    ],
    "CACCAC": [
        1,
        19
    ],
    "CACCAG": [
        33,
        19
    ],
    "CACCAT": [
        33,
        51
    ],
    "CACCCA": [
        1,
        35
    ],
    "CACCCC": [
        1,
        3
    ],
    "CACCCG": [
        33,
        3
    ],
    "CACCCT": [
        33,
        35
    ],
    "CACCGA": [
        17,
        35
    ],
    "CACCGC": [
        17,
        3
    ],
    "CACCGG": [
        49,
        3
    ],
    "CACCGT": [
        49,
        35
    ],
    "CACCTA": [
        17,
        51
    ],
    "CACCTC": [
        17,
        19
    ],
    "CACCTG": [
        49,
        19
    ],
    "CACCTT": [
        49,
        51
    ],
    "CACGAA": [
        9,
        51
    ],
    "CACGAC": [
        9,
        19
    ],
    "CACGAG": [
        41,
        19
    ],
    "CACGAT": [
        41,
        51
    ],
    "CACGCA": [
        9,
        35
    ],
    "CACGCC": [
        9,
        3
    ],
    "CACGCG": [
        41,
        3
    ],
    "CACGCT": [
        41,
        35
    ],
    "CACGGA": [
        25,
        35
    ],
    "CACGGC": [
        25,
        3
    ],
    "CACGGG": [
        57,
        3
    ],
    "CACGGT": [
        57,
        35
    ],
    "CACGTA": [
        25,
        51
    ],
    "CACGTC": [
        25,
        19
    ],
    "CACGTG": [
        57,
        19
    ],
    "CACGTT": [
        57,
        51
    ],
    "CACTAA": [
        9,
        59
    ],
    "CACTAC": [
        9,
        27
    ],
    "CACTAG": [
        41,
        27
    ],
    "CACTAT": [
        41,
        59
    ],
    "CACTCA": [
        9,
        43
    ],
    "CACTCC": [
        9,
        11
    ],
    "CACTCG": [
        41,
        11
    ],
    "CACTCT": [
        41,
        43
    ],
    "CACTGA": [
        25,
        43
    ],
    "CACTGC": [
        25,
        11
    ],
    "CACTGG": [
        57,
        11
    ],
    "CACTGT": [
        57,
        43
    ],
    "CACTTA": [
        25,
        59
    ],
    "CACTTC": [
        25,
        27
    ],
    "CACTTG": [
        57,
        27
    ],
    "CACTTT": [
        57,
        59
    ],
    "CAGAAA": [
        5,
        59
    ],
    "CAGAAC": [
        5,
        27
    ],
    "CAGAAG": [
        37,
        27
    ],
    "CAGAAT": [
        37,
        59
    ],
    "CAGACA": [
        5,
        43
    ],
    "CAGACC": [
        5,
        11
    ],
    "CAGACG": [
        37,
        11
    ],
    "CAGACT": [
        37,
        43
    ],
    "CAGAGA": [
        21,
        43
    ],
    "CAGAGC": [
        21,
        11
    ],
    "CAGAGG": [
        53,
        11
    ],
    "CAGAGT": [
        53,
        43
    ],
    "CAGATA": [
        21,
        59
    ],
    "CAGATC": [
        21,
        27
    ],
    "CAGATG": [
        53,
        27
    ],
    "CAGATT": [
        53,
        59
    ],
    "CAGCAA": [
        5,
        51
    ],
    "CAGCAC": [
        5,
        19
    ],
    "CAGCAG": [
        37,
        19
    ],
    "CAGCAT": [
        37,
        51
    ],
    "CAGCCA": [
        5,
        35
    ],
    "CAGCCC": [
        5,
        3
    ],
    "CAGCCG": [
        37,
        3
    ],
    "CAGCCT": [
        37,
        35
    ],
    "CAGCGA": [
        21,
        35
    ],
    "CAGCGC": [
        21,
        3
    ],
    "CAGCGG": [
        53,
        3
    ],
    "CAGCGT": [
        53,
        35
    ],
    "CAGCTA": [
        21,
        51
    ],
    "CAGCTC": [
        21,
        19
    ],
    "CAGCTG": [
        53,
        19
    ],
    "CAGCTT": [
        53,
        51
    ],
    "CAGGAA": [
        13,
        51
    ],
    "CAGGAC": [
        13,
        19
    ],
    "CAGGAG": [
        45,
        19
    ],
    "CAGGAT": [
        45,
        51
    ],
    "CAGGCA": [
        13,
        35
    ],
    "CAGGCC": [
        13,
        3
    ],
    "CAGGCG": [
        45,
        3
    ],
    "CAGGCT": [
        45,
        35
    ],
    "CAGGGA": [
        29,
        35
    ],
    "CAGGGC": [
        29,
        3
    ],
    "CAGGGG": [
        61,
        3
    ],
    "CAGGGT": [
        61,
        35
    ],
    "CAGGTA": [
        29,
        51
    ],
    "CAGGTC": [
        29,
        19
    ],
    "CAGGTG": [
        61,
        19
    ],
    "CAGGTT": [
        61,
        51
    ],
    "CAGTAA": [
        13,
        59
    ],
    "CAGTAC": [
        13,
        27
    ],
    "CAGTAG": [
        45,
        27
    ],
    "CAGTAT": [
        45,
        59
    ],
    "CAGTCA": [
        13,
        43
    ],
    "CAGTCC": [
        13,
        11
    ],
    "CAGTCG": [
        45,
        11
    ],
    "CAGTCT": [
        45,
        43
    ],
    "CAGTGA": [
        29,
        43
    ],
    "CAGTGC": [
        29,
        11
    ],
    "CAGTGG": [
        61,
        11
    ],
    "CAGTGT": [
        61,
        43
    ],
    "CAGTTA": [
        29,
        59
    ],
    "CAGTTC": [
        29,
        27
    ],
    "CAGTTG": [
        61,
        27
    ],
    "CAGTTT": [
        61,
        59
    ],
    "CATAAA": [
        5,
        63
    ],
    "CATAAC": [
        5,
        31
    ],
    "CATAAG": [
        37,
        31
    ],
    "CATAAT": [
        37,
        63
    ],
    "CATACA": [
        5,
        47
    ],
    "CATACC": [
        5,
        15
    ],
    "CATACG": [
        37,
        15
    ],
    "CATACT": [
        37,
        47
    ],
    "CATAGA": [
        21,
        47
    ],
    "CATAGC": [
        21,
        15
    ],
    "CATAGG": [
        53,
        15
    ],
    "CATAGT": [
        53,
        47
    ],
    "CATATA": [
        21,
        63
    ],
    "CATATC": [
        21,
        31
    ],
    "CATATG": [
        53,
        31
    ],
    "CATATT": [
        53,
        63
    ],
    "CATCAA": [
        5,
        55
    ],
    "CATCAC": [
        5,
        23
    ],
    "CATCAG": [
        37,
        23
    ],
    "CATCAT": [
        37,
        55
    ],
    "CATCCA": [
        5,
        39
    ],
    "CATCCC": [
        5,
        7
    ],
    "CATCCG": [
        37,
        7
    ],
    "CATCCT": [
        37,
        39
    ],
    "CATCGA": [
        21,
        39
    ],
    "CATCGC": [
        21,
        7
    ],
    "CATCGG": [
        53,
        7
    ],
    "CATCGT": [
        53,
        39
    ],
    "CATCTA": [
        21,
        55
    ],
    "CATCTC": [
        21,
        23
    ],
    "CATCTG": [
        53,
        23
    ],
    "CATCTT": [
        53,
        55
    ],
    "CATGAA": [
        13,
        55
    ],
    "CATGAC": [
        13,
        23
    ],
    "CATGAG": [
        45,
        23
    ],
    "CATGAT": [
        45,
        55
    ],
    "CATGCA": [
        13,
        39
    ],
    "CATGCC": [
        13,
        7
    ],
    "CATGCG": [
        45,
        7
    ],
    "CATGCT": [
        45,
        39
    ],
    "CATGGA": [
        29,
        39
    ],
    "CATGGC": [
        29,
        7
    ],
    "CATGGG": [
        61,
        7
    ],
    "CATGGT": [
        61,
        39
    ],
    "CATGTA": [
        29,
        55
    ],
    "CATGTC": [
        29,
        23
    ],
    "CATGTG": [
        61,
        23
    ],
    "CATGTT": [
        61,
        55
    ],
    "CATTAA": [
        13,
        63
    ],
    "CATTAC": [
        13,
        31
    ],
    "CATTAG": [
        45,
        31
    ],
    "CATTAT": [
        45,
        63
    ],
    "CATTCA": [
        13,
        47
    ],
    "CATTCC": [
        13,
        15
    ],
    "CATTCG": [
        45,
        15
    ],
    "CATTCT": [
        45,
        47
    ],
    "CATTGA": [
        29,
        47
    ],
    "CATTGC": [
        29,
        15
    ],
    "CATTGG": [
        61,
        15
    ],
    "CATTGT": [
        61,
        47
    ],
    "CATTTA": [
        29,
        63
    ],
    "CATTTC": [
        29,
        31
    ],
    "CATTTG": [
        61,
        31
    ],
    "CATTTT": [
        61,
        63
    ],
    "CCAAAA": [
        1,
        61
    ],
    "CCAAAC": [
        1,
        29
    ],
    "CCAAAG": [
        33,
        29
    ],
    "CCAAAT": [
        33,
        61
    ],
    "CCAACA": [
        1,
        45
    ],
    "CCAACC": [
        1,
        13
    ],
    "CCAACG": [
        33,
        13
    ],
    "CCAACT": [
        33,
        45
    ],
    "CCAAGA": [
        17,
        45
    ],
    "CCAAGC": [
        17,
        13
    ],
    "CCAAGG": [
        49,
        13
    ],
    "CCAAGT": [
        49,
        45
    ],
    "CCAATA": [
        17,
        61
    ],
    "CCAATC": [
        17,
        29
    ],
    "CCAATG": [
        49,
        29
    ],
    "CCAATT": [
        49,
        61
    ],
    "CCACAA": [
        1,
        53
    ],
    "CCACAC": [
        1,
        21
    ],
    "CCACAG": [
        33,
        21
    ],
    "CCACAT": [
        33,
        53
    ],
    "CCACCA": [
        1,
        37
    ],
    "CCACCC": [
        1,
        5
    ],
    "CCACCG": [
        33,
        5
    ],
    "CCACCT": [
        33,
        37
    ],
    "CCACGA": [
        17,
        37
    ],
    "CCACGC": [
        17,
        5
    ],
    "CCACGG": [
        49,
        5
    ],
    "CCACGT": [
        49,
        37
    ],
    "CCACTA": [
        17,
        53
    ],
    "CCACTC": [
        17,
        21
    ],
    "CCACTG": [
        49,
        21
    ],
    "CCACTT": [
        49,
        53
    ],
    "CCAGAA": [
        9,
        53
    ],
    "CCAGAC": [
        9,
        21
    ],
    "CCAGAG": [
        41,
        21
    ],
    "CCAGAT": [
        41,
        53
    ],
    "CCAGCA": [
        9,
        37
    ],
    "CCAGCC": [
        9,
        5
    ],
    "CCAGCG": [
        41,
        5
    ],
    "CCAGCT": [
        41,
        37
    ],
    "CCAGGA": [
        25,
        37
    ],
    "CCAGGC": [
        25,
        5
    ],
    "CCAGGG": [
        57,
        5
    ],
    "CCAGGT": [
        57,
        37
    ],
    "CCAGTA": [
        25,
        53
    ],
    "CCAGTC": [
        25,
        21
    ],
    "CCAGTG": [
        57,
        21
    ],
    "CCAGTT": [
        57,
        53
    ],
    "CCATAA": [
        9,
        61
    ],
    "CCATAC": [
        9,
        29
    ],
    "CCATAG": [
        41,
        29
    ],
    "CCATAT": [
        41,
        61
    ],
    "CCATCA": [
        9,
        45
    ],
    "CCATCC": [
        9,
        13
    ],
    "CCATCG": [
        41,
        13
    ],
    "CCATCT": [
        41,
        45
    ],
    "CCATGA": [
        25,
        45
    ],
    "CCATGC": [
        25,
        13
    ],
    "CCATGG": [
        57,
        13
    ],
    "CCATGT": [
        57,
        45
    ],
    "CCATTA": [
        25,
        61
    ],
    "CCATTC": [
        25,
        29
    ],
    "CCATTG": [
        57,
        29
    ],
    "CCATTT": [
        57,
        61
    ],
    "CCCAAA": [
        1,
        57
    ],
    "CCCAAC": [
        1,
        25
    ],
    "CCCAAG": [
        33,
        25
    ],
    "CCCAAT": [
        33,
        57
    ],
    "CCCACA": [
        1,
        41
    ],
    "CCCACC": [
        1,
        9
    ],
    "CCCACG": [
        33,
        9
    ],
    "CCCACT": [
        33,
        41
    ],
    "CCCAGA": [
        17,
        41
    ],
    "CCCAGC": [
        17,
        9
    ],
    "CCCAGG": [
        49,
        9
    ],
    "CCCAGT": [
        49,
        41
    ],
    "CCCATA": [
        17,
        57
    ],
    "CCCATC": [
        17,
        25
    ],
    "CCCATG": [
        49,
        25
    ],
    "CCCATT": [
        49,
        57
    ],
    "CCCCAA": [
        1,
        49
    ],
    "CCCCAC": [
        1,
        17
    ],
    "CCCCAG": [
        33,
        17
    ],
    "CCCCAT": [
        33,
        49
    ],
    "CCCCCA": [
        1,
        33
    ],
    "CCCCCC": [
        1,
        1
    ],
    "CCCCCG": [
        33,
        1
    ],
    "CCCCCT": [
        33,
        33
    ],
    "CCCCGA": [
        17,
        33
    ],
    "CCCCGC": [
        17,
        1
    ],
    "CCCCGG": [
        49,
        1
    ],
    "CCCCGT": [
        49,
        33
    ],
    "CCCCTA": [
        17,
        49
    ],
    "CCCCTC": [
        17,
        17
    ],
    "CCCCTG": [
        49,
        17
    ],
    "CCCCTT": [
        49,
        49
    ],
    "CCCGAA": [
        9,
        49
    ],
    "CCCGAC": [
        9,
        17
    ],
    "CCCGAG": [
        41,
        17
    ],
    "CCCGAT": [
        41,
        49
    ],
    "CCCGCA": [
        9,
        33
    ],
    "CCCGCC": [
        9,
        1
    ],
    "CCCGCG": [
        41,
        1
    ],
    "CCCGCT": [
        41,
        33
    ],
    "CCCGGA": [
        25,
        33
    ],
    "CCCGGC": [
        25,
        1
    ],
    "CCCGGG": [
        57,
        1
    ],
    "CCCGGT": [
        57,
        33
    ],
    "CCCGTA": [
        25,
        49
    ],
    "CCCGTC": [
        25,
        17
    ],
    "CCCGTG": [
        57,
        17
    ],
    "CCCGTT": [
        57,
        49
    ],
    "CCCTAA": [
        9,
        57
    ],
    "CCCTAC": [
        9,
        25
    ],
    "CCCTAG": [
        41,
        25
    ],
    "CCCTAT": [
        41,
        57
    ],
    "CCCTCA": [
        9,
        41
    ],
    "CCCTCC": [
        9,
        9
    ],
    "CCCTCG": [
        41,
        9
    ],
    "CCCTCT": [
        41,
        41
    ],
    "CCCTGA": [
        25,
        41
    ],
    "CCCTGC": [
        25,
        9
    ],
    "CCCTGG": [
        57,
        9
    ],
    "CCCTGT": [
        57,
        41
    ],
    "CCCTTA": [
        25,
        57
    ],
    "CCCTTC": [
        25,
        25
    ],
    "CCCTTG": [
        57,
        25
    ],
    "CCCTTT": [
        57,
        57
    ],
    "CCGAAA": [
        5,
        57
    ],
    "CCGAAC": [
        5,
        25
    ],
    "CCGAAG": [
        37,
        25
    ],
    "CCGAAT": [
        37,
        57
    ],
    "CCGACA": [
        5,
        41
    ],
    "CCGACC": [
        5,
        9
    ],
    "CCGACG": [
        37,
        9
    ],
    "CCGACT": [
        37,
        41
    ],
    "CCGAGA": [
        21,
        41
    ],
    "CCGAGC": [
        21,
        9
    ],
    "CCGAGG": [
        53,
        9
    ],
    "CCGAGT": [
        53,
        41
    ],
    "CCGATA": [
        21,
        57
    ],
    "CCGATC": [
        21,
        25
    ],
    "CCGATG": [
        53,
        25
    ],
    "CCGATT": [
        53,
        57
    ],
    "CCGCAA": [
        5,
        49
    ],
    "CCGCAC": [
        5,
        17
    ],
    "CCGCAG": [
        37,
        17
    ],
    "CCGCAT": [
        37,
        49
    ],
    "CCGCCA": [
        5,
        33
    ],
    "CCGCCC": [
        5,
        1
    ],
    "CCGCCG": [
        37,
        1
    ],
    "CCGCCT": [
        37,
        33
    ],
    "CCGCGA": [
        21,
        33
    ],
    "CCGCGC": [
        21,
        1
    ],
    "CCGCGG": [
        53,
        1
    ],
    "CCGCGT": [
        53,
        33
    ],
    "CCGCTA": [
        21,
        49
    ],
    "CCGCTC": [
        21,
        17
    ],
    "CCGCTG": [
        53,
        17
    ],
    "CCGCTT": [
        53,
        49
    ],
    "CCGGAA": [
        13,
        49
    ],
    "CCGGAC": [
        13,
        17
    ],
    "CCGGAG": [
        45,
        17
    ],
    "CCGGAT": [
        45,
        49
    ],
    "CCGGCA": [
        13,
        33
    ],
    "CCGGCC": [
        13,
        1
    ],
    "CCGGCG": [
        45,
        1
    ],
    "CCGGCT": [
        45,
        33
    ],
    "CCGGGA": [
        29,
        33
    ],
    "CCGGGC": [
        29,
        1
    ],
    "CCGGGG": [
        61,
        1
    ],
    "CCGGGT": [
        61,
        33
    ],
    "CCGGTA": [
        29,
        49
    ],
    "CCGGTC": [
        29,
        17
    ],
    "CCGGTG": [
        61,
        17
    ],
    "CCGGTT": [
        61,
        49
    ],
    "CCGTAA": [
        13,
        57
    ],
    "CCGTAC": [
        13,
        25
    ],
    "CCGTAG": [
        45,
        25
    ],
    "CCGTAT": [
        45,
        57
    ],
    "CCGTCA": [
        13,
        41
    ],
    "CCGTCC": [
        13,
        9
    ],
    "CCGTCG": [
        45,
        9
    ],
    "CCGTCT": [
        45,
        41
    ],
    "CCGTGA": [
        29,
        41
    ],
    "CCGTGC": [
        29,
        9
    ],
    "CCGTGG": [
        61,
        9
    ],
    "CCGTGT": [
        61,
        41
    ],
    "CCGTTA": [
        29,
        57
    ],
    "CCGTTC": [
        29,
        25
    ],
    "CCGTTG": [
        61,
        25
    ],
    "CCGTTT": [
        61,
        57
    ],
    "CCTAAA": [
        5,
        61
    ],
    "CCTAAC": [
        5,
        29
    ],
    "CCTAAG": [
        37,
        29
    ],
    "CCTAAT": [
        37,
        61
    ],
    "CCTACA": [
        5,
        45
    ],
    "CCTACC": [
        5,
        13
    ],
    "CCTACG": [
        37,
        13
    ],
    "CCTACT": [
        37,
        45
    ],
    "CCTAGA": [
        21,
        45
    ],
    "CCTAGC": [
        21,
        13
    ],
    "CCTAGG": [
        53,
        13
    ],
    "CCTAGT": [
        53,
        45
    ],
    "CCTATA": [
        21,
        61
    ],
    "CCTATC": [
        21,
        29
    ],
    "CCTATG": [
        53,
        29
    ],
    "CCTATT": [
        53,
        61
    ],
    "CCTCAA": [
        5,
        53
    ],
    "CCTCAC": [
        5,
        21
    ],
    "CCTCAG": [
        37,
        21
    ],
    "CCTCAT": [
        37,
        53
    ],
    "CCTCCA": [
        5,
        37
    ],
    "CCTCCC": [
        5,
        5
    ],
    "CCTCCG": [
        37,
        5
    ],
    "CCTCCT": [
        37,
        37
    ],
    "CCTCGA": [
        21,
        37
    ],
    "CCTCGC": [
        21,
        5
    ],
    "CCTCGG": [
        53,
        5
    ],
    "CCTCGT": [
        53,
        37
    ],
    "CCTCTA": [
        21,
        53
    ],
    "CCTCTC": [
        21,
        21
    ],
    "CCTCTG": [
        53,
        21
    ],
    "CCTCTT": [
        53,
        53
    ],
    "CCTGAA": [
        13,
        53
    ],
    "CCTGAC": [
        13,
        21
    ],
    "CCTGAG": [
        45,
        21
    ],
    "CCTGAT": [
        45,
        53
    ],
    "CCTGCA": [
        13,
        37
    ],
    "CCTGCC": [
        13,
        5
    ],
    "CCTGCG": [
        45,
        5
    ],
    "CCTGCT": [
        45,
        37
    ],
    "CCTGGA": [
        29,
        37
    ],
    "CCTGGC": [
        29,
        5
    ],
    "CCTGGG": [
        61,
        5
    ],
    "CCTGGT": [
        61,
        37
    ],
    "CCTGTA": [
        29,
        53
    ],
    "CCTGTC": [
        29,
        21
    ],
    "CCTGTG": [
        61,
        21
    ],
    "CCTGTT": [
        61,
        53
    ],
    "CCTTAA": [
        13,
        61
    ],
    "CCTTAC": [
        13,
        29
    ],
    "CCTTAG": [
        45,
        29
    ],
    "CCTTAT": [
        45,
        61
    ],
    "CCTTCA": [
        13,
        45
    ],
    "CCTTCC": [
        13,
        13
    ],
    "CCTTCG": [
        45,
        13
    ],
    "CCTTCT": [
        45,
        45
    ],
    "CCTTGA": [
        29,
        45
    ],
    "CCTTGC": [
        29,
        13
    ],
    "CCTTGG": [
        61,
        13
    ],
    "CCTTGT": [
        61,
        45
    ],
    "CCTTTA": [
        29,
        61
    ],
    "CCTTTC": [
        29,
        29
    ],
    "CCTTTG": [
        61,
        29
    ],
    "CCTTTT": [
        61,
        61
    ],
    "CGAAAA": [
        3,
        61
    ],
    "CGAAAC": [
        3,
        29
    ],
    "CGAAAG": [
        35,
        29
    ],
    "CGAAAT": [
        35,
        61
    ],
    "CGAACA": [
        3,
        45
    ],
    "CGAACC": [
        3,
        13
    ],
    "CGAACG": [
        35,
        13
    ],
    "CGAACT": [
        35,
        45
    ],
    "CGAAGA": [
        19,
        45
    ],
    "CGAAGC": [
        19,
        13
    ],
    "CGAAGG": [
        51,
        13
    ],
    "CGAAGT": [
        51,
        45
    ],
    "CGAATA": [
        19,
        61
    ],
    "CGAATC": [
        19,
        29
    ],
    "CGAATG": [
        51,
        29
    ],
    "CGAATT": [
        51,
        61
    ],
    "CGACAA": [
        3,
        53
    ],
    "CGACAC": [
        3,
        21
    ],
    "CGACAG": [
        35,
        21
    ],
    "CGACAT": [
        35,
        53
    ],
    "CGACCA": [
        3,
        37
    ],
    "CGACCC": [
        3,
        5
    ],
    "CGACCG": [
        35,
        5
    ],
    "CGACCT": [
        35,
        37
    ],
    "CGACGA": [
        19,
        37
    ],
    "CGACGC": [
        19,
        5
    ],
    "CGACGG": [
        51,
        5
    ],
    "CGACGT": [
        51,
        37
    ],
    "CGACTA": [
        19,
        53
    ],
    "CGACTC": [
        19,
        21
    ],
    "CGACTG": [
        51,
        21
    ],
    "CGACTT": [
        51,
        53
    ],
    "CGAGAA": [
        11,
        53
    ],
    "CGAGAC": [
        11,
        21
    ],
    "CGAGAG": [
        43,
        21
    ],
    "CGAGAT": [
        43,
        53
    ],
    "CGAGCA": [
        11,
        37
    ],
    "CGAGCC": [
        11,
        5
    ],
    "CGAGCG": [
        43,
        5
    ],
    "CGAGCT": [
        43,
        37
    ],
    "CGAGGA": [
        27,
        37
    ],
    "CGAGGC": [
        27,
        5
    ],
    "CGAGGG": [
        59,
        5
    ],
    "CGAGGT": [
        59,
        37
    ],
    "CGAGTA": [
        27,
        53
    ],
    "CGAGTC": [
        27,
        21
    ],
    "CGAGTG": [
        59,
        21
    ],
    "CGAGTT": [
        59,
        53
    ],
    "CGATAA": [
        11,
        61
    ],
    "CGATAC": [
        11,
        29
    ],
    "CGATAG": [
        43,
        29
    ],
    "CGATAT": [
        43,
        61
    ],
    "CGATCA": [
        11,
        45
    ],
    "CGATCC": [
        11,
        13
    ],
    "CGATCG": [
        43,
        13
    ],
    "CGATCT": [
        43,
        45
    ],
    "CGATGA": [
        27,
        45
    ],
    "CGATGC": [
        27,
        13
    ],
    "CGATGG": [
        59,
        13
    ],
    "CGATGT": [
        59,
        45
    ],
    "CGATTA": [
        27,
        61
    ],
    "CGATTC": [
        27,
        29
    ],
    "CGATTG": [
        59,
        29
    ],
    "CGATTT": [
        59,
        61
    ],
    "CGCAAA": [
        3,
        57
    ],
    "CGCAAC": [
        3,
        25
    ],
    "CGCAAG": [
        35,
        25
    ],
    "CGCAAT": [
        35,
        57
    ],
    "CGCACA": [
        3,
        41
    ],
    "CGCACC": [
        3,
        9
    ],
    "CGCACG": [
        35,
        9
    ],
    "CGCACT": [
        35,
        41
    ],
    "CGCAGA": [
        19,
        41
    ],
    "CGCAGC": [
        19,
        9
    ],
    "CGCAGG": [
        51,
        9
    ],
    "CGCAGT": [
        51,
        41
    ],
    "CGCATA": [
        19,
        57
    ],
    "CGCATC": [
        19,
        25
    ],
    "CGCATG": [
        51,
        25
    ],
    "CGCATT": [
        51,
        57
    ],
    "CGCCAA": [
        3,
        49
    ],
    "CGCCAC": [
        3,
        17
    ],
    "CGCCAG": [
        35,
        17
    ],
    "CGCCAT": [
        35,
        49
    ],
    "CGCCCA": [
        3,
        33
    ],
    "CGCCCC": [
        3,
        1
    ],
    "CGCCCG": [
        35,
        1
    ],
    "CGCCCT": [
        35,
        33
    ],
    "CGCCGA": [
        19,
        33
    ],
    "CGCCGC": [
        19,
        1
    ],
    "CGCCGG": [
        51,
        1
    ],
    "CGCCGT": [
        51,
        33
    ],
    "CGCCTA": [
        19,
        49
    ],
    "CGCCTC": [
        19,
        17
    ],
    "CGCCTG": [
        51,
        17
    ],
    "CGCCTT": [
        51,
        49
    ],
    "CGCGAA": [
        11,
        49
    ],
    "CGCGAC": [
        11,
        17
    ],
    "CGCGAG": [
        43,
        17
    ],
    "CGCGAT": [
        43,
        49
    ],
    "CGCGCA": [
        11,
        33
    ],
    "CGCGCC": [
        11,
        1
    ],
    "CGCGCG": [
        43,
        1
    ],
    "CGCGCT": [
        43,
        33
    ],
    "CGCGGA": [
        27,
        33
    ],
    "CGCGGC": [
        27,
        1
    ],
    "CGCGGG": [
        59,
        1
    ],
    "CGCGGT": [
        59,
        33
    ],
    "CGCGTA": [
        27,
        49
    ],
    "CGCGTC": [
        27,
        17
    ],
    "CGCGTG": [
        59,
        17
    ],
    "CGCGTT": [
        59,
        49
    ],
    "CGCTAA": [
        11,
        57
    ],
    "CGCTAC": [
        11,
        25
    ],
    "CGCTAG": [
        43,
        25
    ],
    "CGCTAT": [
        43,
        57
    ],
    "CGCTCA": [
        11,
        41
    ],
    "CGCTCC": [
        11,
        9
    ],
    "CGCTCG": [
        43,
        9
    ],
    "CGCTCT": [
        43,
        41
    ],
    "CGCTGA": [
        27,
        41
    ],
    "CGCTGC": [
        27,
        9
    ],
    "CGCTGG": [
        59,
        9
    ],
    "CGCTGT": [
        59,
        41
    ],
    "CGCTTA": [
        27,
        57
    ],
    "CGCTTC": [
        27,
        25
    ],
    "CGCTTG": [
        59,
        25
    ],
    "CGCTTT": [
        59,
        57
    ],
    "CGGAAA": [
        7,
        57
    ],
    "CGGAAC": [
        7,
        25
    ],
    "CGGAAG": [
        39,
        25
    ],
    "CGGAAT": [
        39,
        57
    ],
    "CGGACA": [
        7,
        41
    ],
    "CGGACC": [
        7,
        9
    ],
    "CGGACG": [
        39,
        9
    ],
    "CGGACT": [
        39,
        41
    ],
    "CGGAGA": [
        23,
        41
    ],
    "CGGAGC": [
        23,
        9
    ],
    "CGGAGG": [
        55,
        9
    ],
    "CGGAGT": [
        55,
        41
    ],
    "CGGATA": [
        23,
        57
    ],
    "CGGATC": [
        23,
        25
    ],
    "CGGATG": [
        55,
        25
    ],
    "CGGATT": [
        55,
        57
    ],
    "CGGCAA": [
        7,
        49
    ],
    "CGGCAC": [
        7,
        17
    ],
    "CGGCAG": [
        39,
        17
    ],
    "CGGCAT": [
        39,
        49
    ],
    "CGGCCA": [
        7,
        33
    ],
    "CGGCCC": [
        7,
        1
    ],
    "CGGCCG": [
        39,
        1
    ],
    "CGGCCT": [
        39,
        33
    ],
    "CGGCGA": [
        23,
        33
    ],
    "CGGCGC": [
        23,
        1
    ],
    "CGGCGG": [
        55,
        1
    ],
    "CGGCGT": [
        55,
        33
    ],
    "CGGCTA": [
        23,
        49
    ],
    "CGGCTC": [
        23,
        17
    ],
    "CGGCTG": [
        55,
        17
    ],
    "CGGCTT": [
        55,
        49
    ],
    "CGGGAA": [
        15,
        49
    ],
    "CGGGAC": [
        15,
        17
    ],
    "CGGGAG": [
        47,
        17
    ],
    "CGGGAT": [
        47,
        49
    ],
    "CGGGCA": [
        15,
        33
    ],
    "CGGGCC": [
        15,
        1
    ],
    "CGGGCG": [
        47,
        1
    ],
    "CGGGCT": [
        47,
        33
    ],
    "CGGGGA": [
        31,
        33
    ],
    "CGGGGC": [
        31,
        1
    ],
    "CGGGGG": [
        63,
        1
    ],
    "CGGGGT": [
        63,
        33
    ],
    "CGGGTA": [
        31,
        49
    ],
    "CGGGTC": [
        31,
        17
    ],
    "CGGGTG": [
        63,
        17
    ],
    "CGGGTT": [
        63,
        49
    ],
    "CGGTAA": [
        15,
        57
    ],
    "CGGTAC": [
        15,
        25
    ],
    "CGGTAG": [
        47,
        25
    ],
    "CGGTAT": [
        47,
        57
    ],
    "CGGTCA": [
        15,
        41
    ],
    "CGGTCC": [
        15,
        9
    ],
    "CGGTCG": [
        47,
        9
    ],
    "CGGTCT": [
        47,
        41
    ],
    "CGGTGA": [
        31,
        41
    ],
    "CGGTGC": [
        31,
        9
    ],
    "CGGTGG": [
        63,
        9
    ],
    "CGGTGT": [
        63,
        41
    ],
    "CGGTTA": [
        31,
        57
    ],
    "CGGTTC": [
        31,
        25
    ],
    "CGGTTG": [
        63,
        25
    ],
    "CGGTTT": [
        63,
        57
    ],
    "CGTAAA": [
        7,
        61
    ],
    "CGTAAC": [
        7,
        29
    ],
    "CGTAAG": [
        39,
        29
    ],
    "CGTAAT": [
        39,
        61
    ],
    "CGTACA": [
        7,
        45
    ],
    "CGTACC": [
        7,
        13
    ],
    "CGTACG": [
        39,
        13
    ],
    "CGTACT": [
        39,
        45
    ],
    "CGTAGA": [
        23,
        45
    ],
    "CGTAGC": [
        23,
        13
    ],
    "CGTAGG": [
        55,
        13
    ],
    "CGTAGT": [
        55,
        45
    ],
    "CGTATA": [
        23,
        61
    ],
    "CGTATC": [
        23,
        29
    ],
    "CGTATG": [
        55,
        29
    ],
    "CGTATT": [
        55,
        61
    ],
    "CGTCAA": [
        7,
        53
    ],
    "CGTCAC": [
        7,
        21
    ],
    "CGTCAG": [
        39,
        21
    ],
    "CGTCAT": [
        39,
        53
    ],
    "CGTCCA": [
        7,
        37
    ],
    "CGTCCC": [
        7,
        5
    ],
    "CGTCCG": [
        39,
        5
    ],
    "CGTCCT": [
        39,
        37
    ],
    "CGTCGA": [
        23,
        37
    ],
    "CGTCGC": [
        23,
        5
    ],
    "CGTCGG": [
        55,
        5
    ],
    "CGTCGT": [
        55,
        37
    ],
    "CGTCTA": [
        23,
        53
    ],
    "CGTCTC": [
        23,
        21
    ],
    "CGTCTG": [
        55,
        21
    ],
    "CGTCTT": [
        55,
        53
    ],
    "CGTGAA": [
        15,
        53
    ],
    "CGTGAC": [
        15,
        21
    ],
    "CGTGAG": [
        47,
        21
    ],
    "CGTGAT": [
        47,
        53
    ],
    "CGTGCA": [
        15,
        37
    ],
    "CGTGCC": [
        15,
        5
    ],
    "CGTGCG": [
        47,
        5
    ],
    "CGTGCT": [
        47,
        37
    ],
    "CGTGGA": [
        31,
        37
    ],
    "CGTGGC": [
        31,
        5
    ],
    "CGTGGG": [
        63,
        5
    ],
    "CGTGGT": [
        63,
        37
    ],
    "CGTGTA": [
        31,
        53
    ],
    "CGTGTC": [
        31,
        21
    ],
    "CGTGTG": [
        63,
        21
    ],
    "CGTGTT": [
        63,
        53
    ],
    "CGTTAA": [
        15,
        61
    ],
    "CGTTAC": [
        15,
        29
    ],
    "CGTTAG": [
        47,
        29
    ],
    "CGTTAT": [
        47,
        61
    ],
    "CGTTCA": [
        15,
        45
    ],
    "CGTTCC": [
        15,
        13
    ],
    "CGTTCG": [
        47,
        13
    ],
    "CGTTCT": [
        47,
        45
    ],
    "CGTTGA": [
        31,
        45
    ],
    "CGTTGC": [
        31,
        13
    ],
    "CGTTGG": [
        63,
        13
    ],
    "CGTTGT": [
        63,
        45
    ],
    "CGTTTA": [
        31,
        61
    ],
    "CGTTTC": [
        31,
        29
    ],
    "CGTTTG": [
        63,
        29
    ],
    "CGTTTT": [
        63,
        61
    ],
    "CTAAAA": [
        3,
        63
    ],
    "CTAAAC": [
        3,
        31
    ],
    "CTAAAG": [
        35,
        31
    ],
    "CTAAAT": [
        35,
        63
    ],
    "CTAACA": [
        3,
        47
    ],
    "CTAACC": [
        3,
        15
    ],
    "CTAACG": [
        35,
        15
    ],
    "CTAACT": [
        35,
        47
    ],
    "CTAAGA": [
        19,
        47
    ],
    "CTAAGC": [
        19,
        15
    ],
    "CTAAGG": [
        51,
        15
    ],
    "CTAAGT": [
        51,
        47
    ],
    "CTAATA": [
        19,
        63
    ],
    "CTAATC": [
        19,
        31
    ],
    "CTAATG": [
        51,
        31
    ],
    "CTAATT": [
        51,
        63
    ],
    "CTACAA": [
        3,
        55
    ],
    "CTACAC": [
        3,
        23
    ],
    "CTACAG": [
        35,
        23
    ],
    "CTACAT": [
        35,
        55
    ],
    "CTACCA": [
        3,
        39
    ],
    "CTACCC": [
        3,
        7
    ],
    "CTACCG": [
        35,
        7
    ],
    "CTACCT": [
        35,
        39
    ],
    "CTACGA": [
        19,
        39
    ],
    "CTACGC": [
        19,
        7
    ],
    "CTACGG": [
        51,
        7
    ],
    "CTACGT": [
        51,
        39
    ],
    "CTACTA": [
        19,
        55
    ],
    "CTACTC": [
        19,
        23
    ],
    "CTACTG": [
        51,
        23
    ],
    "CTACTT": [
        51,
        55
    ],
    "CTAGAA": [
        11,
        55
    ],
    "CTAGAC": [
        11,
        23
    ],
    "CTAGAG": [
        43,
        23
    ],
    "CTAGAT": [
        43,
        55
    ],
    "CTAGCA": [
        11,
        39
    ],
    "CTAGCC": [
        11,
        7
    ],
    "CTAGCG": [
        43,
        7
    ],
    "CTAGCT": [
        43,
        39
    ],
    "CTAGGA": [
        27,
        39
    ],
    "CTAGGC": [
        27,
        7
    ],
    "CTAGGG": [
        59,
        7
    ],
    "CTAGGT": [
        59,
        39
    ],
    "CTAGTA": [
        27,
        55
    ],
    "CTAGTC": [
        27,
        23
    ],
    "CTAGTG": [
        59,
        23
    ],
    "CTAGTT": [
        59,
        55
    ],
    "CTATAA": [
        11,
        63
    ],
    "CTATAC": [
        11,
        31
    ],
    "CTATAG": [
        43,
        31
    ],
    "CTATAT": [
        43,
        63
    ],
    "CTATCA": [
        11,
        47
    ],
    "CTATCC": [
        11,
        15
    ],
    "CTATCG": [
        43,
        15
    ],
    "CTATCT": [
        43,
        47
    ],
    "CTATGA": [
        27,
        47
    ],
    "CTATGC": [
        27,
        15
    ],
    "CTATGG": [
        59,
        15
    ],
    "CTATGT": [
        59,
        47
    ],
    "CTATTA": [
        27,
        63
    ],
    "CTATTC": [
        27,
        31
    ],
    "CTATTG": [
        59,
        31
    ],
    "CTATTT": [
        59,
        63
    ],
    "CTCAAA": [
        3,
        59
    ],
    "CTCAAC": [
        3,
        27
    ],
    "CTCAAG": [
        35,
        27
    ],
    "CTCAAT": [
        35,
        59
    ],
    "CTCACA": [
        3,
        43
    ],
    "CTCACC": [
        3,
        11
    ],
    "CTCACG": [
        35,
        11
    ],
    "CTCACT": [
        35,
        43
    ],
    "CTCAGA": [
        19,
        43
    ],
    "CTCAGC": [
        19,
        11
    ],
    "CTCAGG": [
        51,
        11
    ],
    "CTCAGT": [
        51,
        43
    ],
    "CTCATA": [
        19,
        59
    ],
    "CTCATC": [
        19,
        27
    ],
    "CTCATG": [
        51,
        27
    ],
    "CTCATT": [
        51,
        59
    ],
    "CTCCAA": [
        3,
        51
    ],
    "CTCCAC": [
        3,
        19
    ],
    "CTCCAG": [
        35,
        19
    ],
    "CTCCAT": [
        35,
        51
    ],
    "CTCCCA": [
        3,
        35
    ],
    "CTCCCC": [
        3,
        3
    ],
    "CTCCCG": [
        35,
        3
    ],
    "CTCCCT": [
        35,
        35
    ],
    "CTCCGA": [
        19,
        35
    ],
    "CTCCGC": [
        19,
        3
    ],
    "CTCCGG": [
        51,
        3
    ],
    "CTCCGT": [
        51,
        35
    ],
    "CTCCTA": [
        19,
        51
    ],
    "CTCCTC": [
        19,
        19
    ],
    "CTCCTG": [
        51,
        19
    ],
    "CTCCTT": [
        51,
        51
    ],
    "CTCGAA": [
        11,
        51
    ],
    "CTCGAC": [
        11,
        19
    ],
    "CTCGAG": [
        43,
        19
    ],
    "CTCGAT": [
        43,
        51
    ],
    "CTCGCA": [
        11,
        35
    ],
    "CTCGCC": [
        11,
        3
    ],
    "CTCGCG": [
        43,
        3
    ],
    "CTCGCT": [
        43,
        35
    ],
    "CTCGGA": [
        27,
        35
    ],
    "CTCGGC": [
        27,
        3
    ],
    "CTCGGG": [
        59,
        3
    ],
    "CTCGGT": [
        59,
        35
    ],
    "CTCGTA": [
        27,
        51
    ],
    "CTCGTC": [
        27,
        19
    ],
    "CTCGTG": [
        59,
        19
    ],
    "CTCGTT": [
        59,
        51
    ],
    "CTCTAA": [
        11,
        59
    ],
    "CTCTAC": [
        11,
        27
    ],
    "CTCTAG": [
        43,
        27
    ],
    "CTCTAT": [
        43,
        59
    ],
    "CTCTCA": [
        11,
        43
    ],
    "CTCTCC": [
        11,
        11
    ],
    "CTCTCG": [
        43,
        11
    ],
    "CTCTCT": [
        43,
        43
    ],
    "CTCTGA": [
        27,
        43
    ],
    "CTCTGC": [
        27,
        11
    ],
    "CTCTGG": [
        59,
        11
    ],
    "CTCTGT": [
        59,
        43
    ],
    "CTCTTA": [
        27,
        59
    ],
    "CTCTTC": [
        27,
        27
    ],
    "CTCTTG": [
        59,
        27
    ],
    "CTCTTT": [
        59,
        59
    ],
    "CTGAAA": [
        7,
        59
    ],
    "CTGAAC": [
        7,
        27
    ],
    "CTGAAG": [
        39,
        27
    ],
    "CTGAAT": [
        39,
        59
    ],
    "CTGACA": [
        7,
        43
    ],
    "CTGACC": [
        7,
        11
    ],
    "CTGACG": [
        39,
        11
    ],
    "CTGACT": [
        39,
        43
    ],
    "CTGAGA": [
        23,
        43
    ],
    "CTGAGC": [
        23,
        11
    ],
    "CTGAGG": [
        55,
        11
    ],
    "CTGAGT": [
        55,
        43
    ],
    "CTGATA": [
        23,
        59
    ],
    "CTGATC": [
        23,
        27
    ],
    "CTGATG": [
        55,
        27
    ],
    "CTGATT": [
        55,
        59
    ],
    "CTGCAA": [
        7,
        51
    ],
    "CTGCAC": [
        7,
        19
    ],
    "CTGCAG": [
        39,
        19
    ],
    "CTGCAT": [
        39,
        51
    ],
    "CTGCCA": [
        7,
        35
    ],
    "CTGCCC": [
        7,
        3
    ],
    "CTGCCG": [
        39,
        3
    ],
    "CTGCCT": [
        39,
        35
    ],
    "CTGCGA": [
        23,
        35
    ],
    "CTGCGC": [
        23,
        3
    ],
    "CTGCGG": [
        55,
        3
    ],
    "CTGCGT": [
        55,
        35
    ],
    "CTGCTA": [
        23,
        51
    ],
    "CTGCTC": [
        23,
        19
    ],
    "CTGCTG": [
        55,
        19
    ],
    "CTGCTT": [
        55,
        51
    ],
    "CTGGAA": [
        15,
        51
    ],
    "CTGGAC": [
        15,
        19
    ],
    "CTGGAG": [
        47,
        19
    ],
    "CTGGAT": [
        47,
        51
    ],
    "CTGGCA": [
        15,
        35
    ],
    "CTGGCC": [
        15,
        3
    ],
    "CTGGCG": [
        47,
        3
    ],
    "CTGGCT": [
        47,
        35
    ],
    "CTGGGA": [
        31,
        35
    ],
    "CTGGGC": [
        31,
        3
    ],
    "CTGGGG": [
        63,
        3
    ],
    "CTGGGT": [
        63,
        35
    ],
    "CTGGTA": [
        31,
        51
    ],
    "CTGGTC": [
        31,
        19
    ],
    "CTGGTG": [
        63,
        19
    ],
    "CTGGTT": [
        63,
        51
    ],
    "CTGTAA": [
        15,
        59
    ],
    "CTGTAC": [
        15,
        27
    ],
    "CTGTAG": [
        47,
        27
    ],
    "CTGTAT": [
        47,
        59
    ],
    "CTGTCA": [
        15,
        43
    ],
    "CTGTCC": [
        15,
        11
    ],
    "CTGTCG": [
        47,
        11
    ],
    "CTGTCT": [
        47,
        43
    ],
    "CTGTGA": [
        31,
        43
    ],
    "CTGTGC": [
        31,
        11
    ],
    "CTGTGG": [
        63,
        11
    ],
    "CTGTGT": [
        63,
        43
    ],
    "CTGTTA": [
        31,
        59
    ],
    "CTGTTC": [
        31,
        27
    ],
    "CTGTTG": [
        63,
        27
    ],
    "CTGTTT": [
        63,
        59
    ],
    "CTTAAA": [
        7,
        63
    ],
    "CTTAAC": [
        7,
        31
    ],
    "CTTAAG": [
        39,
        31
    ],
    "CTTAAT": [
        39,
        63
    ],
    "CTTACA": [
        7,
        47
    ],
    "CTTACC": [
        7,
        15
    ],
    "CTTACG": [
        39,
        15
    ],
    "CTTACT": [
        39,
        47
    ],
    "CTTAGA": [
        23,
        47
    ],
    "CTTAGC": [
        23,
        15
    ],
    "CTTAGG": [
        55,
        15
    ],
    "CTTAGT": [
        55,
        47
    ],
    "CTTATA": [
        23,
        63
    ],
    "CTTATC": [
        23,
        31
    ],
    "CTTATG": [
        55,
        31
    ],
    "CTTATT": [
        55,
        63
    ],
    "CTTCAA": [
        7,
        55
    ],
    "CTTCAC": [
        7,
        23
    ],
    "CTTCAG": [
        39,
        23
    ],
    "CTTCAT": [
        39,
        55
    ],
    "CTTCCA": [
        7,
        39
    ],
    "CTTCCC": [
        7,
        7
    ],
    "CTTCCG": [
        39,
        7
    ],
    "CTTCCT": [
        39,
        39
    ],
    "CTTCGA": [
        23,
        39
    ],
    "CTTCGC": [
        23,
        7
    ],
    "CTTCGG": [
        55,
        7
    ],
    "CTTCGT": [
        55,
        39
    ],
    "CTTCTA": [
        23,
        55
    ],
    "CTTCTC": [
        23,
        23
    ],
    "CTTCTG": [
        55,
        23
    ],
    "CTTCTT": [
        55,
        55
    ],
    "CTTGAA": [
        15,
        55
    ],
    "CTTGAC": [
        15,
        23
    ],
    "CTTGAG": [
        47,
        23
    ],
    "CTTGAT": [
        47,
        55
    ],
    "CTTGCA": [
        15,
        39
    ],
    "CTTGCC": [
        15,
        7
    ],
    "CTTGCG": [
        47,
        7
    ],
    "CTTGCT": [
        47,
        39
    ],
    "CTTGGA": [
        31,
        39
    ],
    "CTTGGC": [
        31,
        7
    ],
    "CTTGGG": [
        63,
        7
    ],
    "CTTGGT": [
        63,
        39
    ],
    "CTTGTA": [
        31,
        55
    ],
    "CTTGTC": [
        31,
        23
    ],
    "CTTGTG": [
        63,
        23
    ],
    "CTTGTT": [
        63,
        55
    ],
    "CTTTAA": [
        15,
        63
    ],
    "CTTTAC": [
        15,
        31
    ],
    "CTTTAG": [
        47,
        31
    ],
    "CTTTAT": [
        47,
        63
    ],
    "CTTTCA": [
        15,
        47
    ],
    "CTTTCC": [
        15,
        15
    ],
    "CTTTCG": [
        47,
        15
    ],
    "CTTTCT": [
        47,
        47
    ],
    "CTTTGA": [
        31,
        47
    ],
    "CTTTGC": [
        31,
        15
    ],
    "CTTTGG": [
        63,
        15
    ],
    "CTTTGT": [
        63,
        47
    ],
    "CTTTTA": [
        31,
        63
    ],
    "CTTTTC": [
        31,
        31
    ],
    "CTTTTG": [
        63,
        31
    ],
    "CTTTTT": [
        63,
        63
    ],
    "GAAAAA": [
        2,
        63
    ],
    "GAAAAC": [
        2,
        31
    ],
    "GAAAAG": [
        34,
        31
    ],
    "GAAAAT": [
        34,
        63
    ],
    "GAAACA": [
        2,
        47
    ],
    "GAAACC": [
        2,
        15
    ],
    "GAAACG": [
        34,
        15
    ],
    "GAAACT": [
        34,
        47
    ],
    "GAAAGA": [
        18,
        47
    ],
    "GAAAGC": [
        18,
        15
    ],
    "GAAAGG": [
        50,
        15
    ],
    "GAAAGT": [
        50,
        47
    ],
    "GAAATA": [
        18,
        63
    ],
    "GAAATC": [
        18,
        31
    ],
    "GAAATG": [
        50,
        31
    ],
    "GAAATT": [
        50,
        63
    ],
    "GAACAA": [
        2,
        55
    ],
    "GAACAC": [
        2,
        23
    ],
    "GAACAG": [
        34,
        23
    ],
    "GAACAT": [
        34,
        55
    ],
    "GAACCA": [
        2,
        39
    ],
    "GAACCC": [
        2,
        7
    ],
    "GAACCG": [
        34,
        7
    ],
    "GAACCT": [
        34,
        39
    ],
    "GAACGA": [
        18,
        39
    ],
    "GAACGC": [
        18,
        7
    ],
    "GAACGG": [
        50,
        7
    ],
    "GAACGT": [
        50,
        39
    ],
    "GAACTA": [
        18,
        55
    ],
    "GAACTC": [
        18,
        23
    ],
    "GAACTG": [
        50,
        23
    ],
    "GAACTT": [
        50,
        55
    ],
    "GAAGAA": [
        10,
        55
    ],
    "GAAGAC": [
        10,
        23
    ],
    "GAAGAG": [
        42,
        23
    ],
    "GAAGAT": [
        42,
        55
    ],
    "GAAGCA": [
        10,
        39
    ],
    "GAAGCC": [
        10,
        7
    ],
    "GAAGCG": [
        42,
        7
    ],
    "GAAGCT": [
        42,
        39
    ],
    "GAAGGA": [
        26,
        39
    ],
    "GAAGGC": [
        26,
        7
    ],
    "GAAGGG": [
        58,
        7
    ],
    "GAAGGT": [
        58,
        39
    ],
    "GAAGTA": [
        26,
        55
    ],
    "GAAGTC": [
        26,
        23
    ],
    "GAAGTG": [
        58,
        23
    ],
    "GAAGTT": [
        58,
        55
    ],
    "GAATAA": [
        10,
        63
    ],
    "GAATAC": [
        10,
        31
    ],
    "GAATAG": [
        42,
        31
    ],
    "GAATAT": [
        42,
        63
    ],
    "GAATCA": [
        10,
        47
    ],
    "GAATCC": [
        10,
        15
    ],
    "GAATCG": [
        42,
        15
    ],
    "GAATCT": [
        42,
        47
    ],
    "GAATGA": [
        26,
        47
    ],
    "GAATGC": [
        26,
        15
    ],
    "GAATGG": [
        58,
        15
    ],
    "GAATGT": [
        58,
        47
    ],
    "GAATTA": [
        26,
        63
    ],
    "GAATTC": [
        26,
        31
    ],
    "GAATTG": [
        58,
        31
    ],
    "GAATTT": [
        58,
        63
    ],
    "GACAAA": [
        2,
        59
    ],
    "GACAAC": [
        2,
        27
    ],
    "GACAAG": [
        34,
        27
    ],
    "GACAAT": [
        34,
        59
    ],
    "GACACA": [
        2,
        43
    ],
    "GACACC": [
        2,
        11
    ],
    "GACACG": [
        34,
        11
    ],
    "GACACT": [
        34,
        43
    ],
    "GACAGA": [
        18,
        43
    ],
    "GACAGC": [
        18,
        11
    ],
    "GACAGG": [
        50,
        11
    ],
    "GACAGT": [
        50,
        43
    ],
    "GACATA": [
        18,
        59
    ],
    "GACATC": [
        18,
        27
    ],
    "GACATG": [
        50,
        27
    ],
    "GACATT": [
        50,
        59
    ],
    "GACCAA": [
        2,
        51
    ],
    "GACCAC": [
        2,
        19
    ],
    "GACCAG": [
        34,
        19
    ],
    "GACCAT": [
        34,
        51
    ],
    "GACCCA": [
        2,
        35
    ],
    "GACCCC": [
        2,
        3
    ],
    "GACCCG": [
        34,
        3
    ],
    "GACCCT": [
        34,
        35
    ],
    "GACCGA": [
        18,
        35
    ],
    "GACCGC": [
        18,
        3
    ],
    "GACCGG": [
        50,
        3
    ],
    "GACCGT": [
        50,
        35
    ],
    "GACCTA": [
        18,
        51
    ],
    "GACCTC": [
        18,
        19
    ],
    "GACCTG": [
        50,
        19
    ],
    "GACCTT": [
        50,
        51
    ],
    "GACGAA": [
        10,
        51
    ],
    "GACGAC": [
        10,
        19
    ],
    "GACGAG": [
        42,
        19
    ],
    "GACGAT": [
        42,
        51
    ],
    "GACGCA": [
        10,
        35
    ],
    "GACGCC": [
        10,
        3
    ],
    "GACGCG": [
        42,
        3
    ],
    "GACGCT": [
        42,
        35
    ],
    "GACGGA": [
        26,
        35
    ],
    "GACGGC": [
        26,
        3
    ],
    "GACGGG": [
        58,
        3
    ],
    "GACGGT": [
        58,
        35
    ],
    "GACGTA": [
        26,
        51
    ],
    "GACGTC": [
        26,
        19
    ],
    "GACGTG": [
        58,
        19
    ],
    "GACGTT": [
        58,
        51
    ],
    "GACTAA": [
        10,
        59
    ],
    "GACTAC": [
        10,
        27
    ],
    "GACTAG": [
        42,
        27
    ],
    "GACTAT": [
        42,
        59
    ],
    "GACTCA": [
        10,
        43
    ],
    "GACTCC": [
        10,
        11
    ],
    "GACTCG": [
        42,
        11
    ],
    "GACTCT": [
        42,
        43
    ],
    "GACTGA": [
        26,
        43
    ],
    "GACTGC": [
        26,
        11
    ],
    "GACTGG": [
        58,
        11
    ],
    "GACTGT": [
        58,
        43
    ],
    "GACTTA": [
        26,
        59
    ],
    "GACTTC": [
        26,
        27
    ],
    "GACTTG": [
        58,
        27
    ],
    "GACTTT": [
        58,
        59
    ],
    "GAGAAA": [
        6,
        59
    ],
    "GAGAAC": [
        6,
        27
    ],
    "GAGAAG": [
        38,
        27
    ],
    "GAGAAT": [
        38,
        59
    ],
    "GAGACA": [
        6,
        43
    ],
    "GAGACC": [
        6,
        11
    ],
    "GAGACG": [
        38,
        11
    ],
    "GAGACT": [
        38,
        43
    ],
    "GAGAGA": [
        22,
        43
    ],
    "GAGAGC": [
        22,
        11
    ],
    "GAGAGG": [
        54,
        11
    ],
    "GAGAGT": [
        54,
        43
    ],
    "GAGATA": [
        22,
        59
    ],
    "GAGATC": [
        22,
        27
    ],
    "GAGATG": [
        54,
        27
    ],
    "GAGATT": [
        54,
        59
    ],
    "GAGCAA": [
        6,
        51
    ],
    "GAGCAC": [
        6,
        19
    ],
    "GAGCAG": [
        38,
        19
    ],
    "GAGCAT": [
        38,
        51
    ],
    "GAGCCA": [
        6,
        35
    ],
    "GAGCCC": [
        6,
        3
    ],
    "GAGCCG": [
        38,
        3
    ],
    "GAGCCT": [
        38,
        35
    ],
    "GAGCGA": [
        22,
        35
    ],
    "GAGCGC": [
        22,
        3
    ],
    "GAGCGG": [
        54,
        3
    ],
    "GAGCGT": [
        54,
        35
    ],
    "GAGCTA": [
        22,
        51
    ],
    "GAGCTC": [
        22,
        19
    ],
    "GAGCTG": [
        54,
        19
    ],
    "GAGCTT": [
        54,
        51
    ],
    "GAGGAA": [
        14,
        51
    ],
    "GAGGAC": [
        14,
        19
    ],
    "GAGGAG": [
        46,
        19
    ],
    "GAGGAT": [
        46,
        51
    ],
    "GAGGCA": [
        14,
        35
    ],
    "GAGGCC": [
        14,
        3
    ],
    "GAGGCG": [
        46,
        3
    ],
    "GAGGCT": [
        46,
        35
    ],
    "GAGGGA": [
        30,
        35
    ],
    "GAGGGC": [
        30,
        3
    ],
    "GAGGGG": [
        62,
        3
    ],
    "GAGGGT": [
        62,
        35
    ],
    "GAGGTA": [
        30,
        51
    ],
    "GAGGTC": [
        30,
        19
    ],
    "GAGGTG": [
        62,
        19
    ],
    "GAGGTT": [
        62,
        51
    ],
    "GAGTAA": [
        14,
        59
    ],
    "GAGTAC": [
        14,
        27
    ],
    "GAGTAG": [
        46,
        27
    ],
    "GAGTAT": [
        46,
        59
    ],
    "GAGTCA": [
        14,
        43
    ],
    "GAGTCC": [
        14,
        11
    ],
    "GAGTCG": [
        46,
        11
    ],
    "GAGTCT": [
        46,
        43
    ],
    "GAGTGA": [
        30,
        43
    ],
    "GAGTGC": [
        30,
        11
    ],
    "GAGTGG": [
        62,
        11
    ],
    "GAGTGT": [
        62,
        43
    ],
    "GAGTTA": [
        30,
        59
    ],
    "GAGTTC": [
        30,
        27
    ],
    "GAGTTG": [
        62,
        27
    ],
    "GAGTTT": [
        62,
        59
    ],
    "GATAAA": [
        6,
        63
    ],
    "GATAAC": [
        6,
        31
    ],
    "GATAAG": [
        38,
        31
    ],
    "GATAAT": [
        38,
        63
    ],
    "GATACA": [
        6,
        47
    ],
    "GATACC": [
        6,
        15
    ],
    "GATACG": [
        38,
        15
    ],
    "GATACT": [
        38,
        47
    ],
    "GATAGA": [
        22,
        47
    ],
    "GATAGC": [
        22,
        15
    ],
    "GATAGG": [
        54,
        15
    ],
    "GATAGT": [
        54,
        47
    ],
    "GATATA": [
        22,
        63
    ],
    "GATATC": [
        22,
        31
    ],
    "GATATG": [
        54,
        31
    ],
    "GATATT": [
        54,
        63
    ],
    "GATCAA": [
        6,
        55
    ],
    "GATCAC": [
        6,
        23
    ],
    "GATCAG": [
        38,
        23
    ],
    "GATCAT": [
        38,
        55
    ],
    "GATCCA": [
        6,
        39
    ],
    "GATCCC": [
        6,
        7
    ],
    "GATCCG": [
        38,
        7
    ],
    "GATCCT": [
        38,
        39
    ],
    "GATCGA": [
        22,
        39
    ],
    "GATCGC": [
        22,
        7
    ],
    "GATCGG": [
        54,
        7
    ],
    "GATCGT": [
        54,
        39
    ],
    "GATCTA": [
        22,
        55
    ],
    "GATCTC": [
        22,
        23
    ],
    "GATCTG": [
        54,
        23
    ],
    "GATCTT": [
        54,
        55
    ],
    "GATGAA": [
        14,
        55
    ],
    "GATGAC": [
        14,
        23
    ],
    "GATGAG": [
        46,
        23
    ],
    "GATGAT": [
        46,
        55
    ],
    "GATGCA": [
        14,
        39
    ],
    "GATGCC": [
        14,
        7
    ],
    "GATGCG": [
        46,
        7
    ],
    "GATGCT": [
        46,
        39
    ],
    "GATGGA": [
        30,
        39
    ],
    "GATGGC": [
        30,
        7
    ],
    "GATGGG": [
        62,
        7
    ],
    "GATGGT": [
        62,
        39
    ],
    "GATGTA": [
        30,
        55
    ],
    "GATGTC": [
        30,
        23
    ],
    "GATGTG": [
        62,
        23
    ],
    "GATGTT": [
        62,
        55
    ],
    "GATTAA": [
        14,
        63
    ],
    "GATTAC": [
        14,
        31
    ],
    "GATTAG": [
        46,
        31
    ],
    "GATTAT": [
        46,
        63
    ],
    "GATTCA": [
        14,
        47
    ],
    "GATTCC": [
        14,
        15
    ],
    "GATTCG": [
        46,
        15
    ],
    "GATTCT": [
        46,
        47
    ],
    "GATTGA": [
        30,
        47
    ],
    "GATTGC": [
        30,
        15
    ],
    "GATTGG": [
        62,
        15
    ],
    "GATTGT": [
        62,
        47
    ],
    "GATTTA": [
        30,
        63
    ],
    "GATTTC": [
        30,
        31
    ],
    "GATTTG": [
        62,
        31
    ],
    "GATTTT": [
        62,
        63
    ],
    "GCAAAA": [
        2,
        61
    ],
    "GCAAAC": [
        2,
        29
    ],
    "GCAAAG": [
        34,
        29
    ],
    "GCAAAT": [
        34,
        61
    ],
    "GCAACA": [
        2,
        45
    ],
    "GCAACC": [
        2,
        13
    ],
    "GCAACG": [
        34,
        13
    ],
    "GCAACT": [
        34,
        45
    ],
    "GCAAGA": [
        18,
        45
    ],
    "GCAAGC": [
        18,
        13
    ],
    "GCAAGG": [
        50,
        13
    ],
    "GCAAGT": [
        50,
        45
    ],
    "GCAATA": [
        18,
        61
    ],
    "GCAATC": [
        18,
        29
    ],
    "GCAATG": [
        50,
        29
    ],
    "GCAATT": [
        50,
        61
    ],
    "GCACAA": [
        2,
        53
    ],
    "GCACAC": [
        2,
        21
    ],
    "GCACAG": [
        34,
        21
    ],
    "GCACAT": [
        34,
        53
    ],
    "GCACCA": [
        2,
        37
    ],
    "GCACCC": [
        2,
        5
    ],
    "GCACCG": [
        34,
        5
    ],
    "GCACCT": [
        34,
        37
    ],
    "GCACGA": [
        18,
        37
    ],
    "GCACGC": [
        18,
        5
    ],
    "GCACGG": [
        50,
        5
    ],
    "GCACGT": [
        50,
        37
    ],
    "GCACTA": [
        18,
        53
    ],
    "GCACTC": [
        18,
        21
    ],
    "GCACTG": [
        50,
        21
    ],
    "GCACTT": [
        50,
        53
    ],
    "GCAGAA": [
        10,
        53
    ],
    "GCAGAC": [
        10,
        21
    ],
    "GCAGAG": [
        42,
        21
    ],
    "GCAGAT": [
        42,
        53
    ],
    "GCAGCA": [
        10,
        37
    ],
    "GCAGCC": [
        10,
        5
    ],
    "GCAGCG": [
        42,
        5
    ],
    "GCAGCT": [
        42,
        37
    ],
    "GCAGGA": [
        26,
        37
    ],
    "GCAGGC": [
        26,
        5
    ],
    "GCAGGG": [
        58,
        5
    ],
    "GCAGGT": [
        58,
        37
    ],
    "GCAGTA": [
        26,
        53
    ],
    "GCAGTC": [
        26,
        21
    ],
    "GCAGTG": [
        58,
        21
    ],
    "GCAGTT": [
        58,
        53
    ],
    "GCATAA": [
        10,
        61
    ],
    "GCATAC": [
        10,
        29
    ],
    "GCATAG": [
        42,
        29
    ],
    "GCATAT": [
        42,
        61
    ],
    "GCATCA": [
        10,
        45
    ],
    "GCATCC": [
        10,
        13
    ],
    "GCATCG": [
        42,
        13
    ],
    "GCATCT": [
        42,
        45
    ],
    "GCATGA": [
        26,
        45
    ],
    "GCATGC": [
        26,
        13
    ],
    "GCATGG": [
        58,
        13
    ],
    "GCATGT": [
        58,
        45
    ],
    "GCATTA": [
        26,
        61
    ],
    "GCATTC": [
        26,
        29
    ],
    "GCATTG": [
        58,
        29
    ],
    "GCATTT": [
        58,
        61
    ],
    "GCCAAA": [
        2,
        57
    ],
    "GCCAAC": [
        2,
        25
    ],
    "GCCAAG": [
        34,
        25
    ],
    "GCCAAT": [
        34,
        57
    ],
    "GCCACA": [
        2,
        41
    ],
    "GCCACC": [
        2,
        9
    ],
    "GCCACG": [
        34,
        9
    ],
    "GCCACT": [
        34,
        41
    ],
    "GCCAGA": [
        18,
        41
    ],
    "GCCAGC": [
        18,
        9
    ],
    "GCCAGG": [
        50,
        9
    ],
    "GCCAGT": [
        50,
        41
    ],
    "GCCATA": [
        18,
        57
    ],
    "GCCATC": [
        18,
        25
    ],
    "GCCATG": [
        50,
        25
    ],
    "GCCATT": [
        50,
        57
    ],
    "GCCCAA": [
        2,
        49
    ],
    "GCCCAC": [
        2,
        17
    ],
    "GCCCAG": [
        34,
        17
    ],
    "GCCCAT": [
        34,
        49
    ],
    "GCCCCA": [
        2,
        33
    ],
    "GCCCCC": [
        2,
        1
    ],
    "GCCCCG": [
        34,
        1
    ],
    "GCCCCT": [
        34,
        33
    ],
    "GCCCGA": [
        18,
        33
    ],
    "GCCCGC": [
        18,
        1
    ],
    "GCCCGG": [
        50,
        1
    ],
    "GCCCGT": [
        50,
        33
    ],
    "GCCCTA": [
        18,
        49
    ],
    "GCCCTC": [
        18,
        17
    ],
    "GCCCTG": [
        50,
        17
    ],
    "GCCCTT": [
        50,
        49
    ],
    "GCCGAA": [
        10,
        49
    ],
    "GCCGAC": [
        10,
        17
    ],
    "GCCGAG": [
        42,
        17
    ],
    "GCCGAT": [
        42,
        49
    ],
    "GCCGCA": [
        10,
        33
    ],
    "GCCGCC": [
        10,
        1
    ],
    "GCCGCG": [
        42,
        1
    ],
    "GCCGCT": [
        42,
        33
    ],
    "GCCGGA": [
        26,
        33
    ],
    "GCCGGC": [
        26,
        1
    ],
    "GCCGGG": [
        58,
        1
    ],
    "GCCGGT": [
        58,
        33
    ],
    "GCCGTA": [
        26,
        49
    ],
    "GCCGTC": [
        26,
        17
    ],
    "GCCGTG": [
        58,
        17
    ],
    "GCCGTT": [
        58,
        49
    ],
    "GCCTAA": [
        10,
        57
    ],
    "GCCTAC": [
        10,
        25
    ],
    "GCCTAG": [
        42,
        25
    ],
    "GCCTAT": [
        42,
        57
    ],
    "GCCTCA": [
        10,
        41
    ],
    "GCCTCC": [
        10,
        9
    ],
    "GCCTCG": [
        42,
        9
    ],
    "GCCTCT": [
        42,
        41
    ],
    "GCCTGA": [
        26,
        41
    ],
    "GCCTGC": [
        26,
        9
    ],
    "GCCTGG": [
        58,
        9
    ],
    "GCCTGT": [
        58,
        41
    ],
    "GCCTTA": [
        26,
        57
    ],
    "GCCTTC": [
        26,
        25
    ],
    "GCCTTG": [
        58,
        25
    ],
    "GCCTTT": [
        58,
        57
    ],
    "GCGAAA": [
        6,
        57
    ],
    "GCGAAC": [
        6,
        25
    ],
    "GCGAAG": [
        38,
        25
    ],
    "GCGAAT": [
        38,
        57
    ],
    "GCGACA": [
        6,
        41
    ],
    "GCGACC": [
        6,
        9
    ],
    "GCGACG": [
        38,
        9
    ],
    "GCGACT": [
        38,
        41
    ],
    "GCGAGA": [
        22,
        41
    ],
    "GCGAGC": [
        22,
        9
    ],
    "GCGAGG": [
        54,
        9
    ],
    "GCGAGT": [
        54,
        41
    ],
    "GCGATA": [
        22,
        57
    ],
    "GCGATC": [
        22,
        25
    ],
    "GCGATG": [
        54,
        25
    ],
    "GCGATT": [
        54,
        57
    ],
    "GCGCAA": [
        6,
        49
    ],
    "GCGCAC": [
        6,
        17
    ],
    "GCGCAG": [
        38,
        17
    ],
    "GCGCAT": [
        38,
        49
    ],
    "GCGCCA": [
        6,
        33
    ],
    "GCGCCC": [
        6,
        1
    ],
    "GCGCCG": [
        38,
        1
    ],
    "GCGCCT": [
        38,
        33
    ],
    "GCGCGA": [
        22,
        33
    ],
    "GCGCGC": [
        22,
        1
    ],
    "GCGCGG": [
        54,
        1
    ],
    "GCGCGT": [
        54,
        33
    ],
    "GCGCTA": [
        22,
        49
    ],
    "GCGCTC": [
        22,
        17
    ],
    "GCGCTG": [
        54,
        17
    ],
    "GCGCTT": [
        54,
        49
    ],
    "GCGGAA": [
        14,
        49
    ],
    "GCGGAC": [
        14,
        17
    ],
    "GCGGAG": [
        46,
        17
    ],
    "GCGGAT": [
        46,
        49
    ],
    "GCGGCA": [
        14,
        33
    ],
    "GCGGCC": [
        14,
        1
    ],
    "GCGGCG": [
        46,
        1
    ],
    "GCGGCT": [
        46,
        33
    ],
    "GCGGGA": [
        30,
        33
    ],
    "GCGGGC": [
        30,
        1
    ],
    "GCGGGG": [
        62,
        1
    ],
    "GCGGGT": [
        62,
        33
    ],
    "GCGGTA": [
        30,
        49
    ],
    "GCGGTC": [
        30,
        17
    ],
    "GCGGTG": [
        62,
        17
    ],
    "GCGGTT": [
        62,
        49
    ],
    "GCGTAA": [
        14,
        57
    ],
    "GCGTAC": [
        14,
        25
    ],
    "GCGTAG": [
        46,
        25
    ],
    "GCGTAT": [
        46,
        57
    ],
    "GCGTCA": [
        14,
        41
    ],
    "GCGTCC": [
        14,
        9
    ],
    "GCGTCG": [
        46,
        9
    ],
    "GCGTCT": [
        46,
        41
    ],
    "GCGTGA": [
        30,
        41
    ],
    "GCGTGC": [
        30,
        9
    ],
    "GCGTGG": [
        62,
        9
    ],
    "GCGTGT": [
        62,
        41
    ],
    "GCGTTA": [
        30,
        57
    ],
    "GCGTTC": [
        30,
        25
    ],
    "GCGTTG": [
        62,
        25
    ],
    "GCGTTT": [
        62,
        57
    ],
    "GCTAAA": [
        6,
        61
    ],
    "GCTAAC": [
        6,
        29
    ],
    "GCTAAG": [
        38,
        29
    ],
    "GCTAAT": [
        38,
        61
    ],
    "GCTACA": [
        6,
        45
    ],
    "GCTACC": [
        6,
        13
    ],
    "GCTACG": [
        38,
        13
    ],
    "GCTACT": [
        38,
        45
    ],
    "GCTAGA": [
        22,
        45
    ],
    "GCTAGC": [
        22,
        13
    ],
    "GCTAGG": [
        54,
        13
    ],
    "GCTAGT": [
        54,
        45
    ],
    "GCTATA": [
        22,
        61
    ],
    "GCTATC": [
        22,
        29
    ],
    "GCTATG": [
        54,
        29
    ],
    "GCTATT": [
        54,
        61
    ],
    "GCTCAA": [
        6,
        53
    ],
    "GCTCAC": [
        6,
        21
    ],
    "GCTCAG": [
        38,
        21
    ],
    "GCTCAT": [
        38,
        53
    ],
    "GCTCCA": [
        6,
        37
    ],
    "GCTCCC": [
        6,
        5
    ],
    "GCTCCG": [
        38,
        5
    ],
    "GCTCCT": [
        38,
        37
    ],
    "GCTCGA": [
        22,
        37
    ],
    "GCTCGC": [
        22,
        5
    ],
    "GCTCGG": [
        54,
        5
    ],
    "GCTCGT": [
        54,
        37
    ],
    "GCTCTA": [
        22,
        53
    ],
    "GCTCTC": [
        22,
        21
    ],
    "GCTCTG": [
        54,
        21
    ],
    "GCTCTT": [
        54,
        53
    ],
    "GCTGAA": [
        14,
        53
    ],
    "GCTGAC": [
        14,
        21
    ],
    "GCTGAG": [
        46,
        21
    ],
    "GCTGAT": [
        46,
        53
    ],
    "GCTGCA": [
        14,
        37
    ],
    "GCTGCC": [
        14,
        5
    ],
    "GCTGCG": [
        46,
        5
    ],
    "GCTGCT": [
        46,
        37
    ],
    "GCTGGA": [
        30,
        37
    ],
    "GCTGGC": [
        30,
        5
    ],
    "GCTGGG": [
        62,
        5
    ],
    "GCTGGT": [
        62,
        37
    ],
    "GCTGTA": [
        30,
        53
    ],
    "GCTGTC": [
        30,
        21
    ],
    "GCTGTG": [
        62,
        21
    ],
    "GCTGTT": [
        62,
        53
    ],
    "GCTTAA": [
        14,
        61
    ],
    "GCTTAC": [
        14,
        29
    ],
    "GCTTAG": [
        46,
        29
    ],
    "GCTTAT": [
        46,
        61
    ],
    "GCTTCA": [
        14,
        45
    ],
    "GCTTCC": [
        14,
        13
    ],
    "GCTTCG": [
        46,
        13
    ],
    "GCTTCT": [
        46,
        45
    ],
    "GCTTGA": [
        30,
        45
    ],
    "GCTTGC": [
        30,
        13
    ],
    "GCTTGG": [
        62,
        13
    ],
    "GCTTGT": [
        62,
        45
    ],
    "GCTTTA": [
        30,
        61
    ],
    "GCTTTC": [
        30,
        29
    ],
    "GCTTTG": [
        62,
        29
    ],
    "GCTTTT": [
        62,
        61
    ],
    "GGAAAA": [
        4,
        61
    ],
    "GGAAAC": [
        4,
        29
    ],
    "GGAAAG": [
        36,
        29
    ],
    "GGAAAT": [
        36,
        61
    ],
    "GGAACA": [
        4,
        45
    ],
    "GGAACC": [
        4,
        13
    ],
    "GGAACG": [
        36,
        13
    ],
    "GGAACT": [
        36,
        45
    ],
    "GGAAGA": [
        20,
        45
    ],
    "GGAAGC": [
        20,
        13
    ],
    "GGAAGG": [
        52,
        13
    ],
    "GGAAGT": [
        52,
        45
    ],
    "GGAATA": [
        20,
        61
    ],
    "GGAATC": [
        20,
        29
    ],
    "GGAATG": [
        52,
        29
    ],
    "GGAATT": [
        52,
        61
    ],
    "GGACAA": [
        4,
        53
    ],
    "GGACAC": [
        4,
        21
    ],
    "GGACAG": [
        36,
        21
    ],
    "GGACAT": [
        36,
        53
    ],
    "GGACCA": [
        4,
        37
    ],
    "GGACCC": [
        4,
        5
    ],
    "GGACCG": [
        36,
        5
    ],
    "GGACCT": [
        36,
        37
    ],
    "GGACGA": [
        20,
        37
    ],
    "GGACGC": [
        20,
        5
    ],
    "GGACGG": [
        52,
        5
    ],
    "GGACGT": [
        52,
        37
    ],
    "GGACTA": [
        20,
        53
    ],
    "GGACTC": [
        20,
        21
    ],
    "GGACTG": [
        52,
        21
    ],
    "GGACTT": [
        52,
        53
    ],
    "GGAGAA": [
        12,
        53
    ],
    "GGAGAC": [
        12,
        21
    ],
    "GGAGAG": [
        44,
        21
    ],
    "GGAGAT": [
        44,
        53
    ],
    "GGAGCA": [
        12,
        37
    ],
    "GGAGCC": [
        12,
        5
    ],
    "GGAGCG": [
        44,
        5
    ],
    "GGAGCT": [
        44,
        37
    ],
    "GGAGGA": [
        28,
        37
    ],
    "GGAGGC": [
        28,
        5
    ],
    "GGAGGG": [
        60,
        5
    ],
    "GGAGGT": [
        60,
        37
    ],
    "GGAGTA": [
        28,
        53
    ],
    "GGAGTC": [
        28,
        21
    ],
    "GGAGTG": [
        60,
        21
    ],
    "GGAGTT": [
        60,
        53
    ],
    "GGATAA": [
        12,
        61
    ],
    "GGATAC": [
        12,
        29
    ],
    "GGATAG": [
        44,
        29
    ],
    "GGATAT": [
        44,
        61
    ],
    "GGATCA": [
        12,
        45
    ],
    "GGATCC": [
        12,
        13
    ],
    "GGATCG": [
        44,
        13
    ],
    "GGATCT": [
        44,
        45
    ],
    "GGATGA": [
        28,
        45
    ],
    "GGATGC": [
        28,
        13
    ],
    "GGATGG": [
        60,
        13
    ],
    "GGATGT": [
        60,
        45
    ],
    "GGATTA": [
        28,
        61
    ],
    "GGATTC": [
        28,
        29
    ],
    "GGATTG": [
        60,
        29
    ],
    "GGATTT": [
        60,
        61
    ],
    "GGCAAA": [
        4,
        57
    ],
    "GGCAAC": [
        4,
        25
    ],
    "GGCAAG": [
        36,
        25
    ],
    "GGCAAT": [
        36,
        57
    ],
    "GGCACA": [
        4,
        41
    ],
    "GGCACC": [
        4,
        9
    ],
    "GGCACG": [
        36,
        9
    ],
    "GGCACT": [
        36,
        41
    ],
    "GGCAGA": [
        20,
        41
    ],
    "GGCAGC": [
        20,
        9
    ],
    "GGCAGG": [
        52,
        9
    ],
    "GGCAGT": [
        52,
        41
    ],
    "GGCATA": [
        20,
        57
    ],
    "GGCATC": [
        20,
        25
    ],
    "GGCATG": [
        52,
        25
    ],
    "GGCATT": [
        52,
        57
    ],
    "GGCCAA": [
        4,
        49
    ],
    "GGCCAC": [
        4,
        17
    ],
    "GGCCAG": [
        36,
        17
    ],
    "GGCCAT": [
        36,
        49
    ],
    "GGCCCA": [
        4,
        33
    ],
    "GGCCCC": [
        4,
        1
    ],
    "GGCCCG": [
        36,
        1
    ],
    "GGCCCT": [
        36,
        33
    ],
    "GGCCGA": [
        20,
        33
    ],
    "GGCCGC": [
        20,
        1
    ],
    "GGCCGG": [
        52,
        1
    ],
    "GGCCGT": [
        52,
        33
    ],
    "GGCCTA": [
        20,
        49
    ],
    "GGCCTC": [
        20,
        17
    ],
    "GGCCTG": [
        52,
        17
    ],
    "GGCCTT": [
        52,
        49
    ],
    "GGCGAA": [
        12,
        49
    ],
    "GGCGAC": [
        12,
        17
    ],
    "GGCGAG": [
        44,
        17
    ],
    "GGCGAT": [
        44,
        49
    ],
    "GGCGCA": [
        12,
        33
    ],
    "GGCGCC": [
        12,
        1
    ],
    "GGCGCG": [
        44,
        1
    ],
    "GGCGCT": [
        44,
        33
    ],
    "GGCGGA": [
        28,
        33
    ],
    "GGCGGC": [
        28,
        1
    ],
    "GGCGGG": [
        60,
        1
    ],
    "GGCGGT": [
        60,
        33
    ],
    "GGCGTA": [
        28,
        49
    ],
    "GGCGTC": [
        28,
        17
    ],
    "GGCGTG": [
        60,
        17
    ],
    "GGCGTT": [
        60,
        49
    ],
    "GGCTAA": [
        12,
        57
    ],
    "GGCTAC": [
        12,
        25
    ],
    "GGCTAG": [
        44,
        25
    ],
    "GGCTAT": [
        44,
        57
    ],
    "GGCTCA": [
        12,
        41
    ],
    "GGCTCC": [
        12,
        9
    ],
    "GGCTCG": [
        44,
        9
    ],
    "GGCTCT": [
        44,
        41
    ],
    "GGCTGA": [
        28,
        41
    ],
    "GGCTGC": [
        28,
        9
    ],
    "GGCTGG": [
        60,
        9
    ],
    "GGCTGT": [
        60,
        41
    ],
    "GGCTTA": [
        28,
        57
    ],
    "GGCTTC": [
        28,
        25
    ],
    "GGCTTG": [
        60,
        25
    ],
    "GGCTTT": [
        60,
        57
    ],
    "GGGAAA": [
        8,
        57
    ],
    "GGGAAC": [
        8,
        25
    ],
    "GGGAAG": [
        40,
        25
    ],
    "GGGAAT": [
        40,
        57
    ],
    "GGGACA": [
        8,
        41
    ],
    "GGGACC": [
        8,
        9
    ],
    "GGGACG": [
        40,
        9
    ],
    "GGGACT": [
        40,
        41
    ],
    "GGGAGA": [
        24,
        41
    ],
    "GGGAGC": [
        24,
        9
    ],
    "GGGAGG": [
        56,
        9
    ],
    "GGGAGT": [
        56,
        41
    ],
    "GGGATA": [
        24,
        57
    ],
    "GGGATC": [
        24,
        25
    ],
    "GGGATG": [
        56,
        25
    ],
    "GGGATT": [
        56,
        57
    ],
    "GGGCAA": [
        8,
        49
    ],
    "GGGCAC": [
        8,
        17
    ],
    "GGGCAG": [
        40,
        17
    ],
    "GGGCAT": [
        40,
        49
    ],
    "GGGCCA": [
        8,
        33
    ],
    "GGGCCC": [
        8,
        1
    ],
    "GGGCCG": [
        40,
        1
    ],
    "GGGCCT": [
        40,
        33
    ],
    "GGGCGA": [
        24,
        33
    ],
    "GGGCGC": [
        24,
        1
    ],
    "GGGCGG": [
        56,
        1
    ],
    "GGGCGT": [
        56,
        33
    ],
    "GGGCTA": [
        24,
        49
    ],
    "GGGCTC": [
        24,
        17
    ],
    "GGGCTG": [
        56,
        17
    ],
    "GGGCTT": [
        56,
        49
    ],
    "GGGGAA": [
        16,
        49
    ],
    "GGGGAC": [
        16,
        17
    ],
    "GGGGAG": [
        48,
        17
    ],
    "GGGGAT": [
        48,
        49
    ],
    "GGGGCA": [
        16,
        33
    ],
    "GGGGCC": [
        16,
        1
    ],
    "GGGGCG": [
        48,
        1
    ],
    "GGGGCT": [
        48,
        33
    ],
    "GGGGGA": [
        32,
        33
    ],
    "GGGGGC": [
        32,
        1
    ],
    "GGGGGG": [
        64,
        1
    ],
    "GGGGGT": [
        64,
        33
    ],
    "GGGGTA": [
        32,
        49
    ],
    "GGGGTC": [
        32,
        17
    ],
    "GGGGTG": [
        64,
        17
    ],
    "GGGGTT": [
        64,
        49
    ],
    "GGGTAA": [
        16,
        57
    ],
    "GGGTAC": [
        16,
        25
    ],
    "GGGTAG": [
        48,
        25
    ],
    "GGGTAT": [
        48,
        57
    ],
    "GGGTCA": [
        16,
        41
    ],
    "GGGTCC": [
        16,
        9
    ],
    "GGGTCG": [
        48,
        9
    ],
    "GGGTCT": [
        48,
        41
    ],
    "GGGTGA": [
        32,
        41
    ],
    "GGGTGC": [
        32,
        9
    ],
    "GGGTGG": [
        64,
        9
    ],
    "GGGTGT": [
        64,
        41
    ],
    "GGGTTA": [
        32,
        57
    ],
    "GGGTTC": [
        32,
        25
    ],
    "GGGTTG": [
        64,
        25
    ],
    "GGGTTT": [
        64,
        57
    ],
    "GGTAAA": [
        8,
        61
    ],
    "GGTAAC": [
        8,
        29
    ],
    "GGTAAG": [
        40,
        29
    ],
    "GGTAAT": [
        40,
        61
    ],
    "GGTACA": [
        8,
        45
    ],
    "GGTACC": [
        8,
        13
    ],
    "GGTACG": [
        40,
        13
    ],
    "GGTACT": [
        40,
        45
    ],
    "GGTAGA": [
        24,
        45
    ],
    "GGTAGC": [
        24,
        13
    ],
    "GGTAGG": [
        56,
        13
    ],
    "GGTAGT": [
        56,
        45
    ],
    "GGTATA": [
        24,
        61
    ],
    "GGTATC": [
        24,
        29
    ],
    "GGTATG": [
        56,
        29
    ],
    "GGTATT": [
        56,
        61
    ],
    "GGTCAA": [
        8,
        53
    ],
    "GGTCAC": [
        8,
        21
    ],
    "GGTCAG": [
        40,
        21
    ],
    "GGTCAT": [
        40,
        53
    ],
    "GGTCCA": [
        8,
        37
    ],
    "GGTCCC": [
        8,
        5
    ],
    "GGTCCG": [
        40,
        5
    ],
    "GGTCCT": [
        40,
        37
    ],
    "GGTCGA": [
        24,
        37
    ],
    "GGTCGC": [
        24,
        5
    ],
    "GGTCGG": [
        56,
        5
    ],
    "GGTCGT": [
        56,
        37
    ],
    "GGTCTA": [
        24,
        53
    ],
    "GGTCTC": [
        24,
        21
    ],
    "GGTCTG": [
        56,
        21
    ],
    "GGTCTT": [
        56,
        53
    ],
    "GGTGAA": [
        16,
        53
    ],
    "GGTGAC": [
        16,
        21
    ],
    "GGTGAG": [
        48,
        21
    ],
    "GGTGAT": [
        48,
        53
    ],
    "GGTGCA": [
        16,
        37
    ],
    "GGTGCC": [
        16,
        5
    ],
    "GGTGCG": [
        48,
        5
    ],
    "GGTGCT": [
        48,
        37
    ],
    "GGTGGA": [
        32,
        37
    ],
    "GGTGGC": [
        32,
        5
    ],
    "GGTGGG": [
        64,
        5
    ],
    "GGTGGT": [
        64,
        37
    ],
    "GGTGTA": [
        32,
        53
    ],
    "GGTGTC": [
        32,
        21
    ],
    "GGTGTG": [
        64,
        21
    ],
    "GGTGTT": [
        64,
        53
    ],
    "GGTTAA": [
        16,
        61
    ],
    "GGTTAC": [
        16,
        29
    ],
    "GGTTAG": [
        48,
        29
    ],
    "GGTTAT": [
        48,
        61
    ],
    "GGTTCA": [
        16,
        45
    ],
    "GGTTCC": [
        16,
        13
    ],
    "GGTTCG": [
        48,
        13
    ],
    "GGTTCT": [
        48,
        45
    ],
    "GGTTGA": [
        32,
        45
    ],
    "GGTTGC": [
        32,
        13
    ],
    "GGTTGG": [
        64,
        13
    ],
    "GGTTGT": [
        64,
        45
    ],
    "GGTTTA": [
        32,
        61
    ],
    "GGTTTC": [
        32,
        29
    ],
    "GGTTTG": [
        64,
        29
    ],
    "GGTTTT": [
        64,
        61
    ],
    "GTAAAA": [
        4,
        63
    ],
    "GTAAAC": [
        4,
        31
    ],
    "GTAAAG": [
        36,
        31
    ],
    "GTAAAT": [
        36,
        63
    ],
    "GTAACA": [
        4,
        47
    ],
    "GTAACC": [
        4,
        15
    ],
    "GTAACG": [
        36,
        15
    ],
    "GTAACT": [
        36,
        47
    ],
    "GTAAGA": [
        20,
        47
    ],
    "GTAAGC": [
        20,
        15
    ],
    "GTAAGG": [
        52,
        15
    ],
    "GTAAGT": [
        52,
        47
    ],
    "GTAATA": [
        20,
        63
    ],
    "GTAATC": [
        20,
        31
    ],
    "GTAATG": [
        52,
        31
    ],
    "GTAATT": [
        52,
        63
    ],
    "GTACAA": [
        4,
        55
    ],
    "GTACAC": [
        4,
        23
    ],
    "GTACAG": [
        36,
        23
    ],
    "GTACAT": [
        36,
        55
    ],
    "GTACCA": [
        4,
        39
    ],
    "GTACCC": [
        4,
        7
    ],
    "GTACCG": [
        36,
        7
    ],
    "GTACCT": [
        36,
        39
    ],
    "GTACGA": [
        20,
        39
    ],
    "GTACGC": [
        20,
        7
    ],
    "GTACGG": [
        52,
        7
    ],
    "GTACGT": [
        52,
        39
    ],
    "GTACTA": [
        20,
        55
    ],
    "GTACTC": [
        20,
        23
    ],
    "GTACTG": [
        52,
        23
    ],
    "GTACTT": [
        52,
        55
    ],
    "GTAGAA": [
        12,
        55
    ],
    "GTAGAC": [
        12,
        23
    ],
    "GTAGAG": [
        44,
        23
    ],
    "GTAGAT": [
        44,
        55
    ],
    "GTAGCA": [
        12,
        39
    ],
    "GTAGCC": [
        12,
        7
    ],
    "GTAGCG": [
        44,
        7
    ],
    "GTAGCT": [
        44,
        39
    ],
    "GTAGGA": [
        28,
        39
    ],
    "GTAGGC": [
        28,
        7
    ],
    "GTAGGG": [
        60,
        7
    ],
    "GTAGGT": [
        60,
        39
    ],
    "GTAGTA": [
        28,
        55
    ],
    "GTAGTC": [
        28,
        23
    ],
    "GTAGTG": [
        60,
        23
    ],
    "GTAGTT": [
        60,
        55
    ],
    "GTATAA": [
        12,
        63
    ],
    "GTATAC": [
        12,
        31
    ],
    "GTATAG": [
        44,
        31
    ],
    "GTATAT": [
        44,
        63
    ],
    "GTATCA": [
        12,
        47
    ],
    "GTATCC": [
        12,
        15
    ],
    "GTATCG": [
        44,
        15
    ],
    "GTATCT": [
        44,
        47
    ],
    "GTATGA": [
        28,
        47
    ],
    "GTATGC": [
        28,
        15
    ],
    "GTATGG": [
        60,
        15
    ],
    "GTATGT": [
        60,
        47
    ],
    "GTATTA": [
        28,
        63
    ],
    "GTATTC": [
        28,
        31
    ],
    "GTATTG": [
        60,
        31
    ],
    "GTATTT": [
        60,
        63
    ],
    "GTCAAA": [
        4,
        59
    ],
    "GTCAAC": [
        4,
        27
    ],
    "GTCAAG": [
        36,
        27
    ],
    "GTCAAT": [
        36,
        59
    ],
    "GTCACA": [
        4,
        43
    ],
    "GTCACC": [
        4,
        11
    ],
    "GTCACG": [
        36,
        11
    ],
    "GTCACT": [
        36,
        43
    ],
    "GTCAGA": [
        20,
        43
    ],
    "GTCAGC": [
        20,
        11
    ],
    "GTCAGG": [
        52,
        11
    ],
    "GTCAGT": [
        52,
        43
    ],
    "GTCATA": [
        20,
        59
    ],
    "GTCATC": [
        20,
        27
    ],
    "GTCATG": [
        52,
        27
    ],
    "GTCATT": [
        52,
        59
    ],
    "GTCCAA": [
        4,
        51
    ],
    "GTCCAC": [
        4,
        19
    ],
    "GTCCAG": [
        36,
        19
    ],
    "GTCCAT": [
        36,
        51
    ],
    "GTCCCA": [
        4,
        35
    ],
    "GTCCCC": [
        4,
        3
    ],
    "GTCCCG": [
        36,
        3
    ],
    "GTCCCT": [
        36,
        35
    ],
    "GTCCGA": [
        20,
        35
    ],
    "GTCCGC": [
        20,
        3
    ],
    "GTCCGG": [
        52,
        3
    ],
    "GTCCGT": [
        52,
        35
    ],
    "GTCCTA": [
        20,
        51
    ],
    "GTCCTC": [
        20,
        19
    ],
    "GTCCTG": [
        52,
        19
    ],
    "GTCCTT": [
        52,
        51
    ],
    "GTCGAA": [
        12,
        51
    ],
    "GTCGAC": [
        12,
        19
    ],
    "GTCGAG": [
        44,
        19
    ],
    "GTCGAT": [
        44,
        51
    ],
    "GTCGCA": [
        12,
        35
    ],
    "GTCGCC": [
        12,
        3
    ],
    "GTCGCG": [
        44,
        3
    ],
    "GTCGCT": [
        44,
        35
    ],
    "GTCGGA": [
        28,
        35
    ],
    "GTCGGC": [
        28,
        3
    ],
    "GTCGGG": [
        60,
        3
    ],
    "GTCGGT": [
        60,
        35
    ],
    "GTCGTA": [
        28,
        51
    ],
    "GTCGTC": [
        28,
        19
    ],
    "GTCGTG": [
        60,
        19
    ],
    "GTCGTT": [
        60,
        51
    ],
    "GTCTAA": [
        12,
        59
    ],
    "GTCTAC": [
        12,
        27
    ],
    "GTCTAG": [
        44,
        27
    ],
    "GTCTAT": [
        44,
        59
    ],
    "GTCTCA": [
        12,
        43
    ],
    "GTCTCC": [
        12,
        11
    ],
    "GTCTCG": [
        44,
        11
    ],
    "GTCTCT": [
        44,
        43
    ],
    "GTCTGA": [
        28,
        43
    ],
    "GTCTGC": [
        28,
        11
    ],
    "GTCTGG": [
        60,
        11
    ],
    "GTCTGT": [
        60,
        43
    ],
    "GTCTTA": [
        28,
        59
    ],
    "GTCTTC": [
        28,
        27
    ],
    "GTCTTG": [
        60,
        27
    ],
    "GTCTTT": [
        60,
        59
    ],
    "GTGAAA": [
        8,
        59
    ],
    "GTGAAC": [
        8,
        27
    ],
    "GTGAAG": [
        40,
        27
    ],
    "GTGAAT": [
        40,
        59
    ],
    "GTGACA": [
        8,
        43
    ],
    "GTGACC": [
        8,
        11
    ],
    "GTGACG": [
        40,
        11
    ],
    "GTGACT": [
        40,
        43
    ],
    "GTGAGA": [
        24,
        43
    ],
    "GTGAGC": [
        24,
        11
    ],
    "GTGAGG": [
        56,
        11
    ],
    "GTGAGT": [
        56,
        43
    ],
    "GTGATA": [
        24,
        59
    ],
    "GTGATC": [
        24,
        27
    ],
    "GTGATG": [
        56,
        27
    ],
    "GTGATT": [
        56,
        59
    ],
    "GTGCAA": [
        8,
        51
    ],
    "GTGCAC": [
        8,
        19
    ],
    "GTGCAG": [
        40,
        19
    ],
    "GTGCAT": [
        40,
        51
    ],
    "GTGCCA": [
        8,
        35
    ],
    "GTGCCC": [
        8,
        3
    ],
    "GTGCCG": [
        40,
        3
    ],
    "GTGCCT": [
        40,
        35
    ],
    "GTGCGA": [
        24,
        35
    ],
    "GTGCGC": [
        24,
        3
    ],
    "GTGCGG": [
        56,
        3
    ],
    "GTGCGT": [
        56,
        35
    ],
    "GTGCTA": [
        24,
        51
    ],
    "GTGCTC": [
        24,
        19
    ],
    "GTGCTG": [
        56,
        19
    ],
    "GTGCTT": [
        56,
        51
    ],
    "GTGGAA": [
        16,
        51
    ],
    "GTGGAC": [
        16,
        19
    ],
    "GTGGAG": [
        48,
        19
    ],
    "GTGGAT": [
        48,
        51
    ],
    "GTGGCA": [
        16,
        35
    ],
    "GTGGCC": [
        16,
        3
    ],
    "GTGGCG": [
        48,
        3
    ],
    "GTGGCT": [
        48,
        35
    ],
    "GTGGGA": [
        32,
        35
    ],
    "GTGGGC": [
        32,
        3
    ],
    "GTGGGG": [
        64,
        3
    ],
    "GTGGGT": [
        64,
        35
    ],
    "GTGGTA": [
        32,
        51
    ],
    "GTGGTC": [
        32,
        19
    ],
    "GTGGTG": [
        64,
        19
    ],
    "GTGGTT": [
        64,
        51
    ],
    "GTGTAA": [
        16,
        59
    ],
    "GTGTAC": [
        16,
        27
    ],
    "GTGTAG": [
        48,
        27
    ],
    "GTGTAT": [
        48,
        59
    ],
    "GTGTCA": [
        16,
        43
    ],
    "GTGTCC": [
        16,
        11
    ],
    "GTGTCG": [
        48,
        11
    ],
    "GTGTCT": [
        48,
        43
    ],
    "GTGTGA": [
        32,
        43
    ],
    "GTGTGC": [
        32,
        11
    ],
    "GTGTGG": [
        64,
        11
    ],
    "GTGTGT": [
        64,
        43
    ],
    "GTGTTA": [
        32,
        59
    ],
    "GTGTTC": [
        32,
        27
    ],
    "GTGTTG": [
        64,
        27
    ],
    "GTGTTT": [
        64,
        59
    ],
    "GTTAAA": [
        8,
        63
    ],
    "GTTAAC": [
        8,
        31
    ],
    "GTTAAG": [
        40,
        31
    ],
    "GTTAAT": [
        40,
        63
    ],
    "GTTACA": [
        8,
        47
    ],
    "GTTACC": [
        8,
        15
    ],
    "GTTACG": [
        40,
        15
    ],
    "GTTACT": [
        40,
        47
    ],
    "GTTAGA": [
        24,
        47
    ],
    "GTTAGC": [
        24,
        15
    ],
    "GTTAGG": [
        56,
        15
    ],
    "GTTAGT": [
        56,
        47
    ],
    "GTTATA": [
        24,
        63
    ],
    "GTTATC": [
        24,
        31
    ],
    "GTTATG": [
        56,
        31
    ],
    "GTTATT": [
        56,
        63
    ],
    "GTTCAA": [
        8,
        55
    ],
    "GTTCAC": [
        8,
        23
    ],
    "GTTCAG": [
        40,
        23
    ],
    "GTTCAT": [
        40,
        55
    ],
    "GTTCCA": [
        8,
        39
    ],
    "GTTCCC": [
        8,
        7
    ],
    "GTTCCG": [
        40,
        7
    ],
    "GTTCCT": [
        40,
        39
    ],
    "GTTCGA": [
        24,
        39
    ],
    "GTTCGC": [
        24,
        7
    ],
    "GTTCGG": [
        56,
        7
    ],
    "GTTCGT": [
        56,
        39
    ],
    "GTTCTA": [
        24,
        55
    ],
    "GTTCTC": [
        24,
        23
    ],
    "GTTCTG": [
        56,
        23
    ],
    "GTTCTT": [
        56,
        55
    ],
    "GTTGAA": [
        16,
        55
    ],
    "GTTGAC": [
        16,
        23
    ],
    "GTTGAG": [
        48,
        23
    ],
    "GTTGAT": [
        48,
        55
    ],
    "GTTGCA": [
        16,
        39
    ],
    "GTTGCC": [
        16,
        7
    ],
    "GTTGCG": [
        48,
        7
    ],
    "GTTGCT": [
        48,
        39
    ],
    "GTTGGA": [
        32,
        39
    ],
    "GTTGGC": [
        32,
        7
    ],
    "GTTGGG": [
        64,
        7
    ],
    "GTTGGT": [
        64,
        39
    ],
    "GTTGTA": [
        32,
        55
    ],
    "GTTGTC": [
        32,
        23
    ],
    "GTTGTG": [
        64,
        23
    ],
    "GTTGTT": [
        64,
        55
    ],
    "GTTTAA": [
        16,
        63
    ],
    "GTTTAC": [
        16,
        31
    ],
    "GTTTAG": [
        48,
        31
    ],
    "GTTTAT": [
        48,
        63
    ],
    "GTTTCA": [
        16,
        47
    ],
    "GTTTCC": [
        16,
        15
    ],
    "GTTTCG": [
        48,
        15
    ],
    "GTTTCT": [
        48,
        47
    ],
    "GTTTGA": [
        32,
        47
    ],
    "GTTTGC": [
        32,
        15
    ],
    "GTTTGG": [
        64,
        15
    ],
    "GTTTGT": [
        64,
        47
    ],
    "GTTTTA": [
        32,
        63
    ],
    "GTTTTC": [
        32,
        31
    ],
    "GTTTTG": [
        64,
        31
    ],
    "GTTTTT": [
        64,
        63
    ],
    "TAAAAA": [
        2,
        64
    ],
    "TAAAAC": [
        2,
        32
    ],
    "TAAAAG": [
        34,
        32
    ],
    "TAAAAT": [
        34,
        64
    ],
    "TAAACA": [
        2,
        48
    ],
    "TAAACC": [
        2,
        16
    ],
    "TAAACG": [
        34,
        16
    ],
    "TAAACT": [
        34,
        48
    ],
    "TAAAGA": [
        18,
        48
    ],
    "TAAAGC": [
        18,
        16
    ],
    "TAAAGG": [
        50,
        16
    ],
    "TAAAGT": [
        50,
        48
    ],
    "TAAATA": [
        18,
        64
    ],
    "TAAATC": [
        18,
        32
    ],
    "TAAATG": [
        50,
        32
    ],
    "TAAATT": [
        50,
        64
    ],
    "TAACAA": [
        2,
        56
    ],
    "TAACAC": [
        2,
        24
    ],
    "TAACAG": [
        34,
        24
    ],
    "TAACAT": [
        34,
        56
    ],
    "TAACCA": [
        2,
        40
    ],
    "TAACCC": [
        2,
        8
    ],
    "TAACCG": [
        34,
        8
    ],
    "TAACCT": [
        34,
        40
    ],
    "TAACGA": [
        18,
        40
    ],
    "TAACGC": [
        18,
        8
    ],
    "TAACGG": [
        50,
        8
    ],
    "TAACGT": [
        50,
        40
    ],
    "TAACTA": [
        18,
        56
    ],
    "TAACTC": [
        18,
        24
    ],
    "TAACTG": [
        50,
        24
    ],
    "TAACTT": [
        50,
        56
    ],
    "TAAGAA": [
        10,
        56
    ],
    "TAAGAC": [
        10,
        24
    ],
    "TAAGAG": [
        42,
        24
    ],
    "TAAGAT": [
        42,
        56
    ],
    "TAAGCA": [
        10,
        40
    ],
    "TAAGCC": [
        10,
        8
    ],
    "TAAGCG": [
        42,
        8
    ],
    "TAAGCT": [
        42,
        40
    ],
    "TAAGGA": [
        26,
        40
    ],
    "TAAGGC": [
        26,
        8
    ],
    "TAAGGG": [
        58,
        8
    ],
    "TAAGGT": [
        58,
        40
    ],
    "TAAGTA": [
        26,
        56
    ],
    "TAAGTC": [
        26,
        24
    ],
    "TAAGTG": [
        58,
        24
    ],
    "TAAGTT": [
        58,
        56
    ],
    "TAATAA": [
        10,
        64
    ],
    "TAATAC": [
        10,
        32
    ],
    "TAATAG": [
        42,
        32
    ],
    "TAATAT": [
        42,
        64
    ],
    "TAATCA": [
        10,
        48
    ],
    "TAATCC": [
        10,
        16
    ],
    "TAATCG": [
        42,
        16
    ],
    "TAATCT": [
        42,
        48
    ],
    "TAATGA": [
        26,
        48
    ],
    "TAATGC": [
        26,
        16
    ],
    "TAATGG": [
        58,
        16
    ],
    "TAATGT": [
        58,
        48
    ],
    "TAATTA": [
        26,
        64
    ],
    "TAATTC": [
        26,
        32
    ],
    "TAATTG": [
        58,
        32
    ],
    "TAATTT": [
        58,
        64
    ],
    "TACAAA": [
        2,
        60
    ],
    "TACAAC": [
        2,
        28
    ],
    "TACAAG": [
        34,
        28
    ],
    "TACAAT": [
        34,
        60
    ],
    "TACACA": [
        2,
        44
    ],
    "TACACC": [
        2,
        12
    ],
    "TACACG": [
        34,
        12
    ],
    "TACACT": [
        34,
        44
    ],
    "TACAGA": [
        18,
        44
    ],
    "TACAGC": [
        18,
        12
    ],
    "TACAGG": [
        50,
        12
    ],
    "TACAGT": [
        50,
        44
    ],
    "TACATA": [
        18,
        60
    ],
    "TACATC": [
        18,
        28
    ],
    "TACATG": [
        50,
        28
    ],
    "TACATT": [
        50,
        60
    ],
    "TACCAA": [
        2,
        52
    ],
    "TACCAC": [
        2,
        20
    ],
    "TACCAG": [
        34,
        20
    ],
    "TACCAT": [
        34,
        52
    ],
    "TACCCA": [
        2,
        36
    ],
    "TACCCC": [
        2,
        4
    ],
    "TACCCG": [
        34,
        4
    ],
    "TACCCT": [
        34,
        36
    ],
    "TACCGA": [
        18,
        36
    ],
    "TACCGC": [
        18,
        4
    ],
    "TACCGG": [
        50,
        4
    ],
    "TACCGT": [
        50,
        36
    ],
    "TACCTA": [
        18,
        52
    ],
    "TACCTC": [
        18,
        20
    ],
    "TACCTG": [
        50,
        20
    ],
    "TACCTT": [
        50,
        52
    ],
    "TACGAA": [
        10,
        52
    ],
    "TACGAC": [
        10,
        20
    ],
    "TACGAG": [
        42,
        20
    ],
    "TACGAT": [
        42,
        52
    ],
    "TACGCA": [
        10,
        36
    ],
    "TACGCC": [
        10,
        4
    ],
    "TACGCG": [
        42,
        4
    ],
    "TACGCT": [
        42,
        36
    ],
    "TACGGA": [
        26,
        36
    ],
    "TACGGC": [
        26,
        4
    ],
    "TACGGG": [
        58,
        4
    ],
    "TACGGT": [
        58,
        36
    ],
    "TACGTA": [
        26,
        52
    ],
    "TACGTC": [
        26,
        20
    ],
    "TACGTG": [
        58,
        20
    ],
    "TACGTT": [
        58,
        52
    ],
    "TACTAA": [
        10,
        60
    ],
    "TACTAC": [
        10,
        28
    ],
    "TACTAG": [
        42,
        28
    ],
    "TACTAT": [
        42,
        60
    ],
    "TACTCA": [
        10,
        44
    ],
    "TACTCC": [
        10,
        12
    ],
    "TACTCG": [
        42,
        12
    ],
    "TACTCT": [
        42,
        44
    ],
    "TACTGA": [
        26,
        44
    ],
    "TACTGC": [
        26,
        12
    ],
    "TACTGG": [
        58,
        12
    ],
    "TACTGT": [
        58,
        44
    ],
    "TACTTA": [
        26,
        60
    ],
    "TACTTC": [
        26,
        28
    ],
    "TACTTG": [
        58,
        28
    ],
    "TACTTT": [
        58,
        60
    ],
    "TAGAAA": [
        6,
        60
    ],
    "TAGAAC": [
        6,
        28
    ],
    "TAGAAG": [
        38,
        28
    ],
    "TAGAAT": [
        38,
        60
    ],
    "TAGACA": [
        6,
        44
    ],
    "TAGACC": [
        6,
        12
    ],
    "TAGACG": [
        38,
        12
    ],
    "TAGACT": [
        38,
        44
    ],
    "TAGAGA": [
        22,
        44
    ],
    "TAGAGC": [
        22,
        12
    ],
    "TAGAGG": [
        54,
        12
    ],
    "TAGAGT": [
        54,
        44
    ],
    "TAGATA": [
        22,
        60
    ],
    "TAGATC": [
        22,
        28
    ],
    "TAGATG": [
        54,
        28
    ],
    "TAGATT": [
        54,
        60
    ],
    "TAGCAA": [
        6,
        52
    ],
    "TAGCAC": [
        6,
        20
    ],
    "TAGCAG": [
        38,
        20
    ],
    "TAGCAT": [
        38,
        52
    ],
    "TAGCCA": [
        6,
        36
    ],
    "TAGCCC": [
        6,
        4
    ],
    "TAGCCG": [
        38,
        4
    ],
    "TAGCCT": [
        38,
        36
    ],
    "TAGCGA": [
        22,
        36
    ],
    "TAGCGC": [
        22,
        4
    ],
    "TAGCGG": [
        54,
        4
    ],
    "TAGCGT": [
        54,
        36
    ],
    "TAGCTA": [
        22,
        52
    ],
    "TAGCTC": [
        22,
        20
    ],
    "TAGCTG": [
        54,
        20
    ],
    "TAGCTT": [
        54,
        52
    ],
    "TAGGAA": [
        14,
        52
    ],
    "TAGGAC": [
        14,
        20
    ],
    "TAGGAG": [
        46,
        20
    ],
    "TAGGAT": [
        46,
        52
    ],
    "TAGGCA": [
        14,
        36
    ],
    "TAGGCC": [
        14,
        4
    ],
    "TAGGCG": [
        46,
        4
    ],
    "TAGGCT": [
        46,
        36
    ],
    "TAGGGA": [
        30,
        36
    ],
    "TAGGGC": [
        30,
        4
    ],
    "TAGGGG": [
        62,
        4
    ],
    "TAGGGT": [
        62,
        36
    ],
    "TAGGTA": [
        30,
        52
    ],
    "TAGGTC": [
        30,
        20
    ],
    "TAGGTG": [
        62,
        20
    ],
    "TAGGTT": [
        62,
        52
    ],
    "TAGTAA": [
        14,
        60
    ],
    "TAGTAC": [
        14,
        28
    ],
    "TAGTAG": [
        46,
        28
    ],
    "TAGTAT": [
        46,
        60
    ],
    "TAGTCA": [
        14,
        44
    ],
    "TAGTCC": [
        14,
        12
    ],
    "TAGTCG": [
        46,
        12
    ],
    "TAGTCT": [
        46,
        44
    ],
    "TAGTGA": [
        30,
        44
    ],
    "TAGTGC": [
        30,
        12
    ],
    "TAGTGG": [
        62,
        12
    ],
    "TAGTGT": [
        62,
        44
    ],
    "TAGTTA": [
        30,
        60
    ],
    "TAGTTC": [
        30,
        28
    ],
    "TAGTTG": [
        62,
        28
    ],
    "TAGTTT": [
        62,
        60
    ],
    "TATAAA": [
        6,
        64
    ],
    "TATAAC": [
        6,
        32
    ],
    "TATAAG": [
        38,
        32
    ],
    "TATAAT": [
        38,
        64
    ],
    "TATACA": [
        6,
        48
    ],
    "TATACC": [
        6,
        16
    ],
    "TATACG": [
        38,
        16
    ],
    "TATACT": [
        38,
        48
    ],
    "TATAGA": [
        22,
        48
    ],
    "TATAGC": [
        22,
        16
    ],
    "TATAGG": [
        54,
        16
    ],
    "TATAGT": [
        54,
        48
    ],
    "TATATA": [
        22,
        64
    ],
    "TATATC": [
        22,
        32
    ],
    "TATATG": [
        54,
        32
    ],
    "TATATT": [
        54,
        64
    ],
    "TATCAA": [
        6,
        56
    ],
    "TATCAC": [
        6,
        24
    ],
    "TATCAG": [
        38,
        24
    ],
    "TATCAT": [
        38,
        56
    ],
    "TATCCA": [
        6,
        40
    ],
    "TATCCC": [
        6,
        8
    ],
    "TATCCG": [
        38,
        8
    ],
    "TATCCT": [
        38,
        40
    ],
    "TATCGA": [
        22,
        40
    ],
    "TATCGC": [
        22,
        8
    ],
    "TATCGG": [
        54,
        8
    ],
    "TATCGT": [
        54,
        40
    ],
    "TATCTA": [
        22,
        56
    ],
    "TATCTC": [
        22,
        24
    ],
    "TATCTG": [
        54,
        24
    ],
    "TATCTT": [
        54,
        56
    ],
    "TATGAA": [
        14,
        56
    ],
    "TATGAC": [
        14,
        24
    ],
    "TATGAG": [
        46,
        24
    ],
    "TATGAT": [
        46,
        56
    ],
    "TATGCA": [
        14,
        40
    ],
    "TATGCC": [
        14,
        8
    ],
    "TATGCG": [
        46,
        8
    ],
    "TATGCT": [
        46,
        40
    ],
    "TATGGA": [
        30,
        40
    ],
    "TATGGC": [
        30,
        8
    ],
    "TATGGG": [
        62,
        8
    ],
    "TATGGT": [
        62,
        40
    ],
    "TATGTA": [
        30,
        56
    ],
    "TATGTC": [
        30,
        24
    ],
    "TATGTG": [
        62,
        24
    ],
    "TATGTT": [
        62,
        56
    ],
    "TATTAA": [
        14,
        64
    ],
    "TATTAC": [
        14,
        32
    ],
    "TATTAG": [
        46,
        32
    ],
    "TATTAT": [
        46,
        64
    ],
    "TATTCA": [
        14,
        48
    ],
    "TATTCC": [
        14,
        16
    ],
    "TATTCG": [
        46,
        16
    ],
    "TATTCT": [
        46,
        48
    ],
    "TATTGA": [
        30,
        48
    ],
    "TATTGC": [
        30,
        16
    ],
    "TATTGG": [
        62,
        16
    ],
    "TATTGT": [
        62,
        48
    ],
    "TATTTA": [
        30,
        64
    ],
    "TATTTC": [
        30,
        32
    ],
    "TATTTG": [
        62,
        32
    ],
    "TATTTT": [
        62,
        64
    ],
    "TCAAAA": [
        2,
        62
    ],
    "TCAAAC": [
        2,
        30
    ],
    "TCAAAG": [
        34,
        30
    ],
    "TCAAAT": [
        34,
        62
    ],
    "TCAACA": [
        2,
        46
    ],
    "TCAACC": [
        2,
        14
    ],
    "TCAACG": [
        34,
        14
    ],
    "TCAACT": [
        34,
        46
    ],
    "TCAAGA": [
        18,
        46
    ],
    "TCAAGC": [
        18,
        14
    ],
    "TCAAGG": [
        50,
        14
    ],
    "TCAAGT": [
        50,
        46
    ],
    "TCAATA": [
        18,
        62
    ],
    "TCAATC": [
        18,
        30
    ],
    "TCAATG": [
        50,
        30
    ],
    "TCAATT": [
        50,
        62
    ],
    "TCACAA": [
        2,
        54
    ],
    "TCACAC": [
        2,
        22
    ],
    "TCACAG": [
        34,
        22
    ],
    "TCACAT": [
        34,
        54
    ],
    "TCACCA": [
        2,
        38
    ],
    "TCACCC": [
        2,
        6
    ],
    "TCACCG": [
        34,
        6
    ],
    "TCACCT": [
        34,
        38
    ],
    "TCACGA": [
        18,
        38
    ],
    "TCACGC": [
        18,
        6
    ],
    "TCACGG": [
        50,
        6
    ],
    "TCACGT": [
        50,
        38
    ],
    "TCACTA": [
        18,
        54
    ],
    "TCACTC": [
        18,
        22
    ],
    "TCACTG": [
        50,
        22
    ],
    "TCACTT": [
        50,
        54
    ],
    "TCAGAA": [
        10,
        54
    ],
    "TCAGAC": [
        10,
        22
    ],
    "TCAGAG": [
        42,
        22
    ],
    "TCAGAT": [
        42,
        54
    ],
    "TCAGCA": [
        10,
        38
    ],
    "TCAGCC": [
        10,
        6
    ],
    "TCAGCG": [
        42,
        6
    ],
    "TCAGCT": [
        42,
        38
    ],
    "TCAGGA": [
        26,
        38
    ],
    "TCAGGC": [
        26,
        6
    ],
    "TCAGGG": [
        58,
        6
    ],
    "TCAGGT": [
        58,
        38
    ],
    "TCAGTA": [
        26,
        54
    ],
    "TCAGTC": [
        26,
        22
    ],
    "TCAGTG": [
        58,
        22
    ],
    "TCAGTT": [
        58,
        54
    ],
    "TCATAA": [
        10,
        62
    ],
    "TCATAC": [
        10,
        30
    ],
    "TCATAG": [
        42,
        30
    ],
    "TCATAT": [
        42,
        62
    ],
    "TCATCA": [
        10,
        46
    ],
    "TCATCC": [
        10,
        14
    ],
    "TCATCG": [
        42,
        14
    ],
    "TCATCT": [
        42,
        46
    ],
    "TCATGA": [
        26,
        46
    ],
    "TCATGC": [
        26,
        14
    ],
    "TCATGG": [
        58,
        14
    ],
    "TCATGT": [
        58,
        46
    ],
    "TCATTA": [
        26,
        62
    ],
    "TCATTC": [
        26,
        30
    ],
    "TCATTG": [
        58,
        30
    ],
    "TCATTT": [
        58,
        62
    ],
    "TCCAAA": [
        2,
        58
    ],
    "TCCAAC": [
        2,
        26
    ],
    "TCCAAG": [
        34,
        26
    ],
    "TCCAAT": [
        34,
        58
    ],
    "TCCACA": [
        2,
        42
    ],
    "TCCACC": [
        2,
        10
    ],
    "TCCACG": [
        34,
        10
    ],
    "TCCACT": [
        34,
        42
    ],
    "TCCAGA": [
        18,
        42
    ],
    "TCCAGC": [
        18,
        10
    ],
    "TCCAGG": [
        50,
        10
    ],
    "TCCAGT": [
        50,
        42
    ],
    "TCCATA": [
        18,
        58
    ],
    "TCCATC": [
        18,
        26
    ],
    "TCCATG": [
        50,
        26
    ],
    "TCCATT": [
        50,
        58
    ],
    "TCCCAA": [
        2,
        50
    ],
    "TCCCAC": [
        2,
        18
    ],
    "TCCCAG": [
        34,
        18
    ],
    "TCCCAT": [
        34,
        50
    ],
    "TCCCCA": [
        2,
        34
    ],
    "TCCCCC": [
        2,
        2
    ],
    "TCCCCG": [
        34,
        2
    ],
    "TCCCCT": [
        34,
        34
    ],
    "TCCCGA": [
        18,
        34
    ],
    "TCCCGC": [
        18,
        2
    ],
    "TCCCGG": [
        50,
        2
    ],
    "TCCCGT": [
        50,
        34
    ],
    "TCCCTA": [
        18,
        50
    ],
    "TCCCTC": [
        18,
        18
    ],
    "TCCCTG": [
        50,
        18
    ],
    "TCCCTT": [
        50,
        50
    ],
    "TCCGAA": [
        10,
        50
    ],
    "TCCGAC": [
        10,
        18
    ],
    "TCCGAG": [
        42,
        18
    ],
    "TCCGAT": [
        42,
        50
    ],
    "TCCGCA": [
        10,
        34
    ],
    "TCCGCC": [
        10,
        2
    ],
    "TCCGCG": [
        42,
        2
    ],
    "TCCGCT": [
        42,
        34
    ],
    "TCCGGA": [
        26,
        34
    ],
    "TCCGGC": [
        26,
        2
    ],
    "TCCGGG": [
        58,
        2
    ],
    "TCCGGT": [
        58,
        34
    ],
    "TCCGTA": [
        26,
        50
    ],
    "TCCGTC": [
        26,
        18
    ],
    "TCCGTG": [
        58,
        18
    ],
    "TCCGTT": [
        58,
        50
    ],
    "TCCTAA": [
        10,
        58
    ],
    "TCCTAC": [
        10,
        26
    ],
    "TCCTAG": [
        42,
        26
    ],
    "TCCTAT": [
        42,
        58
    ],
    "TCCTCA": [
        10,
        42
    ],
    "TCCTCC": [
        10,
        10
    ],
    "TCCTCG": [
        42,
        10
    ],
    "TCCTCT": [
        42,
        42
    ],
    "TCCTGA": [
        26,
        42
    ],
    "TCCTGC": [
        26,
        10
    ],
    "TCCTGG": [
        58,
        10
    ],
    "TCCTGT": [
        58,
        42
    ],
    "TCCTTA": [
        26,
        58
    ],
    "TCCTTC": [
        26,
        26
    ],
    "TCCTTG": [
        58,
        26
    ],
    "TCCTTT": [
        58,
        58
    ],
    "TCGAAA": [
        6,
        58
    ],
    "TCGAAC": [
        6,
        26
    ],
    "TCGAAG": [
        38,
        26
    ],
    "TCGAAT": [
        38,
        58
    ],
    "TCGACA": [
        6,
        42
    ],
    "TCGACC": [
        6,
        10
    ],
    "TCGACG": [
        38,
        10
    ],
    "TCGACT": [
        38,
        42
    ],
    "TCGAGA": [
        22,
        42
    ],
    "TCGAGC": [
        22,
        10
    ],
    "TCGAGG": [
        54,
        10
    ],
    "TCGAGT": [
        54,
        42
    ],
    "TCGATA": [
        22,
        58
    ],
    "TCGATC": [
        22,
        26
    ],
    "TCGATG": [
        54,
        26
    ],
    "TCGATT": [
        54,
        58
    ],
    "TCGCAA": [
        6,
        50
    ],
    "TCGCAC": [
        6,
        18
    ],
    "TCGCAG": [
        38,
        18
    ],
    "TCGCAT": [
        38,
        50
    ],
    "TCGCCA": [
        6,
        34
    ],
    "TCGCCC": [
        6,
        2
    ],
    "TCGCCG": [
        38,
        2
    ],
    "TCGCCT": [
        38,
        34
    ],
    "TCGCGA": [
        22,
        34
    ],
    "TCGCGC": [
        22,
        2
    ],
    "TCGCGG": [
        54,
        2
    ],
    "TCGCGT": [
        54,
        34
    ],
    "TCGCTA": [
        22,
        50
    ],
    "TCGCTC": [
        22,
        18
    ],
    "TCGCTG": [
        54,
        18
    ],
    "TCGCTT": [
        54,
        50
    ],
    "TCGGAA": [
        14,
        50
    ],
    "TCGGAC": [
        14,
        18
    ],
    "TCGGAG": [
        46,
        18
    ],
    "TCGGAT": [
        46,
        50
    ],
    "TCGGCA": [
        14,
        34
    ],
    "TCGGCC": [
        14,
        2
    ],
    "TCGGCG": [
        46,
        2
    ],
    "TCGGCT": [
        46,
        34
    ],
    "TCGGGA": [
        30,
        34
    ],
    "TCGGGC": [
        30,
        2
    ],
    "TCGGGG": [
        62,
        2
    ],
    "TCGGGT": [
        62,
        34
    ],
    "TCGGTA": [
        30,
        50
    ],
    "TCGGTC": [
        30,
        18
    ],
    "TCGGTG": [
        62,
        18
    ],
    "TCGGTT": [
        62,
        50
    ],
    "TCGTAA": [
        14,
        58
    ],
    "TCGTAC": [
        14,
        26
    ],
    "TCGTAG": [
        46,
        26
    ],
    "TCGTAT": [
        46,
        58
    ],
    "TCGTCA": [
        14,
        42
    ],
    "TCGTCC": [
        14,
        10
    ],
    "TCGTCG": [
        46,
        10
    ],
    "TCGTCT": [
        46,
        42
    ],
    "TCGTGA": [
        30,
        42
    ],
    "TCGTGC": [
        30,
        10
    ],
    "TCGTGG": [
        62,
        10
    ],
    "TCGTGT": [
        62,
        42
    ],
    "TCGTTA": [
        30,
        58
    ],
    "TCGTTC": [
        30,
        26
    ],
    "TCGTTG": [
        62,
        26
    ],
    "TCGTTT": [
        62,
        58
    ],
    "TCTAAA": [
        6,
        62
    ],
    "TCTAAC": [
        6,
        30
    ],
    "TCTAAG": [
        38,
        30
    ],
    "TCTAAT": [
        38,
        62
    ],
    "TCTACA": [
        6,
        46
    ],
    "TCTACC": [
        6,
        14
    ],
    "TCTACG": [
        38,
        14
    ],
    "TCTACT": [
        38,
        46
    ],
    "TCTAGA": [
        22,
        46
    ],
    "TCTAGC": [
        22,
        14
    ],
    "TCTAGG": [
        54,
        14
    ],
    "TCTAGT": [
        54,
        46
    ],
    "TCTATA": [
        22,
        62
    ],
    "TCTATC": [
        22,
        30
    ],
    "TCTATG": [
        54,
        30
    ],
    "TCTATT": [
        54,
        62
    ],
    "TCTCAA": [
        6,
        54
    ],
    "TCTCAC": [
        6,
        22
    ],
    "TCTCAG": [
        38,
        22
    ],
    "TCTCAT": [
        38,
        54
    ],
    "TCTCCA": [
        6,
        38
    ],
    "TCTCCC": [
        6,
        6
    ],
    "TCTCCG": [
        38,
        6
    ],
    "TCTCCT": [
        38,
        38
    ],
    "TCTCGA": [
        22,
        38
    ],
    "TCTCGC": [
        22,
        6
    ],
    "TCTCGG": [
        54,
        6
    ],
    "TCTCGT": [
        54,
        38
    ],
    "TCTCTA": [
        22,
        54
    ],
    "TCTCTC": [
        22,
        22
    ],
    "TCTCTG": [
        54,
        22
    ],
    "TCTCTT": [
        54,
        54
    ],
    "TCTGAA": [
        14,
        54
    ],
    "TCTGAC": [
        14,
        22
    ],
    "TCTGAG": [
        46,
        22
    ],
    "TCTGAT": [
        46,
        54
    ],
    "TCTGCA": [
        14,
        38
    ],
    "TCTGCC": [
        14,
        6
    ],
    "TCTGCG": [
        46,
        6
    ],
    "TCTGCT": [
        46,
        38
    ],
    "TCTGGA": [
        30,
        38
    ],
    "TCTGGC": [
        30,
        6
    ],
    "TCTGGG": [
        62,
        6
    ],
    "TCTGGT": [
        62,
        38
    ],
    "TCTGTA": [
        30,
        54
    ],
    "TCTGTC": [
        30,
        22
    ],
    "TCTGTG": [
        62,
        22
    ],
    "TCTGTT": [
        62,
        54
    ],
    "TCTTAA": [
        14,
        62
    ],
    "TCTTAC": [
        14,
        30
    ],
    "TCTTAG": [
        46,
        30
    ],
    "TCTTAT": [
        46,
        62
    ],
    "TCTTCA": [
        14,
        46
    ],
    "TCTTCC": [
        14,
        14
    ],
    "TCTTCG": [
        46,
        14
    ],
    "TCTTCT": [
        46,
        46
    ],
    "TCTTGA": [
        30,
        46
    ],
    "TCTTGC": [
        30,
        14
    ],
    "TCTTGG": [
        62,
        14
    ],
    "TCTTGT": [
        62,
        46
    ],
    "TCTTTA": [
        30,
        62
    ],
    "TCTTTC": [
        30,
        30
    ],
    "TCTTTG": [
        62,
        30
    ],
    "TCTTTT": [
        62,
        62
    ],
    "TGAAAA": [
        4,
        62
    ],
    "TGAAAC": [
        4,
        30
    ],
    "TGAAAG": [
        36,
        30
    ],
    "TGAAAT": [
        36,
        62
    ],
    "TGAACA": [
        4,
        46
    ],
    "TGAACC": [
        4,
        14
    ],
    "TGAACG": [
        36,
        14
    ],
    "TGAACT": [
        36,
        46
    ],
    "TGAAGA": [
        20,
        46
    ],
    "TGAAGC": [
        20,
        14
    ],
    "TGAAGG": [
        52,
        14
    ],
    "TGAAGT": [
        52,
        46
    ],
    "TGAATA": [
        20,
        62
    ],
    "TGAATC": [
        20,
        30
    ],
    "TGAATG": [
        52,
        30
    ],
    "TGAATT": [
        52,
        62
    ],
    "TGACAA": [
        4,
        54
    ],
    "TGACAC": [
        4,
        22
    ],
    "TGACAG": [
        36,
        22
    ],
    "TGACAT": [
        36,
        54
    ],
    "TGACCA": [
        4,
        38
    ],
    "TGACCC": [
        4,
        6
    ],
    "TGACCG": [
        36,
        6
    ],
    "TGACCT": [
        36,
        38
    ],
    "TGACGA": [
        20,
        38
    ],
    "TGACGC": [
        20,
        6
    ],
    "TGACGG": [
        52,
        6
    ],
    "TGACGT": [
        52,
        38
    ],
    "TGACTA": [
        20,
        54
    ],
    "TGACTC": [
        20,
        22
    ],
    "TGACTG": [
        52,
        22
    ],
    "TGACTT": [
        52,
        54
    ],
    "TGAGAA": [
        12,
        54
    ],
    "TGAGAC": [
        12,
        22
    ],
    "TGAGAG": [
        44,
        22
    ],
    "TGAGAT": [
        44,
        54
    ],
    "TGAGCA": [
        12,
        38
    ],
    "TGAGCC": [
        12,
        6
    ],
    "TGAGCG": [
        44,
        6
    ],
    "TGAGCT": [
        44,
        38
    ],
    "TGAGGA": [
        28,
        38
    ],
    "TGAGGC": [
        28,
        6
    ],
    "TGAGGG": [
        60,
        6
    ],
    "TGAGGT": [
        60,
        38
    ],
    "TGAGTA": [
        28,
        54
    ],
    "TGAGTC": [
        28,
        22
    ],
    "TGAGTG": [
        60,
        22
    ],
    "TGAGTT": [
        60,
        54
    ],
    "TGATAA": [
        12,
        62
    ],
    "TGATAC": [
        12,
        30
    ],
    "TGATAG": [
        44,
        30
    ],
    "TGATAT": [
        44,
        62
    ],
    "TGATCA": [
        12,
        46
    ],
    "TGATCC": [
        12,
        14
    ],
    "TGATCG": [
        44,
        14
    ],
    "TGATCT": [
        44,
        46
    ],
    "TGATGA": [
        28,
        46
    ],
    "TGATGC": [
        28,
        14
    ],
    "TGATGG": [
        60,
        14
    ],
    "TGATGT": [
        60,
        46
    ],
    "TGATTA": [
        28,
        62
    ],
    "TGATTC": [
        28,
        30
    ],
    "TGATTG": [
        60,
        30
    ],
    "TGATTT": [
        60,
        62
    ],
    "TGCAAA": [
        4,
        58
    ],
    "TGCAAC": [
        4,
        26
    ],
    "TGCAAG": [
        36,
        26
    ],
    "TGCAAT": [
        36,
        58
    ],
    "TGCACA": [
        4,
        42
    ],
    "TGCACC": [
        4,
        10
    ],
    "TGCACG": [
        36,
        10
    ],
    "TGCACT": [
        36,
        42
    ],
    "TGCAGA": [
        20,
        42
    ],
    "TGCAGC": [
        20,
        10
    ],
    "TGCAGG": [
        52,
        10
    ],
    "TGCAGT": [
        52,
        42
    ],
    "TGCATA": [
        20,
        58
    ],
    "TGCATC": [
        20,
        26
    ],
    "TGCATG": [
        52,
        26
    ],
    "TGCATT": [
        52,
        58
    ],
    "TGCCAA": [
        4,
        50
    ],
    "TGCCAC": [
        4,
        18
    ],
    "TGCCAG": [
        36,
        18
    ],
    "TGCCAT": [
        36,
        50
    ],
    "TGCCCA": [
        4,
        34
    ],
    "TGCCCC": [
        4,
        2
    ],
    "TGCCCG": [
        36,
        2
    ],
    "TGCCCT": [
        36,
        34
    ],
    "TGCCGA": [
        20,
        34
    ],
    "TGCCGC": [
        20,
        2
    ],
    "TGCCGG": [
        52,
        2
    ],
    "TGCCGT": [
        52,
        34
    ],
    "TGCCTA": [
        20,
        50
    ],
    "TGCCTC": [
        20,
        18
    ],
    "TGCCTG": [
        52,
        18
    ],
    "TGCCTT": [
        52,
        50
    ],
    "TGCGAA": [
        12,
        50
    ],
    "TGCGAC": [
        12,
        18
    ],
    "TGCGAG": [
        44,
        18
    ],
    "TGCGAT": [
        44,
        50
    ],
    "TGCGCA": [
        12,
        34
    ],
    "TGCGCC": [
        12,
        2
    ],
    "TGCGCG": [
        44,
        2
    ],
    "TGCGCT": [
        44,
        34
    ],
    "TGCGGA": [
        28,
        34
    ],
    "TGCGGC": [
        28,
        2
    ],
    "TGCGGG": [
        60,
        2
    ],
    "TGCGGT": [
        60,
        34
    ],
    "TGCGTA": [
        28,
        50
    ],
    "TGCGTC": [
        28,
        18
    ],
    "TGCGTG": [
        60,
        18
    ],
    "TGCGTT": [
        60,
        50
    ],
    "TGCTAA": [
        12,
        58
    ],
    "TGCTAC": [
        12,
        26
    ],
    "TGCTAG": [
        44,
        26
    ],
    "TGCTAT": [
        44,
        58
    ],
    "TGCTCA": [
        12,
        42
    ],
    "TGCTCC": [
        12,
        10
    ],
    "TGCTCG": [
        44,
        10
    ],
    "TGCTCT": [
        44,
        42
    ],
    "TGCTGA": [
        28,
        42
    ],
    "TGCTGC": [
        28,
        10
    ],
    "TGCTGG": [
        60,
        10
    ],
    "TGCTGT": [
        60,
        42
    ],
    "TGCTTA": [
        28,
        58
    ],
    "TGCTTC": [
        28,
        26
    ],
    "TGCTTG": [
        60,
        26
    ],
    "TGCTTT": [
        60,
        58
    ],
    "TGGAAA": [
        8,
        58
    ],
    "TGGAAC": [
        8,
        26
    ],
    "TGGAAG": [
        40,
        26
    ],
    "TGGAAT": [
        40,
        58
    ],
    "TGGACA": [
        8,
        42
    ],
    "TGGACC": [
        8,
        10
    ],
    "TGGACG": [
        40,
        10
    ],
    "TGGACT": [
        40,
        42
    ],
    "TGGAGA": [
        24,
        42
    ],
    "TGGAGC": [
        24,
        10
    ],
    "TGGAGG": [
        56,
        10
    ],
    "TGGAGT": [
        56,
        42
    ],
    "TGGATA": [
        24,
        58
    ],
    "TGGATC": [
        24,
        26
    ],
    "TGGATG": [
        56,
        26
    ],
    "TGGATT": [
        56,
        58
    ],
    "TGGCAA": [
        8,
        50
    ],
    "TGGCAC": [
        8,
        18
    ],
    "TGGCAG": [
        40,
        18
    ],
    "TGGCAT": [
        40,
        50
    ],
    "TGGCCA": [
        8,
        34
    ],
    "TGGCCC": [
        8,
        2
    ],
    "TGGCCG": [
        40,
        2
    ],
    "TGGCCT": [
        40,
        34
    ],
    "TGGCGA": [
        24,
        34
    ],
    "TGGCGC": [
        24,
        2
    ],
    "TGGCGG": [
        56,
        2
    ],
    "TGGCGT": [
        56,
        34
    ],
    "TGGCTA": [
        24,
        50
    ],
    "TGGCTC": [
        24,
        18
    ],
    "TGGCTG": [
        56,
        18
    ],
    "TGGCTT": [
        56,
        50
    ],
    "TGGGAA": [
        16,
        50
    ],
    "TGGGAC": [
        16,
        18
    ],
    "TGGGAG": [
        48,
        18
    ],
    "TGGGAT": [
        48,
        50
    ],
    "TGGGCA": [
        16,
        34
    ],
    "TGGGCC": [
        16,
        2
    ],
    "TGGGCG": [
        48,
        2
    ],
    "TGGGCT": [
        48,
        34
    ],
    "TGGGGA": [
        32,
        34
    ],
    "TGGGGC": [
        32,
        2
    ],
    "TGGGGG": [
        64,
        2
    ],
    "TGGGGT": [
        64,
        34
    ],
    "TGGGTA": [
        32,
        50
    ],
    "TGGGTC": [
        32,
        18
    ],
    "TGGGTG": [
        64,
        18
    ],
    "TGGGTT": [
        64,
        50
    ],
    "TGGTAA": [
        16,
        58
    ],
    "TGGTAC": [
        16,
        26
    ],
    "TGGTAG": [
        48,
        26
    ],
    "TGGTAT": [
        48,
        58
    ],
    "TGGTCA": [
        16,
        42
    ],
    "TGGTCC": [
        16,
        10
    ],
    "TGGTCG": [
        48,
        10
    ],
    "TGGTCT": [
        48,
        42
    ],
    "TGGTGA": [
        32,
        42
    ],
    "TGGTGC": [
        32,
        10
    ],
    "TGGTGG": [
        64,
        10
    ],
    "TGGTGT": [
        64,
        42
    ],
    "TGGTTA": [
        32,
        58
    ],
    "TGGTTC": [
        32,
        26
    ],
    "TGGTTG": [
        64,
        26
    ],
    "TGGTTT": [
        64,
        58
    ],
    "TGTAAA": [
        8,
        62
    ],
    "TGTAAC": [
        8,
        30
    ],
    "TGTAAG": [
        40,
        30
    ],
    "TGTAAT": [
        40,
        62
    ],
    "TGTACA": [
        8,
        46
    ],
    "TGTACC": [
        8,
        14
    ],
    "TGTACG": [
        40,
        14
    ],
    "TGTACT": [
        40,
        46
    ],
    "TGTAGA": [
        24,
        46
    ],
    "TGTAGC": [
        24,
        14
    ],
    "TGTAGG": [
        56,
        14
    ],
    "TGTAGT": [
        56,
        46
    ],
    "TGTATA": [
        24,
        62
    ],
    "TGTATC": [
        24,
        30
    ],
    "TGTATG": [
        56,
        30
    ],
    "TGTATT": [
        56,
        62
    ],
    "TGTCAA": [
        8,
        54
    ],
    "TGTCAC": [
        8,
        22
    ],
    "TGTCAG": [
        40,
        22
    ],
    "TGTCAT": [
        40,
        54
    ],
    "TGTCCA": [
        8,
        38
    ],
    "TGTCCC": [
        8,
        6
    ],
    "TGTCCG": [
        40,
        6
    ],
    "TGTCCT": [
        40,
        38
    ],
    "TGTCGA": [
        24,
        38
    ],
    "TGTCGC": [
        24,
        6
    ],
    "TGTCGG": [
        56,
        6
    ],
    "TGTCGT": [
        56,
        38
    ],
    "TGTCTA": [
        24,
        54
    ],
    "TGTCTC": [
        24,
        22
    ],
    "TGTCTG": [
        56,
        22
    ],
    "TGTCTT": [
        56,
        54
    ],
    "TGTGAA": [
        16,
        54
    ],
    "TGTGAC": [
        16,
        22
    ],
    "TGTGAG": [
        48,
        22
    ],
    "TGTGAT": [
        48,
        54
    ],
    "TGTGCA": [
        16,
        38
    ],
    "TGTGCC": [
        16,
        6
    ],
    "TGTGCG": [
        48,
        6
    ],
    "TGTGCT": [
        48,
        38
    ],
    "TGTGGA": [
        32,
        38
    ],
    "TGTGGC": [
        32,
        6
    ],
    "TGTGGG": [
        64,
        6
    ],
    "TGTGGT": [
        64,
        38
    ],
    "TGTGTA": [
        32,
        54
    ],
    "TGTGTC": [
        32,
        22
    ],
    "TGTGTG": [
        64,
        22
    ],
    "TGTGTT": [
        64,
        54
    ],
    "TGTTAA": [
        16,
        62
    ],
    "TGTTAC": [
        16,
        30
    ],
    "TGTTAG": [
        48,
        30
    ],
    "TGTTAT": [
        48,
        62
    ],
    "TGTTCA": [
        16,
        46
    ],
    "TGTTCC": [
        16,
        14
    ],
    "TGTTCG": [
        48,
        14
    ],
    "TGTTCT": [
        48,
        46
    ],
    "TGTTGA": [
        32,
        46
    ],
    "TGTTGC": [
        32,
        14
    ],
    "TGTTGG": [
        64,
        14
    ],
    "TGTTGT": [
        64,
        46
    ],
    "TGTTTA": [
        32,
        62
    ],
    "TGTTTC": [
        32,
        30
    ],
    "TGTTTG": [
        64,
        30
    ],
    "TGTTTT": [
        64,
        62
    ],
    "TTAAAA": [
        4,
        64
    ],
    "TTAAAC": [
        4,
        32
    ],
    "TTAAAG": [
        36,
        32
    ],
    "TTAAAT": [
        36,
        64
    ],
    "TTAACA": [
        4,
        48
    ],
    "TTAACC": [
        4,
        16
    ],
    "TTAACG": [
        36,
        16
    ],
    "TTAACT": [
        36,
        48
    ],
    "TTAAGA": [
        20,
        48
    ],
    "TTAAGC": [
        20,
        16
    ],
    "TTAAGG": [
        52,
        16
    ],
    "TTAAGT": [
        52,
        48
    ],
    "TTAATA": [
        20,
        64
    ],
    "TTAATC": [
        20,
        32
    ],
    "TTAATG": [
        52,
        32
    ],
    "TTAATT": [
        52,
        64
    ],
    "TTACAA": [
        4,
        56
    ],
    "TTACAC": [
        4,
        24
    ],
    "TTACAG": [
        36,
        24
    ],
    "TTACAT": [
        36,
        56
    ],
    "TTACCA": [
        4,
        40
    ],
    "TTACCC": [
        4,
        8
    ],
    "TTACCG": [
        36,
        8
    ],
    "TTACCT": [
        36,
        40
    ],
    "TTACGA": [
        20,
        40
    ],
    "TTACGC": [
        20,
        8
    ],
    "TTACGG": [
        52,
        8
    ],
    "TTACGT": [
        52,
        40
    ],
    "TTACTA": [
        20,
        56
    ],
    "TTACTC": [
        20,
        24
    ],
    "TTACTG": [
        52,
        24
    ],
    "TTACTT": [
        52,
        56
    ],
    "TTAGAA": [
        12,
        56
    ],
    "TTAGAC": [
        12,
        24
    ],
    "TTAGAG": [
        44,
        24
    ],
    "TTAGAT": [
        44,
        56
    ],
    "TTAGCA": [
        12,
        40
    ],
    "TTAGCC": [
        12,
        8
    ],
    "TTAGCG": [
        44,
        8
    ],
    "TTAGCT": [
        44,
        40
    ],
    "TTAGGA": [
        28,
        40
    ],
    "TTAGGC": [
        28,
        8
    ],
    "TTAGGG": [
        60,
        8
    ],
    "TTAGGT": [
        60,
        40
    ],
    "TTAGTA": [
        28,
        56
    ],
    "TTAGTC": [
        28,
        24
    ],
    "TTAGTG": [
        60,
        24
    ],
    "TTAGTT": [
        60,
        56
    ],
    "TTATAA": [
        12,
        64
    ],
    "TTATAC": [
        12,
        32
    ],
    "TTATAG": [
        44,
        32
    ],
    "TTATAT": [
        44,
        64
    ],
    "TTATCA": [
        12,
        48
    ],
    "TTATCC": [
        12,
        16
    ],
    "TTATCG": [
        44,
        16
    ],
    "TTATCT": [
        44,
        48
    ],
    "TTATGA": [
        28,
        48
    ],
    "TTATGC": [
        28,
        16
    ],
    "TTATGG": [
        60,
        16
    ],
    "TTATGT": [
        60,
        48
    ],
    "TTATTA": [
        28,
        64
    ],
    "TTATTC": [
        28,
        32
    ],
    "TTATTG": [
        60,
        32
    ],
    "TTATTT": [
        60,
        64
    ],
    "TTCAAA": [
        4,
        60
    ],
    "TTCAAC": [
        4,
        28
    ],
    "TTCAAG": [
        36,
        28
    ],
    "TTCAAT": [
        36,
        60
    ],
    "TTCACA": [
        4,
        44
    ],
    "TTCACC": [
        4,
        12
    ],
    "TTCACG": [
        36,
        12
    ],
    "TTCACT": [
        36,
        44
    ],
    "TTCAGA": [
        20,
        44
    ],
    "TTCAGC": [
        20,
        12
    ],
    "TTCAGG": [
        52,
        12
    ],
    "TTCAGT": [
        52,
        44
    ],
    "TTCATA": [
        20,
        60
    ],
    "TTCATC": [
        20,
        28
    ],
    "TTCATG": [
        52,
        28
    ],
    "TTCATT": [
        52,
        60
    ],
    "TTCCAA": [
        4,
        52
    ],
    "TTCCAC": [
        4,
        20
    ],
    "TTCCAG": [
        36,
        20
    ],
    "TTCCAT": [
        36,
        52
    ],
    "TTCCCA": [
        4,
        36
    ],
    "TTCCCC": [
        4,
        4
    ],
    "TTCCCG": [
        36,
        4
    ],
    "TTCCCT": [
        36,
        36
    ],
    "TTCCGA": [
        20,
        36
    ],
    "TTCCGC": [
        20,
        4
    ],
    "TTCCGG": [
        52,
        4
    ],
    "TTCCGT": [
        52,
        36
    ],
    "TTCCTA": [
        20,
        52
    ],
    "TTCCTC": [
        20,
        20
    ],
    "TTCCTG": [
        52,
        20
    ],
    "TTCCTT": [
        52,
        52
    ],
    "TTCGAA": [
        12,
        52
    ],
    "TTCGAC": [
        12,
        20
    ],
    "TTCGAG": [
        44,
        20
    ],
    "TTCGAT": [
        44,
        52
    ],
    "TTCGCA": [
        12,
        36
    ],
    "TTCGCC": [
        12,
        4
    ],
    "TTCGCG": [
        44,
        4
    ],
    "TTCGCT": [
        44,
        36
    ],
    "TTCGGA": [
        28,
        36
    ],
    "TTCGGC": [
        28,
        4
    ],
    "TTCGGG": [
        60,
        4
    ],
    "TTCGGT": [
        60,
        36
    ],
    "TTCGTA": [
        28,
        52
    ],
    "TTCGTC": [
        28,
        20
    ],
    "TTCGTG": [
        60,
        20
    ],
    "TTCGTT": [
        60,
        52
    ],
    "TTCTAA": [
        12,
        60
    ],
    "TTCTAC": [
        12,
        28
    ],
    "TTCTAG": [
        44,
        28
    ],
    "TTCTAT": [
        44,
        60
    ],
    "TTCTCA": [
        12,
        44
    ],
    "TTCTCC": [
        12,
        12
    ],
    "TTCTCG": [
        44,
        12
    ],
    "TTCTCT": [
        44,
        44
    ],
    "TTCTGA": [
        28,
        44
    ],
    "TTCTGC": [
        28,
        12
    ],
    "TTCTGG": [
        60,
        12
    ],
    "TTCTGT": [
        60,
        44
    ],
    "TTCTTA": [
        28,
        60
    ],
    "TTCTTC": [
        28,
        28
    ],
    "TTCTTG": [
        60,
        28
    ],
    "TTCTTT": [
        60,
        60
    ],
    "TTGAAA": [
        8,
        60
    ],
    "TTGAAC": [
        8,
        28
    ],
    "TTGAAG": [
        40,
        28
    ],
    "TTGAAT": [
        40,
        60
    ],
    "TTGACA": [
        8,
        44
    ],
    "TTGACC": [
        8,
        12
    ],
    "TTGACG": [
        40,
        12
    ],
    "TTGACT": [
        40,
        44
    ],
    "TTGAGA": [
        24,
        44
    ],
    "TTGAGC": [
        24,
        12
    ],
    "TTGAGG": [
        56,
        12
    ],
    "TTGAGT": [
        56,
        44
    ],
    "TTGATA": [
        24,
        60
    ],
    "TTGATC": [
        24,
        28
    ],
    "TTGATG": [
        56,
        28
    ],
    "TTGATT": [
        56,
        60
    ],
    "TTGCAA": [
        8,
        52
    ],
    "TTGCAC": [
        8,
        20
    ],
    "TTGCAG": [
        40,
        20
    ],
    "TTGCAT": [
        40,
        52
    ],
    "TTGCCA": [
        8,
        36
    ],
    "TTGCCC": [
        8,
        4
    ],
    "TTGCCG": [
        40,
        4
    ],
    "TTGCCT": [
        40,
        36
    ],
    "TTGCGA": [
        24,
        36
    ],
    "TTGCGC": [
        24,
        4
    ],
    "TTGCGG": [
        56,
        4
    ],
    "TTGCGT": [
        56,
        36
    ],
    "TTGCTA": [
        24,
        52
    ],
    "TTGCTC": [
        24,
        20
    ],
    "TTGCTG": [
        56,
        20
    ],
    "TTGCTT": [
        56,
        52
    ],
    "TTGGAA": [
        16,
        52
    ],
    "TTGGAC": [
        16,
        20
    ],
    "TTGGAG": [
        48,
        20
    ],
    "TTGGAT": [
        48,
        52
    ],
    "TTGGCA": [
        16,
        36
    ],
    "TTGGCC": [
        16,
        4
    ],
    "TTGGCG": [
        48,
        4
    ],
    "TTGGCT": [
        48,
        36
    ],
    "TTGGGA": [
        32,
        36
    ],
    "TTGGGC": [
        32,
        4
    ],
    "TTGGGG": [
        64,
        4
    ],
    "TTGGGT": [
        64,
        36
    ],
    "TTGGTA": [
        32,
        52
    ],
    "TTGGTC": [
        32,
        20
    ],
    "TTGGTG": [
        64,
        20
    ],
    "TTGGTT": [
        64,
        52
    ],
    "TTGTAA": [
        16,
        60
    ],
    "TTGTAC": [
        16,
        28
    ],
    "TTGTAG": [
        48,
        28
    ],
    "TTGTAT": [
        48,
        60
    ],
    "TTGTCA": [
        16,
        44
    ],
    "TTGTCC": [
        16,
        12
    ],
    "TTGTCG": [
        48,
        12
    ],
    "TTGTCT": [
        48,
        44
    ],
    "TTGTGA": [
        32,
        44
    ],
    "TTGTGC": [
        32,
        12
    ],
    "TTGTGG": [
        64,
        12
    ],
    "TTGTGT": [
        64,
        44
    ],
    "TTGTTA": [
        32,
        60
    ],
    "TTGTTC": [
        32,
        28
    ],
    "TTGTTG": [
        64,
        28
    ],
    "TTGTTT": [
        64,
        60
    ],
    "TTTAAA": [
        8,
        64
    ],
    "TTTAAC": [
        8,
        32
    ],
    "TTTAAG": [
        40,
        32
    ],
    "TTTAAT": [
        40,
        64
    ],
    "TTTACA": [
        8,
        48
    ],
    "TTTACC": [
        8,
        16
    ],
    "TTTACG": [
        40,
        16
    ],
    "TTTACT": [
        40,
        48
    ],
    "TTTAGA": [
        24,
        48
    ],
    "TTTAGC": [
        24,
        16
    ],
    "TTTAGG": [
        56,
        16
    ],
    "TTTAGT": [
        56,
        48
    ],
    "TTTATA": [
        24,
        64
    ],
    "TTTATC": [
        24,
        32
    ],
    "TTTATG": [
        56,
        32
    ],
    "TTTATT": [
        56,
        64
    ],
    "TTTCAA": [
        8,
        56
    ],
    "TTTCAC": [
        8,
        24
    ],
    "TTTCAG": [
        40,
        24
    ],
    "TTTCAT": [
        40,
        56
    ],
    "TTTCCA": [
        8,
        40
    ],
    "TTTCCC": [
        8,
        8
    ],
    "TTTCCG": [
        40,
        8
    ],
    "TTTCCT": [
        40,
        40
    ],
    "TTTCGA": [
        24,
        40
    ],
    "TTTCGC": [
        24,
        8
    ],
    "TTTCGG": [
        56,
        8
    ],
    "TTTCGT": [
        56,
        40
    ],
    "TTTCTA": [
        24,
        56
    ],
    "TTTCTC": [
        24,
        24
    ],
    "TTTCTG": [
        56,
        24
    ],
    "TTTCTT": [
        56,
        56
    ],
    "TTTGAA": [
        16,
        56
    ],
    "TTTGAC": [
        16,
        24
    ],
    "TTTGAG": [
        48,
        24
    ],
    "TTTGAT": [
        48,
        56
    ],
    "TTTGCA": [
        16,
        40
    ],
    "TTTGCC": [
        16,
        8
    ],
    "TTTGCG": [
        48,
        8
    ],
    "TTTGCT": [
        48,
        40
    ],
    "TTTGGA": [
        32,
        40
    ],
    "TTTGGC": [
        32,
        8
    ],
    "TTTGGG": [
        64,
        8
    ],
    "TTTGGT": [
        64,
        40
    ],
    "TTTGTA": [
        32,
        56
    ],
    "TTTGTC": [
        32,
        24
    ],
    "TTTGTG": [
        64,
        24
    ],
    "TTTGTT": [
        64,
        56
    ],
    "TTTTAA": [
        16,
        64
    ],
    "TTTTAC": [
        16,
        32
    ],
    "TTTTAG": [
        48,
        32
    ],
    "TTTTAT": [
        48,
        64
    ],
    "TTTTCA": [
        16,
        48
    ],
    "TTTTCC": [
        16,
        16
    ],
    "TTTTCG": [
        48,
        16
    ],
    "TTTTCT": [
        48,
        48
    ],
    "TTTTGA": [
        32,
        48
    ],
    "TTTTGC": [
        32,
        16
    ],
    "TTTTGG": [
        64,
        16
    ],
    "TTTTGT": [
        64,
        48
    ],
    "TTTTTA": [
        32,
        64
    ],
    "TTTTTC": [
        32,
        32
    ],
    "TTTTTG": [
        64,
        32
    ],
    "TTTTTT": [
        64,
        64
    ]
}