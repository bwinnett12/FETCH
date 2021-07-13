__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

# In this file, reports such as statistics, matrix representations, and other portrayals of the storage are represented
import os, csv


# A blanket statement to generate each arm of the report. Chain called from running main (-r)
def generate_reports(reports_path, indexes_path):
    generate_gene_matrix(reports_path, indexes_path)


# Makes a file for presence or absence of genes
def generate_gene_matrix(reports_path, indexes_path):

    file_genes = file_species = 0
    try:
        file_genes = open(indexes_path.rstrip("/") + "/genes.lst").readlines()
        file_species = open(indexes_path.rstrip("/") + "/species.lst").readlines()
    except FileNotFoundError:
        print("'genes or species.lst' not found. Indexes are not properly set up or config file has a typo")
        print("Try resetting indexes with '-i' or if storage is empty; fetch something!")
        quit()

    # Constructs a dictionary to hold data. Each entry will be a species and then a nest of each gene
    # So perfect_dict = {species1: {gene1: 1, gene2: 0, gene3: 1}} etc
    perfect_dict = {}

    # Makes a dictionary of genes to serve as a template
    gene_dict = {}
    for gene in file_genes:
        gene = gene.lstrip(";").rstrip("\n")
        gene_dict[gene] = "0"  # 0 (Zero) in this case means not present or not found

    # To make the dictionary, use species.lst for each key then gene.lst to fill every nested key
    for species in file_species:
        species = species.lstrip(";").rstrip("\n")
        perfect_dict[species] = gene_dict.copy()  # Adds species as dictionary entry

    # Iterates through each species and replaces zeroes with ones (if gene is present)
    for species in perfect_dict.items():

        # First gets every gene in that species index
        file_species_specific = open(indexes_path.rstrip("/") + "/species/" + species[0] + ".lst").readlines()
        # Then cleans up every gene
        species_specific = [gene.lstrip(";").rstrip("\n") for gene in file_species_specific]

        # Replaces each instance of presence of a gene with 1
        for gene in species_specific:
            species[1][gene] = "1"


    file_csv_loc = reports_path.rstrip("/") + "/genes.csv"  # A variable for saving the report to

    # Deletes if a file is present
    if os.path.isfile(file_csv_loc):
        os.remove(file_csv_loc)
    file_csv = open(file_csv_loc, "w")

    csv_writer = csv.writer(file_csv)  # Generic name, but only one writer
    species_row, values = zip(*perfect_dict.items())    # Splits the dict into a keys for the first row
    species_row = list(species_row)
    species_row.insert(0, "genes")
    csv_writer.writerow(species_row)  # Top shelf

    total_values = list(perfect_dict.values())
    # Each line is going to be all of one particular gene

    for gene in gene_dict.keys():  # Iterates through each gene in dictionary
        current_line = [gene]  # First entry will be gene name

        for species in total_values:  # Iterates through each species
            current_line.append(species[gene])  # Adds the 1 or 0 representing presence

        csv_writer.writerow(current_line) # Writes that line



if __name__ == '__main__':
    reports_path = "./reports/"
    indexes_path = "./indexes/"
    # generate_gene_matrix(reports_path, indexes_path)
    generate_reports(reports_path, indexes_path)
