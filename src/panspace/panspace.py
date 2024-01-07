"""Tool panspace"""

from enum import Enum
import typer
from typing_extensions import Annotated
from typing import Optional

# import yaml
import json

import numpy as np
from pathlib import Path

# types for typer
from .trainer import app as app_trainer
from .index import app as app_index

app = typer.Typer()
app.add_typer(app_index, name="index")
app.add_typer(app_trainer, name="trainer")

@app.command("docs", help="Open documentation webpage")
def github():
    typer.launch("https://github.com/jorgeavilacartes/embedding-bacteria")