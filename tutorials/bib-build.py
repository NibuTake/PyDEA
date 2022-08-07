import glob
import re
import shutil
from pathlib import Path
from typing import Dict, List

import bibtexparser


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
        declare_block += f"#     :numref:`{self._get_url(bib_dict)}`. \n"
        return declare_block

    def _get_url(self, bib_dict: Dict[str, str]) -> str:
        keys = list(set(["doi", "url"]) & set(bib_dict.keys()))
        if len(keys) > 0:
            return bib_dict[keys[0]]
        else:
            return "---"


class Replacer:
    def __init__(self, content: str):
        self._start = "# <bib>"
        self._end = "</bib>"
        reg = re.compile(rf"{self._start}.+{self._end}")
        self.matched_IDs = reg.findall(content)
        self._content = content
        self.ref_maker = ReferenceMaker()

    @property
    def content(self) -> str:
        print(self.matched_IDs)

        for matched_ID in self.matched_IDs:
            bib_item = bib_database.get(self._get_ID(matched_ID))
            embed_content = self.ref_maker.value(bib_item)
            self._content = self._content.replace(matched_ID, embed_content)
        return self._content

    def _get_ID(self, matched_ID: str):
        return matched_ID[len(self._start) : -len(self._end)]


if __name__ == "__main__":
    try:
        shutil.rmtree("./tutorials/build")
    except:
        pass

    shutil.copytree("./tutorials/src", "./tutorials/build")

    bib_database = BibStore()
    files = glob.glob("./tutorials/build/**/*")

    for file in files:
        print(file)

        read_write_path = Path(file)
        content = read_write_path.read_text()
        replacer = Replacer(content)
        read_write_path.write_text(replacer.content)
