import os

from datapizza.clients.openai import OpenAIClient
from dotenv import load_dotenv

from agents.recommendation_agent import (
    create_recommendation_agent,
)


load_dotenv()

client = OpenAIClient(
    api_key=os.getenv("OPENAI_API_KEY"),
    model="gpt-4o-mini",
)

agent = create_recommendation_agent(client)

print()
print("🎲 GameMaster AI")
print("digitare exit per uscire")
print()

while True:

    question = input("> ")

    if question.lower() == "exit":
        break

    response = agent.run(question)

    print()
    print(response.text)
    print()
