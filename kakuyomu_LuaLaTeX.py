# coding:utf-8

# import
import requests
import pathlib
import re
from bs4 import BeautifulSoup
import time
import novel_maker
import formatter

# kakuyomu_LuaLaTeX class


class kakuyomu_LuaLaTeX():
    mainSoup = None

    # constructor : get mainpage html
    def __init__(self, url):
        res = requests.get(url)

        if res.status_code == requests.codes.ok:
            self.mainSoup = BeautifulSoup(res.text, "html.parser")

            if not self.isWorks_main():
                print("not works main page")
                quit()

            print("Title  : " + self.get_title())
            print("Author : " + self.get_author())

        else:
            print("not exist")
            quit()

    # Determine if it is the main page or not
    def isWorks_main(self):
        if self.mainSoup.find(attrs={"data-route": "public:works:work"}) is not None:
            return True
        else:
            return False

    # get novel title
    def get_title(self):
        return self.mainSoup.find("h1", id="workTitle").getText()

    # get novel author
    def get_author(self):
        return self.mainSoup.find("span", id="workAuthor-activityName").getText()

    # get episode link hrefs list
    def get_episodeLinks(self):
        episodes_hrefs = []
        links = ["https://kakuyomu.jp" + link["href"] for link in self.mainSoup.find_all(
            "a", {"class", "widget-toc-episode-episodeTitle"})]
        return links

    def get_contentsDict(self, link):
        soup = BeautifulSoup(requests.get(link).text, "html.parser")
        contents_dict = {"chapter": None, "section": None,
                         "title": None, "episode": None}

        chapter = soup.find(
            "p", {"class", "chapterTitle level1 js-vertical-composition-item"})
        section = soup.find(
            "p", {"class", "chapterTitle level2 js-vertical-composition-item"})
        if chapter:
            contents_dict["chapter"] = chapter.string
        if section:
            contents_dict["section"] = section.string

        contents_dict["title"] = soup.find(
            "p", {"class", "widget-episodeTitle js-vertical-composition-item"}).string
        contents_dict["episode"] = formatter.html_to_TeX_format("\\leavevmode \\\\\n".join(
            [str(html) for html in soup.find_all("p", id=re.compile("\d+"))]))

        return contents_dict

    # create a pdf file by creating and compiling a .tex file.
    def set_novel(self):
        save_pass = "./out/kakuyomu/"
        title = self.get_title()
        author = self.get_author()
        novel = novel_maker.novel_maker(save_pass, title, author)

        novel.set_header()
        links = self.get_episodeLinks()
        for link in links:
            time.sleep(1)
            contents = self.get_contentsDict(link)
            if contents["chapter"]:
                novel.set_chapter(
                    formatter.escape_to_TeX_format(contents["chapter"]))
                print("[chapter] -> " + contents["chapter"])
            if contents["section"]:
                novel.set_section(
                    formatter.escape_to_TeX_format(contents["section"]))
                print("\t[section] -> " + contents["section"])

            novel.set_subsection(
                formatter.escape_to_TeX_format(contents["title"]))
            print("\t\t[subsection] -> " + contents["title"])

            novel.set_text(contents["episode"])

        novel.set_footer()
        novel.compile()


if __name__ == "__main__":
    # """
    print("                 ■                               ")
    print("   ■■           ■■                               ")
    print("   ■■           ■■■■■■    ■■■■■■■■        ■■     ")
    print("   ■■■■■■      ■■   ■            ■        ■      ")
    print("■■■■    ■     ■■    ■            ■        ■      ")
    print("   ■    ■    ■■    ■■            ■       ■■  ■   ")
    print("   ■   ■■          ■       ■■■■■■■       ■   ■   ")
    print("   ■   ■■         ■■             ■       ■    ■  ")
    print("  ■    ■■        ■■              ■      ■    ■■■ ")
    print(" ■■    ■        ■■        ■■■■■■■■    ■■■■■■■■ ■■")
    print("■■   ■■■       ■                                 ")
    # """
    print("Enter the URL of the main page of the work posted on kakuyomu.")
    download_url = input()
    novelData = kakuyomu_LuaLaTeX(download_url)
    novelData.set_novel()
