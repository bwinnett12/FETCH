from pathlib import Path
import sys
path = str(Path(Path(__file__).parent.absolute()).parent.absolute())
sys.path.insert(0, path)


import configparser
import argparse
import glob
import os

from fetcher import fetch
from puller import pull_query_to_fasta
from indexer import reset_indexes, ensure_folder_scheme_storage, ensure_folder_scheme_indexes
from reporter import generate_reports
from tool_helper import tool_fasttree, tool_mafft



def main():

    # Part where argparser figures out your command
    parser = argparse.ArgumentParser(description='Parse NCBI and then work with Biological data')

    # Argument for specifying database
    parser.add_argument('-b',
                        dest='database',
                        default="nucleotide",
                        help='Specifies the database to fetch from. Default nucleotide.')

    # Argument for clearing out the storage folder (Mostly for testing purposes)
    parser.add_argument('-d', '--delete',
                        dest='delete',
                        default=False,
                        action='store_true',
                        help="Delete current storage along with output, reports, and indexes.")

    # Argument for fetching
    parser.add_argument('-f', '--fetch',
                        dest='fetch',
                        default="",
                        help='Fetches from ncbi and adds to storage: \n '
                             'Usage: -f [Accession number or boolean operators]')

    # Argument for resetting indexes
    parser.add_argument('-i', '--index',
                        dest='index',
                        action='store_true',
                        help='Resets the indexes. This can be done manually through this method or specified to do it'
                             ' everytime from the configs.')

    # Argument for running mafft on aligned files
    parser.add_argument('-m', '--mafft',
                        dest='mafft',
                        default=False,
                        action='store_true',
                        help="Runs mafft when pulling. Optional alignment but requires -p or --pull to be effective. "
                             "Can also be specified to run automatically in config")

    # Argument for pulling files from storage
    parser.add_argument('-p', '--pull',
                        dest='pull',
                        default=False,
                        action='store_true',
                        help="Pull from storage. "
                             "The genes and species specified are specified in genes.lst and species.lst.")

    # Argument for running the report
    parser.add_argument('-r', '--report',
                        dest='report',
                        default=False,
                        action='store_true',
                        help="Report. Generate all report")

    # Set up a structure at desired location
    parser.add_argument('-s', '--setup',
                        dest='setup_structure',
                        default=False,
                        action='store_true',
                        help="Usage [s] " + "\n"
                                            "Sets up a default structure at locations specified in config."
                                            "Do this before anything else to ensure that everything is set up properly."
                                            "This should be done if moving any component to a different"
                                            "location outside of FETCH folder. No other modifiers necessary")


    # Argument for fasttree
    parser.add_argument('-t', '--tree',
                        dest='fasttree',
                        default=False,
                        action='store_true',
                        help="Runs FastTree on aligned folders in storage.\n"
                             "Make sure to run mafft option first and to specify FastTree location in config "
                             "(Even if on path).")

    # This stores all of the values from the parser
    args = parser.parse_args()

    database = args.database.lower() if args.database.lower() != "nucleotide" else "nucleotide"
    delete = args.delete
    query_fetch = args.fetch
    index = args.index
    mafft_args = args.mafft
    pull = args.pull
    report = args.report
    setup_structure = args.setup_structure
    fasttree = args.fasttree

    # Testing output
    output = "Output: \n"

    # This is the part where we are reading from the config
    config = configparser.ConfigParser()
    config.read('ncbifetcher.config')

    email = config['OPTIONS']['email']
    location_index = config['INDEX']['index_location']
    location_output = config['OUTPUT']['output_location']
    location_reports = config['REPORTS']['reports_location']
    location_storage = config['STORAGE']['storage_location']

    reset_indexes_default = config['OPTIONS']['reset_indexes_everytime']

    # Tools options
    tools_run_mafft_config = config['TOOLS']['run_mafft_everytime']
    tools_fasttree_path = config['TOOLS']["fasttree_path"]
    tools_fasttree_generate_error_log = config['TOOLS']["fasttree_generate_error_log"]


    # Testing: Deletes everything in the folders and resets the indexes
    if delete:
        print("Deleting... \n")

        delete_folder_contents(location_storage)
        delete_folder_contents(location_output)
        delete_folder_contents(location_reports)
        delete_folder_contents(location_index)

        # Optional resetting indexes
        if reset_indexes_default == 1 or reset_indexes_default:
            reset_indexes(location_storage, location_index)
        return

    # Fetches from genbank
    if len(query_fetch) >= 1:
        # If the input is a file, fetches all from the file
        if os.path.isfile(query_fetch):
            print("Fetching from file: ", query_fetch)
            accession_numbers_from_file = []
            lines = open(query_fetch, "r")

            for line in lines:  # Gets every possible entry from file
                accession_numbers_from_file.append(line.strip().strip('\n'))

            accession_numbers_from_file = ','.join(accession_numbers_from_file)

            # Fetches based on the accession numbers
            fetch(accession_numbers_from_file, location_storage, email, database)

        else:  # Fetches the single query
            print("Fetching...")
            fetch(query_fetch, location_storage, email, database)

        # Optional resetting indexes
        if reset_indexes_default == 1 or reset_indexes_default:
            reset_indexes(location_storage, location_index)
        return

    # This is a way to sort the indexes
    if index:
        print("Resetting indexes...")
        output += "Index: \n"

        reset_indexes(location_storage, location_index)
        return

    # Pulling from storage - Default set to wherever index says to go
    if pull:
        print("Pulling...")

        pull_query_to_fasta(location_output, location_index, location_storage,
                            run_mafft=mafft_args or tools_run_mafft_config == 1 or tools_run_mafft_config == "true")
        return

    # For running mafft alone
    if mafft_args and not pull:
        print("Running mafft...")
        for file in glob.glob(location_output.rstrip("/") + "/*.fa"):
            tool_mafft(file)

    # For setting up a file structure at a location other than default
    if setup_structure:
        print("Setting up structure at : ")
        ensure_folder_scheme_storage(location_storage)
        print("Storage: " + location_storage)

        ensure_folder_scheme_indexes(location_index)
        print("Indexes: " + location_index)

        os.makedirs(location_output, exist_ok=True)
        print("Output: " + location_output)

        os.makedirs(location_reports, exist_ok=True)
        print("Reports: " + location_reports)

        return

    # For running the report
    if report:
        print("Reporting...")
        generate_reports(location_reports, location_index)
        return

    if fasttree:
        print("Running Fasttree...")
        generate_error_log = False if int(tools_fasttree_generate_error_log) == 0 else True
        tool_fasttree(location_output, tools_fasttree_path, generate_error_log)
        return
    
    return "FETCH ran successfully"




# If you want to start fresh with your storage contents
def delete_folder_contents(folder):
    structure = [[folder + "*/*"], [folder + "*"]]
    for type in structure:
        for style in type:
            files = glob.glob(style)
            files = [file for file in files if os.path.isfile(file) and
                     "genes.lst" not in file and "species.lst" not in file]

            for f in files:
                os.remove(f)


if __name__ == "__main__":
    main()
