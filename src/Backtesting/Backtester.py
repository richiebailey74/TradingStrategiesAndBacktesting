import matplotlib.pyplot as plt
from src.Utils import CurrentPosition, StockData, StockOrder

class Backtester:
    def __init__(self, strategy, data, initial_capital, transaction_cost_pct):
        self.strategy = strategy
        self.data = data.copy()
        self.initial_capital = initial_capital
        self.transaction_cost_pct = transaction_cost_pct
        self.longs_profits_and_losses = []
        self.shorts_profits_and_losses = []
        self.results = None
        self.current_position = CurrentPosition(0, 0, initial_capital)

    # figure out how to integrate the mean reversion trading strategy (and eventually the other strategies) with this backtester
    # make it so that the backtester feeds the strat data and thus its internal state will be altered
    # backtester will track the capital gains and losses
    # backtester will track changes and provide graphs to give insights into results and how they perform

    def backtest(self):
        count = 0
        first = True

        for ind in self.data.index:
            temp_data = self.data.loc[ind]
            stock_data = StockData(temp_data['open'], temp_data['high'], temp_data['low'], temp_data['close'],
                                   temp_data['volume'], ind)

            # fulfill order from the last iteration
            if not first:
                self.update_position(stock_data.open_p, stock_order, self.current_position)

            first = False

            stock_order = self.strategy.execute(self.current_position, stock_data)

            count += 1
            if count % 50000 == 0:
                print(f"Progress: {count}/{self.data.shape[0]} data points complete")

        # for the last data point
        self.update_position(stock_data.close_p, stock_order, self.current_position)

        capital_in_assets = 0
        for key, value in self.current_position.longs_owned_tracker.items():
            capital_in_assets += key * value

        for key, value in self.current_position.shorts_sold_tracker.items():
            capital_in_assets += key * value

        print(f"\nLiquid capital: ${self.current_position.capital}")
        print(f"Capital in assets: ${capital_in_assets}")
        print(f"Total capital: ${self.current_position.capital + capital_in_assets}")
        print(f"Relative gain or loss: {(self.current_position.capital + capital_in_assets) / self.initial_capital}")

        plt.plot(list(range(len(self.longs_profits_and_losses))), self.longs_profits_and_losses)
        plt.plot(list(range(len(self.shorts_profits_and_losses))), self.shorts_profits_and_losses)
        plt.legend(['longs', 'shorts'])

    def update_position(self, stock_val, order, position):

        if not isinstance(order, StockOrder):
            raise TypeError("Object passed to the Backtester object must be of type StockOrder")

        if not isinstance(position, CurrentPosition):
            raise TypeError(
                "Fundamental issue with backtester, current position not in correct format, investigate source code")

        # order to buy a long: take money out of the capital of current position and credit longs to current position
        if order.longs_to_buy > 0:
            position.longs_owned += order.longs_to_buy
            position.capital -= stock_val * order.longs_to_buy
            if stock_val not in position.longs_owned_tracker:
                position.longs_owned_tracker[stock_val] = order.longs_to_buy
            else:
                position.longs_owned_tracker[stock_val] += order.longs_to_buy

        # order to sell a long: remove longs from current position and credit capital to current position
        if order.longs_to_sell > 0:
            position.longs_owned -= order.longs_to_sell
            position.capital += stock_val * order.longs_to_sell
            to_sell = order.longs_to_sell
            to_del = []
            for key, value in position.longs_owned_tracker.items():
                if value == to_sell:
                    self.longs_profits_and_losses.append(to_sell * (stock_val - key))
                    to_del.append(key)
                    break
                elif value > to_sell:
                    self.longs_profits_and_losses.append(to_sell * (stock_val - key))
                    position.longs_owned_tracker[key] = value - to_sell
                    break
                elif value < to_sell:
                    self.longs_profits_and_losses.append(to_sell * (stock_val - key))
                    to_del.append(key)

            for d in to_del:
                del position.longs_owned_tracker[d]

        # order to buy a short: remove shorts sold to current position and take money out of capital of current position
        if order.shorts_to_buy > 0:
            position.shorts_sold -= order.shorts_to_buy
            position.capital -= stock_val * order.shorts_to_buy
            to_buy = order.shorts_to_buy
            to_del = []
            for key, value in position.shorts_sold_tracker.items():
                if value == to_buy:
                    self.shorts_profits_and_losses.append(to_buy * (key - stock_val))
                    to_del.append(key)
                    break
                elif value > to_buy:
                    self.shorts_profits_and_losses.append(to_buy * (key - stock_val))
                    position.shorts_sold_tracker[key] = value - to_buy
                    break
                elif value < to_buy:
                    self.shorts_profits_and_losses.append(to_buy * (key - stock_val))
                    to_del.append(key)

            for d in to_del:
                del position.shorts_sold_tracker[d]

        # order to sell a short: add shorts sold to current position and credit capital to current position
        if order.shorts_to_sell > 0:
            position.shorts_sold += order.shorts_to_sell
            position.capital += stock_val * order.shorts_to_sell
            if stock_val not in position.shorts_sold_tracker:
                position.shorts_sold_tracker[stock_val] = order.shorts_to_sell
            else:
                position.shorts_sold_tracker[stock_val] += order.shorts_to_sell
