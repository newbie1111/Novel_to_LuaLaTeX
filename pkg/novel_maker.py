import subprocess
import pathlib
import requests
import re
import pprint


class Novel_maker():

    def __init__(self, save_dir="./", title="unknown", author="unknown", file_name="novel.tex"):
        if not pathlib.Path(save_dir).exists():
            pathlib.Path(save_dir).mkdir(parents=True)
        self.save_dir = pathlib.Path(save_dir).resolve()
        self.save_tex = pathlib.Path(save_dir + "/" + file_name).resolve()
        self.title = title
        self.author = author

    def begin_document(self):
        with open(self.save_tex, "w", encoding="utf-8") as f:
            f.write("\\documentclass[]{ltjtbook}\n"
                    + "\\usepackage{B6tate}\n"
                    + "\\title{" + self.title + "}\n"
                    + "\\author{" + self.author + "}\n\n"
                    + "\\begin{document}\n"
                    + "\\maketitle\n"
                    + "\\tableofcontents\n\n")

    def set_part(self, part):
        with open(self.save_tex, "a", encoding="utf-8") as f:
            f.write("\\part{" + part + "}\n")

    def set_chapter(self, chapter):
        with open(self.save_tex, "a", encoding="utf-8") as f:
            f.write("\t\\chapter{" + chapter + "}\n")

    def set_section(self, section):
        with open(self.save_tex, "a", encoding="utf-8") as f:
            f.write("\t\t\\section{" + section + "}\n")

    def set_subsection(self, subsection):
        with open(self.save_tex, "a", encoding="utf-8") as f:
            f.write("\t\t\t\\subsection{" + subsection + "}\n")

    def set_text(self, text="", path="./"):
        directory = pathlib.Path(re.sub("(.+/).*", r"\1", path)).resolve()
        input_path = pathlib.Path(path).resolve()
        try:
            if not directory.exists():
                directory.mkdir(parents=True)
            if text:
                with open(input_path, "w", encoding="utf-8") as f:
                    f.write(text)
        except Exception as identifier:
            print(identifier)
        finally:
            with open(self.save_tex, "a", encoding="utf-8") as f:
                f.write("\t\t\t\t\\leavevmode\\\\\n"
                        + "\t\t\t\t\\input{"
                        + str(input_path).replace("\\", "/")
                        + "}\n")

    def end_document(self):
        with open(self.save_tex, "a", encoding="utf-8") as f:
            f.write("\\end{document}")

    def compile(self, batchmode=False):
        args = ["lualatex"]
        if batchmode:
            args.extend(["-interaction", "batchmode"])
        args.extend(["-output-directory", self.save_dir, self.save_tex])

        subprocess.run(args)
        subprocess.run(args)
