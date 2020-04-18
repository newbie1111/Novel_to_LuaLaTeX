import re
import time
from collections import OrderedDict
import json
import pathlib
import io
import requests  # pip install
from bs4 import BeautifulSoup  # pip install
import img2pdf  # pip install
from PIL import Image  # pip install
import novel_luatex
import novel_maker


class Hameln(novel_luatex.Novel_LuaTeX):
    def __init__(self, url):
        super().__init__(url)
        self.root_dir = "./hameln/" + self.get_unique_code()
        self.image_dir = self.root_dir + "/pic"

    def is_save_dir_exists(self):
        return pathlib.Path(self.root_dir + "/toc.json").exists()

    def get_works_title(self):
        return self.main_soup.select_one("span[itemprop=name]").get_text()

    def get_works_author(self):
        return self.main_soup.select_one("span[itemprop=author]").get_text()

    def get_unique_code(self):
        unique_code = self.main_soup.select_one(
            "meta[property='og:url']")["content"]
        unique_code = re.sub(".+/novel/(.+)/", r"\1", unique_code)
        return unique_code

    def get_table_of_contents(self):
        table_of_contents = OrderedDict({"": OrderedDict({})})
        now_chapter = ""

        for tag in self.main_soup.select("tr td strong , tr td a"):
            if tag.name == "strong":
                now_chapter = tag.string.replace("\u3000", " ")
                table_of_contents.update(OrderedDict(
                    {now_chapter: OrderedDict({})}))
            elif tag.name == "a":
                title = tag.string.replace("\u3000", " ")
                href = re.sub("\.(/.+)",
                              "https://syosetu.org/novel/"
                              + self.get_unique_code()
                              + r"\1",
                              tag["href"])
                table_of_contents[now_chapter].update(
                    OrderedDict({title: href}))

        return table_of_contents

    def get_episode_text(self, ep_soup):
        pass

    def set_episode_image(self, ep_soup):
        image_links = [img["href"] for img in ep_soup.select(
            "div #honbun > p > a[alt='挿絵'][name='img']")]

        if not pathlib.Path(self.image_dir).exists():
            pathlib.Path(self.image_dir).mkdir(parents=True)

        for link in image_links:
            image = Image.open(io.BytesIO(
                requests.get(link).content)).convert("RGB")
            image_name = re.sub(".+/(.+)\..+", r"\1.pdf", link)
            image.save(self.image_dir + "/" + image_name)
            print("\t\t[image] -> "
                  + "(" + self.image_dir + "/" + image_name + ")")

        """
        WARNING:root:Image contains transparency which cannot be retained in PDF.
        WARNING:root:img2pdf will not perform a lossy operation.
        WARNING:root:You can remove the alpha channel using imagemagick:
        WARNING:root:  $ convert input.png -background white -alpha remove -alpha off output.png
        img2pdf.AlphaChannelError: Refusing to work on images with alpha channel

        ValueError: cannot save mode RGBA
        """

    def get_escaped_text(self, text):
        return re.sub(r"([#$%&_^{}\[\]])", r"\\\1", text)

    def set_novel(self, batchmode=False, update=False):
        novel = novel_maker.Novel_maker(self.root_dir,
                                        self.get_works_title(),
                                        self.get_works_author())
        toc = self.get_table_of_contents()
        prev_toc = self.get_json(self.root_dir + "/toc.json")

        novel.begin_document()
        for chap_num, chap in enumerate(toc.keys()):
            chap_dir = ""
            if chap:
                chap_dir = "/chap" + str(chap_num)
                novel.set_chapter(self.get_escaped_text(chap))
                print("[chapter] -> " + chap)

            for sec_num, sec in enumerate(toc[chap].keys()):
                save_dir = self.root_dir + "/tex" + chap_dir
                tex_path = save_dir + "/ep" + str(sec_num) + ".tex"
                sec_text = ""

                print("\t[episode] -> " + sec + "(" + tex_path + ")", end=" ")
                novel.set_section(self.get_escaped_text(sec))
                if update:
                    try:
                        prev_toc[chap][sec]
                    except KeyError as ke:
                        print("<new>", end="")
                        # time.sleep(1)
                        ep_soup = self.get_soup(toc[chap][sec])
                        #sec_text = self.get_episode_text(ep_soup)
                        self.set_episode_image(ep_soup)
                else:
                    # time.sleep(1)
                    ep_soup = self.get_soup(toc[chap][sec])
                    #sec_text = self.get_episode_text(ep_soup)
                    self.set_episode_image(ep_soup)
                novel.set_text(sec_text, tex_path)
                print("done.")

        novel.end_document()
        # novel.compile(batchmode)
        self.set_json(self.root_dir + "/toc.json", toc)


if __name__ == "__main__":
    print("hameln")
    data = Hameln(input())
    update = True
    batchmode = False

    print("works title  : " + data.get_works_title())
    print("works author : " + data.get_works_author())

    if data.is_save_dir_exists():
        print("更新モードが使用できます。使用しますか？[Y/N]")
        update = True if re.match("[Yy]", input()) else False
    else:
        print("新しくダウンロードする小説です。")
        update = False

    print("LuaTeXのコンパイルのログを表示しますか？[Y/N]")
    batchmode = False if re.match("[Yy]", input()) else True

    data.set_novel(batchmode, update)
