# crawly.py
import investpy
import pandas as pd
import datetime
from script.get_database_stock import GetDatabase
import matplotlib.pyplot as plt
import argparse
import random
from config.config import Config


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-in", "--input_directory", type=str, default=Config.DEFAULT_INPUT,
                        help="It is directory of csv file")
    opt = parser.parse_args()

    # read csv and put to database
    object_getdatabase = GetDatabase("database.db")
    list_stock_name = pd.read_csv(opt.input_directory, encoding='utf-8')
    for company in list_stock_name["Code"]:
        # Load data
        start = Config.START_TIME
        end = datetime.datetime.now().strftime("%d/%m/%Y")
        df = investpy.get_stock_historical_data(stock=company, country='United States', from_date=start, to_date=end)
        df = pd.DataFrame(df)
        df.to_csv(f".\\output\\{company}.csv")

        # send to database
        object_getdatabase.create_table(company)
        object_to_save = pd.read_csv(f"./output/{company}.csv", encoding='utf-8')
        object_to_save = object_to_save.values.tolist()
        object_getdatabase.input_data(company, object_to_save, company)

    fig, ax = plt.subplots()
    for company in list_stock_name["Code"]:
        color = {'k': 'r', 'h': 'g', 'a': 'b'}
        sysbol = {'k': '*', 'h': 'o', 'a': '^'}
        price_stock = pd.read_csv(f"./output/{company}.csv", encoding='utf-8')
        ax.plot(price_stock["Date"], price_stock["Close"],
                f'{random.choice(list(color.values()))}{random.choice(list(sysbol.values()))}-', label=company)

    fig.suptitle('Stock price chart', fontsize=20)
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Price (USD)', fontsize=16)
    plt.minorticks_off()
    plt.legend(loc='best')
    plt.show()
    fig.savefig(f'.\\output\\{datetime.datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.jpg')

    print("Finish")
