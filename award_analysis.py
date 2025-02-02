import marimo

__generated_with = "0.10.19"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    import pandas as pd
    return mo, pd


@app.cell
def _(pd):
    # Read the CSV file with specific columns and limit to 1000 records
    selected_columns = [
        'transaction_description',
        'contract_transaction_unique_key',
        'current_total_value_of_award',
        'awarding_office_name',
        'recipient_name',
        'total_dollars_obligated',
        'parent_award_agency_name',
        'awarding_agency_name',
        'treasury_accounts_funding_this_award'
    ]

    # Read CSV and then drop NA values
    df = pd.read_csv(
        'FY2025_All_Contracts_Full_20250107_1.csv',
        usecols=selected_columns,
        # nrows=1000
    ).dropna()  # This will remove rows with any NA values
    return df, selected_columns


@app.cell
def _(pd):
    df2 = pd.read_csv('FY2025_All_Contracts_Full_20250107_1.csv')
    return (df2,)


@app.cell
def _(df2):
    df2.count()
    return


@app.cell
def _(df2):
    df2.columns
    return


@app.cell
def _(df2):
    df2
    return


@app.cell
def _(df2):
    print(df2.columns)
    return


@app.cell
def _(df2):
    df2
    return


@app.cell
def _(df):
    df
    return


@app.cell
def _(df):
    print("first five rows")
    print(df.head())
    return


@app.cell
def _(df):
    print("\nLast 5 Rows")
    print(df.tail())
    return


@app.cell
def _(df):
    print("\nDataframe Info")
    print(df.info())
    return


@app.cell
def _(df):
    print("\nSummary Statistics")
    print(df.describe())
    return


@app.cell
def _(df):
    print("\nData Types")
    print(df.dtypes)
    return


@app.cell
def _(df):
    print("\nColumn Names:")
    print(df.columns.tolist())
    return


@app.cell
def _(df):
    print("\nShape of Dataframe")
    print(df.shape)
    return


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    selected_columns_ii = df[['recipient_name','total_dollars_obligated']]
    print("\nSelected Columns (first 5 rows:")
    print(selected_columns_ii.head())
    return (selected_columns_ii,)


@app.cell
def _(df):
    filtered_df = df[df['total_dollars_obligated']>100000000]
    print("\nFiltered Rows where df total_dollars_obligated more than 100,000,000 dollars")
    print(filtered_df.head())
    return (filtered_df,)


@app.cell
def _(df):
    sorted_df = df.sort_values(by='total_dollars_obligated', ascending=False)
    sorted_df
    return (sorted_df,)


@app.cell
def _(df):
    grouped_counts = df.groupby('recipient_name').size().reset_index(name='count')
    grouped_counts.sort_values(by='count',ascending=False)
    return (grouped_counts,)


@app.cell
def _(df):
    df.columns
    return


@app.cell
def _(df):
    grouped_counts_gov = df.groupby('awarding_agency_name').size().reset_index(name='count')
    grouped_counts_gov.sort_values(by='count',ascending=False)
    return (grouped_counts_gov,)


@app.cell
def _():
    # how can i sum the total_dollars_obligated by awarding_agency_name?
    return


@app.cell
def _(df):
    pivot_table_df = df.pivot_table(index='awarding_agency_name',values='total_dollars_obligated',aggfunc=sum)
    # pivot_table_df = pivot_table_df.sort_values('total_dollars_obligated',ascending=False)
    # pivot_table_df
    return (pivot_table_df,)


@app.cell
def _(pivot_table_df):
    pivot_table_df
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
