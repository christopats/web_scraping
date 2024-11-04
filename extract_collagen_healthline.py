import pandas as pd
import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
import time

# Function to print debug messages with timestamp
def print_debug(message):
    print(f"DEBUG [{time.strftime('%Y-%m-%d %H:%M:%S')}]: {message}")

# Load the JSON data
print_debug("Loading JSON data...")
try:
    with open('articles.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print_debug("JSON data loaded successfully.")
except Exception as e:
    print(f"Error loading JSON data: {e}")
    exit()

# Convert JSON data to pandas DataFrame
print_debug("Converting JSON data to pandas DataFrame...")
try:
    df = pd.DataFrame(data)
    print_debug("DataFrame created successfully.")
except Exception as e:
    print(f"Error creating DataFrame: {e}")
    exit()

# Text Preprocessing
print_debug("Downloading NLTK stopwords and punkt tokenizer...")
nltk.download('stopwords')
nltk.download('punkt')
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    try:
        tokens = word_tokenize(text)
        tokens = [word.lower() for word in tokens if word.isalpha()]
        tokens = [word for word in tokens if word not in stop_words]
        return ' '.join(tokens)
    except Exception as e:
        print(f"Error in preprocessing text: {e}")
        return ""

print_debug("Preprocessing text data...")
try:
    df['cleaned_body'] = df['bodyText'].apply(preprocess_text)
    print_debug("Text data preprocessed successfully.")
except Exception as e:
    print(f"Error preprocessing text data: {e}")
    exit()

# Extract sentences containing specific keywords
keywords_benefits = ['benefit', 'improve', 'increase', 'support', 'help']
keywords_implications = ['lack', 'deficiency', 'reduce', 'decrease', 'loss']
keywords_products = ['product', 'supplement', 'brand', 'capsule', 'powder']

def extract_sentences(text, keywords):
    try:
        sentences = sent_tokenize(text)
        relevant_sentences = [sentence for sentence in sentences if any(keyword in sentence for keyword in keywords)]
        return relevant_sentences
    except Exception as e:
        print(f"Error in extracting sentences: {e}")
        return []

print_debug("Extracting sentences with specific keywords...")
try:
    df['benefit_sentences'] = df['bodyText'].apply(lambda text: extract_sentences(text, keywords_benefits))
    df['implication_sentences'] = df['bodyText'].apply(lambda text: extract_sentences(text, keywords_implications))
    df['product_sentences'] = df['bodyText'].apply(lambda text: extract_sentences(text, keywords_products))
    print_debug("Sentences extracted successfully.")
except Exception as e:
    print(f"Error extracting sentences: {e}")
    exit()

# Combine all sentences for each category
print_debug("Combining sentences for each category...")
try:
    all_benefit_sentences = ' '.join([' '.join(sentences) for sentences in df['benefit_sentences']])
    all_implication_sentences = ' '.join([' '.join(sentences) for sentences in df['implication_sentences']])
    all_product_sentences = ' '.join([' '.join(sentences) for sentences in df['product_sentences']])
    print_debug("Sentences combined successfully.")
except Exception as e:
    print(f"Error combining sentences: {e}")
    exit()

print(f"Benefit Sentences: {all_benefit_sentences}")
print(f"Implication Sentences: {all_implication_sentences}")
print(f"Product Sentences: {all_product_sentences}")

# Create word clouds for visualization
# def create_wordcloud(text, title):
#     print_debug(f"Creating word cloud for {title}...")
#     try:
#         start_time = time.time()
#         wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
#         elapsed_time = time.time() - start_time
#         print_debug(f"Word cloud for {title} generated in {elapsed_time:.2f} seconds.")
        
#         plt.figure(figsize=(10, 5))
#         plt.imshow(wordcloud, interpolation='bilinear')
#         plt.title(title)
#         plt.axis('off')
#         plt.show()
#         print_debug(f"Word cloud for {title} created successfully.")
#     except Exception as e:
#         print(f"Error creating word cloud for {title}: {e}")

# print_debug("Creating word clouds for visualization...")
# create_wordcloud(all_benefit_sentences, 'Most Commonly Mentioned Benefits')
# create_wordcloud(all_implication_sentences, 'Implications of Lack of Collagen')
# create_wordcloud(all_product_sentences, 'Products Available')

# # Frequency Analysis
# def get_most_common_phrases(sentences, num_phrases=20):
#     try:
#         tokens = word_tokenize(sentences)
#         tokens = [token for token in tokens if token.isalpha() and token not in stop_words]
#         phrases = Counter(tokens).most_common(num_phrases)
#         return phrases
#     except Exception as e:
#         print(f"Error in frequency analysis: {e}")
#         return []

# print_debug("Performing frequency analysis on benefits...")
# benefits_phrases = get_most_common_phrases(all_benefit_sentences)
# print("Most Common Benefits:")
# print(benefits_phrases)

# print_debug("Performing frequency analysis on implications...")
# implications_phrases = get_most_common_phrases(all_implication_sentences)
# print("Most Common Implications of Lack of Collagen:")
# print(implications_phrases)

# print_debug("Performing frequency analysis on products...")
# products_phrases = get_most_common_phrases(all_product_sentences)
# print("Most Common Products Mentioned:")
# print(products_phrases)

# print_debug("Script execution completed.")

# # Additional TextBlob and TF-IDF analysis (if any) can be added below with similar debugging.
