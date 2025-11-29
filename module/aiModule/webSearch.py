from haystack.utils import Secret
import os
from haystack.components.websearch import SearchApiWebSearch
from haystack.components.fetchers import LinkContentFetcher
from haystack.components.converters import HTMLToDocument
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
WEB_SEARCH_API_KEY = os.getenv('WEB_SEARCH_API_KEY')

web_search = SearchApiWebSearch(api_key=Secret.from_token(WEB_SEARCH_API_KEY), top_k=2)
link_content = LinkContentFetcher()
html_converter = HTMLToDocument()