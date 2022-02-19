__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"

# In this file, reports such as statistics, matrix representations, and other portrayals of the storage are represented
import glob
import os, csv


# A blanket statement to generate each arm of the report. Chain called from running main (-r)
def generate_reports(reports_path, indexes_path):
    generate_gene_matrix(reports_path, indexes_path)
    generate_storage_report(reports_path, indexes_path)


# Generates a document that contains a statistics about your whole storage
def generate_storage_report(reports_path, indexes_path):
    # Compartmentalizing the writing of the report for readability - Returns a string that can be written at once
    def write_gene_presence():
        out_string = "Gene presence by percentage:\n"  # Initialized string with starting message

        for key, value in perfect_dict.items():
            out_string += key + ": " + "{:.1%}".format(sum(value) / len(value)) + "%\n"  # Each line is a gene + %
        return out_string + "\n"

    # Compartmentalizing the writing of the report for readability - Returns a string that can be written at once
    def write_gene_presence_species():

        out_string = "Gene presence by percentage (per species):\n"  # Initialized string with starting message
        i = 0  # Value for keeping track of the moving array

        for species in field:
            count = 0  # Roving amount of possible genes present (reset for each species)
            total = 0  # Roving amount of total genes present (reset for each species)

            for value in perfect_dict.values():  # Iterates through each gene and determines presence
                count += 1  # Increments count
                total += value[i]  # Increments count only if presence

            out_string += species + ": " + "{:.1%}".format(total / count) + "%\n"  # Each line is gene + %
            i += 1  # Moves up species to next column (How the dictionaries are setup

        return out_string + "\n"

    # Compartmentalizing the writing of the report
    # This adds what genes were missing from each species
    def write_missing_genes():
        out_string = "Genes missing by species:\n"

        # Making a dictionary out of the genes.lst
        all_gene = open(indexes_path.rstrip("/") + "/genes.lst", "r").readlines()
        all_gene = [x.lstrip(";").rstrip("\n") for x in all_gene]
        dict_gene = {}

        # Fill dictionary with 0s representing not present
        for single_gene in all_gene:
            dict_gene[single_gene] = 0

        dict_gene = dict(sorted(dict_gene.items()))

        # Iterate through species possible
        for species in sorted(glob.glob(indexes_path.rstrip("/") + "/species/*.lst")):
            species_name = species.split("/")[-1].replace(".lst", "").replace("-", " ")

            # Copy so not to interupt original values
            dict_temp = dict_gene.copy()

            # A list of what genes are contained per species
            species_lines = open(species, "r").readlines()
            species_lines = [x.lstrip(";").rstrip("\n") for x in species_lines]

            # If gene is present, add it. Anything not added is considered not there
            for gene in species_lines:
                dict_temp[gene] = 1

            # If there is nothing missing, skips writing
            if 0 in dict_temp.values():
                out_string += species_name + ":\n"

                # Time to create a string from the dictionary
                for key, value in dict_temp.items():
                    if value == 0:
                        out_string += key + "\n"

                out_string += "\n"

        return out_string

    # Compartmentalizing the writing of the report
    # This adds what species were missing from each gene
    def write_missing_genes_by_species():
        out_string = "Species missing by gene:\n"

        # Making a dictionary out of the species.lst
        all_species = open(indexes_path.rstrip("/") + "/species.lst", "r").readlines()
        all_species = [x.lstrip(";").rstrip("\n") for x in all_species]
        dict_species = {}

        # Fill dictionary with 0s representing not present
        for single_species in all_species:
            dict_species[single_species] = 0

        # Alphabetically sorts the list
        dict_species = dict(sorted(dict_species.items()))

        # Iterate through every possible gene
        for gene in sorted(glob.glob(indexes_path.rstrip("/") + "/genes/*.lst")):
            gene_name = gene.split("/")[-1].rstrip(".lst")

            dict_temp = dict_species.copy()

            gene_lines = open(gene, "r").readlines()
            gene_lines = [x.lstrip(";").rstrip("\n") for x in gene_lines]

            # If species is present, add it. Anything not added is considered not there
            for species in gene_lines:
                dict_temp[species] = 1

            # If nothing missing, nothing to report
            if 0 in dict_temp.values():
                out_string += gene_name + ":\n"

                # Time to create a string from the dictionary
                for key, value in dict_temp.items():
                    if value == 0:
                        out_string += key + "\n"

                out_string += "\n"
            else:
                continue

        return out_string


    gene_matrix = ""
    try:
        gene_matrix = csv.reader(open(reports_path.rstrip("/") + "/genes_matrix.csv", "r"), delimiter=',')
    except FileNotFoundError:
        print("'genes or species.lst' not found. Indexes are not properly set up or config file has a typo")
        quit()

    # if len(gene_matrix) == 0:   # TODO - Make a catch for broken gene matrices
    #     print("Gene matrix is empty... Try fetching something!")

    field = next(gene_matrix)
    field.pop(0)  # Removes the "genes" from the csv
    perfect_dict = {}  # A dictionary to contain what is on the csv

    for row in gene_matrix:  # Iterates through each row of the csv and adds to a dictionary
        gene = row[0]
        row.pop(0)
        perfect_dict[gene] = list(map(int, row))

    file_txt_loc = reports_path.rstrip("/") + "/FETCH_report.txt"  # A variable for saving the report to

    # Deletes if a file is present
    if os.path.isfile(file_txt_loc):
        os.remove(file_txt_loc)
    file_txt = open(file_txt_loc, "w")

    # This section represents the header for the text file
    file_txt.write("~~~~~~~~~~~ BEGIN REPORT ~~~~~~~~~~~\n\n"
                   "This is the FETCH report. The information detailed in here represents what is contained\n"
                   "within your genomes that you have fetched. Information will be broken down by section,\n"
                   "with an Rshiny accompaniment to come. If there is any other diagnostics that you would\n"
                   "like to see added, please write to the authors via email or directly to github.\n"
                   "\n")

    file_txt.write(write_gene_presence())  # Writes gene presence for individual genes
    file_txt.write("*********\n")

    file_txt.write(write_gene_presence_species())  # Writes gene presence for individual genes
    file_txt.write("*********\n")

    file_txt.write(write_missing_genes())
    file_txt.write("********\n")

    file_txt.write(write_missing_genes_by_species())

    file_txt.write("~~~~~~~~~~~ END REPORT ~~~~~~~~~~~")


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

    # JUst in case the indexes are empty (nothing has been fetched)
    if len(file_genes) == 0 or len(file_species) == 0:
        print("Indexes (and therefore storages are empty), try fetching something")
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

    file_csv_loc = reports_path.rstrip("/") + "/genes_matrix.csv"  # A variable for saving the report to

    # Deletes if a file is present
    if os.path.isfile(file_csv_loc):
        os.remove(file_csv_loc)
    file_csv = open(file_csv_loc, "w")

    csv_writer = csv.writer(file_csv)  # Generic name, but only one writer
    species_row, values = zip(*perfect_dict.items())  # Splits the dict into a keys for the first row
    species_row = list(species_row)
    species_row.insert(0, "genes")
    csv_writer.writerow(species_row)  # Top shelf

    total_values = list(perfect_dict.values())
    # Each line is going to be all of one particular gene

    for gene in gene_dict.keys():  # Iterates through each gene in dictionary
        current_line = [gene]  # First entry will be gene name

        for species in total_values:  # Iterates through each species
            current_line.append(species[gene])  # Adds the 1 or 0 representing presence

        csv_writer.writerow(current_line)  # Writes that line
