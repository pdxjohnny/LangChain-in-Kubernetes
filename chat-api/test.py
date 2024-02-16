from langserve import RemoteRunnable
from langchain.prompts.chat import ChatPromptTemplate

openai_llm = RemoteRunnable("http://localhost:8000/openai_api")

question = ("Tell me about k8s")
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a highly educated person who loves to use big words. "
            + "You are also concise. Never answer in more than three sentences.",
        ),
        ("human", question),
    ]
).format_messages()
save=openai_llm.invoke(prompt)
print(save.content)