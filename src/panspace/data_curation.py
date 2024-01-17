import typer 
from typing_extensions import Annotated
from pathlib import Path 

from rich.progress import track
from rich import print 
from rich.console import Console

console=Console()
app = typer.Typer(help="Find outliers and mislabaled samples.")