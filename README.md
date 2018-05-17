# Fakenews

Generate **fake news** headlines with the power of non-stationary [_Markov chains_](https://en.wikipedia.org/wiki/Markov_chain).  
In reality this generator is not limited to news-headlines but it is designed to generate single sentence sequences rather than arbitrary length blobs.

## ![bing bing bong](https://imgur.com/Ssxmml4.jpg) How-to

The program is run with `python3`.

```
$   python3 fakenews.py
```
This script with default configuration will generate a new model from available data unless there is already a cached model available. Output is then printed on _stdout_. The `markovmodel.py`  module may can be used as a stand-alone generator without printed output. See the implementation of `fakenews.py` for more details.

### Command-line options
```
-n, --samples       # specifies the number of headlines to generate (default 10)
-o, --order         # specifies the order of the Markov-chain (default 2)
--refresh-cache     # tells the program to ignore cached data and generate a new model (default false)
```

#### Example usage

```
$   python3 fakenews.py -n 100 --refresh-cache --order 3
```
This operation generates _100 fake headlines_, _ignoring_ existing caches, using a fresh _3rd order_ Markov chain.

## ![bing bing bong](https://imgur.com/Ssxmml4.jpg) Tips and tricks

When the order in increased, the generated content gets closer to the original data. This often means that things like _sentence structure, word ordering and grammar_ persists, which gives a more credible and lifelike result. However, by increasing the order you also add constraints on the generator and the amount of required data also increases.

If, for example, the average length of the headlines in your dataset is 5 words and you generate headlines of _order 2_; this means that the generator will use all pairs of consecutive words from the data. I've made the generator non-stationary which basically means that the position of each pair is also taken into account. For an _order 3_ model, all triples of consecutive words are used, etc. Thus, when the _order_ increases, the amount of combinations that can be made from these tuples decreases. So if the size of the data is too small and the _order_ is represented by a too large number; the generated headlines will be identical to those of the dataset.

## ![bing bing bong](https://imgur.com/Ssxmml4.jpg) Caching

Caching is turned on by default. This feature is put in place to make subsequent usage faster but can be ignored at runtime. The chain used by the generator may take fairly long time to calculate, depending on the size of your data and your CPU/memory, so if you plan to run the script several times I recommend that you leave caching of the chain enabled.

To invalidate the cache and calculate a new chain, the `--refresh-cache` command-line option can be specified. This is useful when new data has been added and you want to expand the chain. The cache can also be manually invalidated by removing the `.cache.pkl` storage.

## ![bing bing bong](https://imgur.com/Ssxmml4.jpg) Source data
The generator draws all its source data from all the files stored in the `data/` subdirectory so place your datasets there. Each line of those files are treated like a single coherent headline by the parser.

Right now there is **no good** character filtering policy, so most _unicode characters_ are accepted. However, all **double quotation** characters are removed.

_Currently I can't share the Swedish datasets I've been using during development. I'm working on a solution but in the meantime you'll have to use your own. Open APIs or [non-agressive web-scraping](https://www.scrapehero.com/how-to-prevent-getting-blacklisted-while-scraping/) should do the trick, although note that intensive web-scraping may be viewed as a denial of service attack._
