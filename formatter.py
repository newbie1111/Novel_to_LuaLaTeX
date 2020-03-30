
# coding:utf-8
import re
import pathlib

# get text for LuaLaTeX format


def html_to_TeX_format(html_text, image_save_pass=None):
    result = re.sub("([#$%&_{}])", r"\\\1", html_text)
    result = result.replace("<ruby><rb>", "\\ruby[g]{")
    result = re.sub("</rb><rp>[(（《]</rp><rt>", "}{", result)
    result = re.sub("</rt><rp>[)）》]</rp></ruby>|</em>", "}", result)
    result = result.replace("<em class=\"emphasisDots\">", "\\kenten{")
    result = re.sub("<.??a.*?>|<.??span>|<.??p.*?>|<br/>", "", result)
    result = result.replace("\u3000", "")

    if image_save_pass:

        figure_begin = r"\\begin{figure}\n" + r"\\begin{center}\n" + \
            r"\\begin{minipage}<y>[htbp]{93mm}\n"
        figure_end = r"\\end{minipage}\n" + \
            r"\\end{center}\n" + r"\\end{figure}\n"

        path = str(pathlib.Path(image_save_pass).resolve()).replace("\\", "/")

        result = re.sub("<img .* src=\".*\/icode/(i\d+).*\"/>",
                        figure_begin + "\\\includegraphics[width=93mm]{" + path + "/\\1.jpg}\n" + figure_end, result)

    return result


def escape_to_TeX_format(text):
    return re.sub("([#$%&_{}])", r"\\\1", text)
