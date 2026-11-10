# Employee Sentiment Analysis · Evidence curation

Turn a validated summary into a reviewable narrative. In offline mode the largest absolute topic gap is selected. An optional local model may choose a topic from the supplied evidence IDs. Python fills in the actual counts, so the selection step cannot change a metric.

```sh
python curate.py propose
python curate.py approve --confirm-topic "Growth opportunities"
```

A draft records its evidence hash. Approval requires the matching topic, unchanged data and reproducible text. To try an installed Ollama model, add `--model MODEL_NAME` to the proposal command. That optional route sends the topic names and differences to the local Ollama endpoint. The included example is fictional. This public adaptation replaces enterprise prompts, provider settings and employee contact routes. [Related repositories](https://github.com/search?q=user%3AMRodriguez2010+topic%3Aemployee-sentiment-analysis&type=repositories)

## Historical source examples

The [archived public ratings](public-data/historical-ratings.csv) contain the company, platform, five-point rating and review count for 18 source observations. Run `python ratings-evidence.py` for a source-linked review queue. This five-point series is separate from the fictional favorable-share narrative example.
