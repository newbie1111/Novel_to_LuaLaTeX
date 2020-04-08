import requests
import re
import pathlib
from bs4 import BeautifulSoup
import time
from collections import OrderedDict

import novel_maker
import formatter
import pprint


class hameln_LuaLaTeX():
    main_soup = None

    def __init__(self, url):
        res = requests.get(url=url)
        res.encoding = res.apparent_encoding
        self.main_soup = BeautifulSoup(res.text, "html.parser")

        if not (self.is_works_main_url(url=url) and res.status_code == requests.codes.ok):
            print("wrong url or forbidden.")
            quit()

    def is_works_main_url(self, url):
        url_check = re.fullmatch(r"(https://syosetu.org/novel/\d+).??", url)
        page_check = self.main_soup.select("tr a")
        return True if url_check and page_check else False

    def get_title(self):
        return self.main_soup.find("span", {"itemprop": "name"}).getText()

    def get_author(self):
        return self.main_soup.find("span", {"itemprop": "author"}).getText()

    def get_unique_code(self):
        unique_code = self.main_soup.find(
            "meta", {"property": "og:url"})["content"]
        unique_code = re.sub(".*/novel/(.*)/", r"\1", unique_code)
        return unique_code

    def get_table_of_contents(self):
        table_of_contents = OrderedDict({"": []})
        now_section = ""

        for tr in self.main_soup.select("tr"):
            now_section = tr.td.strong.text if tr.td.strong else now_section
            now_section = now_section.replace("\u3000", " ")
            href = tr.a["href"] if tr.a else tr.a
            title = tr.td.a.text if tr.td.a else ""
            title = title.replace("\u3000", " ")

            try:
                href = re.sub(r".(/.*)", "https://syosetu.org/novel/" +
                              self.get_unique_code() + r"\1", href)
                table_of_contents[now_section].append((title, href))
            except Exception as identifier:
                table_of_contents.update({now_section: []})

        return table_of_contents

    def get_episode_text_and_image(self, href):
        res = requests.get(url=href)
        soup = BeautifulSoup(res.text, "html.parser")
        episode = (r"\leavevmode \\" +
                   "\n").join([str(text) for text in soup.find_all("p", id=re.compile("\d+"))])
        image = [img["href"] for img in soup.find_all("a", {"name": "img"})]
        return {"episode": episode, "image": image}

    def set_novel(self):
        save_pass = "./out/hameln/" + self.get_unique_code()
        title = self.get_title()
        author = self.get_author()
        table_of_contents = self.get_table_of_contents()
        novel = novel_maker.novel_maker(save_pass, title, author)

        novel.set_header()
        for key in table_of_contents.keys():
            if key:
                novel.set_chapter(formatter.escape_to_TeX_format(key))
                print("[chapter] -> " + title)
            for title, link in table_of_contents[key]:
                novel.set_subsection(title)
                print("\t[subsection] -> " + title)
                episode = self.get_episode_text_and_image(link)
                novel.set_text(formatter.html_to_TeX_format(
                    episode["episode"], image_save_pass=save_pass + "/pic"))
                if episode["image"]:
                    novel.save_illusts(episode["image"])
                    for img in episode["image"]:
                        print("image > " + img)
        novel.set_footer()
        novel.compile()


if __name__ == "__main__":
    print(""
          + "                                 ■       ■  ■        ■■       \n"
          + "   ■   ■                         ■       ■■ ■         ■■      \n"
          + "   ■   ■■                    ■■ ■■       ■  ■          ■     ■\n"
          + "  ■     ■                     ■■■        ■  ■               ■■\n"
          + "  ■     ■■   ■■■■■■■■■■■       ■■        ■  ■    ■         ■■ \n"
          + " ■■      ■                    ■■ ■       ■  ■   ■         ■■  \n"
          + "■■       ■■                  ■■   ■     ■■  ■  ■■        ■■   \n"
          + "■                           ■■          ■   ■■■        ■■■    \n"
          + "                           ■■          ■     ■        ■  \n")
    print("Enter the URL of the main page of the work posted on hameln.")
    download_url = input()
    novel_data = hameln_LuaLaTeX(download_url)
    print("Title : " + novel_data.get_title())
    print("Author : " + novel_data.get_author())
    novel_data.set_novel()
