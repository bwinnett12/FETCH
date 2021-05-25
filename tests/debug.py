__author__ = "Bill Winnett"
__email__ = "bwinnett12@gmail.com"
# A file with a "main" to the program for easy debugging
# To operate, import whatever function you want to test
# Currently doesn't use the config so every option has to be manually implemented

from indexer import reset_indexes
# from FETCH.writer import *
# from FETCH.puller import *
# from FETCH.fetcher import *
# import glob

if __name__ == '__main__':
    storage_path = "../storage/"
    indexes_path = "../indexes/"
    print("Welcome to the debugging world of FETCH")
    reset_indexes(storage_path, indexes_path)

