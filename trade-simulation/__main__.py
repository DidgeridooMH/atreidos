import numpy as np
from historical import retrieve_ticker_data, prepare_price
import onnxruntime as ort
from strategy import get_action, execute_action
import json

print("Reading config...")
with open("config.json", "r") as configfile:
    config = json.load(configfile)

print("Loading ticker information...")
symbol_data, history = retrieve_ticker_data()

print(f"Loading {config['model']}...")
session = ort.InferenceSession(config["model"])

buffer = symbol_data[-6:]
buffer.append(prepare_price(config["current_price"], config["pe_ratio"], history))

print("Loading gain buffer...")
with open("gain.json", "r") as gainfile:
    try:
        gain_buffer = json.load(gainfile)
    except:
        print("Gain buffer not found. Assuming empty")
        gain_buffer = []

print("Running prediction network...")
prediction = session.run(None, {"input": [buffer]})

print("Getting best action...")
gain = (prediction[0] / buffer[-1][-2]) - 1.0
gain_buffer.append(gain)
if len(gain_buffer) > 1:
    std = np.std(gain_buffer)
    if std != 0:
        gain = ((gain - np.mean(gain_buffer)) / np.std(gain_buffer)) * 0.5
    if len(gain_buffer) == 7:
        gain_buffer = gain_buffer[1:]
action_id, action = get_action(gain)

print("Executing action...")
print(f"\tStart Action : C:{config['cash_balance']} S:{config['stock_balance']}")
print(f"\tAS: {action} | AID: {action_id}")
cash_balance, stock_balance = execute_action(
    action,
    buffer[-1][-2],
    config["initial_investment"],
    config["cash_balance"],
    config["stock_balance"],
)
print(f"\tEnd Action : C:{cash_balance} S:{stock_balance}")

print(f"Caching gain buffer of {len(gain_buffer)} indices...")
with open("gain.json", "w") as gainfile:
    json.dump(gain_buffer, gainfile)
