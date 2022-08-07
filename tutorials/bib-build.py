import glob
import shutil
from pathlib import Path
from typing import Dict, List

import bibtexparser

try:
    shutil.rmtree("./tutorials/build")
except:
    pass

shutil.copytree("./tutorials/src", "./tutorials/build")


class BibStore:
    def __init__(self):
        with open("./tutorials/ref.bib") as bibtex_file:
            bib_database = bibtexparser.load(bibtex_file)
        self._data_dict = self._store_database(bib_database.entries)

    def _store_database(self, bib_database: List[dict]) -> Dict[str, str]:
        data_dict = dict()
        for bib_item in bib_database:
            data_dict.update({bib_item["ID"]: bib_item})
        return data_dict

    def get(self, ID: str):
        return self._data_dict[ID]


class ReferenceMaker:
    def __init__(self):
        pass

    def value(self, bib_dict: Dict[str, str]) -> str:
        declare_block = "#    Author\n"
        declare_block += f'#       {bib_dict["author"]}. \n'
        declare_block += "#    Title\n"
        declare_block += f'#       *{bib_dict["title"]}*, \n'
        declare_block += f'#     {bib_dict["journal"]}, \n'
        declare_block += f'#     {bib_dict["year"]}. \n'
        declare_block += f'#     :numref:`{bib_dict["doi"]}`. \n'
        return declare_block


bib_database = BibStore()
ref_maker = ReferenceMaker()
files = glob.glob("./tutorials/build/**/*")

for file in files:
    print(file)
    read_write_path = Path(file)

    # 読み込み
    content = read_write_path.read_text()

    # 置換
    content = content.replace(
        "# THOMPSON199093", ref_maker.value(bib_database.get("THOMPSON199093"))
    )

    # 書き出し
    read_write_path.write_text(content)
