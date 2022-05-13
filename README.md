# Make a reference library in minutes direct from RefSeq.
Reference library generator. Downloads genomes from RefSeq.

Each new library contains representatives of every species within the Genera you specify. The highest spec genome assemblies are selected. You can choose how many representatives from each species to include. Please note, for some species the quantity you specify may not be available.

Your new library will be stored in a folder named with the date and time.

<code>python3 universal-RIG.py \<genera> \<max> \<extension> </code>
  
### Example 1:
  
<code>python3 universal-RIG.py Bacillus 3 fasta </code>

Your new library will contain three genomes of each species within the Genus Bacillus. The genomes will be saved with the file extension <code>.fasta</code>.
 
### Example 2: 
  
<code>python3 universal-RIG.py Oenococcus,Weissella 10 fna </code>
  
Your new library will contain ten genomes of each species within the Genera Oenococcus and Weissella. The genomes will be saved with the file extension <code>.fna</code>. Note: there is no space between the Genera.

  
