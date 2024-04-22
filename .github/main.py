import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


def EMA(p, index, N):
    alfa = 2 / (N + 1)

    alfa = 1 - alfa

    num_sum = 0
    den_sum = 0
    for i in range(0, N + 1):
        power = alfa ** i
        num_sum = num_sum + p[index - i] * power
        den_sum = den_sum + power

    wynik = num_sum / den_sum
    return wynik


def MACD(p):
    macd = []
    for i in range(26, len(p)):  # pomijamy pierwsze 26 probek
        val = EMA(p, i, 12) - EMA(p, i, 26)
        macd.append(val)
    return macd


def signal(macd):
    signal = []
    for i in range(9, len(macd)):
        val = EMA(macd, i, 9)
        signal.append(val)
    return signal


def make_money(macd, signal, data, capital, is_x, is_y):
    shares = 0
    last_buy = 40
    last_sell = 40
    for i in range(1, len(macd)):
        index = i + 35
        if macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
            # macd przecina signal od dolu -> kupno
            capital, shares = buy(index, data, capital, shares)
            is_x.append(index)
            is_y.append(data[index])
        elif macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:
            # macd przecina signal od gory -> sprzedaz
            capital, shares = sell(index, data, capital, shares)
            is_x.append(index)
            is_y.append(data[index])
        if last_buy < 100:
            last_buy += 1
        if last_sell < 100:
            last_sell += 1
    if capital == 0:
        capital, shares = sell(len(data)-1, data, capital, shares)

    return capital


def buy(index, data, capital, shares):
    price = data[index]
    print("Kapital przed zakupem = ", capital)
    print("Cena akcji = ", price)
    capital = capital * 50/100
    shares += capital/price
    last_buy = 0
    print("Kupiłem ", shares, " akcji")
    print("Kapital po zakupie = ", capital, "\n")
    return capital, shares


def sell(index, data, capital, shares):
    price = data[index]
    print("Kapital przed sprzedażą = ", capital)
    print("Cena akcji = ", price)
    shares = shares * 50/100
    capital += shares*price
    last_sell = 0
    print("Sprzedalem ", shares, " akcji")
    print("Kapital po sprzedaży = ", capital, "\n")
    return capital, shares

def main():
    input = pd.read_csv("wig20_d.csv")
    data = input['Zamkniecie']

    macd = MACD(data)
    sig = signal(macd)
    macd = macd[9:]
    is_x = []
    is_y = []

    capital = 1000
    print("POCZATKOWY KAPITAL = ", capital, "\n")

    capital = make_money(macd, sig, data, capital, is_x, is_y)

    print("\nOSTATECZNY KAPITAL = ", capital)

    income = capital/1000

    print("CALKOWITY ZYSK W STOSUNKU DO KAPITALU POCZATKOWEGO = " + "{0:.0%}".format(income))

    date = input['Data']

    # wykres kursu bez dat
    plt.plot(range(0, len(data)), data, linewidth=0.7, color='b')
    # wyswietlenia punktow przeciecia
    plt.plot(is_x, is_y, 'r+')
    plt.show()

    # wykres kursu
    date = pd.to_datetime(date)
    DF = pd.DataFrame()
    DF['value'] = data
    DF = DF.set_index(date)
    plt.plot(DF, linewidth=0.7, color='b')
    plt.show()

    # wykres macd
    macd_date = date[35:]
    macd_date = pd.to_datetime(macd_date)
    macd_DF = pd.DataFrame()
    macd_DF['value'] = macd
    macd_DF = macd_DF.set_index(macd_date)
    plt.plot(macd_DF, linewidth=1, color='g', label="MACD")
    # wykres signal
    macd_DF['value'] = sig
    plt.plot(macd_DF, linewidth=1, color='r', label="Signal")
    plt.legend(loc='lower right')
    plt.show()


if __name__ == "__main__":
    main()
