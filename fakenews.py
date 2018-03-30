import markovmodel
import sys

def main():
    """ Generate fake headlines """
    chain = markovmodel.Markovchain()
    num_samples = 10

    # let user define number of generated samples
    if len(sys.argv) > 1:
        try:
            num_samples = int(sys.argv[1])
        except:
            sys.exit('1st argument must be an integer')

    for _ in range(num_samples):
        print(chain.generate())

if __name__ == "__main__":
    main()
