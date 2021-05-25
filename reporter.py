__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

# In this file, reports such as statistics, matrix representations, and other portrayals of the storage are represented
import os


# Makes a file for presence or absence of genes
def generate_gene_matrix(reports_path, indexes_path):

    file_matrix_loc = reports_path.rstrip("/") + "/genes.csv"

    # Makes a file if not present if not opens a new one
    if not os.path.isfile(file_matrix_loc):
        file_matrix = open(file_matrix_loc, "x")
    file_matrix = open(file_matrix_loc, "w")

    try:
        file_genes = open(indexes_path.rstrip("/") + "/genes.lst").readlines()
        file_species = open(indexes_path.rstrip("/") + "/species.lst").readlines()
    except FileNotFoundError:
        print("'genes or species.lst' not found. Indexes are not properly set up or config file has a typo")
        quit()

    # Constructs a dictionary to hold data. Each entry will be a species and then a nest of each gene
    # So perfect_dict = {species1: {gene1: Y, gene2: N, gene3: Y}} etc
    perfect_dict = {}

    # Makes a dictionary of genes to paste into each species key
    gene_dict = {}
    for gene in file_genes:
        gene = gene.lstrip(";").rstrip("\n")
        gene_dict[gene] = "0"  # 0 (Zero) in this case means not present or not found

    # To make the dictionary, use species.lst for each key then gene.lst to fill every nested key
    for species in file_species:
        species = species.lstrip(";").rstrip("\n")
        perfect_dict[species] = gene_dict

    r = 2

    # Go through each species index and go line by line through each index
    # If the gene is present, change that element in the dictionary to a "1"
    # Once the index is done, close it and go to the next one


    # Once each species is finished, time to generate the matrix file. See the Viraj's for an example for formatting
    # species,pid,id,mito,og_present,og,geneid,tp,rc,mfprob,mf,mtslen,domcomb
    # cele,cele10000,nd,nonmito,no_og,no_og,no_og,S,3,0.066,No_mitochondrial_presequence,65,7TM_GPCR_Srx

    # Column one (Species will be the... Actually get back to this







if __name__ == '__main__':
    reports_path = "./reports/"
    indexes_path = "./indexes/"
    generate_gene_matrix(reports_path, indexes_path)
