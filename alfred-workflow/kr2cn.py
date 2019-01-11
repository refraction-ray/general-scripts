import requests
import re
import json
import sys

def filter_mean(s):
    s = re.sub(r"<.*?>","",s)
    s = s.strip()
    return s
    
def kr2cn(word):
    url = "https://zh.dict.naver.com/cndictApi/search/all?sLn=ko&q=%s&mode=pc&pageNo=1&format=json"%word
    try:
        r = requests.get(url)
        itemList = r.json().get('searchResults').get('searchEntryList').get('items')
        if not itemList:
            return None
        return [{"entry": a.get('entryNameTTS') ,"hanja": a.get('fantizi'), "meaning":[(b.get('partsLabel'),filter_mean(b.get("mean")) ) for b in a.get('meanList')]} for a in itemList ]
    except:
        return None

if __name__ == "__main__":
    result = []
    word = sys.argv[1] # pbpaste|xargs python3 kr2cn.py
    # word = sys.stdin.readlines()[0] # pbpaste|python3 kr2cn.py 
    con = kr2cn(word)
    if not con:
        result = {'items': [{'title':'no such word'}]}
    else:
        for entry in con:
            title = entry.get("entry")
            if entry.get("hanja"):
                title += "("+entry.get('hanja')+")"
            subtitle = ""
            for mean in entry.get('meaning'):
                subtitle += mean[0] + ": " + mean[1]
            result.append({'title': title,
                'subtitle': subtitle})
        result={'items':result}
    print(json.dumps(result))