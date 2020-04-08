import re
import pathlib


def html_to_TeX_format(html_text, image_save_pass=None):
    result = re.sub(
        r"<ruby><rb>({.+?})</rb><rp>\(</rp><rt>{.+?}</rt><rp>\)</rp></ruby>", r"\1", html_text)  # 牌変換ツール用
    result = re.sub(r"([#$%&_^{}\[\]])", r"\\\1", result)
    result = result.replace("<ruby><rb>", "\\ruby[g]{")
    result = result.replace("<em class=\"emphasisDots\">", "\\kenten{")
    result = re.sub("</rb><rp>[(（《]</rp><rt>", "}{", result)
    result = re.sub("</rt><rp>[)）》]</rp></ruby>|</em>", "}", result)
    result = re.sub(r"(\\ruby[g]|\\kenten){\s+?", r"\1{", result)
    result = re.sub("\s+?}", "}", result)

    if image_save_pass:

        figure_begin = r"\\begin{figure}\n" + r"\\begin{center}\n" + \
            r"\\begin{minipage}<y>[htbp]{93mm}\n"
        figure_end = r"\\end{minipage}\n" + \
            r"\\end{center}\n" + r"\\end{figure}\n"

        path = str(pathlib.Path(image_save_pass).resolve()).replace("\\", "/")
        result = re.sub(r"<a.*?\"挿絵\" href=\".+/(.+?)\".+?>.*?</a>", figure_begin +
                        r"\\includegraphics[width=93mm]{" + path + r"/\1}" + "\n" + figure_end, result)
        result = re.sub("<img .* src=\".*\/icode/(i\d+).*\"/>",
                        figure_begin + "\\\includegraphics[width=93mm]{" + path + "/\\1.jpg}\n" + figure_end, result)

    result = re.sub(
        "<.??a.*?>|<.??span>|<.??p.*?>|<.??div.*?>|<br/>", "", result)
    result = result.replace("\u3000", "")

    return result


def escape_to_TeX_format(text):
    return re.sub("([#$%&_{}])", r"\\\1", text).replace("\u3000", " ")
