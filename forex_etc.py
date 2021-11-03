from datetime import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def main():
    df_exchange = pd.read_csv(
        'exchange.csv', encoding='cp932', header=1, names=['date', 'USD', 'rate'],
        index_col=0, parse_dates=True)

    min_date = datetime(1973, 1, 1)
    max_date = datetime.now()
    plt.subplot(1, 1, 1)
    plt.plot(df_exchange.index, df_exchange.USD, label='ドル・円')
    plt.xlim(min_date, max_date)
    plt.ylim(50, 250)
    plt.legend(loc='best')  


def parse_year_and_month(year: str, month: str) -> datetime:
    year = int(year[:-1])
    month = int(month[:-1])
    year += (1900 if year >= 63 else 2000)
    return datetime(year, month, 1)


def parse_japanese_date(s: str) -> datetime:
    base_years = {'S': 1925, 'H': 1988, 'R': 2018}
    era = s[0]
    year, month, day = s[1:].split('.')
    year = base_years[era] + int(year)
    return datetime(year, int(month), int(day))


if __name__ == '__main__':
    main()