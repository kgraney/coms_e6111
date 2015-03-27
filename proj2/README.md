COMS E6111 - Project 2
======================

# Running the program

To run a query through the program execute the `main.py` script with the appropriate arguments.

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

# Internal design

# Manifest of project files
* `freebase.py`
* `freebase_test.py`
* `infobox.py`
* `main.py`
* `README.md`
* `transcript_infobox.txt`
* `transcript_question.txt`


