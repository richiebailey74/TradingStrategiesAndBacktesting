class FinancialInstrumentData:
    def getData(self):
        raise NotImplementedError(
            "The base class cannot be used, a particular security or derivative type must implement this class!")


class StockData(FinancialInstrumentData):

    def __init__(self, open_p, high_p, low_p, close_p, volume, time_index):
        self.open_p = open_p
        self.high_p = high_p
        self.low_p = low_p
        self.close_p = close_p
        self.volume = volume
        self.time_index = time_index

    def getData(self):
        return self.open_p, self.high_p, self.low_p, self.close_p, self.volume, self.time_index
