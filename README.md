# ncbifetcher

#### Hello there
This program is designed to be a user friendly storage space for mitochondrial genomes, elements, genes, and protein outputs. The program has integration for ncbi through biopython while also the user has an option to import their own sequences, genomes, etc to all be integrated. The program also has keeps records of what is stored in storage. With these records, another module can pull what is specified from these records (indexes) and consolidate them into a fasta file. Mafft is supported so the outputed files can then be aligned as another output.

If there are any questions, concerns, or nice stories; please don't hesitate to contact at wwinnett@iastate.edu.

This project was made in conjunction with Lavrov lab and under the supervision of Dr. Muthye and Dr. Lavrov.

### Instructions:

First, run this command (from the project directory) to ensure that your system has all of the required dependencies:

```
pip install .
```

Then you must enter any information into ncbifetcher.config. Email is required to fetch anything

All of the available features are an adjustment of this command from within the cloned file:
```
python3 main.py --help
```
Instead of using --help or -h, you can sub arguments to do what you need. 

There are a couple of things that you can do with this project:
1) Download genbank (.gb), genomes(.fa), and genes (.fa) to the base storage file (default is in project directory). You can do this by running with the extension **-f [Accession Number or ncbi query]**:

```
python3 main.py -f [ncbi query]
```

Query can be treated as if you were searching ncbi by itself. So things like accession numbers, taxonomy (such as txid2754381[Organism]), or boolean operators (mouse AND mitochondria). Running this can also updates the indexes (gene.lst and species.lst). It is on by default, but can be switched off from the ncbifetcher.config

2) The genes can be pulled from storage and consolidated into a new fasta file containing all of the genes from a species and from a gene. To specify which genes and/or species, uncomment the genes or species you want from the index. 

```
Selected: ATP6,
Unselected or commented out: ;ATP6.
```

By default, the comment is a semi-colon. The indexes location is also under the indexes folder in the project directory. The outputs are fastas and the clustal aligned files. 

To run this feature, run the original command with -p

```
python3 main.py -p
```

3) You can manually reset the indexes (genes.lst and species.lst) by running with -i
```
python3 main.py -i
```

4) You can switch the location of your storage from inside the cloned file to a site of your own specification. To do so, you must first run with the -s extension 
```
python3 main.py -s [Destination]
```
That command sets up a file structure at that location. You must also switch the location within ncbifetcher.config under "storage_location=''"

### Road map 
- Parse the gene bank and download raw data
- Save the raw data to a .gb file
- Create a fasta out of the individual pieces to it (as .fa)
- Create an amino acid version of the fasta (as .faa)
- Create a fasta out of the whole genome (full\_fa/*.fa)
- Create an amino acid fasta out of the whole genome (full_faa/*.faa)
- Create a battery that does all three processes

##### Indexer
- Save the storage as an smooth and easy way to work with the saved files
- Automate refreshing and resetting of indexes

##### Puller
- Neatly pull out desired information as directed by the indexes. Save them as a fasta
- Align the fasta and save as a clustal aligned file (.aln)

#### TODO
- [x] Allow for the storage and output to have easy integration
- [x] Allow the program to be called from the command line
- [ ] Implement an algorithm for output of puller
- [x] Allow translation to be specified by the genbank file rather than default
- [x] Allow the user to specify an optional parameters to the argument.
- [ ] Reintegrate alignment
- [-] Add more optional parameters within the command utility and config file

- [ ] Codon align selected genes PAL2NAL
- [ ] Run Gblocks on alignment
- [ ] Run RAXML / FASTREE to get phylogenetic trees


###### Late game TODO 
- [ ] Integrate R shiny
- [ ] Provide windows support for mafft

#### Known issues
- [x] Translating of sequence is not being called.
