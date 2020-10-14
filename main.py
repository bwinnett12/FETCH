import configparser
import argparse

from fetcher import fetch, delete_folder_contents
from puller import pull_query_to_fasta
from indexer import reset_indexes, ensure_folder_scheme


def main():
    # Part where argparser figures out your command
    parser = argparse.ArgumentParser(description='Parse NCBI and then work with Biological data')

    # Argument for clearing out the storage folder (Mostly for testing purposes)
    parser.add_argument('-d', '--delete',
                        dest='delete',
                        default=False,
                        action='store_true',
                        help="delete current storage [only for testing purposes]")

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
    fetch_query = args.fetch
    index = args.index
    mafft_args = args.mafft
    pull = args.pull
    setup_structure = args.setup_structure

    # Testing output
    output = "Output: \n"

    # THis is the part where we are reading from the config

    config = configparser.ConfigParser()
    config.read('ncbifetcher.config')

    email = config['OPTIONS']['email']
    location_index = config['INDEX']['index_location']
    location_storage = config['STORAGE']['storage_location']
    location_output = config['OUTPUT']['output_location']

    reset_indexes_default = config['OPTIONS']['reset_indexes_everytime']
    run_mafft_config = config['OPTIONS']['run_mafft_everytime']

    # Testing: Deletes everything in the folders and resets the indexes
    if delete:
        print("deleting... \n")
        delete_folder_contents(location_storage)
        delete_folder_contents(location_output)

        # Optional resetting indexes
        if reset_indexes_default == 1 or reset_indexes_default:
            reset_indexes(location_storage)
        return

    # Fetches from genbank
    if len(fetch_query) >= 1:
        fetch(fetch_query, location_storage, email)

        # Optional resetting indexes
        if reset_indexes_default == 1 or reset_indexes_default:
            reset_indexes(location_storage)
        return

    # This is a way to sort the indexes
    if index:
        output += "Index: \n"

        reset_indexes(location_storage)
        return

    # Pulling from storage - Default set to wherever index says to go
    if pull:
        output += "Pulling \n"

        pull_query_to_fasta(location_output, run_mafft=mafft_args or run_mafft_config == 1 or run_mafft_config == "true")
        return

    # For setting up a file structure at a location other than default
    if len(setup_structure) >= 1:
        ensure_folder_scheme(setup_structure)
        return


if __name__ == "__main__":
    main()
