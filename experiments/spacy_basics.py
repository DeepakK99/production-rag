import spacy

nlp = spacy.load("en_core_web_sm")

queries = [
    "How do I make carrot halva?",
    "What ingredients are needed for Coriander Fish?",
    "Which recipe uses chicken?",
    "Give me the complete method for carrot halva.",
]

for text in queries:
    doc = nlp(text)
    print([t.pos_ for t in doc])
    terms = [
        token.lemma_.lower()
        for token in doc
        if not token.is_stop
        and not token.is_punct
        # and token.pos_ in ["NOUN", "PROPN", "ADJ"]
    ]

    print(f"{text}")
    print("→", " ".join(terms))
    print()

import spacy

nlp = spacy.load("en_core_web_sm")
for query in queries:
    doc = nlp(query)

    # Extract the base noun phrases directly
    extracted_keywords = []
    for chunk in doc.noun_chunks:
        # chunk.text will yield 'delicious carrot halva'
        # Splitting them gives you the individual terms safely
        extracted_keywords.extend([token.text for token in chunk])

    print(extracted_keywords) 
    # Output: ['delicious', 'carrot', 'halva']
