import marimo

__generated_with = "0.10.19"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    import matplotlib.pyplot as plt

    # -------------------------------
    # 1. Read CSV file with selected columns and drop rows with any missing values
    # -------------------------------

    selected_columns = [
        'period_of_performance_current_end_date',
        'transaction_description',
        'contract_transaction_unique_key',
        'current_total_value_of_award',
        'recipient_name',
        'potential_total_value_of_award',
        'parent_award_agency_name',
        'awarding_sub_agency_name',
        'awarding_agency_name',
        'awarding_office_name',
    ]

    # Read CSV (uncomment nrows=1000 if you want to limit to 1000 records)
    df = pd.read_csv(
        'FY2025_All_Contracts_Full_20250107_1.csv',
        usecols=selected_columns,
        # nrows=1000
    ).dropna()

    # -------------------------------
    # 2. Print Basic DataFrame Information
    # -------------------------------
    print("Data Types:")
    print(df.dtypes)
    print("\nFirst 5 Rows:")
    print(df.head())
    print("\nSummary Statistics:")
    print(df.describe())

    # -------------------------------
    # 3. Filter for 'Agency for International Development'
    # -------------------------------
    df_aid = df[df['awarding_agency_name'] == 'Agency for International Development'].copy()
    if df_aid.empty:
        print("\nNo records found for 'Agency for International Development'.")
    else:
        # Convert date column to datetime for time series analysis
        df_aid['period_of_performance_current_end_date'] = pd.to_datetime(
            df_aid['period_of_performance_current_end_date'], errors='coerce'
        )

        # -------------------------------
        # 4. Grouping: Sum Awards by Recipient
        # -------------------------------
        # Group by recipient and sum current_total_value_of_award
        recipient_sum = df_aid.groupby('recipient_name')['current_total_value_of_award'].sum()
        
        # Convert award amounts to billions and round to two decimals
        recipient_sum_billions = (recipient_sum / 1e9).round(2)
        
        # Print results with comma formatting
        print("\nTotal Award Amounts by Recipient (in Billions):")
        for recipient, amount in recipient_sum_billions.sort_values(ascending=False).items():
            print(f"{recipient}: ${amount:,.2f}B")
        
        # -------------------------------
        # 5. Bar Chart: Top 10 Recipients by Award Amount
        # -------------------------------
        top10 = recipient_sum_billions.sort_values(ascending=False).head(10)
        plt.figure(figsize=(10, 6))
        top10.plot(kind='bar', color='skyblue')
        plt.ylabel('Award Amount (Billions of $)')
        plt.title("Top 10 Recipients by Award Amount\n(Agency for International Development)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # -------------------------------
        # 6. Pie Chart: Award Share for Top 10 Recipients
        # -------------------------------
        plt.figure(figsize=(8, 8))
        top10.plot(kind='pie', autopct='%1.1f%%', startangle=140, pctdistance=0.85)
        plt.ylabel('')
        plt.title("Award Share of Top 10 Recipients\n(Agency for International Development)")
        # Draw a circle at the center to turn it into a donut chart (optional)
        centre_circle = plt.Circle((0,0),0.70,fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.tight_layout()
        plt.show()
        
        # -------------------------------
        # 7. Time Series: Awards Over Time
        # -------------------------------
        # Group by month (extract year and month) and sum awards
        df_aid['year_month'] = df_aid['period_of_performance_current_end_date'].dt.to_period('M')
        time_series = df_aid.groupby('year_month')['current_total_value_of_award'].sum()
        # Convert to billions and round
        time_series_billions = (time_series / 1e9).round(2)
        
        # Convert PeriodIndex to Timestamp for plotting
        time_series_billions.index = time_series_billions.index.to_timestamp()
        
        plt.figure(figsize=(12, 6))
        plt.plot(time_series_billions.index, time_series_billions.values, marker='o', linestyle='-')
        plt.xlabel("Month")
        plt.ylabel("Award Amount (Billions of $)")
        plt.title("Time Series of Award Amounts\n(Agency for International Development)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    return (
        amount,
        centre_circle,
        df,
        df_aid,
        fig,
        pd,
        plt,
        recipient,
        recipient_sum,
        recipient_sum_billions,
        selected_columns,
        time_series,
        time_series_billions,
        top10,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
