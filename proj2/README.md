COMS E6111 - Project 2
======================

# Running the program

To run a query through the program execute the `main.py` script with the
appropriate arguments.

```
python main.py -api_key <api_key> -query_type <type> -query <query>
```

The following arguments should be provided to the script
* `<api_key>`: A Bing Search API key
* `<type>`: The type of query to perform.  Must be either `infobox` or
`question`.
* `<query>`: The search query string, which should be passed as a single
argument (i.e. terms separated by white space should be enclosed in quotes if
the invoking shell requires such annotation).  For the `question` query type
the only supported question is of the form "Who created _x_?".

The script will perform the type of query requested and print the results.
For an infobox query, an ASCII pretty-printed box will be displayed.  For a
question query a list of results in the assignment-specified format will
be printed.

# Internal design
The design of this application is as described in the assignment.  From a code
perspective, `freebase.py` contains classes for querying the Freebase API and
`infobox.py` contains code that processes the API responses and pretty prints
an ASCII infobox.  Constraints defined in the assignment were taken into
account in all the code for this project, therefore the code for this project
is not very general purpose.

## Infobox creation
Following the design described in the assignment, we query for Freebase topics,
and then choose the first topic that matches a subset of categories.  After
choosing the topic, we print an infobox about it that includes the information
asked for in the assignment.

## Question answering
We answer questions only of one type, and only for a fixed number of
categories.  This makes the question answering consist of not much more than
querying freebase once for each category, and then printing the results.  For
consistency, results are sorted alphabetically before printing.

# Manifest of project files
* `freebase.py`
* `freebase_test.py`
* `infobox.py`
* `main.py`
* `README.md`
* `transcript_infobox.txt`
* `transcript_question.txt`


