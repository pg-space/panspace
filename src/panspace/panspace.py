"""Tool panspace"""

MARKDOWN = """
# `panspace` WHAT-TO-DO?   
- `panspace` is a tool for building and querying an embedding-based index for assemblies. 

- It trains a model (autoencoder) to create a vector representation of the k-mer distributions of each assembly
in a low dimensional space (default dim=256), the 'panspace'.

- `panspace` represents each k-mer distribution of an assembly with its FCGR representation.

- Once an autoencoder is trained, the Encoder is removed and used to map the assemblies to the embedding space. 

A step-by-step guide to help you

With no labels, the way to go is to use the AutoencoderFCGR:

1. Create FCGR dataset | `panspace trainer fcgr --help`
2. Train Autoencoder | `panspace trainer train-autoencoder --help`
3. Extract Encoder  | `panspace trainer split-autoencoder --help`
4. Create Index | `panspace index create --help`
5. Query Index | `panspace index query --help`

If you have labels for your assemblies, the way to go is with to train the CNNFCGR architecture with Metric Learning

1. Create FCGR dataset | `panspace trainer fcgr --help`
2. Train CNNFCGR | `panspace trainer metric-learning --help`
4. Create Index | `panspace index create --help`
5. Query Index | `panspace index query --help`
"""
import typer

from panspace import version as VERSION

# types for typer
from panspace.trainer import app as app_trainer
from panspace.index import app as app_index
from panspace.data_curation import app as app_data_curation
from panspace.stats_assembly import app as app_stats_assembly
from panspace.fcgr import app as app_fcgr


from rich.progress import track
from rich import print 
from rich.console import Console
from rich.markdown import Markdown

console=Console()
app = typer.Typer(name="panspace",rich_markup_mode="rich", 
                  help=f"""
                        :cat: Welcome to [blue bold]pan[/blue bold][green bold]space[/green bold] (version {VERSION}),
                        a tool for Indexing and Querying a bacterial [blue bold]pan-genome[/blue bold]
                        based on [green bold]embeddings[/green bold]
                        """)
app.add_typer(app_index, name="index")
app.add_typer(app_trainer, name="trainer")
app.add_typer(app_data_curation, name="data-curation")
app.add_typer(app_stats_assembly, name="stats-assembly")
app.add_typer(app_fcgr, name="fcgr")

@app.command("docs", help=f"Open documentation webpage.")
def github() -> None:
    typer.launch("https://github.com/pg-space/panspace")

@app.command("what-to-do", help=":cat: If you are new here, check this step-by-step guide")
def what_to_do() -> None:
    md = Markdown(MARKDOWN)
    console.print(
        md
    )

@app.command("utils", help="Extract info from text or log files")
def info_from_logs(path_log) -> None:
    from .utils import LogInfo
    loginfo = LogInfo()
    console.print(
        loginfo(path_log)
    )

@app.command("app",help="Run streamlit app")
def run_streamlit() -> None:
    import os
    from pathlib import Path

    console.rule("[bold blue]Running Streamlit Application")
    console.print(Markdown("## panspace"))
    console.print("Starting Streamlit application...")
    
    # Get absolute path to the Streamlit app relative to this file
    current_dir = Path(__file__).resolve().parent
    path_app = current_dir / "streamlit" / "app.py"    
    os.system(f"streamlit run {path_app}")


if __name__ == "__main__":
    app()