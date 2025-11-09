"""
Typesense client connector
Handles vector search operations
"""

import typesense
from config.settings import settings


class TypesenseConnector:
    """Typesense client for vector search"""

    def __init__(self):
        """Initialize Typesense client"""
        self.client = typesense.Client({
            "nodes": [{
                "host": settings.typesense_host,
                "port": settings.typesense_port,
                "protocol": settings.typesense_protocol,
            }],
            "api_key": settings.typesense_api_key,
            "connection_timeout_seconds": 5,
        })
        self.collection = settings.typesense_collection

    def vector_search(self, query_vector: list, k: int = 5, source_filter: str = None):
        """
        Perform vector similarity search

        Args:
            query_vector: Embedding vector as list of floats
            k: Number of results to return
            source_filter: Optional source document filter

        Returns:
            List of search results with documents and distances
        """
        vec_str = ",".join([str(x) for x in query_vector])

        search_params = {
            "collection": self.collection,
            "q": "*",
            "per_page": k,
            "vector_query": f"embedding:([{vec_str}], k:{k})"
        }

        # Add source filter if provided
        if source_filter:
            search_params["filter_by"] = f"source:={source_filter}"

        # Execute search
        result = self.client.multi_search.perform(
            {"searches": [search_params]},
            {}
        )

        return result["results"][0].get("hits", [])

    def health_check(self) -> bool:
        """Check if Typesense is healthy"""
        try:
            self.client.collections.retrieve()
            return True
        except Exception:
            return False


# Singleton instance
typesense_connector = TypesenseConnector()