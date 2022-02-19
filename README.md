## Hello there
This tool is FETCH. It is a tool for retrieving (fetching) mitochondrial genomes and biological data from NCBI for user friendly storage along with consolidation, recording of total storage contents, and allows connection to other tools.


### Setup
There are two simple strategies to setting up FETCH. The variation to choose rests upon if you want to install dependencies to your system or to a local contained folder.
- Standard method (preferred)
```
python3 setup.py develop
```

Alternatively, if you are using a remote server in which you do not have root permissions or wish to have dependencies stored discretely:
```
bash containment.bash
```
Installs all dependencies needed for the project into /src/. There may be dependencies that you already have installed, but it should take priority of local folder contents


###### Folder setup and preuse tasks
By default, folders are not set up. This is because some users want their storage on a separate drive, folder, or project location. To choose a location, change the value in ncbifetcher.config to whatever you wish. Notice, there are four folder locations that can be changed. Afterwards, fetch will set up the folders up for you with this command:
```
python3 FETCH.py -s
```

While you are in ncbifetcher.config, you need to add your email in to retrieve NCBI data


### Nomenclature / Roadmap
 - Setup (-s or –setup): Sets up all local files for FETCH.
 - Fetch (-f or --fetch): Fetching retrieves any genome or any nucleotide based sequence from NCBI via accession number; as a single, concatenation, or text file full of accession numbers. The query also works as a boolean search parameter so you can type in anything you would directly on NCBI. This act stores (as fasta files) the genome, every gene individually and its translated equivalent, every gene together and its translated equivalent, and the genbank file as you would see if you searched the accession number on NCBI (as a text file) into storage.

 - Database (-b): Specifies which database of NCBI to fetch from. Default is nucleotide

 - Index (-i or –index): An up to date register of what is found in storage with multiple lists to clarify the data. Inside the indexes folder, there are four items: a genes.lst, a species.lst, a genes folder, and a species folder. The list files contain a list of every gene or species that is found in storage. Each record is commented out using a semi-colon. This is important because anything not commented out will be pulled. Running the -i command resets the indexes and re-comments everything. The folders contain a listing of what genes are contained per species and what species have a gene.

 - Pull (-p or --pull): Consolidates every instance of a gene into a single fasta. Decommenting an index specifies which genes you wish you have pulled. For example, un-commenting ATP6 (;ATP6 → ATP6) and pulling will withdraw every instance of ATP6 into output.

 - Report (-r or –report): Generates reports and storage-wide reports. Currently available are a text report and a csv gene / species presence matrix.

 - MAFFT (-m or --mafft): Runs mafft on all output files. Must have specified mafft in config if mafft not on path

 - FastTree (-t or -tree): Runs fasttree on all output files. Must have specified fasttree location even if on path (/usr/bin/fastttree)

 - Delete (-d or --delete): Deletes everything in storage, reports, indexes, and output

### Case study
If you are like me and a wall of commands means the same as a Hawaiian to Greek dictionary to an English speaker, then a case study is the way to go. So let’s take for an example someone who is interested in the studying the evolutionary change in marsupials of Australia via the ATP6 and ND2 but we also want to see a genome wide profile of these organisms. <br/>


The first thing we want to do is find some genomes on NCBI that we are interested in.
+ KY996502.1 – Macropus giganteus mitochondrion, complete genome. (Eastern Grey Kangaroo)
+ AB241053.1 - Phascolarctos cinereus mitochondrial DNA, nearly complete genome(Koala)
+ AB241055.1 - Petaurus breviceps mitochondrial DNA, nearly complete genome (Sugar Glider)
+ KY996507.1 - Notamacropus agilis mitochondrion, complete genome (Agile Wallaby)

We can either append these together with commas or place them in a text file. I will place one in the tests file of FETCH as marsupial.txt.

Next step is to set up FETCH. Clone it from the github and then run setup. So… From command line…
```
git clone https://github.com/bwinnett12/FETCH.git
```

