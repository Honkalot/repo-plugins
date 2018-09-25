import httplib, logon, re, xbmcgui

from urllib2 import unquote

#cookie = {}
show = {}
shows = "/shows"

def popup(text):
  xbmcgui.Dialog().ok('plugin.video.tyt', text)

def Get_Show_Episodes(page):
#  page = sendResponse(cookie, page) # main show episode list
#  with open('main_show.html', 'w') as f:
#    f.write(page)
#  videos = []
  hosts = {}
  episodes = re.compile('id="tag">(.+?)</div></tyt-feed-tag><!----><!.+?href="(.+?)".+?data-image-id="(.+?)".+?underbox"><.+?"">(.+?)</h1>.+?Hosts:(.+?)</span></span>.+?<!----><!----><!----><!---->.+?href=".+?"> (.+?)</a>',re.DOTALL).findall(page)
  i = 0
  for date, link, image_id, title, allhosts, description in episodes:
    hosts_decoded = re.compile('href="(.+?)">(.+?)<',re.DOTALL).findall(allhosts)
    image = re.search('data-image-id="%s".+?url\((.+?)\)' % image_id, page, re.MULTILINE | re.DOTALL).group(1)
    x = 0
    for host_info, host in hosts_decoded:
      hosts[x] = {"host": host,
                  "info": host_info
                  }
      x+=1
    show[i] = {"date" : date,
               "title": title,
               "image": image,
               "link": link,
               "description": description,
               "hosts" : hosts
              }
    i+=1
  return show

def Watch_Episode(page):
#  page = sendResponse(cookie, page) # main show episode list
#  with open('main_show_episode.html', 'w') as f:
#    f.write(page)
  episode = re.compile('tap to download" href="(.+?)">.+?tap to download" href="(.+?)">',re.DOTALL).findall(page)
  for link in episode: return link

def List_Shows(page):
#  page = sendResponse(cookie, page)

#  with open('shows.html', 'w') as f:
#    f.write(page)
  
  shows = re.compile('class="show responsive-background" aria-label="(.+?)".+?href="(.+?)".+?"(.+?)".+?summary.+?"">(.+?)<',re.DOTALL).findall(page)
  i = 0
  for showname, link, image_id, description in shows:
    #need to find banner, then web_header_image
    banner =  re.search('data-image-id="%s".+?url\((.+?)\)' % image_id, page, re.MULTILINE | re.DOTALL).group(1)
    background = re.search('<script id="tytapp-state".+?%s.+?web_header_image.+?:&q;(.+?)&q' % banner, page, re.MULTILINE | re.DOTALL).group(1)
    image2 = re.search('href="%s".+?data-image-id="(.+?)"' % link, page, re.MULTILINE | re.DOTALL).group(1)
    avatar =  re.search('data-image-id="%s".+?url\((.+?)\)' % image2, page, re.MULTILINE | re.DOTALL).group(1)
    show[i] = {"show" : showname,
               "background": background,
               "description": description,
               "link" : link,
               "banner" : banner,
               "avatar" : avatar}
    i+=1
  return show
#loggedin, cookies = logon.logon('brian_soucy@hotmail.com', 'eliteelite420')
#logon.save_cookie(cookies)

#List_Shows(shows)
#Get_Show_Episodes(show[11]["link"] + "/episodes")#?page=3")
#hd, sd = Watch_Episode(main_show_episode)

