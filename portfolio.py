import pandas as pd
import chromadb
import uuid
import json  # Import JSON for safe conversion of complex data types

class Portfolio:
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)
        self.chroma_client = chromadb.PersistentClient(path="vectorstore")  # Fixed PersistentClient syntax
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    def load_portfolio(self):
        if self.collection.count() == 0:  # Explicit check instead of 'not'
            for _, row in self.data.iterrows():
                document_text = json.dumps(row["Techstack"]) if isinstance(row["Techstack"], dict) else str(row["Techstack"])
                metadata = {"links": row["Links"]}

                self.collection.add(
                    documents=[document_text],  # Ensure document is a string
                    metadatas=[metadata],  # Metadata should be a list of dictionaries
                    ids=[str(uuid.uuid4())]
                )

    def query_links(self, skills):
        skills_text = json.dumps(skills) if isinstance(skills, dict) else str(skills)

        result = self.collection.query(query_texts=[skills_text], n_results=2)
        return result.get("metadatas", [])
