COMS E6111 - Project 3
======================
Kevin Graney (kmg2165@columbia.edu)

# Running the program
To generate association rules for a transaction file execute the `main.py`
script with the required arguments.
```
python main.py <integrated datafile> <min_sup> <min_conf>
```
The following arguments should be provided to the script
* `<integrated datafile>`: The path to the integrated datafile.  In the case of
  the project submission this is `data/integrated.csv.gz`.
* `<min_sup>`: The minimum support level for frequent itemsets, must be a real
  value between 0 and 1
* `<min_conf>`: The minimum confidence for association rules, must be a real
  value between 0 and 1

## Sample run
```
python main.py data/integrated.csv.gz 0.05 0.80
```
The output from this run is provided in `example-run.txt`.

# Dataset description
The dataset used is from the NYPD's Stop & Frisk logs for 2003.  Other years'
information is available, however only a single year was used for this project
to keep runtime down.  The single year provides over 160,000 transactions, which
is well over the assignment minimum of 1,000.

This dataset was chosen because it fits nicely into the transaction list model,
and there is plenty of data available to draw interesting conclusions from.
Unlike some other datasets from NYC.gov these files are fairly well organized
and are available for historical periods.

Only select fields from the dataset were used to create the integrated dataset
file.  The processing code that generated the integrated dataset file can
be found in `data.py`, and is called by the `main()` method in `convert.py`.

In generating the integrated dataset file each entry in the log is considered
a transaction.  The yes/no question responses provide an easy way to add items
to these transactions: add the question statement for which there is a yes/no
response to every transaction where the answer is yes.  It is also possible
to add a negation of the question statement for cases where the answer is no,
but this was avoided because it doubles the average transaction length (and
our algorithms have non-ideal complexity so runtime is negatively affected
by this).

In addition to the yes/no questions a couple other columns were added where
an obvious conversion between the answer to a discrete set of terms is either
provided or trivial to implement.  One yes/no question was also excluded,
which is the one asking "DID OFFICER EXPLAIN REASON FOR STOP?"  Including this
question adds noise since nearly every transaction has it present, thus it
was removed.

To create the integrated dataset file from NYC.gov data use `convert.py`.
```
python convert.py data/2003.csv.gz ./data/integrated.csv.gz
```

# Internal design
The implementation of the apriori algorithm and method for finding association
rules from the frequent itemsets are in `assoc_list.py`.  The apriori algorithm
is implemented directly from the text without significant modification.
Constructing association rules is done in a naive manner by building
all possible rules for every subset of items from the fequent itemsets.
Some memoization is done during association rule construction to avoid
searching the same subsets multiple times.  Only the association rules with
confidence of at least `min_conf` are returned.

The file format used for datafiles is gzipped csv, which was chosen to reduce
the size of the integrated and source datafiles.

# Manifest of project files

