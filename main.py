import random

BOT_NAME = "MiniBot"
COMMANDS = {"/history", "/last", "/stats", "/quit"}
GREETINGS = ("hello", "hi", "γεια")
ROLES = ("user", "assistant")

Message = dict[str, str]  # type alias: {"role": ..., "content": ...}


def say(*lines: str) -> None:
    """Print one or more lines as the bot."""
    for line in lines:
        print(f"{BOT_NAME}> {line}")


def fake_llm(prompt: str, *, temperature: float = 0.0) -> str:
    """Rule-based stand-in for a real LLM call."""
    if prompt.endswith("?"):
        if random.random() < temperature:  # higher temperature = more "creative"
            return "Hmm, let me think... maybe 41?"
        return f"Good question ({len(prompt)} chars). I'm a fake LLM, so: 42."
    if prompt.lower() in GREETINGS:
        return "Hello! Ask me something."
    return f"You said '{prompt}'. Tell me more."


def ask(history: list[Message], prompt: str, **llm_options: float) -> str:
    """Record the prompt, get a reply from the LLM, record the reply."""
    history.append({"role": "user", "content": prompt})
    reply = fake_llm(prompt, **llm_options)  # forward options as named args
    history.append({"role": "assistant", "content": reply})
    return reply


def count_by_role(history: list[Message], roles: tuple[str, ...] = ROLES) -> dict[str, int]:
    return {role: len([m for m in history if m["role"] == role]) for role in roles}


def last_question(history: list[Message]) -> str | None:
    questions = [
        m["content"]
        for m in history
        if m["role"] == "user" and m["content"].endswith("?")
    ]
    return questions[-1] if questions else None


def handle_command(command: str, history: list[Message]) -> bool:
    """Run a slash command. Return False when the chat should end."""
    if command not in COMMANDS:
        say(f"Unknown command. Try: {', '.join(sorted(COMMANDS))}")
    elif command == "/quit":
        say(f"Bye! We talked for {count_by_role(history)['user']} turns.")
        return False
    elif command == "/history":
        if not history:
            say("No messages yet.")
        for i, message in enumerate(history, start=1):
            print(f"  {i}. {message['role']}: {message['content']}")
    elif command == "/last":
        question = last_question(history)
        if question is None:
            say("You haven't asked anything yet.")
        else:
            say(f"Your last question was: '{question}'")
    elif command == "/stats":
        user_text = " ".join([m["content"] for m in history if m["role"] == "user"])
        say(
            f"Messages per role: {count_by_role(history)}",
            f"Unique words you used: {len(set(user_text.lower().split()))}",
        )
    return True


def main() -> None:
    say(f"Ready. Commands: {', '.join(sorted(COMMANDS))}")
    history: list[Message] = []

    while True:
        text = input("you> ").strip()

        if not text:
            say("I'm listening...")
            continue

        if text.startswith("/"):
            if not handle_command(text, history):
                break
            continue

        reply = ask(history, text, temperature=0.3)
        say(f"[turn {len(history) // 2}] {reply}")


if __name__ == "__main__":
    main()