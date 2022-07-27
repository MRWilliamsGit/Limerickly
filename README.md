[![Limerickly Test](https://github.com/MRWilliamsGit/Limerickly/actions/workflows/main.yml/badge.svg)](https://github.com/MRWilliamsGit/Limerickly/actions/workflows/main.yml)

# Limerickly
*Build a limerick with an AI poet*

### AIPI 561 | Summer 2022 | Maria Williams & Miranda Morris


## Background
A limerick is a five-line poem that is often playful, humorous, or nonsensical, using an AABBA rhyme scheme.
### Example:
<img src="https://www.rd.com/wp-content/uploads/2021/04/limerick5.jpg" width="350">


## Data
This app uses the [Datamuse API](https://www.datamuse.com/api/) to find rhymes. No other datasources are used.
Datamuse is a word-finding query engine that can be used to find words that are likely within the given context and match with the given constraints. Examples of uses include autocomplete, relevancy ranking in searches, assistive writing applications, and word games.

<img src="https://www.datamuse.com/api/datamuse-logo-rgb.png" width="150">


## Modeling
This app uses a pretrained BERT model to generate rhyming lines. 

For each new line:
* The script creates a "line" of empty masks and a final rhyming word.
* BERT predicts what words should fill the empty spaces. 
* Since all the new words are generated at the same time, they do not relate to each other and will probably not make sense as a sentence. Only the first and last new words, which have the previous line and the end of the line for context, are retained.
* The prediction is run again with the two new words until all spaces are filled by words generated with context.

## Continuous Integration and Delivery
This app is continuousy controlled by an automatic system that first vetts any script changes for formatting and scripting errors, and then automatically updates the app with approved changes. Changes are first checked by a test script run by Github Actions, and only code changes that pass the tests are committed to the public repository and reflected in the app. Once changes are committed, the Streamlit app automatically rebuilds itself.

## Deployment
Access app here: [Limerickly App](https://mrwilliamsgit-limerickly-main-fqmats.streamlitapp.com/)
