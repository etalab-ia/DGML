import matplotlib

matplotlib.use("Agg")

import urllib
from pathlib import Path
from typing import Dict
from fastapi import FastAPI
from sqlitedict import SqliteDict
import pandas as pd
from csv_detective.explore_csv import routine
from pandas_profiling import ProfileReport
from fastapi.responses import HTMLResponse
from logging.config import dictConfig
import logging
from config_logger import log_config

logging.config.dictConfig(log_config)
logger = logging.getLogger("api-logger")
resources_df: pd.DataFrame = pd.read_csv("./assets/dgf_resources.tar.gz", sep=";")

app = FastAPI(root_path="/profiler")


def get_profile(csv_path: Path, resource_metadata: Dict[str, str],
                csv_metadata: Dict):
    csv_id = resource_metadata["id"]
    csv_url = resource_metadata["url"]
    dataset_name = resource_metadata["dataset.title"]
    target_df = pd.read_csv(csv_path.as_posix(), sep=csv_metadata["separator"],
                            encoding=csv_metadata["encoding"])

    profile = ProfileReport(target_df, title=f"{dataset_name}:\t{csv_id}",
                            config_file="config_profiler.yml")

    profile.set_variables(dataset={"url": csv_url, "description": dataset_name})
    html_str = profile.to_html()
    return {"html": html_str, "json": profile.to_json()}


def get_resource_metadata(resource_id: str):
    resource_info = resources_df[resources_df.id == resource_id].to_dict("records")
    return resource_info[0]


def download_file(resource_metadata: str):
    logger.info(f"Trying to download file {resource_metadata['url']}")
    file_name, headers = urllib.request.urlretrieve(resource_metadata["url"])
    # TODO: check if download was successful
    return Path(file_name)


def get_csv_metadata(file_path: str):
    csv_metadata = routine(file_path, user_input_tests=None)
    # TODO : check if metadata works
    return csv_metadata


def get_report(resource_id: str, resource_url: str = None):
    cache = SqliteDict('./cache.sqlite', autocommit=True)
    try:

        # 1. Check if it is not in the cache
        if resource_id in cache and False:
            logger.info(f"Great! We found csv {resource_id} in cache")
            return cache[resource_id]

        # 2. It is not there. Let's get the download url
        if not resource_url:
            resource_metadata = get_resource_metadata(resource_id=resource_id)
            logger.info(f"Found the following info from the catalogue: {resource_metadata}")
        else:
            resource_metadata = {"id": resource_id, "resource_url": resource_url}
            logger.warning(f"Did not found any info for resource {resource_id}")

        # 3. Try to download the csv
        file_path = download_file(resource_metadata=resource_metadata)

        # 4. Get csv metadata
        csv_detective_info = get_csv_metadata(file_path)
        logger.info(f"Got csv-detective metadata")
        # 5. Get and cache profile
        report = get_profile(file_path, resource_metadata=resource_metadata,
                             csv_metadata=csv_detective_info)
        logger.info(f"Got csv profile")

        # 6. Save report in cache
        cache[resource_id] = report
        logger.info(f"Saved csv profile in sqlite db")
        return report
    except Exception as e:
        logger.error(f"Could not get pandas profiling of file {resource_id}. Error {e}")
        raise e
    finally:
        cache.close()


@app.get("/{resource_id}", response_class=HTMLResponse)
def read_item(resource_id: str, resource_url: str = None):
    report_html = get_report(resource_id=resource_id, resource_url=resource_url)["html"]
    return report_html
