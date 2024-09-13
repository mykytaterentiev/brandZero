from sentence_transformers import SentenceTransformer

# Load the pre-trained Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Function to generate an embedding
def generate_embedding(text):
    return model.encode(text).tolist()
