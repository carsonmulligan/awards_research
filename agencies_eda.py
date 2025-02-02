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

    # --- Data loading code (same as before) ---
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

    df = pd.read_csv(
        'FY2025_All_Contracts_Full_20250107_1.csv',
        usecols=selected_columns,
        # nrows=1000
    ).dropna()

    df['period_of_performance_current_end_date'] = pd.to_datetime(
        df['period_of_performance_current_end_date'], errors='coerce'
    )

    # Get the sorted unique agency names and print them
    agency_names = sorted(df['awarding_agency_name'].unique())
    print("Available Awarding Agencies:")
    for i, agency in enumerate(agency_names, 1):
        print(f"{i}. {agency}")

    # Ask the user to input a number corresponding to an agency
    agency_index = int(input("Select an agency by entering its number: ")) - 1
    if 0 <= agency_index < len(agency_names):
        agency_name = agency_names[agency_index]
    else:
        print("Invalid selection. Exiting.")
        exit()

    # --- Analysis function (same as before, with amounts in millions) ---
    def analyze_agency(agency_name):
        df_agency = df[df['awarding_agency_name'] == agency_name].copy()
        
        if df_agency.empty:
            print(f"\nNo records found for {agency_name}.")
            return
        
        # Group by recipient and sum the current_total_value_of_award
        recipient_sum = df_agency.groupby('recipient_name')['current_total_value_of_award'].sum()
        recipient_sum_millions = (recipient_sum / 1e6).round(2)
        
        print(f"\nTotal Award Amounts by Recipient for {agency_name} (in Millions):")
        for recipient, amount in recipient_sum_millions.sort_values(ascending=False).items():
            print(f"{recipient}: ${amount:,.2f}M")
        
        # Bar Chart: Top 10 Recipients
        top10 = recipient_sum_millions.sort_values(ascending=False).head(10)
        plt.figure(figsize=(10, 6))
        top10.plot(kind='bar', color='skyblue')
        plt.ylabel('Award Amount (Millions of $)')
        plt.title(f"Top 10 Recipients by Award Amount\n({agency_name})")
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        plt.show()
        
        # Pie Chart: Award Share for Top 10 Recipients
        plt.figure(figsize=(8, 8))
        top10.plot(kind='pie', autopct='%1.1f%%', startangle=140, pctdistance=0.85)
        plt.ylabel('')
        plt.title(f"Award Share of Top 10 Recipients\n({agency_name})")
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        fig = plt.gcf()
        fig.gca().add_artist(centre_circle)
        plt.tight_layout()
        plt.show()
        
        # Time Series: Awards Over Time
        df_agency['year_month'] = df_agency['period_of_performance_current_end_date'].dt.to_period('M')
        time_series = df_agency.groupby('year_month')['current_total_value_of_award'].sum()
        time_series_millions = (time_series / 1e6).round(2)
        time_series_millions.index = time_series_millions.index.to_timestamp()
        
        plt.figure(figsize=(12, 6))
        plt.plot(time_series_millions.index, time_series_millions.values, marker='o', linestyle='-')
        plt.xlabel("Month")
        plt.ylabel("Award Amount (Millions of $)")
        plt.title(f"Time Series of Award Amounts\n({agency_name})")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    # Run the analysis for the selected agency
    analyze_agency(agency_name)

    return (
        agency,
        agency_index,
        agency_name,
        agency_names,
        analyze_agency,
        df,
        i,
        pd,
        plt,
        selected_columns,
    )


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
