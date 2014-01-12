import requests, pyquery, datetime, html2text, os, re
from django.template.defaultfilters import slugify

from codrspace.models import Post, Photo

urls = [
'http://cyberchuck-video.homeip.net/txrx/?p=1881',
'http://cyberchuck-video.homeip.net/txrx/?p=1872',
'http://cyberchuck-video.homeip.net/txrx/?p=1863',
'http://cyberchuck-video.homeip.net/txrx/?p=1646',
'http://cyberchuck-video.homeip.net/txrx/?p=1634',
'http://cyberchuck-video.homeip.net/txrx/?p=1595',
'http://cyberchuck-video.homeip.net/txrx/?p=1565',
'http://cyberchuck-video.homeip.net/txrx/?p=1476',
'http://cyberchuck-video.homeip.net/txrx/?p=1462',
'http://cyberchuck-video.homeip.net/txrx/?p=1396',
'http://cyberchuck-video.homeip.net/txrx/?p=1405',
'http://cyberchuck-video.homeip.net/txrx/?p=1353',
'http://cyberchuck-video.homeip.net/txrx/?p=1344',
'http://cyberchuck-video.homeip.net/txrx/?p=1339',
'http://cyberchuck-video.homeip.net/txrx/?p=1330',
'http://cyberchuck-video.homeip.net/txrx/?p=1315',
'http://cyberchuck-video.homeip.net/txrx/?p=1302',
'http://cyberchuck-video.homeip.net/txrx/?p=1293',
'http://cyberchuck-video.homeip.net/txrx/?p=1279',
'http://cyberchuck-video.homeip.net/txrx/?p=1272',
'http://cyberchuck-video.homeip.net/txrx/?p=1269',
'http://cyberchuck-video.homeip.net/txrx/?p=1241',
'http://cyberchuck-video.homeip.net/txrx/?p=1230',
'http://cyberchuck-video.homeip.net/txrx/?p=1188',
'http://cyberchuck-video.homeip.net/txrx/?p=1164',
'http://cyberchuck-video.homeip.net/txrx/?p=1135',
'http://cyberchuck-video.homeip.net/txrx/?p=1112',
'http://cyberchuck-video.homeip.net/txrx/?p=1081',
'http://cyberchuck-video.homeip.net/txrx/?p=931',
'http://cyberchuck-video.homeip.net/txrx/?p=958',
'http://cyberchuck-video.homeip.net/txrx/?p=870',
'http://cyberchuck-video.homeip.net/txrx/?p=890',
'http://cyberchuck-video.homeip.net/txrx/?p=784',
'http://cyberchuck-video.homeip.net/txrx/?p=761',
'http://cyberchuck-video.homeip.net/txrx/?p=252',
'http://cyberchuck-video.homeip.net/txrx/?p=231',
'http://cyberchuck-video.homeip.net/txrx/?p=235',
'http://cyberchuck-video.homeip.net/txrx/?p=75',
'http://cyberchuck-video.homeip.net/txrx/?p=212',
'http://cyberchuck-video.homeip.net/txrx/?p=242',
'http://cyberchuck-video.homeip.net/txrx/?p=59',
'http://cyberchuck-video.homeip.net/txrx/?p=60',
'http://cyberchuck-video.homeip.net/txrx/?p=61',
'http://cyberchuck-video.homeip.net/txrx/?p=62',
'http://cyberchuck-video.homeip.net/txrx/?p=63',
'http://cyberchuck-video.homeip.net/txrx/?p=64',
'http://cyberchuck-video.homeip.net/txrx/?p=65',
'http://cyberchuck-video.homeip.net/txrx/?p=66',
'http://cyberchuck-video.homeip.net/txrx/?p=67',
'http://cyberchuck-video.homeip.net/txrx/?p=68',
'http://cyberchuck-video.homeip.net/txrx/?p=53',
'http://cyberchuck-video.homeip.net/txrx/?p=54',
'http://cyberchuck-video.homeip.net/txrx/?p=55',
'http://cyberchuck-video.homeip.net/txrx/?p=56',
'http://cyberchuck-video.homeip.net/txrx/?p=58',
'http://cyberchuck-video.homeip.net/txrx/?p=57'
]

authors = {
    'rgbiv': 106,
    'rtavk3': 3,
    'KingJacob': 659,
    'patrick': 18,
    'txrxlabs': 660,
    'wanjun': 661,
    'quintar': 662,
    'hackerspace': 663,
}

def get_cache(path,getter,root='data',mode='r'):
    path = os.path.join(root,path)
    if os.path.exists(path):
        f = open(path,mode)
        data = f.read()
        f.close()
        return data
    f = open(path,'w')
    text = getter()
    f.write(text)
    f.close()
    print "got " + path
    return text

def get_url(url):
    r = requests.get(url)
    replace = [(u'\xed','&iacute;'),(u'arstarst',"&#39;"),(u'\xa0',' '),(u'\xe1','&aacute;'),(u'\u2013','-'),(u'\u2014','-'),
               (u'\u2019',"&#39"),(u'\u201c','&ldquo;'),(u'\u201d','&rdquo;')]
    text = r.text
    for t in replace:
        text = text.replace(*t)
    return text

#f = open("data/data.py",'r')
#posts = eval(f.read())
#f.close()

posts = {}

for i,url in enumerate(urls):
    if url in posts:
        continue
    text = get_cache(str(i)+".html",lambda: get_url(url))
    try:
        P = pyquery.PyQuery(text)
    except Exception,e:
        print "url fail: %s"%e
        continue
    content = html2text.html2text(P(".post-content").html())
    title = P("h1").text().strip()
    
    author = P(".post-author").text()
    date = P(".post-date")
    time = date.next().text().upper()
    publish_dt = datetime.datetime.strptime("%s %s"%(date.text(),time),"%b %d, %Y %I:%M %p")
    if not author in authors:
        print "not found: %s"%repr(author)
        continue

    images = re.findall(r'!\[\]\(([^\)]+)\)',content)
    for i in images:
        i_url = i.replace('\n','')
        def get_image():
            return requests.get(i_url,stream=True).raw.read()
        get_cache(i_url.split('/')[-1],get_image,root='media/uploads/photos/2013-06',mode='wb')
        image_path = 'media/uploads/photos/2013-06/'+i_url.split('/')[-1]
        p = Photo(file=image_path)
        new_content = content.replace('![](%s)'%i,'![](/%s)'%image_path)
        if new_content == content:
            print "Fail!"
            break
        content = new_content
            
    s =  '\n'*5+"TITLE: %s\n"%title
    s +=  "\n\nAUTHOR MISSING\n\n: "+author
    s +=  "DATETIME: %s\n"%publish_dt
    s +=  "CONTENT: \n"+content[:500]
        #print s
    command = 'y' #raw_input("keep it(y)? (c)ut first line? (s)kip?")
    posts[url] = {
        'title': title,
        'author_id': authors[author],
        'publish_dt': publish_dt,
        'slug': slugify(title),
        'status': 'published',
        'content': content,
        }
    if Post.objects.filter(title=title):
        continue
    obj = Post(**posts[url])
    obj.save()
    posts[url]['id'] = obj.id

f =open('data/data.py','w')
f.write(repr(posts))
f.close()
