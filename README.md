# TradingStrategiesAndBacktesting

This repository contains a trading strategies and a backtester capable for generalization and scalability to other types of financial instruments data (in progress).

Data generation takes advantage of AlphaVantage high frequency data, from which the trading strategies and backtester can be tested/validated.

So far, the trading strategies contained are momentum based, mean reversion based, and candlestick based. Currently being worked on are more advanced versions of these strategies, along with strategies that leverage ML models like: SVM, Random Forests (and Boosting), and neural networks (feed forward and convolutional).

Also, currently being worked on is implementing options trading strategies with high frequency options data, like: butterflies, iron condors, and covered puts/calls.

Future work will be focused on expanding to futures contract trading, as well as market making.
