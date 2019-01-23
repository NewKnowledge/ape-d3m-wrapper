# Ape D3M Wrapper

Wrapper of the nk_ape into D3M infrastructure. All code is written in Python 3.5 and must be run in 3.5 or greater.

The base library for nk_ape can be found here: https://github.com/NewKnowledge/nk_ape

## Install

pip3 install -e git+https://github.com/NewKnowledge/ape-d3m-wrapper.git#egg=APEd3mWrapper --process-dependency-links

## Output
Input pandas dataframe augmented with related concepts as predicted by APE. 

## Available Functions

#### produce
Produce primitive's best guess for the structural type of each input column. The input is a pandas dataframe. The output is input pandas dataframe augmented with related concepts as predicted by APE.
