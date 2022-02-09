import re
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.properties import (
    NumericProperty, ObjectProperty
)


from conversions import conversions
class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    num = NumericProperty(0)
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join([re.sub(pat, '', s) for s in substring.split('.', 1)])
        
        retval = super().insert_text(s, from_undo=from_undo)
        self.num = float(self.text)
        return retval

    def set_value(self, value):
        self.text = f'{value:.3f}'

class FormPair(BoxLayout):
    val_input = ObjectProperty(None)
    def setup_signals(self):
        self.val_input.bind(text=self.on_text)
    def set_value(self, *args, **kwargs):
        return self.val_input.set_value(*args, **kwargs)
    
class ConversionWidget(BoxLayout):
    laser_widget = ObjectProperty(None)
    ev_widget = ObjectProperty(None)
    nm_widget = ObjectProperty(None)
    cm_widget = ObjectProperty(None)
    thz_widget = ObjectProperty(None)

    def __init__(self):
        super().__init__()
        self.laser_widget.val_input.bind(num=self._on_laser)
        self.ev_widget.val_input.bind(num=self._on_ev)
        self.nm_widget.val_input.bind(num=self._on_nm)
        self.cm_widget.val_input.bind(num=self._on_cm)
        self.thz_widget.val_input.bind(num=self._on_thz)

    
    def _on_laser(self, instance, new):
        self.evaluate_all(laser=new)
    def _on_ev(self, instance, new):
        self.evaluate_all(ev=new)
    def _on_nm(self, instance, new):
        self.evaluate_all(nm=new)
    def _on_cm(self, instance, new):
        self.evaluate_all(cm=new)
    def _on_thz(self, instance, new):
        self.evaluate_all(thz=new)
 
    def evaluate_all(self, **kwargs):#laser=None, ev=None, nm=None, cm=None):
        others = ['nm', 'ev', 'cm', 'thz']
        if 'laser' in kwargs:
            hz = 0
            laser = kwargs['laser']
        # laser = kwargs.get('laser', self.laser)
        else:
            name, val = list(kwargs.items())[0]
            laser=self.laser_widget.val_input.num
            hz = kwargs.get('hz', conversions['to_hz'][name](val, laser=laser))
            others.remove(name)
            
        for attr in others:
            widget = getattr(self, f'{attr}_widget')
            try:
                getattr(widget, 'set_value')(conversions['hz_to'][attr](hz, laser=laser))
            except ZeroDivisionError:
                getattr(widget, 'set_value')(0)

    
class ConversionApp(App):
    def build(self):
        return ConversionWidget()

if __name__ == '__main__':
    ConversionApp().run()
