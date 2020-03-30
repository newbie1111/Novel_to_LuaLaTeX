
# coding:utf-8
import re

# get text for LuaLaTeX format


def html_to_TeX_format(html_text):
    result = re.sub("([#$%&_{}])", r"\\\1", html_text)
    result = result.replace("<ruby><rb>", "\\ruby[g]{")
    result = re.sub("</rb><rp>[(（《]</rp><rt>", "}{", result)
    result = re.sub("</rt><rp>[)）》]</rp></ruby>|</em>", "}", result)
    result = result.replace("<em class=\"emphasisDots\">", "\\kenten{")
    result = re.sub("<.??a.*?>|<.??span>|<.??p.*?>|<br/>", "", result)
    result = result.replace("\u3000", "")
    return result


def escape_to_TeX_format(text):
    return re.sub("([#$%&_{}])", r"\\\1", text)
