import ui
import time
import textwrap

class MainView(ui.View):
  class TitleBar(ui.View):
    def __init__(self,name='title_bar',frame=(0,0,240,30)):
      self.name=name
      self.frame=frame
      self.bg_color=(.9,.9,.9)
      self.flex='WB'
      self.alpha=0
      
      def slider_action(sender):
        body = sender.superview.superview['body']
        body.alpha = sender.value
        body.touch_enabled = sender.value
      
      setting_slider = ui.Slider(
        name = 'slider',
        x = self.width-100,
        flex = 'LTB',
        value = 1.0,
        action = slider_action)
      label = ui.ImageView(
        name='label',
        flex='RB',
        frame=(0,0,30,30),
        image=ui.Image.named('iob:grid_24')
        )
        
      self.add_subview(setting_slider)
      self.add_subview(label)
    
    def add_nodes(self,*views):
      neig = next(i for i in self.subviews if i.name=='slider')
      for v in views:
        v.frame = (
          neig.x-v.width-5,
          0,
          v.width,
          self.height)
        v.flex = 'LTB'
        self.add_subview(v)
        neig=v
    
    def layout(self):
      for v in filter(lambda v:v.alpha==0,
                 filter(lambda v:v.x>30, self.subviews)
                 or []):
        v.alpha = 1
      for v in filter(lambda v: v.x<30,
                 filter(lambda v:v.name!='label'
                                 and v.alpha!=0,
                        self.subviews)
                 or []):
        v.alpha = 0
      
    def touch_began(self,touch):
      self.superview.superview.selected()
      
      self.start = tuple(touch.location)
      self.o_p_frame = ui.Rect(*self.superview.frame)
      self.began_time = time.time()
    
    def touch_moved(self,touch):
      parent = self.superview
      parent.x += touch.location[0]-self.start[0]
      parent.y += touch.location[1]-self.start[1]
      if parent.y <= 25:
        parent.y = 25
        
    def touch_ended(self, touch):
      if sum([(self.superview.frame[i]-self.o_p_frame[i])**2 for i in range(2)])<=2:
        if touch.location[0]<30:
          parent = self.superview
          if time.time()-self.began_time<0.1:
            ui.animate(lambda : parent.mode_change((not(parent.mode-2))+2))
          else:
            self.superview.superview['conf'].update()
        
  class Controller(ui.View):
    def __init__(self,frame=(0,0,240,17),name='controller'):
      self.flex = 'WT'
      self.name = name
      self.frame = frame
      self.set_labels()
      
    def set_labels(self):
      sets = [
        {'name':'center','text':'–'*10,'flex':'WTB','frame':(0,self.height/2-25/2,self.width,25)},
        {'name':'left','text':'•','flex':'RTB','frame':(0,self.height/2-25/2,25,25)},
        {'name':'right','text':'•','flex':'LTB','frame':(self.width-25,self.height/2-25/2,25,25)}
      ]
      for i in sets:
        l = ui.Label(
              text_color=(.9,.9,.9),
              bg_color=(0,0,0),
              alignment=1,
              **i)
        self.add_subview(l)
      
    def touch_began(self, touch):
      self.superview.superview.selected()
      
      self.start = tuple(touch.location)
      self.o_frame = ui.Rect(*self.frame)
      self.o_p_frame = ui.Rect(*self.superview.frame)
      self.mode = (touch.location[0]<25)+(self.frame[2]-25<touch.location[0])*2
      
    def touch_moved(self, touch):
      parent = self.superview
      parent.height += (self.o_frame.height-self.start[1])-(self.height-touch.location[1])
      if parent.height <= 40:
        parent.height = 40
        
      if self.mode == 0:
        if parent.permissions.get(self.name,{}).get('x-move'):
          parent.x += touch.location[0]-self.start[0]
      elif self.mode == 1:
        n = touch.location[0]-self.start[0]
        parent.x += n
        parent.width -= n
      elif self.mode == 2:
        parent.width += (self.o_frame.width-self.start[0])-(parent.frame.width-touch.location[0])
      
      if parent.width <= 30:
        parent.width = 30
      
    def touch_ended(self, touch):
      if sum([(self.frame[1+i]-self.o_frame[1+i])**2 for i in range(3)])<=1:
        parent = self.superview
        ui.animate(lambda:parent.mode_change(not parent.mode))
  
  def __init__(self,_body=ui.View()):
    self.name = 'main'
    self.mode = 0
    self.frame = (0,0,240,240)
    
    body = self.setup_body(_body)
    title_bar = self.TitleBar(name='title_bar',frame=(0,0,self.width,30))
    controller = self.Controller(name='controller',frame=(0,self.height-17,self.width,17))
    
    self.add_subview(body)
    self.add_subview(title_bar)
    self.add_subview(controller)
    
    self.permissions = {'controller':{'x-move':True}}
  
  def __setattr__(self, name, value):
    super().__setattr__(name, value)
    if name in 'xy':
      self.superview.moved(self)
  
  def layout(self):
    title_exist = bool(self['title_bar'].alpha)*30
    body = self['body']
    if body is None:
      raise ValueError('body is None')
    body.frame = (
      0,
      title_exist,
      self.width,
      self.height-17-title_exist)
  
  def setup_body(self,_body):
    _body.height=self.height-17
    _body.bg_color=(0,0,1)
    _body.name='body'
    return _body
  
  def mode_change(self,mode):
    self.mode = mode
    
    if self.mode == 1:
      self.height += 30
      self['body'].height -= 30
      self['body'].y = 30
      self['title_bar'].alpha = 1
      self.y = 30
      self.permissions = {'controller':{'x-move':False}}
      
    elif self.mode == 0:
      self['title_bar'].alpha = 0
      self.height -= 30
      self['body'].height += 30
      self['body'].y = 0
      self.y = 0
      self.permissions = {'controller':{'x-move':True}}
      
    elif self.mode == 2:
      self['controller'].alpha=0
      self.height = 30
      self.width = 30
      
    elif self.mode == 3:
      self['controller'].alpha=1
      self.height = 240+30+17
      self.width = 240
      
    
