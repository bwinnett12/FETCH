
import configparser

from fetcher import battery


def parse_config():
    config = configparser.ConfigParser()
    config.read('ncbifetcher.config')
    print(config.sections())

    email = config['OPTIONS']['email']

    location_index = config['INDEX']['index_location']
    location_storage = config['STORAGE']['location_storage']
    print(email)


def main():
    config = configparser.ConfigParser()
    config.read('ncbifetcher.config')

    email = config['OPTIONS']['email']
    location_index = config['INDEX']['index_location']
    location_storage = config['STORAGE']['location_storage']

    # battery('txid36190[Organism] mitochondria', location_storage, email)
    # parse_config()



if __name__ == "__main__":
    main()
