from typing import Optional


TAF_RATE = 1.45e-4
RTF_RATE = 8 / 1_000_000

TIERS = [
    [None, -1.0, -10],
    [-1.0, -0.8, -15],
    [-0.8, -0.6, -20],
    [-0.6, -0.4, -50],
    [-0.4, -0.2, -75],
    [-0.2, -0.15, -100],
    [-0.15, 0.15, 0],
    [0.15, 0.2, 100],
    [0.2, 0.4, 75],
    [0.4, 0.6, 50],
    [0.6, 0.8, 20],
    [0.8, 1.0, 15],
    [1.0, None, 10],
]


def get_action(gain: float) -> (int, float):
    for i, action in enumerate(TIERS):
        if (action[0] is None or gain > action[0]) and (
            action[1] is None or gain <= action[1]
        ):
            return i, action[2]


def sell_stock(
    amount: float, current_price: float, cash_balance: float, stock_balance: float
) -> (float, float):
    amount = min(amount, stock_balance)
    print(f"\tSell {amount} at {current_price}")
    sell_amount = amount * current_price
    if sell_amount > 500:
        sell_amount -= RTF_RATE * sell_amount
    sell_amount -= min(round(TAF_RATE * amount, 2), 7.27)
    cash_balance += amount * current_price
    stock_balance -= amount
    return cash_balance, stock_balance


def buy_stock(
    amount: float, current_price: float, cash_balance: float, stock_balance: float
) -> (float, float):
    amount = min(amount, cash_balance)
    print(f"\tBuy ${amount} at {current_price}")
    cash_balance -= amount
    stock_balance += amount / current_price
    return cash_balance, stock_balance


def execute_action(
    action: float,
    current_price: float,
    initial_cash: float,
    cash_balance: float,
    stock_balance: float,
) -> (float, float):
    if action < 0:
        return sell_stock(
            (-action * initial_cash) / current_price,
            current_price,
            cash_balance,
            stock_balance,
        )
    elif action > 0:
        return buy_stock(
            action * initial_cash, current_price, cash_balance, stock_balance
        )
    else:
        print(f"\tHold at {current_price}")
    return cash_balance, stock_balance
