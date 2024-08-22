import csv
from datetime import datetime

class Stock:
    price_per_date = {} # Faster to use a dictionary.
    name = "" # Might come in handy to know what stock is what.

    def __init__(self, new_name):
        self.name = new_name
        self.price_per_date = {}

    def add_date_price(self, date, price):
        self.price_per_date[date] = price
    
    def Price(self, date):
        return self.price_per_date.get(date, fr"Unknown price of {self.name} for {date}.")

class Portfolio:
    stack_of_stocks = []

    def __init__(self):
        self.stack_of_stocks = []

    def add_new_stock(self, new_stock, units):
        self.stack_of_stocks.append([new_stock, units])

    def Profit(self, start_date, end_date):
        total_profit = 0 # We'll collect the differences using this variable.
        clean_results = True # We want to sanity check the results. In case we're missing the value for any specified date, we want to alert the user.

        for pair in self.stack_of_stocks: # Simple for loop over our stack of stocks.
            element, amount = pair[0], pair[1]
            end_price = element.Price(end_date) # Get the corresponding prices.
            start_price = element.Price(start_date)
            end_price_problem = isinstance(end_price, str) # Check if we get the expected numerical price or the error message.
            start_price_problem = isinstance(start_price, str)
            if end_price_problem:
                clean_results = False
                print(end_price)
            if start_price_problem:
                clean_results = False
                print(start_price)
            if not (end_price_problem or start_price_problem):
                total_profit = total_profit + amount*(end_price - start_price)
                
        if clean_results:
            print(fr"All values correctly computed for current portfolio between {start_date} and {end_date}")
        else:
            print("Some values missing for current portfolio. Total profit calculation is not accurate.")
            
        return total_profit

    ###### The following functions allow us to compute the annualized return. #######
    
    def determine_day_difference(self, start_date, end_date):
        days_elapsed = ((datetime.fromisoformat(end_date)).date() - (datetime.fromisoformat(start_date)).date()).days
        return days_elapsed

    def cumulative_return(self, starting_value, ending_value):
        return float(ending_value-starting_value)/starting_value

    def annualized_return(self, start_date, end_date):
        elapsed_days = self.determine_day_difference(start_date, end_date)
        if elapsed_days < 365:
            print(fr"CAREFUL, ELAPSED PERIOD ({elapsed_days} days) LESS THAN ONE YEAR: When this measure is used with less than one year's worth of data it extrapolates the same rate of return for the missing period, until a year is completed. This constitutes an approximation with incomplete data.")
        starting_value = 0
        ending_value = 0
        for pair in self.stack_of_stocks:
            element, amount = pair[0], pair[1]

            end_price = element.Price(end_date) # Get the corresponding prices.
            start_price = element.Price(start_date)

            starting_value = starting_value + amount*start_price
            ending_value = ending_value + amount*end_price

        current_annualized_return = ((1 + self.cumulative_return(starting_value, ending_value))**(float(365)/elapsed_days)) - 1

        return current_annualized_return


def load_stock_data(file_path = fr'./stock_details_5_years_csv.csv'):
    with open(file_path) as csvfile:
        reader = csv.reader(csvfile, delimiter = ",")
        header = next(reader)
        unique_stocks = {}
        for row in reader:
            company = row[8]
            stock = unique_stocks.get(company, Stock(company))
            stock.add_date_price(row[0], float(row[1]))
            unique_stocks[company] = stock
        
        print(fr"Total loaded stocks: {len(unique_stocks)}.")
        return unique_stocks

if __name__ == '__main__':
    
    ################################## Load stock data ###################################
    available_stocks = load_stock_data() # We'll load some sample data from https://www.kaggle.com/datasets/iveeaten3223times/massive-yahoo-finance-dataset
    ######################################################################################

    new_Portfolio = Portfolio()

    # We will load NVDA, GOOGL, MSFT and AAPL stocks into our portfolio.

    ################################## NVDA ##############################################
    NVDA = available_stocks['NVDA'] #This object contains the information of the Nvidia stock.

    print(fr"NVDA price at 2019-01-08 00:00:00-05:00 is {NVDA.Price("2019-01-08 00:00:00-05:00")}") #Should be 36.39084278
    print(fr"NVDA price at 2022-05-23 00:00:00-04:00 is {NVDA.Price("2022-05-23 00:00:00-04:00")}") #Should be 162.5578276

    new_Portfolio.add_new_stock(NVDA, 1)

    print("\n1 NVDA stock portfolio.")
    print(new_Portfolio.Profit('2019-01-08 00:00:00-05:00', '2022-05-23 00:00:00-04:00')) #Should be 126.16698482
    ######################################################################################

    ################################## Add the rest of the stocks ########################
    new_Portfolio.add_new_stock(available_stocks['GOOGL'], 1)
    new_Portfolio.add_new_stock(available_stocks['MSFT'], 1)
    new_Portfolio.add_new_stock(available_stocks['AAPL'], 1)
    ######################################################################################

    ################################## Compute profit ####################################
    print("\n1 NVDA, GOOGL, MSFT and AAPL stock portfolio.")
    print(new_Portfolio.Profit('2019-01-08 00:00:00-05:00', '2022-05-23 00:00:00-04:00'))

    print("\nNow inverting dates.")
    print(new_Portfolio.Profit('2022-05-23 00:00:00-04:00', '2019-01-08 00:00:00-05:00')) # Gives us a loss. We could also check for date consistency (end date should be later than start date).
    ######################################################################################

    ################################## Extras ############################################
    new_Portfolio = Portfolio()

    new_Portfolio.add_new_stock(available_stocks['GOOGL'], 20) # We can define the number of stocks.
    new_Portfolio.add_new_stock(available_stocks['MSFT'], 0.3) # And this number can be a fraction of a whole stock.
    new_Portfolio.add_new_stock(available_stocks['AAPL'], 10)
    new_Portfolio.add_new_stock(available_stocks['NVDA'], 150)

    print("\n20 GOOGL stocks, 0.3 MSFT stocks, 10 AAPL stocks and 150 NVDA stocks portfolio.")
    print(new_Portfolio.Profit('2023-10-30 00:00:00-04:00', '2023-11-21 00:00:00-05:00'))


    # We can also compute the annualized return of the portfolio.
    new_Portfolio = Portfolio()

    new_Portfolio.add_new_stock(available_stocks['NVDA'], 1)
    print("\nAnnualized return for a portfolio of 1 NVDA stock between 2021-11-22 and 2023-11-22")
    print(new_Portfolio.annualized_return('2021-11-22 00:00:00-05:00', '2023-11-22 00:00:00-05:00'))

    # Note that using this measure for periods smaller than 1 year leads to approximated results.
    print("\nAnnualized return for a portfolio of 1 NVDA stock between 2021-11-22 and 2021-11-30")
    print(new_Portfolio.annualized_return('2021-11-22 00:00:00-05:00', '2021-11-30 00:00:00-05:00')) # Which is funny, because the real stock price fell even harder.


    # Finally, let's make a multi-stock portfolio annualized return test.

    new_Portfolio.add_new_stock(available_stocks['MSFT'], 1)
    print("\nAnnualized return for a portfolio of 1 NVDA and 1 MSFT stock between 2021-11-22 and 2023-11-22")
    print(new_Portfolio.annualized_return('2021-11-22 00:00:00-05:00', '2023-11-22 00:00:00-05:00'))

    # There's a lot of fine details about this we could improve, but I think it serves as a decent toy example.

    
