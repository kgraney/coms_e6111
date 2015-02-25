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

If the _precision@10_ is below the target precision, a new query is displayed
and executed, with a new round of 10 relevance prompts displayed to the user.


# Internal Design
Query modification works by using the vector space model to compare the relevant
documents, as marked by the user, with the other documents returned by Bing and
the query.  This comparison is used to suggest new terms to add to the query,
with the goal being to return more relevant results.  Vectors are computed for
each of the search results returned as well as each query that is executed.

## Computing vectors
```TODO: add how the vectors are computed (and write the code!)
```

All vectors are unit vectors.

## Query modification method
Query modification works by maintaining a cumulative relevance vector for all
results marked as relevant by the user.  For each result the user marks as
relevant the relevance vector is updated to represent the arithmetic mean of
the result vectors.

This artithmetic mean is preserved across queries, so if the user feedback from
both the first and second second queries result in a _precision@10_ less than
the target the relevance vector used to produce the third query will be the
cumulative arithmetic mean of the relevant results from both the first and
second queries.  This design assumes the user maintains a consistent notion of
relevance during an entire single execution of this program.

# Manifest of project files
* `bing.py`
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
* `nltk/__init__.py`
* `nltk/align/__init__.py`
* `nltk/align/api.py`
* `nltk/align/bleu.py`
* `nltk/align/gale_church.py`
* `nltk/align/gdfa.py`
* `nltk/align/ibm1.py`
* `nltk/align/ibm2.py`
* `nltk/align/ibm3.py`
* `nltk/align/phrase_based.py`
* `nltk/align/util.py`
* `nltk/app/__init__.py`
* `nltk/app/chartparser_app.py`
* `nltk/app/chunkparser_app.py`
* `nltk/app/collocations_app.py`
* `nltk/app/concordance_app.py`
* `nltk/app/nemo_app.py`
* `nltk/app/rdparser_app.py`
* `nltk/app/srparser_app.py`
* `nltk/app/wordfreq_app.py`
* `nltk/app/wordnet_app.py`
* `nltk/book.py`
* `nltk/ccg/__init__.py`
* `nltk/ccg/api.py`
* `nltk/ccg/chart.py`
* `nltk/ccg/combinator.py`
* `nltk/ccg/lexicon.py`
* `nltk/chat/__init__.py`
* `nltk/chat/eliza.py`
* `nltk/chat/iesha.py`
* `nltk/chat/rude.py`
* `nltk/chat/suntsu.py`
* `nltk/chat/util.py`
* `nltk/chat/zen.py`
* `nltk/chunk/__init__.py`
* `nltk/chunk/api.py`
* `nltk/chunk/named_entity.py`
* `nltk/chunk/regexp.py`
* `nltk/chunk/util.py`
* `nltk/classify/__init__.py`
* `nltk/classify/api.py`
* `nltk/classify/decisiontree.py`
* `nltk/classify/maxent.py`
* `nltk/classify/megam.py`
* `nltk/classify/naivebayes.py`
* `nltk/classify/positivenaivebayes.py`
* `nltk/classify/rte_classify.py`
* `nltk/classify/scikitlearn.py`
* `nltk/classify/svm.py`
* `nltk/classify/tadm.py`
* `nltk/classify/util.py`
* `nltk/classify/weka.py`
* `nltk/cluster/__init__.py`
* `nltk/cluster/api.py`
* `nltk/cluster/em.py`
* `nltk/cluster/gaac.py`
* `nltk/cluster/kmeans.py`
* `nltk/cluster/util.py`
* `nltk/collocations.py`
* `nltk/compat.py`
* `nltk/corpus/__init__.py`
* `nltk/corpus/europarl_raw.py`
* `nltk/corpus/reader/__init__.py`
* `nltk/corpus/reader/aligned.py`
* `nltk/corpus/reader/api.py`
* `nltk/corpus/reader/bnc.py`
* `nltk/corpus/reader/bracket_parse.py`
* `nltk/corpus/reader/chasen.py`
* `nltk/corpus/reader/childes.py`
* `nltk/corpus/reader/chunked.py`
* `nltk/corpus/reader/cmudict.py`
* `nltk/corpus/reader/conll.py`
* `nltk/corpus/reader/dependency.py`
* `nltk/corpus/reader/framenet.py`
* `nltk/corpus/reader/ieer.py`
* `nltk/corpus/reader/indian.py`
* `nltk/corpus/reader/ipipan.py`
* `nltk/corpus/reader/knbc.py`
* `nltk/corpus/reader/lin.py`
* `nltk/corpus/reader/nombank.py`
* `nltk/corpus/reader/nps_chat.py`
* `nltk/corpus/reader/pl196x.py`
* `nltk/corpus/reader/plaintext.py`
* `nltk/corpus/reader/ppattach.py`
* `nltk/corpus/reader/propbank.py`
* `nltk/corpus/reader/rte.py`
* `nltk/corpus/reader/semcor.py`
* `nltk/corpus/reader/senseval.py`
* `nltk/corpus/reader/sentiwordnet.py`
* `nltk/corpus/reader/sinica_treebank.py`
* `nltk/corpus/reader/string_category.py`
* `nltk/corpus/reader/switchboard.py`
* `nltk/corpus/reader/tagged.py`
* `nltk/corpus/reader/timit.py`
* `nltk/corpus/reader/toolbox.py`
* `nltk/corpus/reader/udhr.py`
* `nltk/corpus/reader/util.py`
* `nltk/corpus/reader/verbnet.py`
* `nltk/corpus/reader/wordlist.py`
* `nltk/corpus/reader/wordnet.py`
* `nltk/corpus/reader/xmldocs.py`
* `nltk/corpus/reader/ycoe.py`
* `nltk/corpus/util.py`
* `nltk/data.py`
* `nltk/decorators.py`
* `nltk/downloader.py`
* `nltk/draw/__init__.py`
* `nltk/draw/cfg.py`
* `nltk/draw/dispersion.py`
* `nltk/draw/table.py`
* `nltk/draw/tree.py`
* `nltk/draw/util.py`
* `nltk/featstruct.py`
* `nltk/grammar.py`
* `nltk/help.py`
* `nltk/inference/__init__.py`
* `nltk/inference/api.py`
* `nltk/inference/discourse.py`
* `nltk/inference/mace.py`
* `nltk/inference/nonmonotonic.py`
* `nltk/inference/prover9.py`
* `nltk/inference/resolution.py`
* `nltk/inference/tableau.py`
* `nltk/internals.py`
* `nltk/jsontags.py`
* `nltk/lazyimport.py`
* `nltk/metrics/__init__.py`
* `nltk/metrics/agreement.py`
* `nltk/metrics/association.py`
* `nltk/metrics/confusionmatrix.py`
* `nltk/metrics/distance.py`
* `nltk/metrics/paice.py`
* `nltk/metrics/scores.py`
* `nltk/metrics/segmentation.py`
* `nltk/metrics/spearman.py`
* `nltk/misc/__init__.py`
* `nltk/misc/babelfish.py`
* `nltk/misc/chomsky.py`
* `nltk/misc/minimalset.py`
* `nltk/misc/sort.py`
* `nltk/misc/wordfinder.py`
* `nltk/parse/__init__.py`
* `nltk/parse/api.py`
* `nltk/parse/chart.py`
* `nltk/parse/dependencygraph.py`
* `nltk/parse/earleychart.py`
* `nltk/parse/featurechart.py`
* `nltk/parse/generate.py`
* `nltk/parse/malt.py`
* `nltk/parse/nonprojectivedependencyparser.py`
* `nltk/parse/pchart.py`
* `nltk/parse/projectivedependencyparser.py`
* `nltk/parse/recursivedescent.py`
* `nltk/parse/shiftreduce.py`
* `nltk/parse/stanford.py`
* `nltk/parse/util.py`
* `nltk/parse/viterbi.py`
* `nltk/probability.py`
* `nltk/sem/__init__.py`
* `nltk/sem/boxer.py`
* `nltk/sem/chat80.py`
* `nltk/sem/cooper_storage.py`
* `nltk/sem/drt.py`
* `nltk/sem/drt_glue_demo.py`
* `nltk/sem/evaluate.py`
* `nltk/sem/glue.py`
* `nltk/sem/hole.py`
* `nltk/sem/lfg.py`
* `nltk/sem/linearlogic.py`
* `nltk/sem/logic.py`
* `nltk/sem/relextract.py`
* `nltk/sem/skolemize.py`
* `nltk/sem/util.py`
* `nltk/stem/__init__.py`
* `nltk/stem/api.py`
* `nltk/stem/isri.py`
* `nltk/stem/lancaster.py`
* `nltk/stem/porter.py`
* `nltk/stem/regexp.py`
* `nltk/stem/rslp.py`
* `nltk/stem/snowball.py`
* `nltk/stem/wordnet.py`
* `nltk/tag/__init__.py`
* `nltk/tag/api.py`
* `nltk/tag/brill.py`
* `nltk/tag/brill_trainer.py`
* `nltk/tag/brill_trainer_orig.py`
* `nltk/tag/hmm.py`
* `nltk/tag/hunpos.py`
* `nltk/tag/mapping.py`
* `nltk/tag/senna.py`
* `nltk/tag/sequential.py`
* `nltk/tag/stanford.py`
* `nltk/tag/tnt.py`
* `nltk/tag/util.py`
* `nltk/tbl/__init__.py`
* `nltk/tbl/api.py`
* `nltk/tbl/demo.py`
* `nltk/tbl/erroranalysis.py`
* `nltk/tbl/feature.py`
* `nltk/tbl/rule.py`
* `nltk/tbl/template.py`
* `nltk/test/__init__.py`
* `nltk/test/align.doctest`
* `nltk/test/align_fixt.py`
* `nltk/test/all.py`
* `nltk/test/bnc.doctest`
* `nltk/test/ccg.doctest`
* `nltk/test/chat80.doctest`
* `nltk/test/childes.doctest`
* `nltk/test/childes_fixt.py`
* `nltk/test/chunk.doctest`
* `nltk/test/classify.doctest`
* `nltk/test/classify_fixt.py`
* `nltk/test/collocations.doctest`
* `nltk/test/compat.doctest`
* `nltk/test/compat_fixt.py`
* `nltk/test/corpus.doctest`
* `nltk/test/corpus_fixt.py`
* `nltk/test/data.doctest`
* `nltk/test/dependency.doctest`
* `nltk/test/discourse.doctest`
* `nltk/test/discourse_fixt.py`
* `nltk/test/doctest_nose_plugin.py`
* `nltk/test/drt.doctest`
* `nltk/test/featgram.doctest`
* `nltk/test/featstruct.doctest`
* `nltk/test/framenet.doctest`
* `nltk/test/generate.doctest`
* `nltk/test/gluesemantics.doctest`
* `nltk/test/gluesemantics_malt.doctest`
* `nltk/test/gluesemantics_malt_fixt.py`
* `nltk/test/grammar.doctest`
* `nltk/test/grammartestsuites.doctest`
* `nltk/test/index.doctest`
* `nltk/test/inference.doctest`
* `nltk/test/inference_fixt.py`
* `nltk/test/internals.doctest`
* `nltk/test/japanese.doctest`
* `nltk/test/logic.doctest`
* `nltk/test/metrics.doctest`
* `nltk/test/misc.doctest`
* `nltk/test/nonmonotonic.doctest`
* `nltk/test/nonmonotonic_fixt.py`
* `nltk/test/paice.doctest`
* `nltk/test/parse.doctest`
* `nltk/test/portuguese_en.doctest`
* `nltk/test/portuguese_en_fixt.py`
* `nltk/test/probability.doctest`
* `nltk/test/probability_fixt.py`
* `nltk/test/propbank.doctest`
* `nltk/test/relextract.doctest`
* `nltk/test/resolution.doctest`
* `nltk/test/runtests.py`
* `nltk/test/segmentation_fixt.py`
* `nltk/test/semantics.doctest`
* `nltk/test/semantics_fixt.py`
* `nltk/test/sentiwordnet.doctest`
* `nltk/test/simple.doctest`
* `nltk/test/stem.doctest`
* `nltk/test/tag.doctest`
* `nltk/test/tokenize.doctest`
* `nltk/test/toolbox.doctest`
* `nltk/test/tree.doctest`
* `nltk/test/treetransforms.doctest`
* `nltk/test/unit/__init__.py`
* `nltk/test/unit/test_2x_compat.py`
* `nltk/test/unit/test_classify.py`
* `nltk/test/unit/test_collocations.py`
* `nltk/test/unit/test_corpora.py`
* `nltk/test/unit/test_corpus_views.py`
* `nltk/test/unit/test_hmm.py`
* `nltk/test/unit/test_naivebayes.py`
* `nltk/test/unit/test_seekable_unicode_stream_reader.py`
* `nltk/test/unit/test_stem.py`
* `nltk/test/unit/test_tag.py`
* `nltk/test/unit/utils.py`
* `nltk/test/util.doctest`
* `nltk/test/wordnet.doctest`
* `nltk/test/wordnet_fixt.py`
* `nltk/test/wordnet_lch.doctest`
* `nltk/test/wsd.doctest`
* `nltk/text.py`
* `nltk/tokenize/__init__.py`
* `nltk/tokenize/api.py`
* `nltk/tokenize/punkt.py`
* `nltk/tokenize/regexp.py`
* `nltk/tokenize/sexpr.py`
* `nltk/tokenize/simple.py`
* `nltk/tokenize/stanford.py`
* `nltk/tokenize/texttiling.py`
* `nltk/tokenize/treebank.py`
* `nltk/tokenize/util.py`
* `nltk/toolbox.py`
* `nltk/tree.py`
* `nltk/treetransforms.py`
* `nltk/util.py`
* `nltk/VERSION`
* `nltk/wsd.py`
* `nltk_data/corpora/stopwords/danish`
* `nltk_data/corpora/stopwords/dutch`
* `nltk_data/corpora/stopwords/english`
* `nltk_data/corpora/stopwords/finnish`
* `nltk_data/corpora/stopwords/french`
* `nltk_data/corpora/stopwords/german`
* `nltk_data/corpora/stopwords/hungarian`
* `nltk_data/corpora/stopwords/italian`
* `nltk_data/corpora/stopwords/norwegian`
* `nltk_data/corpora/stopwords/portuguese`
* `nltk_data/corpora/stopwords/README`
* `nltk_data/corpora/stopwords/russian`
* `nltk_data/corpora/stopwords/spanish`
* `nltk_data/corpora/stopwords/swedish`
* `nltk_data/corpora/stopwords/turkish`
* `nltk_data/corpora/stopwords.zip`
* `nltk_data/tokenizers/punkt/czech.pickle`
* `nltk_data/tokenizers/punkt/danish.pickle`
* `nltk_data/tokenizers/punkt/dutch.pickle`
* `nltk_data/tokenizers/punkt/english.pickle`
* `nltk_data/tokenizers/punkt/estonian.pickle`
* `nltk_data/tokenizers/punkt/finnish.pickle`
* `nltk_data/tokenizers/punkt/french.pickle`
* `nltk_data/tokenizers/punkt/german.pickle`
* `nltk_data/tokenizers/punkt/greek.pickle`
* `nltk_data/tokenizers/punkt/italian.pickle`
* `nltk_data/tokenizers/punkt/norwegian.pickle`
* `nltk_data/tokenizers/punkt/polish.pickle`
* `nltk_data/tokenizers/punkt/portuguese.pickle`
* `nltk_data/tokenizers/punkt/PY3/czech.pickle`
* `nltk_data/tokenizers/punkt/PY3/danish.pickle`
* `nltk_data/tokenizers/punkt/PY3/dutch.pickle`
* `nltk_data/tokenizers/punkt/PY3/english.pickle`
* `nltk_data/tokenizers/punkt/PY3/estonian.pickle`
* `nltk_data/tokenizers/punkt/PY3/finnish.pickle`
* `nltk_data/tokenizers/punkt/PY3/french.pickle`
* `nltk_data/tokenizers/punkt/PY3/german.pickle`
* `nltk_data/tokenizers/punkt/PY3/greek.pickle`
* `nltk_data/tokenizers/punkt/PY3/italian.pickle`
* `nltk_data/tokenizers/punkt/PY3/norwegian.pickle`
* `nltk_data/tokenizers/punkt/PY3/polish.pickle`
* `nltk_data/tokenizers/punkt/PY3/portuguese.pickle`
* `nltk_data/tokenizers/punkt/PY3/README`
* `nltk_data/tokenizers/punkt/PY3/slovene.pickle`
* `nltk_data/tokenizers/punkt/PY3/spanish.pickle`
* `nltk_data/tokenizers/punkt/PY3/swedish.pickle`
* `nltk_data/tokenizers/punkt/PY3/turkish.pickle`
* `nltk_data/tokenizers/punkt/README`
* `nltk_data/tokenizers/punkt/slovene.pickle`
* `nltk_data/tokenizers/punkt/spanish.pickle`
* `nltk_data/tokenizers/punkt/swedish.pickle`
* `nltk_data/tokenizers/punkt/turkish.pickle`
* `nltk_data/tokenizers/punkt.zip`
* `parsing.py`
* `README.md`
* `results.py`
* `results_test.py`
* `sample_data/sample_output.json`
* `sample_data/sample_output.xml`
* `sample_data/sample_output_formatted.json`
* `sample_data/sample_output_formatted.xml`
* `vector_model.py`
* `vector_model_test.py`
