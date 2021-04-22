import requests
import pandas as pd
import os


def latest_catalog():
    """This function returns the pandas dataframe of the latest version of dgf resource catalog
    (https://www.data.gouv.fr/en/datasets/catalogue-des-donnees-de-data-gouv-fr/#_)"""
    #dgf_catalog = 'https://www.data.gouv.fr/fr/datasets/r/4babf5f2-6a9c-45b5-9144-ca5eae6a7a6d'  # latest url of the catalog
    dgf_catalog = './latest_dgf_catalog.zip' # latest downloaded csv
    dgf_catalog_df = pd.read_csv(dgf_catalog, delimiter=";", compression='zip',error_bad_lines=False)
    pd.set_option('display.max_colwidth', None)  # to stop pandas from "cutting" long urls
    return dgf_catalog_df


def fixed_catalog():
    """This function returns the pandas dataframe containg a 'catalog' of our datasets"""
    dgf_catalog_df = pd.read_csv('catalog.csv')
    pd.set_option('display.max_colwidth', None)  # to stop pandas from "cutting" long urls
    return dgf_catalog_df


def info_from_catalog(id: str, catalog: pd.DataFrame):
    """This function returns a dictionary containing : the resource url, the resource format and the url of its data.gouv.fr page
    --------------------------------------------
    :param:     id: id of the dgf resource
    :type:      id: string"""

    url = catalog[catalog['id'] == id]['url']
    if url.empty:
        raise Exception(f"The dataset with id {id} was not found in DGF catalog")
    url = url.values.item()

    file_format = catalog[catalog['id'] == id]['format'].values.item()
    dgf_page = catalog[catalog['id'] == id]['dataset.url'].values.item()
    format_is_nan = catalog[catalog['id'] == id]['format'].isnull().values.any()
    catalog_dict = {'url_resource': url, 'format': file_format, 'url_dgf': dgf_page, 'format_is_nan': format_is_nan}
    return catalog_dict


def is_referenced(url, id, catalog_info):
    """Given the url of  a resource from the catalog, this function returns True if the resource is referenced by data.gouv.fr
    False otherwise
    :param      :url: url of a resource in the catalog
    :type       :url: string"""
    dgf_page = catalog_info['url_dgf']
    headers = requests.head(url).headers
    downloadable = 'attachment' in headers.get('Content-Disposition', '')
    # download_zip = 'application/zip' in headers.get('Content-Type','')
    if downloadable == False:
        if os.path.isfile(f'./datasets/resources/{id}/{id}.csv') == False:
            raise Exception(f'This id is associated to a dataset not referenced by data.gouv.fr. \n '
                            f'Please download the dataset from here: {dgf_page}\n'
                            f'Then manually upload it in the corresponding folder and name it: {id}.csv')
    return downloadable


def detect_csv(request):
    """Given the url request for a csv or txt file, this function returns a dictionary containing the csv encoding and separator.
    -------------------------------------------
    :param        url: url containing the csv
    :type         url: string"""
    text = request.text[0:100]
    encoding = request.encoding
    if ";" in text:
        sep = ";"
    elif "," in text:
        sep = ","
    elif "|" in text:
        sep = "|"
    elif "\t" in text:
        sep = "\t"
    else:
        raise TypeError('separator not detected')
    url_dict = {'encoding': encoding, 'separator': sep}
    return url_dict


def load_dataset(id, catalog_info, output_dir):
    """This function loads a csv in the datasets folder/creates a pandas dataframe given its id if the dataset is referenced by data.gouv.fr.
    Otherwise, you get an error and you should manually upload it.
    Remark: on data.gouv.fr, datasets are available in various "formats": json, shp, csv, zip, document, xls, pdf, html, xlsx,geojson etc.
    to this day, our repository only contains files with .csv,.txt, .xls extensions, therefore we only treat these extensions.
    -------------------
    :param:     id: id of the dgf resource (must be a txt, csv or xls file)
    :type:      id: string"""
    url = catalog_info['url_resource']
    referenced = is_referenced(url=url, id=id, catalog_info=catalog_info)
    if referenced is True:  # if the dataset is referenced
        file_format = catalog_info['format']
        format_is_nan = catalog_info['format_is_nan']
        request = requests.get(url)
        delimiter = detect_csv(request)['separator']
        encoding = detect_csv(request)['encoding']
        if file_format == 'csv' or format_is_nan:  # if the format is not available on dgf, we assume it is a csv by default
            if url.rsplit('.', 1)[-1] == 'zip':
                dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='zip',
                                        error_bad_lines=False)
            elif url.rsplit('.', 1)[-1] == 'gz':
                dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='gzip',
                                        error_bad_lines=False)
            elif url.rsplit('.', 1)[-1] == 'bz2':
                dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='bz2',
                                        error_bad_lines=False)
            elif url.rsplit('.', 1)[-1] == 'xz':
                dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='xz',
                                        error_bad_lines=False)
            else:
                dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding)
        elif file_format == 'txt':
            dataframe = pd.read_table(url, sep=delimiter, encoding=encoding)
        elif (file_format == 'xls') or (file_format == 'xlsx'):
            dataframe = pd.read_excel(url, sheet_name=None)
        elif file_format == 'zip':
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='zip',
                                    error_bad_lines=False)
        elif file_format == 'gz':
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='gzip',
                                    error_bad_lines=False)
        elif file_format == 'bz2':
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='bz2',
                                    error_bad_lines=False)
        elif file_format == 'xz':
            dataframe = pd.read_csv(url, sep=None, engine='python', encoding=encoding, compression='xz',
                                    error_bad_lines=False)
        else:
            raise TypeError(
                'Please choose a dataset that has one of the following extensions: .csv, .txt, .xls or choose '
                'a compressed file having one of these extensions.')

        dataframe.to_csv(output_dir.joinpath(f"{id}.csv"))
        return dataframe
    else:
        dataframe = pd.read_csv(f"./datasets/resources/{id}/{id}.csv", sep=None, engine='python')
        return dataframe

# Remark on separators detection : the 'python engine' in pd.read_csv/read_table  works pretty well most of the time. However, it does not handle well some
# exceptions (see for instance the dataset: 90a98de0-f562-4328-aa16-fe0dd1dca60f).
# Improvements/to do: detect_csv:  separators detection should be handled better (not very robust, possibly does not cover all the exceptions)
