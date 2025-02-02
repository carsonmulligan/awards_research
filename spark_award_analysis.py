import marimo
import os
import sys

__generated_with = "0.10.19"
app = marimo.App()


@app.cell
def _():
    import marimo as mo
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import desc
    return SparkSession, desc, mo


@app.cell
def _(SparkSession):
    # Set Java Home if not set
    if not os.environ.get('JAVA_HOME'):
        # Try to find Java installation
        java_home = '/Library/Java/JavaVirtualMachines/jdk-17.jdk/Contents/Home'  # Common macOS Java location
        os.environ['JAVA_HOME'] = java_home
    
    # Initialize Spark Session with more detailed configuration
    spark = SparkSession.builder \
        .appName("Award Analysis") \
        .config("spark.driver.memory", "4g") \
        .config("spark.sql.shuffle.partitions", "4") \
        .config("spark.driver.extraJavaOptions", "-Xss4M") \
        .config("spark.executor.extraJavaOptions", "-Xss4M") \
        .config("spark.driver.host", "localhost") \
        .master("local[*]") \
        .getOrCreate()
        
    # Print Spark configuration for debugging
    print("Spark Configuration:")
    print(f"Spark Version: {spark.version}")
    print(f"Java Home: {os.environ.get('JAVA_HOME')}")
    print(f"Python Version: {sys.version}")
    
    return (spark,)


@app.cell
def _(spark):
    # Define the schema for better performance and data type control
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

    # Read CSV with PySpark
    df = spark.read.csv(
        'FY2025_All_Contracts_Full_20250107_1.csv',
        header=True,
        inferSchema=True
    ).select(selected_columns) \
    .na.drop()  # Drop rows with any null values
    return df, selected_columns


@app.cell
def _(mo):
    mo.md("""### Dataset Overview""")
    return


@app.cell
def _(mo):
    mo.md("""### Sample Data""")
    return


@app.cell
def _(df, mo):
    mo.md("### Basic Statistics")
    # Calculate basic statistics for numerical columns
    numeric_stats = df.select([
        'current_total_value_of_award',
        'total_dollars_obligated'
    ]).summary()
    return (numeric_stats,)


@app.cell
def _(desc, df, mo):
    mo.md("### Top Recipients by Total Value")
    # Group by recipient and calculate total awards
    top_recipients = df.groupBy('recipient_name') \
        .agg({'current_total_value_of_award': 'sum'}) \
        .orderBy(desc('sum(current_total_value_of_award)')) \
        .limit(10)
    return (top_recipients,)


@app.cell
def _(desc, df, mo):
    mo.md("### Awards by Agency")
    # Analyze distribution by awarding agency
    agency_distribution = df.groupBy('awarding_agency_name') \
        .count() \
        .orderBy(desc('count')) \
        .limit(10)
    return (agency_distribution,)


@app.cell
def _(spark):
    # Clean up Spark session when done
    spark.stop()
    return


if __name__ == "__main__":
    app.run()
