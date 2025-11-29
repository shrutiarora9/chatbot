import difflib
import random
from datetime import datetime

# Dialogue states
STATE_IDLE = "IDLE"
STATE_AWAIT_CONFIRM = "AWAIT_CONFIRMATION"

AFFIRMATIVE = {"yes", "y", "yeah", "yep", "sure", "ok", "okay", "please", "ya", "yea"}
NEGATIVE = {"no", "n", "nope", "nah"}

NAME_PATTERNS = [
    "my name is",
    "i am",
    "call me",
    "mera naam",
    "naam",
]


def try_extract_name(text):
    t = text.lower()
    for phrase in NAME_PATTERNS:
        if phrase in t:
            idx = t.find(phrase)
            extracted = text[idx + len(phrase):].strip()
            if not extracted:
                return None
            return extracted.split()[0].strip(".,!?").capitalize()
    return None

# KNOWLEDGE BASE 
KNOWLEDGE_BASE = {

    "paper trading": {
        "keywords": [
            "paper trading", "virtual trading", "demo trading", "practice trading",
            "paper trade", "mock trading", "practice stock market", "paper account"
        ],
        "answer": "Paper trading is a simulation based trading method where you can practice buying and selling without using real money. It helps beginners understand charts, order placement, and market behavior in a risk free environment. Since trades follow real market prices, it feels similar to live trading but without financial pressure. You can test intraday trading, swing trading, or strategies based on indicators and patterns. Paper trading builds confidence and discipline, but it also has limitations. Emotional reactions like fear and greed do not appear strongly because no money is at risk. Some platforms also do not simulate slippage or partial fills. To learn properly, treat paper trading seriously, use stop loss, journal trades, and review performance regularly.",
        "videos": [
            "https://youtu.be/kaofQlooJug?si=G1x3FsMVlZiKlPxt",
            "https://youtu.be/EZHCk5i6Uh0?si=EQ-4_lD76SUm5qFU"
        ]
    },

    "stock market basics": {
        "keywords": [
            "stock market", "share market", "shares", "equity", "stocks",
            "nifty", "sensex", "market basics", "what is stock market"
        ],
        "answer": "The stock market is a platform where you buy and sell shares of companies. When you buy a share, you own a small part of the company. Prices change based on supply and demand. If more people want to buy, the price rises. If more people want to sell, the price falls. Markets work through exchanges like NSE, BSE, NYSE, or NASDAQ. Investors earn through capital gains or dividends, while traders focus on short term price movements. Important concepts include indices like NIFTY and SENSEX, market hours, settlement cycles, and brokerage charges. A clear understanding of the difference between investing and trading helps beginners make better decisions.",
        "videos": ["https://youtu.be/by9_zHQzeZk?si=PQYoPMeqMAbwWjw5"]
    },

    "order types": {
        "keywords": [
            "order types", "market order", "limit order", "stop loss order",
            "types of orders", "trading orders", "how to place order"
        ],
        "answer": "Order types define how your trades are executed. A Market Order buys or sells instantly at the current price but may experience slippage. A Limit Order executes only at your chosen price, giving more control but no guarantee of execution. A Stop Loss Order automatically exits your position when the price reaches a trigger level, protecting you from larger losses. A Stop Limit Order triggers a limit order instead of a market order, reducing slippage but risking a non fill. Trailing stops move automatically as price moves in your favor. Time based orders like GTC or IOC provide additional control. Understanding order types is essential for safe and effective trading.",
        "videos": ["https://youtu.be/WHQjIbKmyI0?si=g88Qkb0hP9wNai-J"]
    },

    "technical analysis": {
        "keywords": [
            "technical analysis", "chart analysis", "price action",
            "ta study", "technical indicators", "chart reading"
        ],
        "answer": "Technical analysis is the study of price charts and patterns to predict future movements. It is based on three ideas: market action reflects everything, prices move in trends, and history repeats itself. Traders use tools such as candlestick charts, trendlines, support and resistance, and indicators like moving averages, RSI, and MACD. Chart patterns like triangles and double tops help identify reversals or continuations. Technical analysis provides probabilities, not certainties, so risk management is crucial. It is widely used for intraday and swing trading. Successful traders combine chart analysis with discipline, backtesting, and consistent rules.",
        "videos": ["https://youtu.be/mRfVY9Wbnrs?si=YbrMtVsIqDvdY_UY"]
    },

    "indicators": {
        "keywords": [
            "indicators", "trading indicators", "technical indicators",
            "indicator tools", "momentum indicators", "volatility indicators",
            "moving averages", "bollinger bands indicator"
        ],
        "answer": "Indicators are mathematical tools applied to price and volume data. They help traders understand trend strength, momentum, volatility, and market direction. Common indicators include Moving Averages for trend, RSI for overbought or oversold levels, MACD for momentum changes, and Bollinger Bands for volatility. Indicators simplify decision making but should not be used alone. Most indicators are lagging because they use historical data. Too many indicators can cause confusion, so traders usually combine one trend indicator with one momentum indicator. Proper backtesting ensures that indicators work well in different market conditions. Indicators support decision making but cannot replace risk management.",
        "videos": ["https://youtu.be/94Vph1miSYg?si=u0sZuos8P-vFDA4o"]
    },

    "candlestick patterns": {
        "keywords": [
            "candlestick patterns", "candlestick chart", "candles",
            "bullish patterns", "bearish patterns", "chart candles",
            "candlestick trading", "doji candle", "hammer candle", "engulfing candle"
        ],
        "answer": "Candlestick patterns display price movement within a specific time period using open, high, low, and close values. They help traders understand market psychology. Bullish patterns like Hammer and Bullish Engulfing suggest potential upward reversals. Bearish patterns like Shooting Star and Bearish Engulfing indicate possible downward movement. Neutral patterns such as Doji show indecision. Candlestick patterns work best when combined with support and resistance, trend direction, and volume. They offer useful signals but are not always accurate, so traders should confirm them with other tools and always use stop loss. Learning these patterns improves timing and entry decisions.",
        "videos": ["https://youtu.be/EVlQgmirnCg?si=9iOjn9npEke1DpXy"]
    },

    "fundamental analysis": {
        "keywords": [
            "fundamental analysis", "company financials", "intrinsic value",
            "fundamental study", "balance sheet analysis", "pe ratio", "eps ratio",
            "financial statements"
        ],
        "answer": "Fundamental analysis evaluates a company’s financial health to find its true value. It studies revenue, profit, debt, cash flow, and management quality. Investors analyze financial statements such as the balance sheet, income statement, and cash flow statement. Ratios like PE, PB, ROE, and EPS help compare companies. Fundamental analysis also considers economic factors like inflation, interest rates, and industry growth. It is mainly used for long term investing, not short term trading. The goal is to find strong companies that can grow steadily. By understanding fundamentals, investors reduce risk and make better decisions about which stocks to hold.",
        "videos": ["https://youtu.be/sx8sBN2prAE?si=yGRMnVo0ks7oo8xm"]
    },

    "risk management": {
        "keywords": [
            "risk management", "stop loss rules", "risk control",
            "capital protection", "risk reward", "position sizing",
            "money management", "risk strategy"
        ],
        "answer": "Risk management protects your capital by controlling losses. Key tools include stop loss, position sizing, and risk reward ratios. A common rule is to risk only 1 to 2 percent of total capital on each trade. Traders also avoid overleveraging and overtrading. Using a consistent stop loss strategy prevents large drawdowns. Risk management reduces emotional decision making and keeps losses manageable. Even the best strategies fail without proper risk control. Successful traders focus more on protecting capital than chasing big profits. Long term success depends on discipline and consistency in following risk management rules.",
        "videos": ["https://youtu.be/s7KApswForA?si=12qsR4KKQc54wEeq"]
    },

    "trading psychology": {
        "keywords": [
            "trading psychology", "trader mindset", "trading emotions",
            "fear in trading", "greed in trading", "emotional control",
            "psychology of trading"
        ],
        "answer": "Trading psychology deals with emotions that affect trading decisions. Fear, greed, overconfidence, impatience, and revenge trading can lead to big mistakes. Even with a good strategy, emotional reactions can ruin performance. Traders must develop discipline, patience, and a rule based approach. Keeping a trading journal helps identify emotional patterns and bad habits. Confidence grows through practice and consistency, not impulsive trades. Managing expectations, accepting losses, and avoiding the urge to chase the market are important. Strong psychology separates successful traders from losing traders. Controlling emotions is just as important as analyzing charts.",
        "videos": ["https://youtu.be/TmmbgvDMLdQ?si=HdQDlv1LD64A_ZzG"]
    },

    "intraday trading": {
        "keywords": [
            "intraday trading", "day trading", "scalping", "intraday strategy",
            "intraday market", "day trade", "intraday meaning"
        ],
        "answer": "Intraday trading involves buying and selling within the same trading day. No positions are carried overnight. It requires quick analysis, fast execution, and strong discipline. Intraday traders focus on liquid stocks or indices that show clear movement. Popular strategies include breakout trading, pullback trading, and scalping. Traders use short time frame charts like 1 minute, 5 minute, or 15 minute intervals. Stop loss and proper position sizing are essential because prices can move quickly. Intraday trading offers high potential returns but also high risk. Avoiding overtrading, controlling emotions, and following a clear plan are key to success.",
        "videos": ["https://youtu.be/e5ye17EHZos?si=CbXwjGCGvQ5G0fQ_"]
    },

    "swing trading": {
        "keywords": [
            "swing trading", "swing strategy", "short term trading",
            "few days trading", "swing trader"
        ],
        "answer": "Swing trading is a method where traders hold positions for several days to a few weeks. The goal is to capture medium term price movements by identifying trends, pullbacks, and breakouts. Swing traders rely heavily on chart patterns, moving averages, support and resistance, and indicators like RSI or MACD. Because trades last longer than intraday, there is less stress and fewer decisions per day. However, overnight risk exists because global events can affect prices when markets are closed. Good swing traders create clear entry rules, stop loss placements, and target levels before entering a trade. They avoid emotional decisions and stick to tested strategies. Swing trading requires patience, discipline, and consistent analysis of market structure.",
        "videos": ["https://youtu.be/LJF3frcDgRM?si=gKuqCHHL9LF1smOx"]
    },

    "pnl calculation": {
        "keywords": [
            "pnl", "profit and loss", "how to calculate pnl", "profit calculation",
            "loss calculation", "returns calculation"
        ],
        "answer": "PnL stands for Profit and Loss. It measures how much money you gained or lost from a trade. The basic formula is: PnL equals (Sell Price minus Buy Price) multiplied by Quantity. For example, if you bought a stock at 100 and sold it at 120 with quantity 10, your PnL is (120 - 100) x 10 which equals 200. Negative results indicate loss. Traders also consider brokerage charges, taxes, and other fees when calculating net PnL. Tracking PnL helps you understand if your strategy is working. Maintaining a PnL journal lets you review patterns, winning rates, and average gain or loss. PnL is the core metric that shows trading performance.",
        "videos": ["https://youtu.be/02hkI7RcFeM?si=8qZzHf7SMw4X3sEi"]
    },

    "margin and leverage": {
        "keywords": [
            "margin", "leverage", "margin trading", "leverage trading",
            "margin requirements", "leverage meaning"
        ],
        "answer": "Margin and leverage allow traders to control larger positions with a smaller amount of capital. Margin is the minimum money you must deposit to open a trade. Leverage multiplies your buying power. For example, with 5x leverage, 1000 capital lets you trade 5000 worth of assets. While leverage increases potential profits, it also increases risk. Losses can grow quickly and may exceed your initial margin. Intraday traders often use leverage for short term opportunities, but beginners should be cautious. Using stop loss, proper position sizing, and avoiding overleveraging is essential. High leverage without discipline can wipe out trading accounts. Always understand the risks before using margin.",
        "videos": ["https://youtu.be/cLF7DsFsmRY?si=K4KKn7Q-y8LlNGHi"]
    },

    "futures trading": {
        "keywords": [
            "futures trading", "futures contract", "derivatives trading",
            "index futures", "stock futures", "futures meaning"
        ],
        "answer": "Futures are settled daily through mark to market, meaning gains and losses are added to or deducted from your margin every day. Traders Futures trading involves buying or selling a contract that represents an asset to be delivered at a future date at a predetermined price. These contracts exist for stocks, indices, commodities, and currencies. Futures allow traders to speculate on price movements without owning the underlying asset. They provide leverage, meaning small capital can control larger value. However, this increases both profit and loss potential. must understand contract size, expiry dates, lot values, and margin requirements. Futures trading requires strict risk management because price swings can be large.",
        "videos": ["https://youtu.be/LSnQnhg2bgQ?si=tlJ3Obmy0JBYmwLz"]
    },

    "options trading": {
        "keywords": [
            "options trading", "call option", "put option", "option strategies",
            "strike price", "options basics", "option premium"
        ],
        "answer": "Options are financial contracts that give the buyer the right but not the obligation to buy or sell an asset at a fixed price called the strike price. A Call option gives the right to buy, and a Put option gives the right to sell. Options have a premium, expiry date, and lot size. They allow traders to benefit from upward, downward, or even sideways markets depending on the strategy used. While options offer flexibility, they are more complex than stocks or futures. Factors such as volatility, time decay, and option Greeks affect price. Beginners should learn basics before trading real money. Proper risk control is essential because options can move very fast.",
        "videos": ["https://youtu.be/ROg-N-ACL8I?si=1VKNMSNHTiBMeTcZ"]
    },

    "chart patterns": {
        "keywords": [
            "chart patterns", "trading patterns", "support resistance patterns",
            "triangle pattern", "double top", "double bottom",
            "head and shoulders pattern"
        ],
        "answer": "Chart patterns are visual shapes formed by price movement on a chart. They help traders understand market psychology and predict potential movements. Common continuation patterns include triangles, flags, and pennants, which suggest that the trend is likely to continue. Reversal patterns like double top, double bottom, and head and shoulders indicate a possible change in direction. Chart patterns work best when combined with volume analysis and support or resistance levels. They are not guarantees but probability tools. Traders use patterns to set entry points, stop loss levels, and profit targets. Consistent practice is required to recognize patterns quickly and avoid false signals.",
        "videos": ["https://youtu.be/dP7Le1YdUXw?si=0NmV7a5oUbBVNGhB"]
    },

    "brokerage charges": {
        "keywords": [
            "brokerage charges", "brokerage fees", "trading charges",
            "broker charges", "gst on trading", "stt charges"
        ],
        "answer": "Brokerage charges are fees you pay to your broker for executing trades. They may include brokerage fee, Securities Transaction Tax, GST, exchange charges, SEBI charges, and stamp duty. These costs reduce your net profit or increase your net loss, so understanding them is important for accurate PnL calculation. Some brokers offer zero brokerage for equity delivery, while intraday and derivatives trading usually have fixed or percentage based charges. Small frequent trades can lead to higher cumulative charges. Traders must review their broker’s pricing, compare alternatives, and always include charges when analyzing strategy performance. Choosing a low cost broker can significantly improve overall profitability.",
        "videos": ["https://youtu.be/cQL2W4CsRBI?si=b2j78DSJ3hJ8M9Qt"]
    },

    "ipo": {
        "keywords": [
            "ipo", "initial public offering", "ipo allotment",
            "ipo listing", "apply ipo", "ipo meaning"
        ],
        "answer": "IPO stands for Initial Public Offering. It is the process through which a private company offers its shares to the public for the first time. Companies launch an IPO to raise capital for growth, expansion, or debt repayment. Investors can apply for IPO shares through their broker or bank using ASBA. IPOs can be oversubscribed, meaning more people apply than available shares. Allotment is not guaranteed. After listing on the stock exchange, the share price may rise or fall depending on market demand and company fundamentals. IPO investing can be profitable, but it also carries risk because newly listed stocks can be highly volatile.",
        "videos": ["https://youtu.be/Kw7hgNDxxhA?si=weZNN904vDL9w3HO"]
    },

    "portfolio diversification": {
        "keywords": [
            "portfolio diversification", "diversify portfolio",
            "spread risk", "multiple stocks", "portfolio meaning"
        ],
        "answer": "Portfolio diversification means spreading investments across different assets to reduce risk. Instead of putting all money into one stock, a diversified portfolio includes multiple stocks, sectors, or even asset classes like bonds and gold. The idea is that if one investment performs poorly, others may perform better and balance the overall return. Diversification helps reduce the impact of market volatility and unexpected events. It does not eliminate risk but improves stability. Long term investors use diversification to achieve steady growth while protecting capital. Building a diversified portfolio requires selecting assets with low correlation and regularly reviewing performance to maintain balance.",
        "videos": ["https://youtu.be/TBTwTZ7ND6k?si=39f4BrUv92IN8RH0"]
    },

    "trading strategies": {
        "keywords": [
            "trading strategies", "trading strategy", "market strategy",
            "trading rules", "strategy trading", "best strategy",
            "breakout strategy", "ma crossover strategy", "strategy meaning",
            "trading setup"
        ],
        "answer": "Trading strategies are predefined rules that guide when to enter and exit trades. Common strategies include breakout trading, moving average crossover, trend following, pullback trading, and mean reversion. A good strategy defines entry rules, stop loss placement, position size, and target levels. Traders test strategies using backtesting and paper trading before using real money. Consistency is critical because frequent rule changes lead to poor results. No strategy works all the time, so traders must adapt to market conditions. The best strategies are simple, tested, and easy to follow under pressure. Combining a strategy with strict risk management improves long term success.",
        "videos": ["https://youtu.be/bAV8_Of7nLU?si=9w1JCUJXnRSGlxk2"]
    }

}

