
import pandas as pd
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    csv_filename = 'csv_data.csv'
    df = pd.read_csv(csv_filename)
    print(df.head(3)) #вывод перывых
    print(df.tail(1)) #вывод последних
    print(len(df)) #количество значений в таблице
    print(df.groupby('price').count())
    print(df.groupby('count').count())
    print(df.groupby('add_cost').count())
    print(df.groupby('product').count())

