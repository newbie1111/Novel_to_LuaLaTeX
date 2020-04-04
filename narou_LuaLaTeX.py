import requests
import pathlib
import re
from bs4 import BeautifulSoup
import time
import novel_maker
import formatter


class narou_LuaLaTeX():
    mainSoup = None
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"}

    # constructor : get mainpage html
    def __init__(self, url):
        res = requests.get(url, headers=self.header)
        res.encoding = res.apparent_encoding

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
        if self.mainSoup.find("div", {"class": "index_box"}) is not None:
            return True
        else:
            return False

    # get novel title
    def get_title(self):
        # css selector
        return self.mainSoup.find("p", {"class", "novel_title"}).getText()

    # get novel author
    def get_author(self):
        return self.mainSoup.find("div", {"class", "novel_writername"}).a.getText()

    def get_unique_number(self):
        return re.sub("/(n.+)/.+", r"\1", (self.mainSoup.select_one("dd.subtitle").a["href"]))

    # get episode link href list
    def get_episodeLinks(self):
        links = ["https://ncode.syosetu.com" + link.a["href"]
                 for link in self.mainSoup.select("dd.subtitle")]
        return links

    def get_contentsDict(self, link):
        res = requests.get(url=link, headers=self.header)
        res.encoding = res.apparent_encoding
        soup = BeautifulSoup(res.text, "html.parser")
        contents_dict = {"chapter": None, "title": None,
                         "episode": None, "illust": None}

        chapter = soup.find("p", {"class", "chapter_title"})
        if chapter:
            contents_dict["chapter"] = chapter.string

        contents_dict["title"] = soup.find(
            "p", {"class", "novel_subtitle"}).string
        contents_dict["episode"] = "\\leavevmode \\\\\n".join(
            [str(html) for html in soup.find_all("p", id=re.compile("\d+"))])
        contents_dict["illust"] = [
            "https:" + str(img["src"]) for img in soup.find_all("img", src=re.compile("icode/i\d+"))]

        return contents_dict

    # create a pdf file by creating and compiling a .tex file.
    def set_novel(self):
        save_pass = "./out/narou/" + self.get_unique_number()
        title = self.get_title()
        author = self.get_author()
        novel = novel_maker.novel_maker(save_pass, title, author)
        now_chapter = ""

        novel.set_header()
        links = self.get_episodeLinks()
        for link in links:
            time.sleep(1)
            contents = self.get_contentsDict(link)
            if contents["chapter"] and contents["chapter"] != now_chapter:
                novel.set_chapter(
                    formatter.escape_to_TeX_format(contents["chapter"]))
                now_chapter = contents["chapter"]
                print("[chapter] -> " + contents["chapter"])
            novel.set_subsection(
                formatter.escape_to_TeX_format(contents["title"]))
            print("\t[subsection] -> " + contents["title"])

            if contents["illust"]:
                novel.save_illusts(contents["illust"])

            novel.set_text(formatter.html_to_TeX_format(
                contents["episode"], image_save_pass=save_pass + title + "/pic"))

        novel.set_footer()

        novel.compile()


if __name__ == "__main__":
    print("   ■■             ■■          ■■■  ")
    print("   ■           ■■■■■■           ■  ")
    print(" ■■■■■  ■■        ■■               ")
    print("  ■■     ■■       ■         ■■■■■■ ")
    print("  ■    ■         ■■■■■      ■    ■■")
    print("  ■    ■        ■■   ■■           ■")
    print(" ■     ■      ■■      ■           ■")
    print("■■  ■■■■              ■          ■■")
    print("    ■  ■■■          ■■■         ■■ ")
    print("    ■■■■        ■■■■■■        ■■■  ")
    print("Enter the URL of the main page of the work posted on narou.")
    download_url = input()
    novelData = narou_LuaLaTeX(download_url)
    novelData.set_novel()
