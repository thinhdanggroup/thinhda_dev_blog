from transformers import pipeline

nlp = pipeline("sentiment-analysis")
result = nlp("I love this product!")[0]

print(f"label: {result['label']}, with score: {round(result['score'], 4)}")