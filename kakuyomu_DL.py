# coding:utf-8
import requests
import copy
import pathlib
import re
import write_novel


class kakuyomu_DL():
    url = ""

    def __init__(self, url):
        self.url = url

    def getURL(self):
        return self.url

    def getContents(self):
        response = requests.get(self.url)
        if(response.status_code != requests.codes.ok):
            print("無効なURLです")
            quit()
        return response.text

    def getTitle(self):
        text = self.getContents()
        tmp = text.split("<title>")
        tmp = tmp[1].split("</title>")
        data = tmp[0].split("（")
        data[1] = data[1].replace("） - カクヨム", "")
        return data

    def getStructure(self, str):  # 対象話の文章構造を取得する

        header_html = str.split("<header id=\"contentMain-header\">")
        header_html = header_html[1].split("</header>")

        # 余計なheaderの削除
        book_structure = re.sub(
            "<.*div.*>|<p id.*/p>|<.?span>|\\n", "", header_html[0])

        # 章-節-項への置き換え
        book_structure = book_structure.replace(
            "<p class=\"chapterTitle level1 js-vertical-composition-item\">", "\\chapter{")
        book_structure = book_structure.replace(
            "<p class=\"chapterTitle level2 js-vertical-composition-item\">", "\\section{")
        book_structure = book_structure.replace(
            "<p class=\"widget-episodeTitle js-vertical-composition-item\">", "\\subsection{")
        book_structure = book_structure.replace("</p>", "}\n")
        book_structure = book_structure.replace("\u3000", "")

        return book_structure

    def host_url(self):
        url = self.url
        tmp = url.split("https://kakuyomu.jp/")
        url = tmp[1]
        return url

    def scraiping_url(self):
        result_url = []
        text = self.getContents()
        result = text.split(self.host_url() + "/episodes/")
        for i in range(1, len(result)):
            tmp_url = result[i].split("\"")
            result_url.append(tmp_url[0])

        result_url.pop(0)  # 「1話目から読む」にある第一話リンクを消去する
        return result_url

    def save_Contents(self):
        result = []
        number = self.scraiping_url()
        for i in number:
            response = requests.get(self.url + "/episodes/" + i)
            result.append(response.text)
        return result

    def scraiping_Contents(self):

        response = self.save_Contents()
        text = []
        text_data = []

        for string in response:

            output = False
            data = re.split("(<p id=\"p\d*\">)", string)
            title = self.getStructure(data[0])
            data.pop(0)

            for str in data:
                if output:

                    s = str.split("</div>")
                    replace_text = s[0]

                    # ルビ用の置き換え
                    replace_text = replace_text.replace(
                        "<ruby><rb>", "\\ruby[g]{")
                    replace_text = replace_text.replace("</rb><rp>", "}")
                    replace_text = replace_text.replace("（</rp><rt>", "{")
                    replace_text = replace_text.replace("</rt><rp>）", "}")
                    replace_text = replace_text.replace("</rp></ruby>", "")

                    # 傍点用の置き換え
                    replace_text = replace_text.replace(
                        "<em class=\"emphasisDots\">", "\\kenten{")
                    replace_text = replace_text.replace("<span>", "")
                    replace_text = replace_text.replace("</span>", "")
                    replace_text = replace_text.replace("</em>", "}")

                    # 改行用の置き換え
                    replace_text = replace_text.replace("</p>", "\\\\")
                    replace_text = replace_text.replace("<br />", "")
                    replace_text = re.sub(
                        "(<p id=\"p\d*\" class=\"blank\">)", "", replace_text)

                    # 行頭のタグ削除
                    replace_text = re.sub(
                        "(<p id=\"p\d*\">)", "", replace_text)

                    text.append(replace_text)
                else:
                    output = not output

            result_text = copy.deepcopy("".join(text))
            result_text = result_text.replace("\u3000", "")
            text_data.append({title: result_text})
            text = []

        return text_data

    def save_text(self):

        bookData = self.getTitle()
        print("Title : " + bookData[0])
        print("Author : " + bookData[1])

        text = self.scraiping_Contents()
        p = pathlib.Path("./kakuyomu/" + bookData[0])

        if(p.exists() == False):
            p.mkdir(parents=True)

        novel_data = write_novel.write_novel(
            "./kakuyomu/" + bookData[0], bookData[0], bookData[1])

        novel_data.in_header()

        for i in text:
            for title in i.keys():
                novel_data.in_Text(title)
                novel_data.in_Text(i[title])

        novel_data.in_footer()
        novel_data.compile_LuaLaTex()
