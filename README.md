# Atreidos

A stock price prediction network for algorithmic trading. The goal of atreidos is to have an accurate
prediction model that can enable a decision agent to make informed trades on a daily basis. The hope is
that these informed trades to eventually outperform index funds such as the SPY 500 by avoiding their
downturns and leveraging their up swings.

## Network Architecture

Atreidos currently leverages convolutional neural networks with recurrent neural networks. CNNs give the
model local feature data while the RNNs provide it with long term data. These two feature sets are able to
accurately predict pricing even on new data it has not seen before. For more detail check out the notebook
here: [Daily SPY Price LPM.ipynb](https://github.com/DidgeridooMH/atreidos/blob/main/ml-prediction-model/Daily%20SPY%20Price%20LPM.ipynb)

## Future Plans

The atreidos system is still in very early stages. Next steps are as follows:
- Train more data through the network to avoid overfitting to one asset.
- Expand the network to cross correlate between assets of similar or countering market sectors.
- Design more intelligent decision agents to operate on the predicted data.
- Implement a system to paper trade and test potential agents.
