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
import os
import subprocess
import typer

from pathlib import Path
from rich import print 
from rich.console import Console
from rich.markdown import Markdown
from rich.progress import track
from typing_extensions import Annotated
from typing import Optional

from panspace import version as VERSION
from panspace.trainer import app as app_trainer
from panspace.index import app as app_index
from panspace.data_curation import app as app_data_curation
from panspace.stats_assembly import app as app_stats_assembly
from panspace.fcgr import app as app_fcgr

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
    console.rule("[bold blue]Running Streamlit Application")
    console.print(Markdown("## panspace"))
    console.print("Starting Streamlit application...")
    
    # Get absolute path to the Streamlit app relative to this file
    current_dir = Path(__file__).resolve().parent
    path_app = current_dir / "streamlit" / "app.py"    
    os.system(f"streamlit run {path_app}")


@app.command("query-smk")
def run_pipeline(
    dir_sequences: Annotated[Path, typer.Option(help="Path to input sequences directory")] = ...,
    path_encoder: Annotated[Path, typer.Option(help="Path to encoder weights (.keras) file")] = ...,
    path_index: Annotated[Path, typer.Option(help="Path to FAISS or index file")] = ...,
    fcgr_bin: Annotated[Optional[Path], typer.Option(help="Path to FCGR binary. Only used if --fast-version is used")] = None,
    kmer: Annotated[int, typer.Option(help="K-mer size")] = 8,
    mask: Annotated[str, typer.Option(help="Mask pattern for k-mers")] = "11111111",
    neighbors: Annotated[int, typer.Option(help="Number of neighbors")] = 11,
    preprocessing: Annotated[str, typer.Option(help="Preprocessing method")] = "clip_scale_zero_one",
    percentile_clip: Annotated[int, typer.Option(help="Percentile for clipping")] = 80,
    outdir: Annotated[Path, typer.Option(help="Output directory")] = "test-query/",
    gpu: Annotated[bool, typer.Option(help="Use GPU if available")] = False,
    kmc_threads: Annotated[int, typer.Option(help="Number of KMC threads")] = 2,
    cores: Annotated[int, typer.Option(help="total number of cores to use")] = 8,
    fast_version: Annotated[bool, typer.Option(help="")] = False,
):
    """
    Run the Snakemake pipeline with the specified configuration.
    """
    assert dir_sequences.is_dir()
    assert path_encoder.is_file()
    assert path_index.is_file()
    assert fcgr_bin.is_file()

    current_dir = Path(__file__).resolve().parent
    pipeline_version = "query_fast.smk" if fast_version else "query.smk" 
    snakefile = current_dir / "pipelines" / pipeline_version

    cmd = [
        "snakemake",
        "--snakefile", str(snakefile),
        "--cores", str(cores),
        "--use-conda",
        "--config",
        f"dir_sequences={str(dir_sequences)}",
        f"kmer={kmer}",
        f"mask={mask}",
        f"neighbors={neighbors}",
        f"preprocessing={preprocessing}",
        f"percentile_clip={percentile_clip}",
        f"path_encoder={str(path_encoder)}",
        f"path_index={str(path_index)}",
        f"outdir={str(outdir)}",
        f"gpu={str(gpu)}",
        f"kmc_threads={kmc_threads}",
        f"fcgr_bin={str(fcgr_bin)}",
        "--rerun-incomplete"
    ]

    typer.echo(f"Running Snakemake pipeline:\n{' '.join(cmd)}")
    subprocess.run(cmd, check=True)

if __name__ == "__main__":
    app()