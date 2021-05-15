import typing as t
from pathlib import Path

import camelot
import pandas as pd
import typer

app = typer.Typer()


def normalize_dataframes(dataframes: t.List[pd.DataFrame]) -> pd.DataFrame:
    """Correct scraping errors in extracted table that spans multiple pages, and concatenate them."""
    # the first row really ought to be the header names and also has spurious whitespace.
    colnames = [c.replace("\n", "") for c in dataframes[0].iloc[0]]
    dataframes[0].drop(0, inplace=True)
    res = pd.concat(dataframes, ignore_index=True)
    res.columns = colnames
    return res


@app.command()
def convert_pdf(
    pdf: Path = typer.Argument(
        ..., max=1, exists=True, file_okay=True, dir_okay=False, resolve_path=True, formats=["pdf"]
    ),
    to: Path = typer.Option(..., exists=False, file_okay=True, dir_okay=False, resolve_path=True, formats=["csv"]),
):
    """Convert a MWRA BioBot data PDF into a CSV for further analysis."""
    typer.echo(f"Extracting data from {pdf.name} ...")
    tables = camelot.read_pdf(str(pdf), pages="all")
    typer.echo(f"Normalizing data ...")
    res = normalize_dataframes([t.df for t in tables])
    res.to_csv(to, index=False)
    typer.echo(f"Wrote {to}")