Change into the FETCH folder and run:
```
python3 setup.py develop
```
FETCH should mostly be operational. The last thing to do is setup the folders to be used. Most of the time, using the FETCH folder is fine. But in some cases and some people want to have their folders for output and storage on separate drives, folders, locales, etc. If you wish to change any locations, edit them in ncbifetcher.config. Before fetching you will need to edit ncbifetcher.config either way to include your email. Always tell NCBI who you are. Otherwise, just run this command:

```
python3 FETCH.py -s
```

Good to go! We are now set up. Let’s get back to the adorable koalas and kangaroos. Since I placed everything into a text file, we can simply fetch that text file. If you didn’t want to do that, you can omit the text file and simply type the accession number. Eitherway:

```
python3 FETCH.py -f tests/marsupial.txt
```

There should be a plethora of files in storage and many in indexes too. If you want to see what species we have, check indexes.lst in indexes/. Or if you want to know what genes are present, check genes.lst in genes/. If there are any more genomes that you wanted to add, there isn’t any specific time. Now, or later it’s totally up to you!

We are still on a mission through: we want to look at ATP6 and ND2 of these marsupials. Next step is to go into the indexes/genes.lst file and comment out those genes. It will prepare to pull every instance of those genes into its own file.

```
;16S-ribosomal-RNA
ATP6
;ATP8
…
;ND1
ND2
;ND3
;ND4
```

Now we are ready to pull! Just go ahead and run the pull command and our output will be loaded with two new files.

```
python3 FETCH.py -p
```

Great! ATP6.fa and ND2.fa! If you wanted to run a tool such as mafft or fasttree; now is the time to do it. I can also be piggybacked onto the prior step such as…

```
python3 FETCH.py -mt
or
python3 FETCH.py -pmt
```

Notice! In order to run mafft, it must be either on path (linux) or the location of mafft’s .exe listed on the ncbifetcher.config. FastTree’s location must be listed even if on path. On linux you can find it by typing “which FastTree” which may yield something like /usr/bin/FastTree.


There you go! You now should have an aligned copy of four mitochondrial ATP6 and ND2 genes with a trees. Not only that, there is a fasta that is available for you to do whatever you want to do with it. With science, there isn’t a guide for everything but it’s up to you to make your own constellations… But before we go, let’s generate a report by simply typing:

```
python3 FETCH.py -r
```

Presto! You now have an easier to handle report of what is in storage. If you add anything else to storage; pulled, reports, and other outputs will need to be updated. But indexes should be automatically refreshed. The worked out files will be in the tests folder under marsupial.

Thank you for reading!

#### TODO
- [ ] Switch pip into poetry
- [x] Implement an algorithm for output of puller
- [ ] Make resetting of indexes optional
- [ ] Add more optional parameters within the command utility and config file

- [ ] Codon align selected genes PAL2NAL
- [ ] Run Gblocks on alignment
- [x] Run RAXML / FASTREE to get phylogenetic trees


##### Late game TODO
- [ ] Integrate R shiny
- [ ] Provide windows support for mafft

##### Known issues

###### Citations

+ Cock PA, Antao T, Chang JT, Chapman BA, Cox CJ, Dalke A, Friedberg I, Hamelryck T, Kauff F, Wilczynski B and de Hoon MJL (2009) Biopython: freely available Python tools for computational molecular biology and bioinformatics. Bioinformatics, 25, 1422-1423
+ Katoh, Misawa, Kuma, Miyata 2002 (Nucleic Acids Res. 30:3059-3066)
MAFFT: a novel method for rapid multiple sequence alignment based on fast Fourier transform.
(describes the FFT-NS-1, FFT-NS-2 and FFT-NS-i strategies)
+ Price MN, Dehal PS, Arkin AP. 2010. FastTree 2 - Approximately Maximum-Likelihood Trees for Large Alignments. Online: PLOS ONE.