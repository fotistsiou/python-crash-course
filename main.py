BOT_NAME = "MiniBot"
COMMANDS = {"/history", "/last", "/stats", "/quit"}  # set: unique items, fast "in"
GREETINGS = ("hello", "hi", "γεια")                  # tuple: fixed, never changes
ROLES = ("user", "assistant")


def main() -> None:
    print(f"{BOT_NAME} is ready. Commands: {', '.join(sorted(COMMANDS))}")

    history = []  # list of dicts: the shape LLM APIs expect

    while True:
        text = input("you> ").strip()

        if not text:
            print(f"{BOT_NAME}> I'm listening...")
            continue

        if text.startswith("/"):
            if text not in COMMANDS:
                print(f"{BOT_NAME}> Unknown command. Try: {', '.join(sorted(COMMANDS))}")
                continue

            if text == "/quit":
                turns = len([m for m in history if m["role"] == "user"])
                print(f"{BOT_NAME}> Bye! We talked for {turns} turns.")
                break

            if text == "/history":
                if not history:
                    print(f"{BOT_NAME}> No messages yet.")
                for i, message in enumerate(history, start=1):  # (index, item) tuples
                    print(f"  {i}. {message['role']}: {message['content']}")
                continue

            if text == "/last":
                questions = [
                    m["content"]
                    for m in history
                    if m["role"] == "user" and m["content"].endswith("?")
                ]
                if questions:
                    print(f"{BOT_NAME}> Your last question was: '{questions[-1]}'")
                else:
                    print(f"{BOT_NAME}> You haven't asked anything yet.")
                continue

            if text == "/stats":
                counts = {role: len([m for m in history if m["role"] == role]) for role in ROLES}
                user_text = " ".join([m["content"] for m in history if m["role"] == "user"])
                unique_words = set(user_text.lower().split())
                print(f"{BOT_NAME}> Messages per role: {counts}")
                print(f"{BOT_NAME}> Unique words you used: {len(unique_words)}")
                continue

        history.append({"role": "user", "content": text})

        if text.endswith("?"):
            reply = f"Good question ({len(text)} chars). I'm a fake LLM, so: 42."
        elif text.lower() in GREETINGS:
            reply = "Hello! Ask me something."
        else:
            reply = f"You said '{text}'. Tell me more."

        history.append({"role": "assistant", "content": reply})
        turn = len(history) // 2  # each turn = 1 user + 1 assistant message
        print(f"{BOT_NAME}> [turn {turn}] {reply}")


if __name__ == "__main__":
    main()