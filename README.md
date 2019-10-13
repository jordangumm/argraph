# ARGraph
So far only a general ARG (CARD) sequence metadata curation script is implemented.

## Setup
1. Make sure you have pipenv installed.
> $ pip install pipenv

2. Install dependencies
Do this within the base directory of the repository.
> $ pipenv install

3. Build to install CARD dependencies
> $ bash build.sh

## Usage
1. Load the virtual environment
> $ pipenv shell

2. Build the gene metadata file
> $ python build_db.py
