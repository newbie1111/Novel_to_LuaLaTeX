import re
import time
from collections import OrderedDict
import json
import pathlib
import requests  # install
from bs4 import BeautifulSoup  # install
import novel_luatex
import novel_maker


class Kakuyomu(novel_luatex.Novel_LuaTeX):

    def __init__(self, url):
        super().__init__(url)
        self.root_dir = "./kakuyomu/" + self.get_unique_code()

    def is_save_dir_exists(self):
        return pathlib.Path(self.root_dir).exists()

    def get_works_title(self):
        return self.main_soup.find("h1", id="workTitle").getText()

    def get_works_author(self):
        return self.main_soup.find("span", id="workAuthor-activityName").getText()

    def get_unique_code(self):
        return re.sub(".+/(.+)", r"\1", self.main_soup.select_one("meta[property='og:url']")["content"])

    def get_table_of_contents(self):
        table_of_contents = OrderedDict(
            {"": OrderedDict({"": OrderedDict({})})})
        now_chapter = ""
        now_section = ""

        for li in self.main_soup.select("li.widget-toc-chapter , li.widget-toc-episode"):
            if "widget-toc-level1" in li["class"]:
                now_chapter = li.span.string.replace("\u3000", " ")
                now_section = ""
                table_of_contents.update(OrderedDict(
                    {now_chapter: OrderedDict({"": OrderedDict({})})}))
            elif "widget-toc-level2" in li["class"]:
                now_section = li.span.string.replace("\u3000", " ")
                table_of_contents[now_chapter].update(
                    OrderedDict({now_section: OrderedDict({})}))
            elif "widget-toc-episode" in li["class"]:
                title = li.a.span.string.replace("\u3000", " ")
                href = "https://kakuyomu.jp" + li.a["href"]
                table_of_contents[now_chapter][now_section].update(
                    OrderedDict({title: href}))

        return table_of_contents

    def get_episode_text(self, ep_soup):
        ep = "\\\\\n".join(
            [str(txt) for txt in ep_soup.find_all("p", id=re.compile("^p\d+"))])
        ep = re.sub(r"([#$%&_^{}\[\]])", r"\\\1", ep)
        ep = ep.replace("<em class=\"emphasisDots\">", "\\kenten{")
        ep = ep.replace("<ruby><rb>", "\\ruby[g]{")
        ep = re.sub("<a href=\"(.+)\">\s*(.+)\s*</a>", r"\\href{\1}{\2}", ep)
        ep = re.sub("</rb><rp>[(（《]</rp><rt>", "}{", ep)
        ep = re.sub("</rt><rp>[)）》]</rp></ruby>|</em>", "}", ep)
        ep = re.sub(r"(\\ruby[g]|\\kenten){\s+?", r"\1{", ep)
        ep = re.sub("\s+?}", "}", ep)
        ep = re.sub("<.??span>|<.??p.*?>|<br/>", "", ep)
        return ep.replace("\u3000", " ")

    def get_escaped_text(self, text):
        return re.sub(r"([#$%&_^{}\[\]])", r"\\\1", text)

    def set_novel(self, batchmode=False, renew=False):
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
                sec_dir = ""
                if sec:
                    sec_dir = "/sec" + str(sec_num)
                    novel.set_section(self.get_escaped_text(sec))
                    print("\t[section] -> " + sec)

                for ep_num, ep in enumerate(toc[chap][sec].keys()):
                    save_dir = self.root_dir + "/tex" + chap_dir + sec_dir
                    tex_path = save_dir + "/ep" + str(ep_num) + ".tex"
                    ep_text = ""

                    time.sleep(1)
                    novel.set_subsection(self.get_escaped_text(ep))
                    if renew:
                        try:
                            prev_toc[chap][sec][ep]
                        except KeyError as ke:
                            print("new  :", end="")
                            ep_text = self.get_episode_text(
                                self.get_soup(toc[chap][sec][ep]))
                    else:
                        ep_text = self.get_episode_text(
                            self.get_soup(toc[chap][sec][ep]))
                    novel.set_text(ep_text, tex_path)
                    print("\t\t[episode] -> " + ep + "(" + tex_path + ")")

        novel.end_document()
        novel.compile(batchmode)
        self.set_json(self.root_dir + "/toc.json", toc)


if __name__ == "__main__":
    print("kakuyomu")
    data = Kakuyomu(input())
    update = True
    log = True

    print("works title  : " + data.get_works_title())
    print("works author : " + data.get_works_author())

    if data.is_save_dir_exists():
        print("更新モードが使用できます。使用しますか？[Y/N]")
        update = True if re.match("[Yy]", input()) else False
    else:
        print("新しくダウンロードする小説です。")
        update = False

    print("LuaTeXのコンパイルのログを表示しますか？[Y/N]")
    log = False if re.match("[Yy]", input()) else True

    data.set_novel(log, update)
