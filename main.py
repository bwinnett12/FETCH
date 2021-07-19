import configparser
import argparse
import glob
import os

from fetcher import fetch, delete_folder_contents
from puller import pull_query_to_fasta
from indexer import reset_indexes, ensure_folder_scheme_storage
from reporter import generate_reports


def main():
    # Part where argparser figures out your command
    parser = argparse.ArgumentParser(description='Parse NCBI and then work with Biological data')

    # Argument for clearing out the storage folder (Mostly for testing purposes)
    parser.add_argument('-d', '--delete',
                        dest='delete',
                        default=False,
                        action='store_true',
                        help="delete current storage")

    # Argument for fetching.
    parser.add_argument('-f', '--fetch',
                        dest='fetch',
                        default="",
                        help='Fetches from ncbi and adds to storage: \n '
                             'Usage: -f [Accession number or boolean operators]')

    parser.add_argument('-i', '--index',
                        dest='index',
                        action='store_true',
                        help='Resets the indexes. This can be done manually through this method or specified to do it'
                             ' everytime from the configs.')

    parser.add_argument('-m', '--mafft',
                        dest='mafft',
                        default=False,
                        action='store_true',
                        help="Runs mafft when pulling. Optional alignment but requires -p or --pull to be effective. "
                             "Can also be specified to run automatically in config")

    parser.add_argument('-p', '--pull',
                        dest='pull',
                        default=False,
                        action='store_true',
                        help="Pull from storage. "
                             "The genes and species specified are specified in genes.lst and species.lst.")

    parser.add_argument('-r', '--report',
                        dest='report',
                        default=False,
                        action='store_true',
                        help="Report. Generate a report "
                             "All reports go to the /reports/ folder unless specified differently.")

    parser.add_argument('-s', '--setup',
                        dest='setup_structure',
                        default="",
                        help="Usage: -s [storage location]" + "\n"
                                                              " Sets up a default structure for storage and indexes."
                                                              "This should be done when moving storage to a location "
                                                              "outside of the cloned folder.")

    # This stores all of the values from the parser
    args = parser.parse_args()

    delete = args.delete

    query_fetch = args.fetch
    index = args.index

    mafft_args = args.mafft
    pull = args.pull
    report = args.report
    setup_structure = args.setup_structure

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
    run_mafft_config = config['OPTIONS']['run_mafft_everytime']

    # Testing: Deletes everything in the folders and resets the indexes
    if delete:
        print("deleting... \n")
        delete_folder_contents(location_storage)
        delete_folder_contents(location_output)

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
            fetch(accession_numbers_from_file, location_storage, email)

        else:  # Fetches the single query
            print("Fetching...")
            fetch(query_fetch, location_storage, email)

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
                            run_mafft=mafft_args or run_mafft_config == 1 or run_mafft_config == "true")
        return

    # For setting up a file structure at a location other than default
    if len(setup_structure) >= 1:
        print("Setting up structure at " + setup_structure + "...")
        ensure_folder_scheme_storage(setup_structure)
        return

    if report:
        print("Reporting...")
        generate_reports(location_reports, location_index)
        return


def delete():


    # If you want to start fresh with your storage contents
    def delete_folder_contents(folder):
        structure = [folder + "*/*"]
        for style in structure:
            files = glob.glob(style)
            for f in files:
                os.remove(f)

if __name__ == "__main__":
    main()
