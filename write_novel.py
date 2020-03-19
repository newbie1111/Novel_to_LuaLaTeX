# coding:utf-8
import subprocess
import pathlib


class write_novel():

    texPath = ""
    texDir = ""
    title = ""
    author = ""

    def __init__(self, path, title, author):

        self.texPath = path + "/contents.tex"
        self.texDir = path
        self.title = title
        self.author = author

    def in_header(self):
        with open(self.texPath, "w") as f:
            f.write("\\documentclass[]{ltjtbook}\n")
            f.write("\\usepackage{B6tate}\n")
            f.write("\\title{" + self.title + "}\n")
            f.write("\\author{" + self.author + "}\n")
            f.write("\\begin{document}\n")
            f.write("\\maketitle\n")
            f.write("\\tableofcontents\n")

    def in_partName(self, name):
        with open(self.texPath, "a") as f:
            f.write("\\part{" + name + "}\n")

    def in_chapterName(self, name):
        with open(self.texPath, "a") as f:
            f.write("\\chapter{" + name + "}\n")

    def in_sectionName(self, name):
        with open(self.texPath, "a") as f:
            f.write("\\section{" + name + "}\n")

<<<<<<< HEAD
    def in_subsectionName(self , name):
        with open(self.texPath , "a") as f:
            f.write("\\subsection{" + name + "}\n")

    def in_Text(self , text):
        with open(self.texPath , "a") as f:
=======
    def in_Text(self, text):
        with open(self.texPath, "a") as f:
>>>>>>> 95e81cdeaa4c886d7b845645d4b505e04aa1cc27
            f.write(text + "\n")

    def in_footer(self):
        with open(self.texPath, "a") as f:
            f.write("\\end{document}\n")

    def compile_LuaLaTex(self):
        p = str(pathlib.Path(self.texPath).resolve())
        dp = str(pathlib.Path(self.texDir).resolve())
        option = "-output-directory"
        subprocess.run(["lualatex", option, dp, p])
        subprocess.run(["lualatex", option, dp, p])