class ConfigView(ui.View):
  def __init__(self):
    self.name='conf'
    self.frame = (187.5-65,283,130,60)
    self.border_width = 1
    self.border_color = (.8,.8,.8)
    self.alpha = 0
    
    class txf_delegate:
      def textfield_should_begin_editing(self, textfield):
        textfield.text = '#'+''.join(f'{int(0xff*i):02x}' for i in textfield.superview.selected_view.bg_color)
        return True
      
      def textview_did_change(self, textview):
        print(textview.txt)
      
    def txf_action(sender):
      text = sender.text
      if len(text)==9:
        setattr(
          sender.superview.selected_view,
          'bg_color',
          tuple(
            int(text[1+2*i:1+2*i+2],16)/255
              for i in range(4)
          ))
      else:
        sender.text = '#00000000'
    
    txf = ui.TextField(
      name = 'txf',
      frame = (0,0,self.width,30),
      action = txf_action,
      delegate = txf_delegate()
      )
    self.add_subview(txf)
    
    wv = ui.WebView(
      name='info_view',
      bg_color=(0,0,0,0),
      frame=(0,30,self.width-30,30)
      )
    self.add_subview(wv)
    
  def touch_began(self,touch):
    self.superview.selected()
    self.update()
    
  def update(self):
    _setattr = lambda d={}:[setattr(self,n,v) for n,v in d.items()]
    if not self.alpha:
      self.y += 10
      self.x += 10
      ui.animate(lambda :_setattr({'alpha':1,'y':self.y-10,'x':self.x-10}))
      
      html = '<form name="f"><select name="s" style="width:400px;font-size:63px">'+''.join(f'<option>{i.name}</option>' for i in self.superview.get_all_views())+'</select></form>'
      self['info_view'].load_html(html)
      
    else:
      ui.animate(lambda :_setattr({'alpha':0,'y':self.y+10,'x':self.x+10}),completion=lambda :_setattr({'y':self.y-10,'x':self.x-10}))
      
      
  @property
  def selected_view(self):
    index = self['info_view'].eval_js('(function (){return document.f.s.selectedIndex;})()')
    return self.superview.get_view_from_index(int(index))
      
class CapsuleView(ui.View):
  def __init__(self,id=0,frame=(0,0,0,0),body=ui.View()):
    self.name = f'capsule-{id}'
    self.id = id
    self.flex='WH'
    self.bg_color=(0,0,0,0)
    self.frame = frame
    
    self.add_subview(MainView(body))
    self.add_subview(ConfigView())
    self.get_all_views()

  def touch_began(self,touch):
    root=self.superview
    for cap in root.subviews:
      if cap is self:
        continue
      for v in cap.subviews:
        if touch.location in v.frame:
          cap.selected()
          return 
          
  def moved(self,view):
    #print(f'{view.name} was moved')
    if view.name == 'main':
      conf = self['conf']
      conf.touch_enabled = True
      conf.x = view.x-conf.width+30
      conf.y = view.y-conf.height+30
    
  def selected(self):
    for i in filter(lambda v:isinstance(v,(ui.TextField,ui.TextView)),self.all_views):
      if isinstance(i,(ui.TextField,)):
        i.enabled = False
        i.enabled = True
      else:
        i.editable=False
        i.editable = True
        
    self.bring_to_front()
  
  def get_view_from_index(self,ind):
    return self.all_views[ind]
  
  def get_all_views(self):
    def collector(v):
      res=[v]
      for i in v.subviews:
        res.extend(collector(i))
      return res
    
    self.all_views = collector(self)
    return self.all_views
    
class RootView(ui.View):
  def __init__(self,body=None,debug=True):
    self.name = 'root'
    self.id = 'root'
    self.count = 0
    self.debug = debug
    if body:
      self.capsule(body)
    
  def capsule(self,body):
    self.add_subview(
      CapsuleView(id=self.count,frame=self.frame,body=body))
    self.count += 1
  
  def present(self):
    super().present(hide_title_bar=True)
    self.bg_color = (.1,.1,.1,.5 if self.debug else 0)
    
    
root = RootView()

def present(*bodies):
  for body in bodies:
    root.capsule(body)
  root.present()
