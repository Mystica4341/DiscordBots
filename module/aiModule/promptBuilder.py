from haystack.components.builders import ChatPromptBuilder
from haystack.dataclasses import ChatMessage

#initialize prompt template
template = ChatMessage.from_system("""
Using the information contained in the context provide a comprehensive and moderate answer for the Question.
translate the answer to the language specified in the question.
When translating, **do not translate proper nouns**.
If the question is not in the context, search for relevant information externally and provide it.
If the question is about analysis, provide a detailed analysis and recommendation based on the context. Finally, please suggest a better solution if possible.
For coding-related, use this format: `text`, and include code snippets as needed.
For confidential or sensitive data, use this format: ||text||, and do not disclose any confidential information in the answer.

Context:
{% for document in documents %}
    {{ document.content }}
{% endfor %}

Question: {{question}}
Answer:
""")

# initialize the prompt builder
prompt_builder = ChatPromptBuilder(template=template, required_variables=["question"], variables=["documents", "question"])