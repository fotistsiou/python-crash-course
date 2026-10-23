BOT_NAME = "MiniBot"


def main() -> None:
    print(f"{BOT_NAME} is ready. Commands: /last, /quit")

    turn = 0
    last_question = None  # nothing asked yet

    while True:
        text = input("you> ").strip()

        if not text:  # "" is falsy: the user just pressed Enter
            print(f"{BOT_NAME}> I'm listening...")
            continue

        if text == "/quit":
            print(f"{BOT_NAME}> Bye! We talked for {turn} turns.")
            break

        if text == "/last":
            if last_question is None:
                print(f"{BOT_NAME}> You haven't asked anything yet.")
            else:
                print(f"{BOT_NAME}> Your last question was: '{last_question}'")
            continue

        turn += 1

        if text.endswith("?"):
            last_question = text
            reply = f"Good question ({len(text)} chars). I'm a fake LLM, so: 42."
        elif text.lower() == "hello":
            reply = "Hello! Ask me something."
        else:
            reply = f"You said '{text}'. Tell me more."

        print(f"{BOT_NAME}> [turn {turn}] {reply}")


if __name__ == "__main__":
    main()