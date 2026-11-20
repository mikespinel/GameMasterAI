import os

from datapizza.clients.openai import (
    OpenAIClient,
)
from dotenv import load_dotenv

from agents.gamemaster_agent import (
    create_gamemaster_agent,
)

load_dotenv()

client = OpenAIClient(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    ),
    model="gpt-4o-mini",
)

agent = create_gamemaster_agent(
    client
)

print()
print("🎲 GameMaster AI")
print("Scrivi exit per uscire")
print()

while True:

    question = input("> ")

    if question.lower() == "exit":
        break

    response = agent.run(
        question
    )

    print()
    print(response.text)
    print()