# DummyBench Paper Summary

## Benchmark Documentation

DummyBench is a synthetic benchmark created for pipeline testing. It covers
task categories relevant to English-language edtech contexts [Q1], uses
datapoints drawn from US undergraduate materials [Q2], encodes inputs as UTF-8
text at roughly 1000 words per item [Q3], labels outputs with a 5-way
categorical taxonomy [Q4], with ground-truth labels produced by US-based
annotators [Q5], and returns a single categorical label per instance [Q6].

## Verbatim Quote Registry

| ID | Page | Dimension | Text |
|----|------|-----------|------|
| Q1 | 1 | input_ontology | "The task taxonomy covers five categories common in US edtech." |
| Q2 | 1 | input_content | "All prompts are drawn from US undergraduate coursework." |
| Q3 | 1 | input_form | "Inputs are UTF-8 text averaging ~1000 words per item." |
| Q4 | 2 | output_ontology | "Outputs use a 5-way categorical label set." |
| Q5 | 2 | output_content | "Ground-truth labels were assigned by annotators based in the United States." |
| Q6 | 2 | output_form | "Each item returns a single categorical label." |
