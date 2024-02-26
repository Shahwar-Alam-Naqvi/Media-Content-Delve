from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes.retriever.multimodal import MultiModalRetriever
import os
from haystack import Document
from haystack import Pipeline

class MultiModalSearch:
    def __init__(self):
        # we have to create embeddings (which are in lower dimensional space) for all the images.
        self.document_stores = InMemoryDocumentStore(embedding_dim=512) 
        document_directory = "qyrus_images" # max 35 K images in general
        images = [
            Document(content = f"{document_directory}/{filename}", content_type = "image")
            for filename in os.listdir(f"./{document_directory}")
        ]  
        
        self.document_stores.write_documents(images)
        
        self.retriever_text_to_image = MultiModalRetriever(
            document_store = self.document_stores,
            query_embedding_model = "sentence-transformers/clip-ViT-B-32",
            query_type = "text",
            document_embedding_models = {"image" : "sentence-transformers/clip-ViT-B-32"}
        )
        
        self.document_stores.update_embeddings(retriever = self.retriever_text_to_image)
        
        self.pipeline = Pipeline()
        
        self.pipeline.add_node(component = self.retriever_text_to_image,
                               name = "retriever_text_to_image",
                               inputs=["Query"])
        
    def search(self, query, top_k=3):
        results = self.pipeline.run(query=query, params = {"retriever_text_to_image": {"top_k": top_k}})
        return sorted(results["documents"], key=lambda d: d.score, reverse=True)
        