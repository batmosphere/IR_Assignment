# Search Engine Using Inverted Index

This project has been written as the CS F369 Informaton Retrieval Assignment 1. The project implements a basic search engine in Python using Inverted Index to query from the Brown Corpus. We could theoretically expand the codebase to search through any similar database with relative ease.

## Team

1. **Aayush Barthwal** - 2015A7PS0XXXH
2. **Mukund Kothari** - 2015B4PS0546H
3. **Rohitt Vashishtha** - 2015A7PS0XXXH
4. **Tushar Aggarwal** - 2015A7PS0047H

## Setting Up

1. First, clone the project from git using `git clone https://github.com/batmosphere/IR_Assignment`.
2. Set up a virtual env (optional) for better namespacing.
3. Run `sudo apt install python3-tk portaudio19-dev python3-all-dev` to install system wide dependencies.
4. Run `pip install -r requirements.txt` to install project wise dependencies.
5. Make sure you have firefox web browser installed and in your `$PATH`. Else, alias your preferred web browser to `firefox` so that we can open the search results in the browser.

## Usage

Run `python Tokenizer.py` to generate the corpus. Note: Tokenizer is compatible with Python 2 only.

Run `python Search_Query.py` to run the Search GUI. Note: Search_Query is compatible with Python 3 only.

## Features

Following is the list of features we support:

1. Case-insensitive Search Results.
2. Normalisation of query and corpus texts.
3. Ranking of Search Results.
4. Tkinter based UI for Querying.
5. Voice input for search text(experimental).
6. Browsing individual Search Results through clickable links.


# Brown Corpus

We have used Brown Corpus in our project. Here is a brief about it.

> The Brown Corpus of Standard American English was the first of the modern, computer readable, general corpora. It was compiled by W.N. Francis and H. Kucera, Brown University, Providence, RI.

> The corpus consists of one million words of American English texts printed in 1961. The texts for the corpus were sampled from 15 different text categories to make the corpus a good standard reference. Today, this corpus is considered small, and slightly dated. The corpus is, however, still used. Much of its usefulness lies in the fact that the Brown corpus lay-out has been copied by other corpus compilers. The LOB corpus (British English) and the Kolhapur Corpus (Indian English) are two examples of corpora made to match the Brown corpus. The availability of corpora which are so similar in structure is a valuable resourse for researchers interested in comparing different language varieties, for example.

> For a long time, the Brown and LOB corpora were almost the only easily available computer readable corpora. Much research within the field of corpus linguistics has therefore been made using these data. By studying the same data from different angles, in different kinds of studies, researchers can compare their findings without having to take into consideration possible variation caused by the use of different data.

> At the University of Freiburg, Germany, researchers are compiling new versions of the LOB and Brown corpora with texts from 1991. This will undoubtedly be a valuable resource for studies of language change in a near diachronic perspective.

> The Brown corpus consists of 500 texts, each consisting of just over 2,000 words. The texts were sampled from 15 different text categories. The number of texts in each category varies (see below). 
