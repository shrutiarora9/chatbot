import random  

tutor_mode = False
tutor_quiz_type = None
tutor_awaiting_reveal = False

TUTOR_SCENARIOS = {
    "CANDLESTICK": [
        {
            "prompt": "SCENARIO: BULLISH ENGULFING",
            "data_display": [
                {"Day": "Yesterday", "Open": 150.50, "Close": 149.80, "Color": "RED"},
                {"Day": "Today", "Open": 149.50, "Close": 152.00, "Color": "GREEN"}
            ],
            "question": "Name this two-day pattern and market implication?",
            "answer_keywords": ["bullish engulfing", "engulfing", "bullish reversal"],
            "correct_answer_name": "BULLISH ENGULFING PATTERN",
            "full_explanation": (
                "Bullish Engulfing = Large green candle covering previous red candle → bullish reversal."
            )
        }
    ],

    "INDICATOR": [
        {
            "prompt": "SCENARIO: MA CROSSOVER",
            "data_display": [
                {"MA_20": 105.00, "MA_50": 105.50},
                {"MA_20": 105.80, "MA_50": 105.30}
            ],
            "question": "What trading signal and action?",
            "answer_keywords": ["bullish", "buy signal", "golden cross", "crossover"],
            "correct_answer_name": "BULLISH CROSSOVER",
            "full_explanation": "20 MA crossing above 50 MA = Bullish crossover / buy signal."
        }
    ]
}

TUTOR_SCENARIOS["current"] = None

# PNL calculator
def calculate_pnl():
    print("\n PnL Calculator Initiated ")
    BROKERAGE_RATE = 0.001  

    try:
        buy_price = float(input("Enter Buying Price per share: ").strip())
        sell_price = float(input("Enter Selling Price per share: ").strip())
        quantity = int(input("Enter Quantity of shares: ").strip())

        if quantity <= 0:
            return "Quantity must be positive."

        gross_pnl = (sell_price - buy_price) * quantity
        buy_value = buy_price * quantity
        sell_value = sell_price * quantity
        brokerage_cost = (buy_value * BROKERAGE_RATE) + (sell_value * BROKERAGE_RATE)
        net_pnl = gross_pnl - brokerage_cost

        return (
            f"\n--- RESULTS ---\n"
            f"Gross PnL: ₹{gross_pnl:.2f}\n"
            f"Brokerage: ₹{brokerage_cost:.2f}\n"
            f"Net PnL: ₹{net_pnl:.2f}\n"
        )

    except ValueError:
        return "Invalid input. Please enter numbers only."

# Tutor mode
def start_tutor():
    global tutor_mode, tutor_quiz_type, tutor_awaiting_reveal
    tutor_mode = True
    tutor_quiz_type = None
    tutor_awaiting_reveal = False

    return (
        "\n Tutor Mode Started \n"
        "Choose:\n"
        "  1. Candlestick\n"
        "  2. Indicator\n"
        "Type 1 or 2"
    )


def start_quiz(type_key):
    global tutor_quiz_type
    tutor_quiz_type = type_key

    scenario = random.choice(TUTOR_SCENARIOS[type_key])
    TUTOR_SCENARIOS["current"] = scenario

    output = f"\n--- {scenario['prompt']} ---\n\nDATA:\n"

    for row in scenario["data_display"]:
        output += str(row) + "\n"

    output += f"\nQUESTION: {scenario['question']}"
    return output


def tutor_handle(user_input):
    global tutor_mode, tutor_quiz_type, tutor_awaiting_reveal

    u = user_input.lower().strip()

    # cancel
    if u in ("cancel", "stop", "exit"):
        tutor_mode = False
        tutor_quiz_type = None
        tutor_awaiting_reveal = False
        return "Tutor closed."

    # choose quiz type
    if tutor_quiz_type is None:
        if u in ("1", "candlestick"):
            return start_quiz("CANDLESTICK")
        if u in ("2", "indicator"):
            return start_quiz("INDICATOR")
        return "Choose 1 or 2."

    scenario = TUTOR_SCENARIOS["current"]

    # awaiting reveal
    if tutor_awaiting_reveal:
        if u == "yes":
            tutor_mode = False
            tutor_awaiting_reveal = False
            return (
                f"\nCorrect Answer: {scenario['correct_answer_name']}\n\n"
                f"{scenario['full_explanation']}"
            )
        if u == "no":
            tutor_awaiting_reveal = False
            return start_quiz(tutor_quiz_type)
        return "Type yes or no."

    # check answer
    if any(kw in u for kw in scenario["answer_keywords"]):
        tutor_mode = False
        tutor_quiz_type = None
        return "Correct! Well done."

    tutor_awaiting_reveal = True
    return "Incorrect. Want to see the right answer? (yes/no)"
