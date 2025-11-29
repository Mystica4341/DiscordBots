from haystack import component
from haystack.dataclasses import Document
from typing import List

@component
class FallbackRetriever:
    def __init__(self, web_search, fetcher, converter):
        self.web_search = web_search
        self.fetcher = fetcher
        self.converter = converter

    @component.output_types(documents=List[Document])
    def run(self, query: str, retriever_docs: List[Document]):
        # Nếu retriever tìm thấy tài liệu → dùng luôn
        if retriever_docs and len(retriever_docs) > 0:
            return {"documents": retriever_docs}

        # Nếu không có → fallback web search
        print("⚠️ Không tìm thấy tài liệu trong Qdrant → sử dụng Web Search")

        try:
            # links = self.web_search.run(query=query)["links"]
            # streams = self.fetcher.run(urls=links)["streams"]
            # docs = self.converter.run(sources=streams)["documents"]
            # 1) SEARCH
            search_output = self.web_search.run(query=query)
            results = search_output.get("results", [])

            # Lấy danh sách link
            links = [item.get("link") for item in results if "link" in item]

            if not links:
                print("⚠️ Web search không trả về link nào")
                return {"documents": retriever_docs}

            # 2) FETCH HTML
            streams = self.fetcher.run(urls=links)["streams"]

            # 3) CONVERT HTML → DOCUMENTS
            docs = self.converter.run(sources=streams)["documents"]

            return {"documents": docs}

        except Exception as e:
            print(f"Fallback Error: {e}")
            return {"documents": retriever_docs}