# Make a reference library in minutes direct from RefSeq.

Basic reference library generator; rendered from curated RefSeq genome assemblies.

Each new library contains representatives of every species within the Genera you specify. The highest spec genome assemblies are selected. You can choose how many representatives from each species to include. Please note, for some species the quantity you specify may not be available.

Your new library will be stored in a folder named with the date.


<pre><code>usage: univeral-RIG.py [-h] [-m [MAXIMUM]] [-e [EXTENSION]] [-v VERBOSITY] [genera]

Basic reference library generator; rendered from curated RefSeq genome assemblies.

positional arguments:
  genera                List genera here. Separate multiple genera with comma ( >> no spaces << )

optional arguments:
  -h, --help            show this help message and exit
  -m [MAXIMUM], --maximum [MAXIMUM]
                        number of strains per species [default: 1]
  -e [EXTENSION], --extension [EXTENSION]
                        the file extension for the assembled genomes [default is .fa]
  -v VERBOSITY, --verbosity VERBOSITY
                        increase output verbosity</code></pre> 

  
## Example 1:
  
<code>python3 universal-RIG.py -m 3 -e fasta Bacillus</code>

Your new library will contain three genome assemblies of each species within the Genus Bacillus. The genomes will be saved with the file extension <code>.fasta</code>.
 
## Example 2: 
  
<code>python3 universal-RIG.py -m 10 -e fna Oenococcus,Weissella </code>
  
Your new library will contain ten genome assemblies of each species within the Genera Oenococcus and Weissella. The genomes will be saved with the file extension <code>.fna</code>. Note: there is no space between the Genera.

## Example 3: 
  
<code>python3 universal-RIG.py Arabidopsis </code>
  
Your new library will contain one genome assembly of each species within the Genus Arabidopsis. The genomes will be saved with the file extension <code>.fa</code>. 
