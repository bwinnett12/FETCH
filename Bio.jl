#=
Bio:
- Julia version: 1.4.2
- Author: bill
- Date: 2020-07-19
=#

translation_table = Dict("ATA"=>'I', "ATC"=>'I', "ATT"=>'I', "ATG"=>'M',
        "ACA"=>'T', "ACC"=>'T', "ACG"=>'T', "ACT"=>'T',
        "AAC"=>'N', "AAT"=>'N', "AAA"=>'K', "AAG"=>'K',
        "AGC"=>'S', "AGT"=>'S', "AGA"=>'R', "AGG"=>'R',
        "CTA"=>'L', "CTC"=>'L', "CTG"=>'L', "CTT"=>'L',
        "CCA"=>'P', "CCC"=>'P', "CCG"=>'P', "CCT"=>'P',
        "CAC"=>'H', "CAT"=>'H', "CAA"=>'Q', "CAG"=>'Q',
        "CGA"=>'R', "CGC"=>'R', "CGG"=>'R', "CGT"=>'R',
        "GTA"=>'V', "GTC"=>'V', "GTG"=>'V', "GTT"=>'V',
        "GCA"=>'A', "GCC"=>'A', "GCG"=>'A', "GCT"=>'A',
        "GAC"=>'D', "GAT"=>'D', "GAA"=>'E', "GAG"=>'E',
        "GGA"=>'G', "GGC"=>'G', "GGG"=>'G', "GGT"=>'G',
        "TCA"=>'S', "TCC"=>'S', "TCG"=>'S', "TCT"=>'S',
        "TTC"=>'F', "TTT"=>'F', "TTA"=>'L', "TTG"=>'L',
        "TAC"=>'Y', "TAT"=>'Y', "TAA"=>'_', "TAG"=>'_',
        "TGC"=>'C', "TGT"=>'C', "TGA"=>'_', "TGG"=>'W',
    )

DnaRaw = "GGAGAGCACTCATCTTGGGGTGGGCTTACTACTTATATGCTTTCAGCAGTTATCCGCTCCGCACTTGGCTACCCAGCGTTTACCGTGGGCACGATAACTGGTACACCAGAGGTGCGTCCTTCCCGGTCCTCTCGTACTTTGGAAGGGTCCTCTCAATGCTCTAACGCCCACACCGGATATGGACCGAACTGTCTCACGACGTTCTGAACCCAGCTCACGTACCGCTTTAATGGGCGAACAGCCCAACCCTTGGAACCTCCTACAGCACCAGGTGGCGAAGAGCCGACATCGAGGTGCCAAACCTTCCCGTCGATGTGGTCTCTTGGGGAAGATCAGCCTGTTATCCCTAGAGTAACTTTTATCCGTTGAGCGACGGCCCTTCCACTCGGCACCGTCGGATCACTAAGGCCGACTTTCGTCCCTGCTCGACGGGTGGGTCTCGCAGTCAAGCTCCCTTCTGCCTTTGCACTCGAGGGCCAATCTCCGTCTGGCCTGAGGAAACCTTTGCACGCCTCCGTTACCTTTTGGGAGGCCTACGCCCCATAGAAACTGTCTACCTGAGACTGTCCCTTGGCCCGTAGGTCCTGACACAAGGTTAGACAGCACGACGCTTGTATTTCTCTCCCACAACCCCGTTTTCACGGTTTAGGCTGCTCCCATTTCGCTCGCCGCTACTACGGGAATCGCTTTTGCTTTCTTTTCCTCTGGCTACTAAGATGTTTCAGTTCGCCAGGTTGTCTCTTGTCTGCCCATGGATTCAGCAGCGTTCGAAAGGTTGACCTATTCGGGAATCTCCGGATCTATGCTTATTTTCAACTCCCCGAAGCATTTCGTCGATTATTACGCCCTTCCTCGTCTCCGGGTGCCTAGGGATCCACCGTAAGCCTTTCCTCGTTTGA"

# DNAarr = split(DnaRaw, "")
# print(typeof(DNAarr))


protein_translation = ""

function translate(raw)

    translated_str = ""
    for i = 1:3:(length(DnaRaw) % 3 == 0 ? length(DnaRaw) : length(DnaRaw) - (length(DnaRaw) % 3))
        translated_str = string(translated_str, translation_table[DnaRaw[i:i+2]])
    end
    return translated_str
end


#     append!(protein_translation, translation_table[DnaRaw[i:i+2]])

translated = translate(DnaRaw)
println(translated)