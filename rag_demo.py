from tools.rulebook_tool import (
    ask_rulebook
)
question = input(
    "Domanda: "
)

result = ask_rulebook(
    question
)
print()
print("RISPOSTA")
print()

print(
    result["answer"]
)
print()
print("FONTI")
print()

for s in result["sources"]:

    print("-", s)