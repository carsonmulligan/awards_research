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

    # For inline plotting (if using Jupyter Notebook)
    # %matplotlib inline

    # ------------------------------------------
    # 1. Load the Data with the New 'recipient_uei' Column
    # ------------------------------------------
    selected_columns = [
        'period_of_performance_current_end_date',
        'transaction_description',
        'contract_transaction_unique_key',
        'current_total_value_of_award',
        'recipient_name',
        'recipient_uei',  # added recipient UEI
        'potential_total_value_of_award',
        'parent_award_agency_name',
        'awarding_sub_agency_name',
        'awarding_agency_name',
        'awarding_office_name',
    ]

    # Read CSV (adjust file path as needed); drop rows with missing values
    df = pd.read_csv(
        'FY2025_All_Contracts_Full_20250107_1.csv',
        usecols=selected_columns,
        # nrows=1000  # uncomment for testing on a subset
    ).dropna()

    # Convert the performance end date to datetime (for time series analysis)
    df['period_of_performance_current_end_date'] = pd.to_datetime(
        df['period_of_performance_current_end_date'], errors='coerce'
    )

    # ------------------------------------------
    # 2. Filter the Data for recipient_uei "KMH5K9V7S518"
    # ------------------------------------------
    recipient_uei_target = "KMH5K9V7S518"
    df_recipient = df[df['recipient_uei'] == recipient_uei_target].copy()

    if df_recipient.empty:
        print(f"No records found for recipient_uei {recipient_uei_target}")
    else:
        # ------------------------------------------
        # Visualization 1: Agency Breakdown (Bar Chart)
        # ------------------------------------------
        # Group by awarding agency and sum awards; convert dollars to millions
        agency_sum = df_recipient.groupby('awarding_agency_name')['current_total_value_of_award'].sum()
        agency_sum_millions = (agency_sum / 1e6).round(2).sort_values(ascending=False)
        
        plt.figure(figsize=(10, 6))
        agency_sum_millions.plot(kind='bar', color='cornflowerblue')
        plt.title(f"Agency Breakdown for recipient_uei {recipient_uei_target}")
        plt.xlabel("Awarding Agency")
        plt.ylabel("Total Award Amount (Millions of $)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # ------------------------------------------
        # Visualization 2: Transaction Description Breakdown (Bar Chart)
        # ------------------------------------------
        # Group by transaction description and sum awards; convert dollars to millions
        tx_sum = df_recipient.groupby('transaction_description')['current_total_value_of_award'].sum()
        tx_sum_millions = (tx_sum / 1e6).round(2).sort_values(ascending=False)
        
        plt.figure(figsize=(10, 6))
        tx_sum_millions.plot(kind='bar', color='seagreen')
        plt.title(f"Transaction Description Breakdown for recipient_uei {recipient_uei_target}")
        plt.xlabel("Transaction Description")
        plt.ylabel("Total Award Amount (Millions of $)")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # ------------------------------------------
        # Visualization 3: Time Series of Award Amounts (Line Chart)
        # ------------------------------------------
        # Create a year-month period column for grouping
        df_recipient['year_month'] = df_recipient['period_of_performance_current_end_date'].dt.to_period('M')
        time_series = df_recipient.groupby('year_month')['current_total_value_of_award'].sum()
        time_series_millions = (time_series / 1e6).round(2)
        # Convert PeriodIndex to timestamps for plotting
        time_series_millions.index = time_series_millions.index.to_timestamp()
        
        plt.figure(figsize=(12, 6))
        plt.plot(time_series_millions.index, time_series_millions.values, marker='o', linestyle='-')
        plt.title(f"Time Series of Award Amounts for recipient_uei {recipient_uei_target}")
        plt.xlabel("Month")
        plt.ylabel("Total Award Amount (Millions of $)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
        
        # ------------------------------------------
        # Visualization 4: Parent Award Agency Breakdown (Pie Chart)
        # ------------------------------------------
        parent_sum = df_recipient.groupby('parent_award_agency_name')['current_total_value_of_award'].sum()
        parent_sum_millions = (parent_sum / 1e6).round(2).sort_values(ascending=False)
        
        plt.figure(figsize=(8, 8))
        parent_sum_millions.plot(kind='pie', autopct='%1.1f%%', startangle=140)
        plt.title(f"Parent Award Agency Breakdown for recipient_uei {recipient_uei_target}")
        plt.ylabel("")  # Hide the y-label for a cleaner pie chart
        plt.tight_layout()
        plt.show()
        
        # ------------------------------------------
        # Additional EDA: Summary Statistics and Data Overview
        # ------------------------------------------
        print(f"Summary Statistics for recipient_uei {recipient_uei_target}:")
        print(df_recipient.describe(include='all'))
        
        print("\nNumber of Transactions by Transaction Description:")
        print(df_recipient['transaction_description'].value_counts())
        
        print("\nUnique Awarding Agencies Involved:")
        print(df_recipient['awarding_agency_name'].unique())

    return (
        agency_sum,
        agency_sum_millions,
        df,
        df_recipient,
        parent_sum,
        parent_sum_millions,
        pd,
        plt,
        recipient_uei_target,
        selected_columns,
        time_series,
        time_series_millions,
        tx_sum,
        tx_sum_millions,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
