import re
from collections import Counter, defaultdict

# Global variables for dynamic learning and context tracking
conversation_history = []  # Stores the history of interactions
sentiment_dict = {"happy": 1, "sad": -1, "great": 2, "terrible": -2}  # Dynamic sentiment dictionary
entity_memory = defaultdict(int)  # Tracks entities and their frequencies
entity_relationships = defaultdict(set)  # Tracks relationships between entities
classification_labels = defaultdict(list)  # Stores user-provided labels for text classification
word_cooccurrence = defaultdict(Counter)  # Tracks word co-occurrence statistics
patterns = defaultdict(int)  # Tracks recognized patterns in user inputs

# 1. Text Preprocessing
def tokenize(text):
    """Split text into words."""
    return re.findall(r'\b\w+\b', text)

def remove_stopwords(tokens, stopwords=None):
    """Remove common stopwords from tokens."""
    if stopwords is None:
        stopwords = {"the", "and", "is", "in", "on", "at", "of", "a", "an"}
    return [word for word in tokens if word.lower() not in stopwords]

def stem(word):
    """Simplistic stemming function."""
    if word.endswith("ing"):
        return word[:-3]
    elif word.endswith("ed"):
        return word[:-2]
    return word

def stem_tokens(tokens):
    """Apply stemming to a list of tokens."""
    return [stem(word) for word in tokens]

# 2. Syntax and Grammar
def pos_tag(word):
    """Basic part-of-speech tagging based on word endings."""
    if word.endswith("ly"):
        return "ADV"
    elif word.endswith("ing"):
        return "VERB"
    elif word.endswith("ed"):
        return "VERB"
    return "NOUN"

def tag_tokens(tokens):
    """Tag tokens with part-of-speech labels."""
    return [(word, pos_tag(word)) for word in tokens]

def dependency_parse(tokens):
    """Simplistic dependency parsing based on token positions."""
    return [(tokens[i], "depends on", tokens[i - 1]) for i in range(1, len(tokens))]

# 3. Semantic Analysis
def word_similarity(word1, word2):
    """Basic word similarity based on shared characters."""
    return len(set(word1) & set(word2)) / max(len(word1), len(word2))

def update_word_cooccurrence(tokens):
    """Update word co-occurrence matrix based on tokens."""
    for i, word in enumerate(tokens):
        for related_word in tokens[max(0, i - 1):i + 2]:
            if word != related_word:
                word_cooccurrence[word][related_word] += 1

def find_synonyms(word):
    """Find potential synonyms based on co-occurrence patterns."""
    if word in word_cooccurrence:
        return [related_word for related_word, count in word_cooccurrence[word].most_common(3)]
    return []

# 4. Pattern Recognition
def recognize_patterns(text):
    """Identify and track recurring patterns in user inputs."""
    tokens = tokenize(text)
    for i in range(len(tokens) - 1):
        pattern = f"{tokens[i]} {tokens[i + 1]}"
        patterns[pattern] += 1

def get_common_patterns():
    """Retrieve the most common patterns."""
    return sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:5]

# 5. Named Entity Recognition (NER)
def extract_entities(text):
    """Extract capitalized words as potential entities."""
    entities = re.findall(r'\b[A-Z][a-z]*\b', text)
    for entity in entities:
        entity_memory[entity] += 1  # Update entity memory dynamically
    return entities

def classify_entities(entities):
    """Classify entities into categories."""
    categories = {"Person": ["John", "Mary"], "Location": ["Paris", "London"], "Organization": ["Google", "Microsoft"]}
    classified = {}
    for entity in entities:
        for category, examples in categories.items():
            if entity in examples:
                classified[entity] = category
    return classified

def update_entity_relationships(entities):
    """Track relationships between entities based on proximity."""
    for i, entity in enumerate(entities):
        for related_entity in entities[max(0, i - 1):i + 2]:
            if entity != related_entity:
                entity_relationships[entity].add(related_entity)

# 6. Sentiment Analysis
def sentiment_analysis(tokens):
    """Basic sentiment analysis using dynamic sentiment dictionary."""
    return sum(sentiment_dict.get(word.lower(), 0) for word in tokens)

