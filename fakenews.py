import markovmodel
import sys
import argparse

def main():
    """ Generate fake headlines """
    args = __parse_arguments()
    chain = markovmodel.Markovchain()

    for _ in range(args.samples):
        print(chain.generate())

def __parse_arguments():
    """ Parse and return input arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--samples',  help='number of generated samples',
                                            action='store',
                                            type=int,
                                            default=10)
    return parser.parse_args()

if __name__ == "__main__":
    main()
