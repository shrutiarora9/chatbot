import chatbot_logic
import quiz_pnl

# GLOBAL STATE
session = {
    "awaiting_confirm": False,   # greeting yes/no mode
    "user_name": None
}

def reset_all_states():
    """Resets all modes to prevent stuck states."""
    session["awaiting_confirm"] = False
    quiz_pnl.tutor_mode = False
    quiz_pnl.tutor_quiz_type = None
    quiz_pnl.tutor_awaiting_reveal = False
    quiz_pnl.TUTOR_SCENARIOS["current"] = None


def main():
    print("\n Chatbot Activated \n")

    while True:
        user = input("You: ").strip()
        if not user:
            continue

        u_low = user.lower()
        # EXIT
        if u_low in ("exit", "quit"):
            print("Bot: Goodbye!")
            break

        # NAME DETECTION
        name = chatbot_logic.try_extract_name(user)
        if name:
            session["user_name"] = name
            print(f"Bot: Nice to meet you, {name}!")
            continue

        # YES/NO GREETING MODE
        if session["awaiting_confirm"]:
            if u_low in ("yes", "y", "sure", "ok", "okay"):
                topics = "\n".join(f"- {t}" for t in chatbot_logic.KNOWLEDGE_BASE.keys())
                print("Bot: Great! Here are the topics:\n" + topics)
                session["awaiting_confirm"] = False
                continue

            elif u_low in ("no", "n", "nah", "nope"):
                print("Bot: No problem! Ask anything.")
                session["awaiting_confirm"] = False
                continue

            else:
                print("Bot: Please answer yes or no.")
                continue

        # GREETING
        if any(g in u_low for g in ["hi", "hello", "hey", "good morning", "good evening"]):
            reset_all_states()
            print("Bot: Hey there! Ready to learn trading? (yes/no)")
            session["awaiting_confirm"] = True
            continue

        # TUTOR MODE ACTIVE
        if quiz_pnl.tutor_mode:
            resp = quiz_pnl.tutor_handle(user)
            print("Bot:", resp)
            continue

        # START TUTOR MODE
        if any(k in u_low for k in ["start tutor", "quiz", "tutor", "analysis test", "test me"]):
            reset_all_states()  # prevent mixing states
            print("Bot:", quiz_pnl.start_tutor())
            continue

        # PnL CALCULATOR
        if any(k in u_low for k in ["calculate pnl", "profit", "loss", "pnl calculator"]):
            reset_all_states()
            print("Bot:", quiz_pnl.calculate_pnl())
            continue

        # NORMAL KNOWLEDGE BASE MODE
        reset_all_states()   # ensure fresh state before kb lookup
        response = chatbot_logic.get_response(user)
        print("Bot:", response)


if __name__ == "__main__":
    main()