def update_sentiment_dict(word, score):
    """Update the sentiment dictionary dynamically."""
    sentiment_dict[word.lower()] = score

def contextual_sentiment_analysis(text):
    """Analyze sentiment with context (e.g., handling negations)."""
    tokens = tokenize(text)
    score = 0
    negation = False
    for word in tokens:
        if word.lower() in {"not", "no"}:
            negation = True
        elif word.lower() in sentiment_dict:
            sentiment = sentiment_dict[word.lower()]
            score += -sentiment if negation else sentiment
            negation = False
    return score

# 7. Text Summarization
def summarize(text):
    """Summarize text by extracting the most frequent words."""
    tokens = tokenize(text)
    word_counts = Counter(tokens)
    return [word for word, _ in word_counts.most_common(5)]

# 8. Dialogue and Context Handling
def add_to_history(text):
    """Add user input to conversation history."""
    conversation_history.append(text)

def resolve_coreference(pronoun):
    """Resolve pronouns to their antecedents using conversation history."""
    pronoun_map = {"he": "John", "she": "Mary", "it": "object"}
    return pronoun_map.get(pronoun.lower(), "unknown")

# 9. Advanced NLP Tasks
def classify_text(text):
    """Classify text into predefined categories."""
    categories = {"sports": ["game", "team", "score"], "politics": ["vote", "election", "policy"]}
    tokens = tokenize(text)
    scores = {category: sum(tokens.count(word) for word in keywords) for category, keywords in categories.items()}
    return max(scores, key=scores.get)

def refine_classification(text, label):
    """Allow users to refine classification by providing labels."""
    classification_labels[label].append(text)

def topic_modeling(text):
    """Identify topics based on word frequency."""
    tokens = tokenize(text)
    word_counts = Counter(tokens)
    return word_counts.most_common(3)

def generate_response(text):
    """Generate a simple response based on input text."""
    if "hello" in text.lower():
        return "Hi there! How can I help you?"
    elif "bye" in text.lower():
        return "Goodbye! Have a great day!"
    return "I'm here to assist you."

# Example Usage
if __name__ == "__main__":
    print("Welcome to the NLP system! Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        # Add input to conversation history
        add_to_history(user_input)

        # Tokenize and preprocess
        tokens = tokenize(user_input)
        filtered_tokens = remove_stopwords(tokens)
        stemmed_tokens = stem_tokens(filtered_tokens)

        # Perform NLP tasks
        entities = extract_entities(user_input)
        classified_entities = classify_entities(entities)
        update_entity_relationships(entities)
        update_word_cooccurrence(tokens)
        recognize_patterns(user_input)
        sentiment = contextual_sentiment_analysis(user_input)
        summary = summarize(user_input)
        classification = classify_text(user_input)
        topics = topic_modeling(user_input)
        response = generate_response(user_input)

        # Display results
        print("Tokens:", tokens)
        print("Filtered Tokens:", filtered_tokens)
        print("Stemmed Tokens:", stemmed_tokens)
        print("Entities:", entities)
        print("Classified Entities:", classified_entities)
        print("Entity Relationships:", dict(entity_relationships))
        print("Word Co-occurrence:", dict(word_cooccurrence))
        print("Recognized Patterns:", get_common_patterns())
        print("Sentiment Score:", sentiment)
        print("Summary:", summary)
        print("Classification:", classification)
        print("Topics:", topics)
        print("Response:", response)

        # Example of dynamic learning
        print("Dynamic Learning: Add a sentiment word (type 'word score') or refine classification (type 'label text') or press Enter to continue.")
        user_update = input("Update sentiment dictionary or classification: ")
        if user_update:
            try:
                if " " in user_update:
                    parts = user_update.split(" ", 1)
                    if len(parts) == 2:
                        if parts[0].isdigit():
                            word, score = parts
                            update_sentiment_dict(word, int(score))
                            print(f"Updated sentiment dictionary: {word} -> {score}")
                        else:
                            label, text = parts
                            refine_classification(text, label)
                            print(f"Refined classification: {text} -> {label}")
                    else:
                        print("Invalid format. Use 'word score' or 'label text'.")
                else:
                    print("Invalid format. Use 'word score' or 'label text'.")
            except ValueError:
                print("Invalid format. Use 'word score' or 'label text'.")