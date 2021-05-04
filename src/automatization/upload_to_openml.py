'''
This script uploads our datasets into openml with its API. It then produces a python snippet
to be pasted in the web page to import the dataset via sklearn through openml

Usage:
    my_script.py <datasets_folder> <output_snippet_folder> [options]

Arguments:
    <datasets_folder>                     A folder with dgf resources ids and csv files wtihin
    <output_snippet_folder>                     A folder with dgf resources ids and csv files wtihin
'''
import logging
import os
from glob import glob
from pathlib import Path

from argopt import argopt
from tqdm import tqdm


def run(doc_path):
    return 1


def main(datasets_folder: Path, output_snippet_folder: Path, n_jobs: int):
    doc_paths = []
    job_output = []
    if not datasets_folder.exists():
        raise FileNotFoundError(datasets_folder.as_posix())
    if not output_snippet_folder.exists():
        raise FileNotFoundError(output_snippet_folder.as_posix())



    for doc_path in tqdm(doc_paths):
        tqdm.write(f"Converting file {doc_path}")
        job_output.append(run(doc_path))

    logging.info(
        f"{sum(job_output)} DOC files were converted to TXT. {len(job_output) - sum(job_output)} files "
        f"had some error.")

    return doc_paths


if __name__ == '__main__':
    parser = argopt(__doc__).parse_args()
    datasets_folder = Path(parser.datasets_folder)
    output_snippet_folder = Path(parser.output_snippet_folder)
    main(datasets_folder=datasets_folder, output_snippet_folder=output_snippet_folder)
