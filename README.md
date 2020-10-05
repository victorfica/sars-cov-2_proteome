# SARS-CoV-2 Proteome Analysis

**This repository is a work on progress!**

The workflow im following is related with the project structure on the repo. All initial coding is made using Notebooks,
so probably notebooks could be updated more frequently. All this work is in `Notebooks` folder. After finishing a basic working code
for certain task, i start to transcribe to the better structured scripts on `src` folder. Im trying to make
some CLI-oriented package.

To test and develop the CLI package we have to locally install our code, for now, using a simple setup.py. 

## Installation

I strongly recommend using a Conda environment, so please create a new one first.

Required packages for run CLI script:
```
biopython (>=1.78)
numpy (>=1.17.2)
fire (0.3.1)
```

To install the package, use developer mode. Run inside `sars-cov-2_proteome` folder :

``` 
$ pip install -e .
```

## Usage

Once installed you can run `sarscov2_processing` executable on command line, this will enter to an special help context
, you can quit from them pressing `Q` key:

```
 $ sarscov2_processing

NAME
    sarscov2_processing - CLI to process SARS-CoV-2 proteins Fasta File from GISAID.

SYNOPSIS
    sarscov2_processing - COMMAND | VALUE

DESCRIPTION
    CLI to process SARS-CoV-2 proteins Fasta File from GISAID.

COMMANDS
    COMMAND is one of the following:

     process
       Process SARS-CoV-2 Samples proteins and write out to respective Fasta Files.

VALUES
    VALUE is one of the following:

     others

     outdir
(END)

```

## Quick Guide

To run the first step (for now) of GISAID protein data processing, first you need the rawdata from GISAID (about 1.5 GB).
You can ask for access on GISAID platform and then download the data. Put the rawdata in `raw` data folder.
After that you can run `process` subcommand inside raw data folder:

```
sarscov2_processing process --rawfile allprot0922.fasta
```

By defautl this will parse the rawdata and write out the reference sample proteins and the non-reference sample proteins
to a fasta file for each protein in the proteome. Also you can specify not process `others` proteins using the negative flag
`--noothers`:

```
sarscov2_processing process --noothers --rawfile allprot0922.fasta
```
