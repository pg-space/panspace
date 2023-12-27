def main(args):
    from pathlib import Path
    import tensorflow as tf

    path_chkpt = args.path_chkpt 
    dirsave   = args.dirsave
    autoencoder = tf.keras.models.load_model(path_chkpt)

    # Encoder-Decoder
    encoder = tf.keras.models.Model(autoencoder.input,autoencoder.get_layer("output_encoder").output)
    decoder = tf.keras.models.Model(autoencoder.get_layer("input_decoder").input, autoencoder.output)

    # save encoder and decoder
    path_save_models = Path(dirsave)
    path_save_models.mkdir(exist_ok=True, parents=True)
    encoder.save(path_save_models.joinpath("encoder.keras"))
    decoder.save(path_save_models.joinpath("decoder.keras"))

if __name__ == "__main__":
    import argparse
    from rich_argparse import RichHelpFormatter
    
    ## Parser
    parser = argparse.ArgumentParser(
                description="Get Encoder and Decoder from Autoencoder", 
                prog="Encoder-Decoder", 
                formatter_class=RichHelpFormatter
                )
    parser.add_argument("--path-chkpt", dest="path_chkpt", type=str, default=None, required=True,
                        help="path to checkpoint"
                        )
                    
    parser.add_argument("--dir-save", dest="dirsave", type=str, default=None, required=True,
                        help="directory to save encoder and decoder models"
                        )

    args = parser.parse_args()

    main(args)