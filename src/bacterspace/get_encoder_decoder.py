import typer 
from typing_extensions import Annotated
from pathlib import Path

app = typer.Typer()

@app.command(help="Save encoder and decoder as separated models")
def main(path_checkpoint: Annotated[Path, typer.Option("--path-checkpoint","-chkpt", help="path to .keras model")],
         dirsave: Annotated[Path, typer.Option("--dirsave","-ds", help="directory to save encoder.keras and decoder.keras")],
         ):
    from pathlib import Path
    import tensorflow as tf

    autoencoder = tf.keras.models.load_model(path_checkpoint)

    # Encoder-Decoder
    encoder = tf.keras.models.Model(autoencoder.input,autoencoder.get_layer("output_encoder").output)
    decoder = tf.keras.models.Model(autoencoder.get_layer("input_decoder").input, autoencoder.output)

    # save encoder and decoder
    path_save_models = Path(dirsave)
    path_save_models.mkdir(exist_ok=True, parents=True)
    encoder.save(path_save_models.joinpath("encoder.keras"))
    decoder.save(path_save_models.joinpath("decoder.keras"))