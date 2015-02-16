COMS E6111 - Project 1
======================

# Running the program
To run a query through the program execute the `main.py` script with the
appropriate arguments.
```
python main.py <apikey> <precision> <query>
```
The following arguments should be provided to the script
* `<apikey>`: A Bing Search API key
* `<precision>`: The target for _precision@10_, a real value between 0 and 1
* `<query>`: The search query string, which should be passed as a single
argument (i.e. terms separated by white space should be enclosed in quotes if
the invoking shell requires such annotation)

The script will the query Bing and interactively prompt the user to mark the top
10 results as relevant or not.  The user can respond to these prompts by
entering `y` if the result is relevant or `n` if the result is not relevant.
After the user does this for all 10 results the _precision@10_ is computed and
displayed.

```
Result #1 ------------------------------------------------------------
Gates Corporation
http://www.gates.com/

Gates Corporation is Powering Progress™ in the Oil & Gas, Energy,
Mining, Marine, Agriculture, Transportation and Automotive Industries.
----------------------------------------------------------------------
Is result #1 relevant? [y/n]
```


# Internal Design

## Query modification method

# Manifest of project files
* `bs4/__init__.py`
* `bs4/builder/__init__.py`
* `bs4/builder/_html5lib.py`
* `bs4/builder/_htmlparser.py`
* `bs4/builder/_lxml.py`
* `bs4/dammit.py`
* `bs4/diagnose.py`
* `bs4/element.py`
* `bs4/testing.py`
* `bs4/tests/__init__.py`
* `bs4/tests/test_builder_registry.py`
* `bs4/tests/test_docs.py`
* `bs4/tests/test_html5lib.py`
* `bs4/tests/test_htmlparser.py`
* `bs4/tests/test_lxml.py`
* `bs4/tests/test_soup.py`
* `bs4/tests/test_tree.py`
* `main.py`
* `parsing.py`
* `README.md`
* `results.py`
* `results_test.py`
* `sample_data/sample_output.json`
* `sample_data/sample_output.xml`
* `sample_data/sample_output_formatted.json`
* `sample_data/sample_output_formatted.xml`
