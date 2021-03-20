import re, collections, os
from bs4 import BeautifulSoup
from smart_open import open
import joblib
id_pattern = re.compile(r'id\s{0,3}=\s{0,3}"([^"]+)"')
class_pattern = re.compile(r'class\s{0,3}=\s{0,3}"([^"]+)"')
DataPoint = collections.namedtuple("DataPoint", ("element", "tags", "classes", "ids", "text"))

def normalize_txt(txt):
    return re.sub("[\n\s]+",' ',str(txt).translate({160: ' '}),flags=re.MULTILINE).strip()

def fuzzy_pattern(txt):
    return re.compile("[^a-zA-Z0-9]{0,6}".join(['']+re.findall("[a-zA-Z0-9]+", txt)+['']))

def cls_soup(el):
    ret = []
    while el:
        try:
            ret.append(tuple(el.attrs["class"]))
        except:
            ret.append(tuple())
        el = el.parent
    return list(reversed(ret))


def ids_soup(el):
    ret = []
    while el:
        try:
            ret.append(el.attrs["id"])
        except:
            ret.append("")
        el = el.parent
    return list(reversed(ret))

def tag_soup(el):
    ret = []
    while el:
        try:
            ret.append(el.name)
        except:
            ret.append("")
        el = el.parent
    return list(reversed(ret))


def generate_dataset(soup):
    html = str(soup)
    ids = id_pattern.findall(html)
    clss= list(set(sum(map(str.split,class_pattern.findall(html)),[])))
    found_strings=set()
    ret=[]
    for id_ in ids:
        x=soup.find(id=id_)
        try:
            s=normalize_txt(x.text.strip())
            if s in found_strings:
                continue
            ret.append(DataPoint(x, tag_soup(x), cls_soup(x),ids_soup(x), s))
            found_strings.add(s)
        except:
            continue
    for cls in clss:
        for x in soup.find_all(class_=cls):
            try:
                s=normalize_txt(x.text.strip())
                if s in found_strings:
                    continue
                ret.append(DataPoint(x, tag_soup(x), cls_soup(x),ids_soup(x), s))
                found_strings.add(s)
            except:
                continue
    return ret

class Kuskus:
    def __init__(self, soup):
        if type(soup)==str:
            soup=BeautifulSoup(soup, "html.parser")
        self.soup=soup
        self.dataset=generate_dataset(soup)
    def __getattr__(self, attr):
        return getattr(self.soup,attr)
    def __str__(self):
        return str(self.soup)
    def __repr__(self):
        return repr(self.soup)
    def fuzzy_match_by_text(self, text):
        return self.soup.findAll(text=fuzzy_pattern(text))
    def prune(self, **kwargs):
        for el in self.soup.findAll(**kwargs):
            el.decompose()
        return self
    def prune_scripts(self):
        for el in self.soup("script"):
            el.decompose()
        return self
    def prune_styles(self):
        for el in self.soup("style"):
            el.decompose()
        return self
    def prune_by_func(self, func):
        assert hasattr(func, "__call__")
        for d in self.dataset:
            if func(d):
                try:
                    d.element.decompose()
                except:
                    continue
        return self
    def prune_by_content_model(self, model, threshold=None, preprocess=str):
        if type(model)==str and os.path.exists(model):
            with open(model, 'rb') as f:
                model = joblib.load(f)
        assert hasattr(model, "predict")
        def pfunc(x):
            if threshold:
                return model.predict_proba([preprocess(x)])[0,1]<threshold
            return not model.predict([preprocess(x)])[0]
        return self.prune_by_func(pfunc)

if __name__=="__main__":
    html="""
    <html><body><div id="content">
    Ba <span class="a b c">boom</span>
    </div></body></html>
    """
    def is_boom(x):
        return x.text=="boom"
    soup=Kuskus(html)
    print(str(soup.prune_by_func(is_boom)))
