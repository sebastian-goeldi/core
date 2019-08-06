import pya
from pathlib import Path
import kppc
import json
import importlib

class Dialog(pya.QDialog):

    def __init__(self, parent = None):
        self.settingspath = Path(__file__).parent.parent/"settings.json"
        grid = pya.QGridLayout(self)
        self.setLayout(grid)
        self.settings = []
        self.setWindowTitle("KLayoutPhotonicPCells Settings")
        vsize = len(vars(kppc.settings))
        self.resize(300,100+vsize*25)
        
        prop = pya.QLabel("Property",self)
        self.layout.addWidget(prop,0,0)
        value = pya.QLabel("Value",self)
        self.layout.addWidget(value,0,1,pya.Qt.AlignmentFlag.AlignRight)
        settingdict = vars(kppc.settings)
        for i,setting in enumerate(settingdict.keys()):
            l = pya.QLabel(setting,self)
            self.layout.addWidget(l,i+1,0)
            s = settingdict[setting]
            if(isinstance(s,bool)):
                v = pya.QCheckBox(self)
                v.toggeled = v.setChecked(s)
            self.layout.addWidget(v,i+1,1,pya.Qt.AlignmentFlag.AlignRight)
            self.settings.append([l,v])
            
        save = pya.QPushButton("Save",self)
        save.clicked = self.save
        abort = pya.QPushButton("Cancel",self)
        abort.clicked = self.abort
        self.layout.addWidget(save,i+2,1)
        self.layout.addWidget(abort,i+2,0)
        
    def abort(self, checked):
        self.reject()
            
    def save(self, checked):
        sdict = {}
        for s in self.settings:
            if isinstance(s[1],pya.QCheckBox):
                sdict[s[0].text] = bool(s[1].checkState.to_i())
        with open(self.settingspath, 'w') as f:
            json.dump(sdict, f, indent=4, sort_keys=True)
        importlib.reload(kppc)
        self.accept()

def open():
    dialog = Dialog(pya.Application.instance().main_window())
    dialog.exec_()
    
open()