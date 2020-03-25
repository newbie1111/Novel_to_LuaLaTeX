# coding:utf-8
import subprocess
import pathlib


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
            f.write("\\tableofcontents\n\n")

    def set_part(self, name):
        with open(self.save_TeX_file, "a") as f:
            f.write("\\part{" + name + "}\n")

    def set_chapter(self, name):
        with open(self.save_TeX_file, "a") as f:
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
