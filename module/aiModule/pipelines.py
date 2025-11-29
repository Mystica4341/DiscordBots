import os
from haystack import Pipeline
import requests
from haystack.dataclasses import ChatMessage
from urllib.parse import urlparse, unquote

# Train Pipeline
from haystack.components.converters import PyPDFToDocument, DOCXToDocument
from haystack.components.joiners import DocumentJoiner 
from haystack.components.routers import FileTypeRouter
from haystack.components.preprocessors import DocumentCleaner
from haystack.components.preprocessors import DocumentSplitter
from haystack.components.writers import DocumentWriter

#import local modules
from module.aiModule.documentStore import documentStore, CreateCollection
from module.aiModule.generator import generator
from module.aiModule.retrievers import retriever
from module.aiModule.embedder import embedderDoc, embedderText
from module.aiModule.promptBuilder import prompt_builder, template
from module.aiModule.webSearch import web_search, link_content, html_converter
from module.aiModule.fallbackRetrivers import FallbackRetriever

"""
Train Pipeline
"""
TrainPipeline = Pipeline()

def trainPipeline():
    try:
      TrainPipeline.add_component("file_router", FileTypeRouter(mime_types=["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]))
      TrainPipeline.add_component("pdfconverter", PyPDFToDocument())
      TrainPipeline.add_component("docxconverter", DOCXToDocument())
      TrainPipeline.add_component("joiner", DocumentJoiner())
      TrainPipeline.add_component("cleaner", DocumentCleaner(remove_empty_lines=True, remove_extra_whitespaces=True))
      TrainPipeline.add_component("splitter", DocumentSplitter(split_by="word", split_length=500, split_overlap=10))
      TrainPipeline.add_component("embedder", embedderDoc())
      TrainPipeline.add_component("writer", DocumentWriter(documentStore()))
    except Exception as e:
      pass
    
    TrainPipeline.connect("file_router.application/pdf", "pdfconverter")
    TrainPipeline.connect("file_router.application/vnd.openxmlformats-officedocument.wordprocessingml.document", "docxconverter")
    TrainPipeline.connect("pdfconverter", "joiner")
    TrainPipeline.connect("docxconverter", "joiner")
    TrainPipeline.connect("joiner", "cleaner")
    TrainPipeline.connect("cleaner", "splitter")
    TrainPipeline.connect("splitter", "embedder")
    TrainPipeline.connect("embedder", "writer")

    return TrainPipeline

"""
QNA Pipeline
"""
QNAPipeline = Pipeline()

def qnaPipeline():
    try:
        QNAPipeline.add_component("text_embedder", embedderText())
        QNAPipeline.add_component("retriever", retriever())
        QNAPipeline.add_component("fallback", FallbackRetriever(web_search=web_search, fetcher=link_content, converter=html_converter))
        QNAPipeline.add_component("prompt_builder", prompt_builder)
        QNAPipeline.add_component("llm", generator)
    except Exception as e:
      pass

    QNAPipeline.connect("text_embedder","retriever.query_embedding")
    QNAPipeline.connect("retriever.documents","fallback.retriever_docs")
    QNAPipeline.connect("fallback.documents","prompt_builder.documents")
    QNAPipeline.connect("prompt_builder.prompt", "llm.messages")

    return QNAPipeline


"""
Function to export
"""
    
def write_docs(file_url):

    """
    Endpoint to upload a DOCX or PDF file and write its content to the vector database.
    """
    CreateCollection()
    response = requests.get(file_url, stream=True)
    file_content = response.content
    # Check file type
    
    # Phân tích URL
    parsed_url = urlparse(file_url)
    
    # Lấy phần đường dẫn và giải mã (unquote) nếu có ký tự đặc biệt
    # Phần này tự động loại bỏ mọi thứ sau dấu '?'
    path = unquote(parsed_url.path)

    file_name = os.path.basename(path)
    print(f"File name: {file_name}, {file_url}")
    with open(file_name, "wb") as temp_file:
        temp_file.write(file_content)
    # Read file content

    # Embed and write documents to the vector database
    try:
        trainPipeline().run({"file_router": {"sources": [file_name]}})
    except Exception as e:
        return f"Error during pipeline run: {e}"
    finally:
        os.remove(file_name)
    return { "answer": f"Tao đã thêm thành công **{file_url}** vào cơ sở dữ liệu." }
  
messages = [template]

def chat(question):
    """
    Endpoint to handle chat messages and generate responses based on the context.
    """
    
    # Create Qdrant collection if it doesn't exist
    CreateCollection()

    # Warm up the pipeline
    qnaPipeline().warm_up()
    
    messages.append(ChatMessage.from_user(question))

    try:
        # Run the query pipeline with the chat history
        response = qnaPipeline().run({
            "text_embedder": {"text": question},
            "fallback": {"query": question},
            "prompt_builder": {
                "question": question,
                "template": messages
            }, 
        })

        # Check if the response contains replies
        if "llm" in response and "replies" in response["llm"] and response["llm"]["replies"]:
            aiResponse = response["llm"]["replies"][0]
    except Exception as e:
        print(f"Error: {e}")
        aiResponse = f"{e}"
        
    # Append the AI response to the chat history
    messages.append(ChatMessage.from_assistant(aiResponse.text))

    return {
        "answer": aiResponse.text,
        "source": aiResponse.meta.get("source", "No source available"),
        "url": aiResponse.meta.get("url", "No URL available")
    }