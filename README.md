# Fakenews

_This project is still under construction but has a stable version as of commit  [485a633](https://github.com/remnestal/fakenews/commit/485a63302c1cc49bf8c66349948dde8793d3c4ef)_


![Trump saying: "You are fake news!!"](https://i.giphy.com/media/l0Iyau7QcKtKUYIda/giphy.gif "You are fake news!!")

Generate **fake news** headlines with the power of _1<sup>st</sup> order Markov chains_.

## Source data
_Currently I can't share the datasets I've been using during development, so you'll have to use your own 🐴_  

The generator draws all its source data from all the files stored in the `data/` subdirectory so place your datasets there. Each line of those files are treated like a single coherent headline by the parser.

Right now there is **no good** character filtering policy, so most _unicode characters_ are accepted. However, all **double quotation** characters are removed.

## How-to
The program is run with python. By default, the generator outputs 10 headlines but you can also specify a single argument with the amount of headlines you desire.
```sh
$   python3 fakenews.py                 # generate some fake headlines
$   python3 fakenews.py --samples 50    # generates 50 fake headlines
```
Currently there is no caching of the matrices used by the generator, so for large datasets _(about 500k lines+)_ the generator may take some time completing.
