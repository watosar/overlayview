import sys 
sys.path.append('../')
import appex
import photos
from template import lay_ui
import ui
      
class CustumBody(ui.View):
  def layout(self):
    self['wv'].width=self.width
    self['wv'].height = self.height

body = ui.load_view()

for i in ['wv','back','forward','url','home']:
  globals()[i]=body[i]

back.action = lambda s:wv.go_back()
forward.action = lambda s:wv.go_forward()
url.action = lambda s:wv.load_url(s.text)
home.action = lambda s:wv.load_url('https://google.com')
class wv_delegate:
  def webview_should_start_load(self, webview, url, nav_type):
    webview.superview['url'].text=url
    return True
wv.delegate = wv_delegate()


wv.load_url('https://google.com') 

root=lay_ui.RootView(body)
root.debug=False
root.present()
