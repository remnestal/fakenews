from os.path import isfile, join
from os import listdir

def main():
    print(_data_files())

def _data_files(datapath='data/', exclude=['.gitignore']):
    """ Return paths of eligible files in the data subdirectory """
    files = list()
    for f in listdir(datapath):
        fpath = join(datapath, f)
        if isfile(fpath) and f not in exclude:
            files.append(fpath)
    return files

if __name__ == "__main__":
    main()
