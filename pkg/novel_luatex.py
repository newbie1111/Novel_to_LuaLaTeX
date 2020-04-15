import requests  # install
from bs4 import BeautifulSoup  # install
from abc import ABCMeta
from abc import abstractmethod
import json
from collections import OrderedDict


class Novel_LuaTeX(metaclass=ABCMeta):

    def __init__(self, url):
        self.main_soup = self.get_soup(url=url)

    def get_soup(self, url):
        __HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}
        res = requests.get(url=url, headers=__HEADERS)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")
        return soup

    def set_json(self, save_path, table_of_contents):
        with open(save_path, "w", encoding="utf-8") as f:
            json.dump(table_of_contents, f, ensure_ascii=False, indent=4)

    def get_json(self, load_path):
        try:
            with open(load_path, "r", encoding="utf-8") as f:
                return json.load(f, object_pairs_hook=OrderedDict)
        except Exception as identifier:
            print(identifier)
            return None

    @abstractmethod
    def get_works_title(self):
        pass

    @abstractmethod
    def get_works_author(self):
        pass

    @abstractmethod
    def get_unique_code(self):
        pass

    @abstractmethod
    def get_table_of_contents(self):
        pass

    @abstractmethod
    def get_episode_text(self, ep_soup):
        pass

    @abstractmethod
    def set_novel():
        pass
