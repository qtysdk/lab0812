

if __name__ == '__main__':
    import pandas as pd

    # sheet_name
    df = pd.read_excel(io="~/Downloads/users.xlsx")
    print(df)