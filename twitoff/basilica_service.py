import basilica
import os
from dotenv import load_dotenv

load_dotenv()

BASILICA_API_KEY = os.getenv("BASILICA_API_KEY", default="OOPS")

def basilica_connection():
    connection = basilica.Connection(BASILICA_API_KEY)
    print(connection)
    return connection

if __name__ == "__main__":
    sentences = [
        "This is a sentence!",
        "This is a similar sentence!",
        "I don't think this sentence is very similar at all...",
    ]

    with basilica.Connection(BASILICA_API_KEY) as c:
        embeddings = list(c.embed_sentences(sentences))

    print(embeddings)