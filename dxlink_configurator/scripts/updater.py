#Updater

import requests
from bs4 import BeautifulSoup
from distutils.version import StrictVersion

version = "v3.1.0"

r = requests.get('https://github.com/AMXAUNZ/Magic-DXLink-Configurator/releases')

soup = BeautifulSoup(r.text)

#print soup

test = soup.find_all("div", class_="release label-latest")
url_path = test[0].find_all('a')[-3].get('href')

online_version = url_path.split('/')[-2]

if StrictVersion(online_version[1:]) > StrictVersion(version[1:]):
    print 'time to update to ', StrictVersion(online_version[1:])
    print url_path
else:
    print 'not updating to', StrictVersion(version[1:])
#    print div.find_all("a")[-3].get('href').split('/')[-2]
      



"""
<div class="release-timeline">
<div class="release label-latest">
<div class="release-meta">
<span class="release-label latest">
<a href="/AMXAUNZ/Magic-DXLink-Configurator/releases/latest">Latest release</a>
</span>
<ul class="tag-references">
<li>
<a class="css-truncate" href="/AMXAUNZ/Magic-DXLink-Configurator/tree/v.3.1.1">
<span class="octicon octicon-tag"></span>
<span class="css-truncate-target">v.3.1.1</span>
</a>
</li>
<li>
<a href="/AMXAUNZ/Magic-DXLink-Configurator/commit/631883d089a35a8316a63dd9a5557649b75e4bbb">
<span class="octicon octicon-git-commit"></span>
            631883d
          </a>
</li>
</ul>
</div><!-- /.meta -->
<div class="release-body commit open">
<div class="release-header">
<h1 class="release-title">
<a href="/AMXAUNZ/Magic-DXLink-Configurator/releases/tag/v.3.1.1">v.3.1.1</a>
</h1>
<p class="release-authorship">
<img alt="@jmagic" class="avatar" height="20" src="https://avatars3.githubusercontent.com/u/1159605?v=3&amp;s=40" width="20"/>
<a href="/jmagic">jmagic</a>
        released this
          <time datetime="2015-03-14T06:53:45Z" is="relative-time">Mar 14, 2015</time>
</p>
</div>
<div class="markdown-body">
<p>A quick couple of fixes here. This addresses:</p>
<p>Double entries when connected to two or more networks.<br/>
Added preference for connection type.<br/>
Added auto download of putty.exe<br/>
Corrected where configure was incrementing devices number 0</p>
<p>Enjoy!</p>
</div>
<h2 class="release-downloads-header">Downloads</h2>
<ul class="release-downloads">
<li>
<a href="/AMXAUNZ/Magic-DXLink-Configurator/releases/download/v.3.1.1/Magic_DXLink_Configurator_Setup_3.1.1.exe" rel="nofollow">
<small class="text-muted right">8.05 MB</small>
<span class="octicon octicon-package left text-muted"></span>
<strong>Magic_DXLink_Configurator_Setup_3.1.1.exe</strong>
</a>
</li>
<li>
#table = soup.find(lambda tag: tag.name=='tr')
# and tag.has_key('id') and tag['id']=="Table1") 
table = soup.find_all( "table" )
#print table[4]
print str(data)

"""