import re
import shutil
import tempfile
import unicodedata
import zipfile
from pathlib import Path


def load_zip_file(zip_file: Path):
    tmp_dir = tempfile.TemporaryDirectory()
    zip = zipfile.ZipFile(zip_file)
    zip_path = zip.extract(member=zip.filelist[0].orig_filename, path=tmp_dir.name)
    return Path(zip_path), tmp_dir


def slugify(value, allow_unicode=False):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py Convert to ASCII if 'allow_unicode' is
    False. Convert spaces or repeated dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize("NFKC", value)
    else:
        value = (
            unicodedata.normalize("NFKD", value)
            .encode("ascii", "ignore")
            .decode("ascii")
        )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
