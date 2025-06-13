from haystack_integrations.components.generators.google_ai import GoogleAIGeminiChatGenerator
import os
from haystack.utils import Secret
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# initialize the generator
generator = GoogleAIGeminiChatGenerator(model="gemini-2.0-flash", api_key=Secret.from_token(GEMINI_API_KEY))