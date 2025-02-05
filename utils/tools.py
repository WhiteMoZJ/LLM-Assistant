from xpinyin import Pinyin

def get_pinyin(name):
    s = Pinyin().get_pinyin(name).split('-')
    result = ''
    for i in range(0,len(s)):
        result = result+s[i].capitalize()
    return result