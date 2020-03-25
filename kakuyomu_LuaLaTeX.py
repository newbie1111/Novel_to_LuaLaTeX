# coding:utf-8

# import
import requests
import pathlib
import re
from bs4 import BeautifulSoup
import novel_maker

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
        links = [link for link in self.mainSoup.find_all(
            "a", {"class", "widget-toc-episode-episodeTitle"})]

        for href in links:
            episodes_hrefs.append("https://kakuyomu.jp" + href["href"])

        return episodes_hrefs

    # get episode text
    def get_Story(self, link):
        soup = BeautifulSoup(requests.get(link).text, "html.parser")
        episode_structure = [str(html) for html in soup.find_all(
            "p", {"class", re.compile("(chapterTitle level\d|widget-episodeTitle).*")})]
        episode_html = [str(html) for html in soup.find_all(
            "p", id=re.compile("\d+"))]

        result = self.get_structure("".join(episode_structure))
        result += "\n" + \
            self.get_text("\\leavevmode \\\\\n".join(episode_html))

        return result

    # get novel structure
    def get_structure(self, text):
        result = text
        result = result.replace(
            "<p class=\"chapterTitle level1 js-vertical-composition-item\"><span>", "\n\\chapter{")
        result = result.replace(
            "<p class=\"chapterTitle level2 js-vertical-composition-item\"><span>", "\n\t\\section{")
        result = result.replace(
            "<p class=\"widget-episodeTitle js-vertical-composition-item\">", "\n\t\t\\subsection{")
        result = re.sub("</span></p>|</p>", "}", result)

        print(result, end="")
        return result

    # get text for LuaLaTeX format
    def get_text(self, text):
        result = text
        result = result.replace("<ruby><rb>", "\\ruby[g]{")
        result = result.replace("</rb><rp>（</rp><rt>", "}{")
        result = result.replace("</rt><rp>）</rp></ruby>", "}")
        result = result.replace("<em class=\"emphasisDots\">", "\\kenten{")
        result = result.replace("</em>", "}")
        result = result.replace("<br/>", "")
        result = re.sub("<.??span>", "", result)
        result = re.sub("<.??p.*?>", "", result)
        result = result.replace("\u3000", "")
        return result

    # create a pdf file by creating and compiling a .tex file.
    def set_novel(self):
        save_pass = "./out/kakuyomu/"
        title = self.get_title()
        author = self.get_author()
        novel = novel_maker.novel_maker(save_pass, title, author)

        novel.set_header()
        links = self.get_episodeLinks()
        for link in links:
            novel.set_text(self.get_Story(link))
        novel.set_footer()

        novel.compile()


if __name__ == "__main__":
    """
    print("■■■■                                     ■                               ")
    print("■                          ■■           ■■                               ")
    print("■                          ■■           ■■■■■■    ■■■■■■■■        ■■     ")
    print("■            ■             ■■■■■■      ■■   ■            ■        ■      ")
    print("■            ■          ■■■■    ■     ■■    ■            ■        ■      ")
    print("■            ■             ■    ■    ■■    ■■            ■       ■■  ■   ")
    print("■            ■             ■   ■■          ■       ■■■■■■■       ■   ■   ")
    print("■            ■             ■   ■■         ■■             ■       ■    ■  ")
    print("■            ■            ■    ■■        ■■              ■      ■    ■■■ ")
    print("             ■           ■■    ■        ■■        ■■■■■■■■    ■■■■■■■■ ■■")
    print("             ■          ■■   ■■■       ■                                 ")
    print("          ■■■■                                         ")
    """
    print("Enter the URL of the main page of the work posted on kakuyomu.")
    download_url = input()
    novelData = kakuyomu_LuaLaTeX(download_url)
    novelData.set_novel()