# MATCHING LOGIC 
def normalize(s):
    return s.lower().strip()


def match_topic(text):
    u = normalize(text)
    words = u.split()
    best_topic = None
    best_score = 0

    for topic, data in KNOWLEDGE_BASE.items():
        score = 0
        for kw in data["keywords"]:
            if len(kw) < 3:
                continue

            # Exact word match
            if kw in words:
                score += 5

            # Phrase match
            elif kw in u:
                score += 3

            # Fuzzy match
            elif difflib.get_close_matches(kw, words, n=1, cutoff=0.8):
                score += 2

        if score > best_score:
            best_score = score
            best_topic = topic

    return best_topic


def get_response(user_input):
    topic = match_topic(user_input)

    if not topic:
        return "Sorry, I didn’t understand. Try asking differently."

    data = KNOWLEDGE_BASE[topic]
    answer = data["answer"]
    videos = data["videos"]

    msg = answer + "\n\nVideo links:\n"
    for v in videos:
        msg += f"- {v}\n"

    return msg.strip()


# Optional standalone testing 
def interactive_chat():
    print("Chatbot activated!")
    while True:
        q = input("You: ")
        if q.lower() in ("quit", "exit"):
            break
        print("Bot:", get_response(q))


if __name__ == "__main__":
    interactive_chat()
