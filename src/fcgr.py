import argparse
from rich_argparse import RichHelpFormatter

from fcgr.fcgr_from_tar import FCGRFromTar

from pathlib import Path
from tqdm import tqdm
from rich.progress import track
from concurrent.futures import ThreadPoolExecutor, as_completed

## Parser
parser = argparse.ArgumentParser(
            description="generate FCGR", 
            prog="fcgr", 
            formatter_class=RichHelpFormatter
            )
parser.add_argument("-k", "--kmer", dest="kmer", type=int, default=6,
                     help="kmer size, the FCGR will be of size (2^kmer,2^kmer). Default 6"
                    )
                
parser.add_argument("--path-fcgr", dest="path_fcgr", type=str, default=None, required=False,
                    help="""directory where to save fcgr generated. A subfolder for each specie will be created inside. \n 
                    if not provided data/fcgr-<kmer>mer will be created"""
                    )

parser.add_argument("--path-tarfile", dest="path_tarfile", type=str, default=None, required=False,
                    help="path to tarfile, it should contain one or several fasta files"
                    )

parser.add_argument("--dir-tarfiles", dest="dir_tarfiles", type=str, default=None, required=False,
                    help="path to tarfile, it should contain one or several fasta files"
                    )

parser.add_argument("-w", "--workers", dest="workers", type=int, default=1, required=False,
                    help="number of workers to use with ThreadPoolExecutor in case --dir-tarfile is provided"
)

args = parser.parse_args()

if __name__=="__main__":
    assert any([args.path_tarfile is not None, args.dir_tarfiles is not None]), "at least one of --path-tarfile or --dir-tarfiles must be provided"
    fcgr = FCGRFromTar(args.kmer, args.path_fcgr)

    # if one tarfile is provided
    if args.path_tarfile is not None:
        fcgr.fcgr_from_tar(args.path_tarfile, progress=track)

    # if a directory of tar files is provided
    elif args.dir_tarfiles is not None:
        tarfiles = list(Path(args.dir_tarfiles).rglob("*tar.xz"))
        n_tars = len(tarfiles)  # Number of iterations required to fill pbar
        
        
        pbar = tqdm(total=n_tars, desc='number of tarfiles')  # Init pbar
        with ThreadPoolExecutor(max_workers=args.workers) as executor:
            for result in executor.map(fcgr.fcgr_from_tar, tarfiles):
                pbar.update(n=1)
                print(result)
