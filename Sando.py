#
# from Bio import SeqIO
#
# with open("./storage/gb/Mus-musculus.gb", "r") as input_handle:
#     with open("./storage/gb/Mus-musculus.fa", "w") as output_handle:
#         sequences = SeqIO.parse(input_handle, "genbank")
#         count = SeqIO.write(sequences, output_handle, "fasta")
#
# print("Converted %i records" % count)


# from Bio import SeqIO
# import os
#
# input_file = "./storage/gb/Mus-musculus.gb"
# output_file_name = "./storage/gb/Mus-musculus.fa"
#
# if not os.path.exists(output_file_name):
#     for rec in SeqIO.parse(input_file, "gb"):
#         for feature in rec.features:
#             for key, val in feature.qualifiers.items():
#                 if "CDS" in val:
#                     with open(output_file_name, "a") as ofile:
#                         ofile.write(
#                             "Protein id: {0}\n{1}: {2}\n{3}\n\n".format(feature.qualifiers['protein_id'][0], key,
#                                                                         val[0], feature.qualifiers['translation'][0]))
# else:
#     print(
#         "The output file already seem to exist in the current workding directory {0}. Please change the name of the output file".format(
#             os.getcwd()))


# from Bio import SeqIO
#
# file_name = "./storage/gb/Mus-musculus.gb"
#
# # stores all the CDS entries
# all_entries = []
#
# with open(file_name, 'r') as GBFile:
#
#     GBcds = SeqIO.InsdcIO.GenBankIterator(GBFile)
#
#     for cds in GBcds:
#         if cds.seq is not None:
#             cds.id = cds.name
#             cds.description = ''
#             all_entries.append(cds)
#
#
# # write file
# SeqIO.write(all_entries, '{}.fasta'.format(file_name[:-3]), 'fasta')

from Bio import SeqIO
from Bio.SeqIO.InsdcIO import GenBankIterator

file_name = "./storage/gb/Mus-musculus.gb"

all_entries = []
with open(file_name) as handle:
    for record in GenBankIterator(handle):
        print(record.id)


