COMS E6111 - Project 3
======================
Kevin Graney (kmg2165@columbia.edu)

# Running the program
To run a query through the program execute the `main.py` script with the
appropriate arguments.
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

# Dataset description
The dataset used is from the NYPD's Stop & Frisk logs for 2003.  Other years'
information is available, however only a single year was used for this project
to keep runtime down.  The single year provides over 160,000 transactions, which
is well over the assignment minimum of 1,000.

Only select fields from the dataset were used to create the integrated dataset
file.  The processing code that generated the integrated dataset file can
be found in `data.py`, and is called by the `main()` method in `convert.py`.

# Internal design

# Manifest of project files

