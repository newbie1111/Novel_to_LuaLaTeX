# coding:utf-8
import subprocess
import pathlib
import requests
import re


class novel_maker():

    title = ""
    author = ""
    save_dirctory = ""
    save_TeX_file = ""

    def __init__(self, path, title, author):
        self.save_dirctory = path + title
        self.save_TeX_file = self.save_dirctory + "/contents.tex"
        self.title = title
        self.author = author

        if pathlib.Path(self.save_dirctory).exists() == False:
            pathlib.Path(self.save_dirctory).mkdir(parents=True)

    def set_header(self):
        with open(self.save_TeX_file, "w") as f:
            f.write("\\documentclass[]{ltjtbook}\n")
            f.write("\\usepackage{../../../sty_files/B6tate}\n")
            f.write("\\title{" + self.title + "}\n")
            f.write("\\author{" + self.author + "}\n")
            f.write("\n\\begin{document}\n")
            f.write("\\maketitle\n")
            f.write("\\tableofcontents\n")
            f.write("\\newpage\n\n")

    def set_part(self, name):
        with open(self.save_TeX_file, "a") as f:
            f.write("\\part{" + name + "}\n")

    def set_chapter(self, name):
        with open(self.save_TeX_file, "a") as f:
            f.write("\\newpage\n")
            f.write("\\chapter{" + name + "}\n")

    def set_section(self, name):
        with open(self.save_TeX_file, "a") as f:
            f.write("\\section{" + name + "}\n")

    def set_subsection(self, name):
        with open(self.save_TeX_file, "a") as f:
            f.write("\\subsection{" + name + "}\n")

    def set_text(self, text):
        with open(self.save_TeX_file, "a") as f:
            f.write(text + "\n")
            f.write("\\newpage\n")

    def save_illusts(self, illusts_url_links):
        save_illusts_pass = self.save_dirctory + "/pic"
        if not pathlib.Path(save_illusts_pass).exists():
            pathlib.Path(save_illusts_pass).mkdir(parents=True)

        for link in illusts_url_links:
            name = re.sub(".*/icode/(i\d+)/", r"/\1" + ".jpg", link)
            with open(save_illusts_pass + name, "wb") as image:
                image.write(requests.get(link).content)

    def set_footer(self):
        with open(self.save_TeX_file, "a") as f:
            f.write("\\end{document}\n")

    def compile(self):
        abs_TeX_pass = str(pathlib.Path(self.save_TeX_file).resolve())
        abs_save_dir = str(pathlib.Path(self.save_dirctory).resolve())

        print("")
        subprocess.run(["lualatex", "-interaction", "batchmode",
                        "-output-directory", abs_save_dir, abs_TeX_pass])
        print("")
        subprocess.run(["lualatex", "-interaction", "batchmode",
                        "-output-directory", abs_save_dir, abs_TeX_pass])
