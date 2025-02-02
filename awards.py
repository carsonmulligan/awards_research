import marimo

__generated_with = "0.10.19"
app = marimo.App(width="medium")


app._unparsable_cell(
    r"""
    pip install openai

    """,
    name="_"
)


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _(spark):
    df = spark.table('/Users/carsonmulligan/Desktop/Projects/Reseach Projects/Award_Research/FY2025_All_Contracts_Full_20250107_1.csv')
    return (df,)


app._unparsable_cell(
    r"""
    !pip install openai
    """,
    name="_"
)


@app.cell
def _():
    return


app._unparsable_cell(
    r"""
    load in FY2025_All_Contracts_Full_20250107_1.csv as a pandas data frame and show the fields so i can group by and do viz 

    """,
    name="_"
)


if __name__ == "__main__":
    app.run()
