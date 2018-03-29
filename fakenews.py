import markovmodel

def main():
    """ Generate fake headlines """
    chain = markovmodel.Markovchain()
    print(chain.generate())

if __name__ == "__main__":
    main()
