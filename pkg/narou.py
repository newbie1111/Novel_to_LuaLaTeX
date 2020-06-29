import re
import time
from collections import OrderedDict
import json
import pathlib
import requests  # install
from bs4 import BeautifulSoup  # install
import img2pdf  # install
import novel_luatex
import novel_maker


class Narou(novel_luatex.Novel_LuaTeX):

    def __init__(self, url):
        super().__init__(url)
        self.root_dir = "./narou/" + self.get_unique_code()
        self.image_dir = self.root_dir + "/pic"

    def is_save_dir_exists(self):
        return pathlib.Path(self.root_dir + "/toc.json").exists()

    def get_works_title(self):
        return self.main_soup.select_one("p.novel_title").get_text()

    def get_works_author(self):
        return self.main_soup.select_one("div.novel_writername").a.get_text()

    def get_unique_code(self):
        return re.sub("/(n.+)/.+", r"\1", self.main_soup.select_one("dd.subtitle").a["href"])

    def get_table_of_contents(self):
        table_of_contents = OrderedDict({"": OrderedDict({})})
        now_chapter = ""

        for tag in self.main_soup.select("div.chapter_title , dd.subtitle"):
            if "chapter_title" in tag["class"]:
                now_chapter = tag.string.replace("\u3000", " ")
                table_of_contents.update(OrderedDict(
                    {now_chapter: OrderedDict({})}))
            elif "subtitle" in tag["class"]:
                title = tag.a.string.replace("\u3000", " ")
                href = "https://ncode.syosetu.com" + tag.a["href"]
                table_of_contents[now_chapter].update(
                    OrderedDict({title: href}))

        return table_of_contents

    def get_episode_text(self, ep_soup):
        ep = "\\\\\n".join(
            [str(txt) for txt in ep_soup.find_all("p", id=re.compile("^L\d+"))])

        ep = re.sub(r"([#$%&_^{}\[\]])", r"\\\1", ep)
        ep = re.sub("<a href=\".+/(i.+)/\".*?>.*?</a>",
                    r"\\begin{figure}\n"
                    + r"\\begin{center}\n"
                    + r"\\begin{minipage}<y>[htbp]{93mm}\n"
                    + r"\\includegraphics[width=93mm]{"
                    + str(pathlib.Path(self.image_dir).resolve()
                          ).replace("\\", "/")
                    + r"/\1}"
                    + r"\\end{minipage}\n"
                    + r"\\end{center}\n"
                    + r"\\end{figure}\n",
                    ep)
        ep = ep.replace("<ruby><rb>", "\\ruby[g]{")
        ep = re.sub("</rb><rp>[(（《]</rp><rt>", "}{", ep)
        ep = re.sub("</rt><rp>[)）》]</rp></ruby>", "}", ep)
        ep = re.sub("\\ruby[g]{\s+?", "\\ruby[g]{", ep)
        ep = re.sub("\s+?}", "}", ep)
        ep = re.sub("<.??span>|<.??p.*?>|<br/>", "", ep)
        return ep.replace("\u3000", " ")

    def set_episode_image(self, ep_soup):
        image_links = ["https:" + img["href"]
                       for img in ep_soup.select("div.novel_view p a")]

        if not pathlib.Path(self.image_dir).exists():
            pathlib.Path(self.image_dir).mkdir(parents=True)

        for link in image_links:
            image_soup = self.get_soup(link)
            image_href = image_soup.select_one("td.imageview").a["href"]
            image_name = re.sub(".+/(i.+)/", r"\1", link) + ".pdf"
            with open(self.image_dir + "/" + image_name, "wb") as f:
                f.write(img2pdf.convert(requests.get(image_href).content))
                print("\t\t[image]"
                      + "(" + str(pathlib.Path(self.image_dir + "/" + image_name).resolve()) + ")")

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

                novel.set_section(self.get_escaped_text(sec))
                if update:
                    try:
                        prev_toc[chap][sec]
                    except KeyError as ke:
                        print("<new>", end="")
                        time.sleep(1)
                        ep_soup = self.get_soup(toc[chap][sec])
                        sec_text = self.get_episode_text(ep_soup)
                        self.set_episode_image(ep_soup)
                    print("\t[episode] -> " + sec +
                          "(" + str(pathlib.Path(tex_path).resolve()) + ")")
                else:
                    time.sleep(1)
                    ep_soup = self.get_soup(toc[chap][sec])
                    sec_text = self.get_episode_text(ep_soup)
                    self.set_episode_image(ep_soup)
                    print("\t[episode] -> " + sec +
                          "(" + str(pathlib.Path(tex_path).resolve()) + ")")

                novel.set_text(sec_text, tex_path)

        novel.end_document()
        novel.compile(batchmode)
        self.set_json(self.root_dir + "/toc.json", toc)


if __name__ == "__main__":
    print("narou")
    data = Narou(input())
    update = True
    batchmode = True

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
