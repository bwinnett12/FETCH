# ncbifetcher

### Instructions:
1) Update the setwd() to your location of the repository install. It should be listed as fetcher.py
2) Run the app.R or load each piece individually
3) In the blank write in the classifiers for gene bank files to install. Ex. NC_012920.1 downloads that file.


### Troubleshooting
If the R packages are missing, they may need to be downloaded. Copy this command into the R terminal:
```
install.packages("shiny")
```

If the Python package for bio is missing, run this command in terminal:
```
python -m pip install bio Bio biopython
```


It may need to be ran as root. If you aren't able to use a terminal or if the terminal doesn't work as efficiently as
it could be, there are alternatives. If using an IDE (such as PyCharm), hover over the package itself and there should
be a download this package button.

#### TODO
- [x] Write a script that parses the ncbi
- [x] Write a front-end that executes the script
- [ ] Configure it to work on the LavrovLab server or some form of university funded hosting
- [ ] Clean up Python
- [ ] Clean up R
- [ ] Add optional folder location specifier
- [ ] Add functionality and user customization for input
