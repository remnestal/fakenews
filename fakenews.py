import markovmodel
import sys
import argparse

def main():
    """ Generate fake headlines """
    args = __parse_arguments()
    chain = markovmodel.Markovchain(refresh_cache=args.refresh_cache, order=args.order)

    for _ in range(args.samples):
        print(chain.generate())

def __parse_arguments():
    """ Parse and return input arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--samples',
                        help='number of generated samples',
                        action='store',
                        type=int,
                        default=10)
    parser.add_argument('-o', '--order',
                        help='order of the markov chain',
                        action='store',
                        type=order_type,
                        default=2)
    parser.add_argument('-f', '--refresh-cache',
                        help='generate a new cache first',
                        action='store_true',
                        default=False)
    return parser.parse_args()

def order_type(x):
    """ Type for asserting lower bounds of the `order`-argument """
    x = int(x)
    if x < 2:
        raise argparse.ArgumentTypeError("Minimum order value is 2")
    else:
        return x

if __name__ == "__main__":
    main()
