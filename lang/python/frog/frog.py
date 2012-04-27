# -*- coding: iso-8859-15 -*-

# frog.py
# Extended turtle-graphics like object oriented graphics
# Dependencies: Python >= 2.5 with Tkinter (compatible with Python 3.0!)

__author__  = "Marco Haase"
__date__    = "14.02.2009"
__version__ = "1.0.1"

"""
This program is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation; either version 3 of the License, or any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program; if not, see <http://www.gnu.org/licenses/>.
"""

# Checking system and platform conditions and choose correct imports

import sys, math, platform, subprocess, os.path
import time as timemodul # to avoid import conflict between time and time()

if sys.version_info[0] == 3: # Python 3.x
    import tkinter as tk
    import tkinter.font as tkFont
    import tkinter.simpledialog as tkSimpleDialog
    import tkinter.messagebox as tkMessageBox
    xrange = range
elif sys.version_info[:2] > (2,4): # Python 2.x (2.5+)
    import Tkinter as tk
    import tkFont, tkSimpleDialog, tkMessageBox
else: # unsupported version
    print("Frog is not compatible with the installed Python-version:")
    print("Python "+sys.version.replace("\n",""))
    print("You need at least Python 2.5 to use the frog module.")
    sys.exit(1)

_LINUX = True if platform.system() == "Linux" else False
_WINDOWS = True if platform.system() == "Windows" else False
_PIL = False  # Python Image Library

if _WINDOWS:
    import winsound
    try:
        import ImageGrab # used for snapshot on Windows OS
        _PIL = True
    except ImportError:
        pass

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +                        class Color                          +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Color(object):
    """Some static methods for conversion of color representation"""

    @staticmethod
    def register(pool):
        """A widget is needed to use tk's RGB-conversion method.
        This method is only called at instantiation of a Pool object."""
        Color._pool = pool

    @staticmethod # private method
    def _toRGB(r,g=None,b=None):
        """Tries to convert rawcolor col into RGB-Format. Possible formats:
        col = 'colorname' e.g. 'blue'
        col = '#rrggbb' e.g. '#A0CC9F' or '#rgb' e.g.
        col = r, g, b   where r|g|b := 0 .. 255
        col = (r, g, b) where r|g|b := 0.0 .. 1.0
        Returns valid tk-colorstring or throws FrogError.
        """
        if g is None and b is not None or g is not None and b is None:
            return None
        try:
            if g is None:
                if isinstance(r,tuple): r,g,b = r
                else: colstr = r
            if g is not None: # 'else' doesn't work! g could be changed
                if isinstance(r,float): r = int(round(255*r))
                if isinstance(g,float): g = int(round(255*g))
                if isinstance(b,float): b = int(round(255*b))
                colstr = "#%02x%02x%02x" %(r,g,b)
            rgb = tuple([v % 256 for v in Color._pool.winfo_rgb(colstr)])
            return rgb
        except:
            return None

    @staticmethod
    def isvalid(*args):
        """Checks whether *args is/are a valid color"""
        if Color._toRGB(*args): return True
        else: return False

    @staticmethod
    def toRGB(*args):
        """Converts any valid color into a Tupel (r,g,b with 0<=r,g,b<=255"""
        rgb = Color._toRGB(*args)
        if rgb is None:
            raise Exception("%s is no valid color" %(str(args)[1:-2]))
        else:
            return rgb

    @staticmethod
    def toRGBrel(*args):
        """Converts any valid color into a Tupel (r,g,b with 0.0<=r,g,b<=1.0"""
        rgb = Color._toRGB(*args)
        if rgb is None:
            raise Exception("%s is no valid color" %(str(args)[1:-2]))
        else:
            return tuple([v/255.0 for v in rgb])

    @staticmethod
    def toRGBstr(*args):
        """Converts any valid color into Hex-Colorstring used e.g. in HTML.
        Different to the other color methods an empty string is allowed
        as argument and is simply passed through - stands for transparency.
        """
        s = args[0]
        if isinstance(s,str) and s.strip()=="":
            return s.strip()
        rgb = Color._toRGB(*args)
        if rgb is None:
            raise Exception("%s is no valid color" %(str(args)[1:-2]))
        else:
            return "#%02x%02x%02x" %rgb

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +                         class Pool                          +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Pool(tk.Canvas,object):

    DEFAULTSIZE = 400, 300 # if none of width, height or bgimage is set
    _timecounter = timemodul.time if _LINUX else timemodul.clock
    _idcounter = 0 # every pool gets an ID, beginning with 1 and so on

    def __init__(self, root=None, width=None, height=None, title=None,
                bgcolor="white", bgimage=None, pos="topleft", resizable=True):
        """If root is None, a Tk() instance is created for a standalone GUI.
        If width/height are None, default values are set. OR, if bgimage is set
        to a valid image-filename, width/height will fit to the size of that
        image as background. If widht/height AND bgimage are set, the image
        is placed in the center of the pool with the given dimensions.
        """
        if root is None: # standalone
            try: # create Tk()-instance if none is running
                tkFont.Font() # only works, if Tk()-instance is running
                self.__root = tk.Toplevel()
            except: # create Toplevel()-instance if Tk() is running
                self.__root = tk.Tk()
            self.__root.resizable(resizable,resizable)
            self.__standalone = True
        else: # embedded
            self.__root = root
            self.__standalone = False
        tk.Canvas.__init__(self,self.__root)
        Color.register(self) # class Color needs instance of Pool
        # ---- configure:
        Pool._idcounter += 1
        self.__id = "Pool-%04i" %Pool._idcounter
        self.__visible = True    # only valid. if pool is standalone
        self.__initialsize = width,height # width/height given at instantiation
        self.__frogs = tuple()   # Collection of all existing frogs
        self.__action = False    # flag to avoid missplacing at acting/resizing
        self._dx, self._dy = 0,0 # delta to move (0,0) to center of pool
        self.setbgcolor(bgcolor) # set bgcolor
        self.setbgimage(bgimage) # set bgimage; width/height are also set
        self.__timerID = {}      # dictionary for timer-events
        self.__fontID = []       # necessary workaround for a bug in tkFont
        self.bind("<Configure>",self._rearrange) # rearrange if resized
        self.focus_set()         # to react on key-events
        if self.__standalone:
            if title is None:
                title = "Pool %i" %Pool._idcounter if Pool._idcounter>1 else "Pool"
            self.__root.title(title)
            self.pack(expand=True,fill=tk.BOTH)
            self._setpos(pos) # set initial position on the screen

    def __str__(self):
        return self.__id

    # ---------- private methods ----------

    def _eventhandler(self,e,func):
        """Universal eventhandler that interprets real events catched by
        pool's method listen() and delivers a dictionary with all necessary
        event-data as only argument to func, which is the really handler.
        Timer- and Close-Event are handled directly in method listen().
        """
        if not e.type in ['2','3','4','5','6','7','8','38']:
            raise Exception("Event-type cannot be handled by listen()")
        if e.type == "38": # MouseWheel - Windows only!
            name = "Up" if e.delta>0 else "Down"
        elif e.type == "4" and _LINUX and e.num in [4,5]:
            e.type = "38" # MouseWheel - simulate event on Linux
            name = "Up" if e.num == 4 else "Down"
        eventtype = {"2":"Key", "3":"KeyRelease", "4":"Button",
                     "5":"ButtonRelease", "6":"Motion",
                     "7":"Enter", "8":"Leave", "38":"MouseWheel"}
        x, y = -self._dx+e.x, self._dy-e.y
        key = "" if e.keysym == "??" else e.keysym
        btn = "" if e.num == "??" else "Button-"+str(e.num)
        ch = "" if e.char == "??" else e.char
        name = key or btn if e.type != "38" else name
        event = {"type":eventtype[e.type], "name":name, "char":ch,
                 "pos":(x,y), "time":e.time, "object":self}
        func(event)

    def _setaction(self,action):
        """Set flag self.__action according to acting frogs."""
        if self.__action == action: return
        self.__action = action
        if not action:
            for frog in self.__frogs:
                if frog.active:
                    self.__action = True
                    break

    def _refresh(self):
        """Set all visible frogs to front of the canvas.
        Must be called after any drawing operation to avoid
        that a frog is being hidden by other items.
        """
        for frog in self.__frogs:
            self.tag_raise(frog._Frog__itemID) # if ID=0 nothing happens
        self.update()

    def _rearrange(self,event=None):
        """Rearrange position of all items after pool has been resized."""
        if self.__action: return # frog is in action - don't rearrange!
        self.__action = True
        dx, dy = 0.5*self.width, 0.5*self.height
        mvx, mvy = dx-self._dx, dy-self._dy
        self._dx, self._dy = dx, dy # new deltas
        for item in self.find_all():
            self.move(item,mvx,mvy)
        self.update()
        self.__action = False

    def _setpos(self,pos):
        """Set position of pool on the screen on startup. Possible Values are:
        left, right, top, bottom; topleft, topright, bottomleft, bottomright
        and center. Default is 'topleft'."""
        self.update()
        pos = pos.lower()
        w, h = self.winfo_width(), self.winfo_height() # without decoration
        sw, sh = self.winfo_screenwidth(),self.winfo_screenheight()
        cx, cy = (sw-w)//2, (sh-h)//2
        positions = {"topleft":"+0+0","top":"+%i+0" %cx, "topright":"-0+0",
            "bottomleft":"+0-0","bottom":"+%i-0" %cx, "bottomright":"-0-0",
            "left":"+0+%i" %cy,"right":"-0+%i" %cy, "center":"+%i+%i" %(cx,cy)}
        try:
            position = positions[pos]
        except KeyError:
            position = "+0+0" # default: topleft
        size = "%ix%i" %(w,h)
        self.__root.geometry(size+position)

    # -------- getter/setter bind to properties

    def getid(self):
        """Return the pool's ID."""
        return self.__id

    def getvisible(self):
        """Return True if the pool is visible, False otherwise.
        Only reliable if pool is standalone; visibility of embedded
        pools depends on the visibility of the Toplevel-widget."""
        return self.__visible

    def setvisible(self,state):
        """Set the pool's visibility-state, if it is a standalone pool.
        Has no effect on embedded pools."""
        if not self.__standalone or state==self.__visible:
            return
        if self.__visible:
            self.__root.withdraw()
        else:
            self.__root.deiconify()
        self.__visible = not self.__visible

    def getwidth(self):
        """Return Pool's width."""
        self.update()
        w = self.winfo_width()
        return w-2 if _LINUX else w-4

    def getheight(self):
        """Return Pool's height."""
        self.update()
        h = self.winfo_height()
        return h-2 if _LINUX else h-4

    def getbgcolor(self):
        """Return Pool's background color."""
        bg = self.cget("background")
        if Color.toRGBstr(bg) != Color.toRGBstr(self.__bgcolor):
            self.__bgcolor = bg   # color might be changed by canvas.config()
        return self.__bgcolor

    def setbgcolor(self,col):
        """Set Pool's background color."""
        if col:
            rgbstr = Color.toRGBstr(col) # raises FrogError if col is invalid
        else:
            col = rgbstr = "white"
        self.__bgcolor = col
        self.config(bg=rgbstr)

    def getbgimage(self):
        """Return filename of Pool's background image."""
        if self.__bgimage:
            return self.__bgimage.cget("file")
        else:
            return None

    def setbgimage(self,filename):
        """Set image filename as background. If width/height of pool are not
        given in self.__initialsize during initialization of pool,
        the pool's width/height are set to the width/height of bgimage.
        If bgimage is None, width/height are set to Pool.DEFAULTSIZE.
        """
        if len(self.find_all())==0: # called while initializing the pool
            w,h = self.__initialsize
            if filename is None:
                self.__bgimage = tk.PhotoImage()
                width = w if w else Pool.DEFAULTSIZE[0]
                height = h if h else Pool.DEFAULTSIZE[1]
            else:
                self.__bgimage = tk.PhotoImage(file=filename)
                width = w if w else self.__bgimage.width()
                height = h if h else self.__bgimage.height()
            self.config(width=width,height=height)
            self.create_image(0,0,image=self.__bgimage)
        elif filename == self.getbgimage(): # nothing to change
            return
        elif filename is None: # delete bgimage
            self.__bgimage = None
            self.itemconfig(1,image=tk.PhotoImage())
        else: # set new bgimage
            self.__bgimage = tk.PhotoImage(file=filename)
            self.itemconfig(1,image=self.__bgimage)
        self.update()

    def gettitle(self):
        """Return Pool's window title, if running standalone."""
        if self.__standalone:
            return self.__root.title()
        else:
            return None

    def settitle(self,title):
        """Has no effect if pool is part of a surrounding Tkinter-GUI."""
        if self.__standalone:
            self.__root.title(title)

    def getfrogs(self):
        """Return list of all existing frogs"""
        return list(self.__frogs)

    def getaction(self):
        """Return True if any frog movement or rearranging of items"""
        return self.__action

    def getresolution(self):
        """Return resolution of screen in dpi.
        Given Value may not be precise, but is good enough to calculate
        scaled measurements.
        """
        xDPI = self.__root.winfo_screenwidth() / (self.__root.winfo_screenmmwidth()/25.4)
        yDPI = self.__root.winfo_screenheight() / (self.__root.winfo_screenmmheight()/25.4)
        return int(round(0.5*(xDPI+yDPI)))

    def getcursor(self):
        """Return current cursor type. Empty string if standard cursor."""
        return self.cget("cursor")

    def setcursor(self,name):
        """Set a special cursor image. For standard cursor set empty string."""
        try:
            self.config(cursor=name)
        except:
            pass

    # ---------- properties --------

    id = property(getid)
    visible = property(getvisible,setvisible)
    width = property(getwidth)
    height = property(getheight)
    bgcolor = property(getbgcolor,setbgcolor)
    bgimage = property(getbgimage,setbgimage)
    title = property(gettitle,settitle)
    frogs = property(getfrogs)
    action = property(getaction)
    resolution = property(getresolution)
    cursor = property(getcursor,setcursor)

    # ---------- other public methods ----------

    def ready(self):
        """Setting up eventloop."""
        if self.__standalone:
            self.__root.mainloop()

    def listen(self,seq,func,add=False):
        """Create a binding between an event, specified by seq and a
        function func which has to provide exactly ONE parameter.
        The event is filtered and interpreted by the method _eventhandler(),
        that provides a dictionary with the needed event-data delivered
        to func. If func is None, unbind is executed.
        Timer-events and Close-event are directly handled here.
        """
        event = {"type":"undefined", "name":"", "char":"",
                 "pos":"", "time":"", "object":self}
        if seq == "<Close>": # Pool is going to be closed
            event["type"] = "Close"
            if func is None:
                func = lambda e : None
            self.__root.protocol("WM_DELETE_WINDOW",lambda e=event:func(e))
        elif "MouseWheel" in seq and _LINUX:
            seq1 = seq.replace("MouseWheel","Button-4")
            seq2 = seq.replace("MouseWheel","Button-5")
            if func is None:
                self.unbind(seq1)
                self.unbind(seq2)
            else:
                add = "+" if add else None
                self.bind(seq1,lambda event,f=func:self._eventhandler(event,f),add)
                self.bind(seq2,lambda event,f=func:self._eventhandler(event,f),"+")
        elif "Timer" in seq: # timer, no real binding
            seqstr = seq[:-1]+"-0>" if seq.endswith("Timer>") else seq
            try:
                seq = seqstr.strip("<>").split("-")
                mod, typ, det = seq if len(seq)==3 else ["Any"]+seq
                time = int(det)
                if func is None: # delete Timer
                    mods = self.__timerID.keys() if mod == "Any" else [mod] if mod in self.__timerID else []
                    for mod in mods:
                        ids = self.__timerID[mod]
                        for idd in ids:
                            self.after_cancel(idd)
                        del self.__timerID[mod]
                else: # func is not None
                    event["type"] = "Timer"
                    event["name"] = "" if mod == "Any" else mod
                    idd = self.after(time,lambda e=event:func(e))
                    if mod in self.__timerID:
                        if not idd in self.__timerID[mod]:
                            self.__timerID[mod].append(idd)
                    else:
                        self.__timerID[mod]=[idd]
            except:
                raise Exception("%s is not a valid event-sequence" %seqstr)
        elif func is None: # unbind
            self.unbind(seq)
        else:
            add = "+" if add else None
            self.bind(seq,lambda event,f=func:self._eventhandler(event,f),add)

    def _capture_with_iview(self,command,area,filename):
        """Make a snapshot with IrfanView and save as filename."""
        geometry = "(%i,%i,%i,%i)" %area
        call = [command,"/capture=3","/crop="+geometry,"/convert="+filename]
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            call.append("/jpgq=95")
        try:
            returncode = subprocess.call(call)
            return False if returncode else True
        except:
            return False

    def _capture_with_PIL(self,command,area,filename):
        """Make a snapshot with PIL's grab()-function and save as filename."""
        if not _PIL: return False
        if self.__standalone:
            x1 = area[0]+self.winfo_rootx()
            y1 = area[1]+self.winfo_rooty()
        else:
            x1 = area[0]+self.winfo_toplevel().winfo_x()+2
            y1 = area[1]+self.winfo_toplevel().winfo_y()+2
        x2, y2 = x1+area[2], y1+area[3]
        try:
            img = ImageGrab.grab((x1,y1,x2,y2))
            if filename.endswith("jpg") or filename.endswith("jpeg"):
                img.save(filename,quality=95)
            else:
                img.save(filename)
            return True
        except:
            return False

    def _capture_with_import(self,command,area,filename):
        """Make a snapshot with ImageMagick's import and save as filename."""
        area = area[2:]+area[:2]
        geometry = "%ix%i+%i+%i" %area
        windowname = self.winfo_toplevel().title()
        call = [command,"-silent","-window",windowname,"-crop",geometry]
        if filename.endswith(".gif"):
            # workaround for gif-images needed; doesn't work in all cases
            # works fine with SuSE 10.0, not with SuSE 11.0
            # possible solution: save as png and convert into gif
            call.extend(["-repage","%ix%i" %area[:2]])
        if filename.endswith(".jpg") or filename.endswith(".jpeg"):
            call.extend(["-quality","95"])
        call.append(filename)
        try:
            returncode = subprocess.call(call)
            return False if returncode else True
        except:
            return False

    def _capture_with_xwd(self,command,area,filename):
        """Make a snapshot with Xorgs xwd and save as filename.
        The area argument is ignored, gif-format is not possible."""
        if filename.endswith(".png"):
            netpbm = ["pnmtopng"]
        elif filename.endswith(".jpeg") or filename.endswith(".jpg"):
            netpbm = ["pnmtojpeg","-quality=95"]
        else:
            return False
        windowname = self.winfo_toplevel().title()
        try:
            imgfile = open(filename,'wb')
            pnmtoimg = subprocess.Popen(netpbm, stdin=subprocess.PIPE, stdout=imgfile, stderr=subprocess.PIPE)
            xwdtopnm = subprocess.Popen(['xwdtopnm'], stdin=subprocess.PIPE, stdout=pnmtoimg.stdin, stderr=subprocess.PIPE)
            xwd = subprocess.Popen([command,'-silent','-nobdrs','-name',windowname], stdout=xwdtopnm.stdin)
            pnmtoimg.communicate()
            imgfile.close()
            return False if pnmtoimg.returncode else True
        except:
            return False

    def snapinfo(self,path=""):
        """Return a dictionary that contains information about what will
        be able if the snapshot()-method is called with path as argument.
        Example for snapdict:
        {'tool':None|<name>, 'command':None|<path+tool>,
        'format':['png','gif','jpg'], 'area': True|False}
        If area is False, only the whole pool can be captured, because the
        capturing-tool doesn't support cropping."""
        snapdict = {"tool":None, "format":[], "area":False}
        if not (_LINUX or _WINDOWS): # other OS are not supported
            return snapdict
        # check existence of possible capture-tools
        pathlist = [os.path.normpath(path)]+os.environ["PATH"].split(":")
        tools = ["import","xwd"] if _LINUX else \
                ["i_view32.exe"] if _WINDOWS else []
        commands = []
        for tool in tools:
            for path in pathlist:
                command = os.path.join(path,tool)
                if os.path.isfile(command):
                    commands.append(command)
        if not commands and _WINDOWS and _PIL: # use PIL if available
            commands = ["PIL"]
        if not commands: # no tool for capturing available
            return snapdict
        snapdict["command"] = commands[0] # choose the best available tool
        snapdict["tool"] = os.path.basename(snapdict["command"])
        # check existence of converters if xwd is used
        if snapdict["tool"] == "xwd": # check available converters
            converter = []
            for conv in ["xwdtopnm","pnmtopng","pnmtojpeg"]:
                for path in pathlist:
                    if os.path.isfile(os.path.join(path,conv)):
                        converter.append(conv)
            if "xwdtopnm" in converter and "pnmtopng" in converter:
                snapdict["format"].append("png")
            if "xwdtopnm" in converter and "pnmtojpeg" in converter:
                snapdict["format"].append("jpg")
        else: # using import or irfanview
            snapdict["format"] = ["png","gif","jpg"]
            snapdict["area"] = True
        return snapdict

    def snapshot(self,filename=None,area=None,path=""):
        """Take a screenshot of the pool or the given area of the pool
        and save it as filename. area is a tuple (x1,y1,x2,y2) of upper left
        and lower right corner of the area that shall be captured.
        If no filename is given, the file will be named 'pool-<timestamp>.png'.
        If no area is given, the whole pool is captured.
        'path' maybe the complete path to the program that shall be used
        to capture the pool; necessary only on Windows systems.
        Returns the used filename at success, "" otherwise.
        """
        # Get info about available capture-tools, imageformats etc.
        snapdict = self.snapinfo(path)
        if not snapdict["format"] or area and not snapdict["area"]:
            return ""
        # Check filename resp. generate one if ommitted
        format = "png"
        if filename is None:
            filename = "pool-"+timemodul.strftime("%Y%m%d-%H%M%S.")+format
        else:
            filename = filename.lower().strip()
            for ext in [".png",".gif",".jpg",".jpeg"]:
                if filename.endswith(ext):
                    format = "jpg" if ext == ".jpeg" else ext[1:]
                    break
            else:
                filename = filename+"."+format
        if not format in snapdict["format"]:
            return ""
        # Transform area from pool coordinates to absolute coordinates
        pad = 1 if _LINUX else 2
        if not area:
            x1, y1 =  pad, pad
            w = self.winfo_toplevel().winfo_width()-2*pad
            h = self.winfo_toplevel().winfo_height()-2*pad
        else:
            x1, y1 = area[0]+self._dx, -area[3]+self._dy
            w, h = area[2]-area[0]+1, area[3]-area[1]+1
        area = tuple(map(int,map(round,(x1,y1,w,h))))
        # call command with filename und area
        capturefunc = {"import":self._capture_with_import,
                        "xwd":self._capture_with_xwd,
                        "i_view32.exe":self._capture_with_iview,
                        "PIL":self._capture_with_PIL}
        ok = capturefunc[snapdict["tool"]](snapdict["command"],area,filename)
        return filename if ok else ""

    def close(self):
        """Close the pool."""
        if self.__standalone:
            for frog in self.frogs:
                frog.exit()
            self.__root.destroy()

# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# +                         class Frog                         +
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Frog(object):

    PI180 = math.pi/180
    _idcounter = 0 # every frog gets an ID

    __shapes = {
        "arrow":((0,10),(10,0),(0,-10)),
        "cross": ((-10,-1),(-1,-1),(-1,-10),(1,-10),(1,-1),(10,-1),(10,1),
                  (1,1),(1,10),(-1,10),(-1,1),(-10,1)),
        "turtle":((16,0),(14,2),(10,1),(7,4),(9,7),(8,9),(5,6),
                  (1,7),(-3,5),(-6,8),(-8,6),(-5,4),(-7,0),(-5,-4),
                  (-8,-6),(-6,-8),(-3,-5),(1,-7),(5,-6),(8,-9),
                  (9,-7),(7,-4),(10,-1),(14,-2)),
        "frog": ((-22,0),(-22,4),(-16,12),(-34,6),(-26,22),(-26,18),
                 (-24,20),(-24,16),(-22,18),(-26,12),(-10,18),(-16,8),
                 (-8,10),(-2,10),(6,6),(10,18),(18,14),(24,16),
                 (22,14),(24,12),(22,12),(24,8),(18,12),(12,14),
                 (8,4),(10,4),(12,6),(12,8),(14,8),(16,6),(20,4),
                 (18,0),(20,-4),(16,-6),(14,-8),(12,-8),(12,-6),
                 (10,-4),(8,-4),(12,-14),(18,-12),(24,-8),(22,-12),
                 (24,-12),(22,-14),(24,-16),(18,-14),(10,-18),(6,-6),
                 (-2,-10),(-8,-10),(-16,-8),(-10,-18),(-26,-12),
                 (-22,-18),(-24,-16),(-24,-20),(-26,-18),(-26,-22),
                 (-34,-6),(-16,-12),(-22,-4)) }

    __DEFAULTSHAPES = tuple(__shapes.keys()) # these shapes are immutable

    def __init__(self, pool=None, visible=True):
        if pool is None:
            raise Exception("Frog cannot live outside a Pool.")
        self.__pool = pool      # frog's pool
        Frog._idcounter += 1
        self.__id = "Frog-%04i" %Frog._idcounter # # the frog's individual ID
        self.__x = 0.0          # x value of position
        self.__y = 0.0          # y value of position
        self.__angle = 0.0      # direction: 0° = east
        self.__way = 0.0        # length of way since start
        self.__color = ""       # color of pen/trace
        self.__bodycolor = ""   # color of frog's body
        self.__shape = "arrow"  # frog's shape
        self.__width = 2        # width of pen/trace
        self.__borderwidth = 2  # thickness of frog's border
        self.__size = ""        # width/height of frog's bounding-box
        self.__visible = False  # frog's visibility
        self.__animate = True   # act with/without frog-animation
        self.__speed = 2.0      # 1.0 (slow) .. 10.0 (fast)
        self.__active = False   # True if frog is acting (read-only)
        self.__fill = False     # fill polygons/circles with fillcolor if True
        self.__fillcolor = ""   # color for fill operations
        self.__font = ""        # will be initialized by default font
        # ---- private ---------
        self.__visiblestate = self.__visible # for backup use if no animation
        self.__anglestate = self.__angle     # for backup use if no animation
        self.__shapetype = "polygon"  # shape is either a polygon or an image
        self.__itemID = 0             # frog's item ID for Canvas-methods
        self.__itemlist = list()      # list of all items created by the frog
        self.__pool._Pool__frogs = self.__pool._Pool__frogs+(self,) # add frog
        # initialize frog in the pool
        self.setfont(tkFont.Font().actual()["family"],12,"bold")
        self.setvisible(True)
        self.setvisible(False)
        self.__color = "black"
        if visible: self.setvisible(True)  # make frog visible

    def __str__(self):
        return self.__id


   # --------- private methods -----------

    def _toTkFont(self,font):
        """Convert a font-tripel (name,size,style) into a tkFont-Objekt.
        Raises an exception if font is invalid.
        """
        name, size, style = font
        if style.lower() not in ["normal","italic","bold","bolditalic"]:
            raise Exception("There's no fontstyle %s" %style)
        wt = "bold" if "bold" in style.lower() else "normal"
        st = "italic" if "italic" in style.lower() else "roman"
        tkfont = tkFont.Font(family=name,size=size,weight=wt,slant=st)
        self.__pool._Pool__fontID.append(tkfont) # to hold a reference because
        return tkfont                            # of a bug in tkFont!

    def _setactive(self,active):
        """Set flag if frog is acting / no longer acting."""
        self.__active = active
        self.__pool._setaction(active)

    def _fillit(self):
        """Check if last movement created a closed figure. If so:
        Replace by a filled polygon with current width and color of frog.
        """
        if not self.__fill: return # nothing to do
        if len(self.__fillinglist)<8: # less than 4 points -> nothing to fill
            return
        x0, y0 = self.__fillinglist[:2]
        x1, y1 = self.__fillinglist[-2:]
        dist = math.hypot(x1-x0,y1-y0)
        if dist>4: return # no closed figure -> nothing to fill
        # closed figure has been created -> replace by filled polygon
        for item in self.__tempitems:
            try:
                self.__itemlist.remove(item)
            except:
                pass
            self.__pool.delete(item)
        polygon = self.__pool.create_polygon(self.__fillinglist[:-2],
                    outline=Color.toRGBstr(self.__color),
                    fill=Color.toRGBstr(self.__fillcolor),width=self.__width)
        self.__itemlist.append(polygon)
        self.__pool._refresh()
        self.__fillinglist = list()
        self.__tempitems = list()

    def _appendline(self,coords):
        """Base method for all drawings except fullcircles.
        coords is a list of coordinates forming a (multi)line.
        Draws the (multi)line with this coordinates and appends it to itemlist.
        Also updating fillinglist according to coordinates, if filling
        status is set. Method is only called by methods _goto() and _circle().
        """
        x0,y0,x1,y1 = coords[:2]+coords[-2:]
        line = self.__pool.create_line(coords,width=self.__width,
                fill=Color.toRGBstr(self.__color),capstyle=tk.ROUND)
        self.__itemlist.append(line)
        self.__pool._refresh()
        if not self.__fill: return # nothing more to do
        # Update fillinglist
        if not self.__fillinglist: # first entry
            self.__fillinglist = coords
            self.__tempitems = [line]
            return
        # Check if current line can be connected to last line in fillinglist
        x,y = self.__fillinglist[-2:]
        d0, d1 = math.hypot(x0-x,y0-y), math.hypot(x1-x,y1-y)
        # add line, if connection to previous line is possible
        if d0<1 or d1<1: # lines can be connected
            if d0<1:
                self.__fillinglist.extend(coords[2:])
            else:
                self.__fillinglist.extend(coords[:-2])
            self.__tempitems.append(line)
            self._fillit() # fill if closed figure has been created
        else: # cannot be connected to previous line: no filling possible
            self.__fillinglist = coords
            self.__tempitems = [line]

    def _goto(self,x,y,draw=False,drawarc=False):
        """Base method for all frog movements. x, y must be float.
        if drawarc is True, it is part of drawing an arc.
        """
        if not self.__animate:
            if draw:
                x0, y0 = self.__pool._dx+self.__x, self.__pool._dy-self.__y
                x1, y1 = self.__pool._dx+x, self.__pool._dy-y
                self._appendline([x0,y0,x1,y1])
            self.__x, self.__y = x, y
            return [] if drawarc else None
        if self.__active: return  # no other movements while moving/drawing
        self._setactive(True)
        ax, ay = self.__x, self.__y
        bx, by = x, y
        dx, dy = bx-ax, by-ay
        d = math.hypot(dx,dy)
        self.__way += d
        steps = int(d/3)+1
        mvx, mvy = dx/steps, dy/steps
        delay = 0 if self.__speed == "max" else \
                20/self.__speed**1.8 if drawarc else 40/self.__speed**1.8
        if draw:
            col = Color.toRGBstr(self.__color)
            x0, y0 = self.__pool._dx+ax, self.__pool._dy-ay
            x00, y00 = x0, y0
            lastitemindex = len(self.__itemlist) # to be able to replace later
        for n in xrange(1,steps+1):
            self.__pool.move(self.__itemID,mvx,-mvy)
            self.__x += mvx
            self.__y += mvy
            if draw:
                x1, y1 = x0+mvx, y0-mvy
                self.__itemlist.append(self.__pool.create_line(x0,y0,x1,y1,
                                fill=col,width=self.__width,capstyle=tk.ROUND))
                x0, y0 = x1, y1
            self.__pool._refresh()
            self.wait(delay)
        self._setactive(False)
        self.__x, self.__y = bx, by # for numerical exactness/correction
        if draw:
            lineparts = self.__itemlist[lastitemindex:]
            del self.__itemlist[lastitemindex:]
            if not drawarc: # remove lineparts to increase performance
                self._appendline([x00,y00,x0,y0])
                for item in lineparts:
                    self.__pool.delete(item)
            else:
                return lineparts
        elif drawarc:
            return []

    def _turnto(self,a,nodelay=False,optimize=False):
        """Base method for all frog turning. a must be float.
        If set 'nodelay' frog will set to angle a without delay/animation.
        If set 'optimize' frog will choose orientation, so that rotation
        is no larger than 180 degrees.
        """
        if not self.__animate or not self.__visible:
            self.__angle = a % 360
            return
        if self.__active:
            return  # no other movements while moving/drawing
        self._setactive(True)
        phi = a-self.__angle
        if optimize and abs(phi)>180: # calculate shortest way
            phi = (phi%360+360)%360
            phi = phi-360 if phi>180 else phi
        phi *= -Frog.PI180
        # Note: canv.coords() returns a list in Py2, but a map in Py3!
        coords = list(self.__pool.coords(self.__itemID))
        xp, yp = self.__x+self.__pool._dx, -self.__y+self.__pool._dy
        if nodelay or self.__speed == "max":
            steps, delay = 1, 0
        else:
            steps = int(abs(phi/math.pi*30))+1
            delay = 40/self.__speed**1.8
        mvphi = phi/steps # rad
        deltaphi = -mvphi/Frog.PI180 # deg
        sinphi, cosphi = math.sin(mvphi), math.cos(mvphi)
        for n in xrange(steps):
            for p in xrange(0,len(coords),2):
                x, y = coords[p], coords[p+1]
                coords[p] = (x-xp)*cosphi-(y-yp)*sinphi+xp
                coords[p+1] = (y-yp)*cosphi+(x-xp)*sinphi+yp
            self.__pool.coords(self.__itemID,*coords)
            self.__angle = (self.__angle + deltaphi) % 360
            self.wait(delay)
            self.__pool.update()
        self._setactive(False)
        self.__angle = a % 360 # for numerical exactness/correction

    def _fullcircle(self,radius):
        """Draw a fullcircle at one time without animation.
        Used for drawing without animation and to replace a full circle
        after animated drawing is complete.
        """
        x0 = self.__pool._dx+self.__x-radius
        y0 = self.__pool._dy-self.__y-radius
        x0 = x0-radius*math.cos((90-self.__angle)*Frog.PI180)
        y0 = y0-radius*math.sin((90-self.__angle)*Frog.PI180)
        x1, y1 = x0+radius*2, y0+radius*2
        col = Color.toRGBstr(self.__color)
        fcol = Color.toRGBstr(self.__fillcolor) if self.__fill else ""
        circle = self.__pool.create_oval(x0,y0,x1,y1,width=self.__width,
                            outline=col,fill=fcol)
        self.__itemlist.append(circle)
        if self.__fill:
            self.__fillinglist = list() # important: clear fillinglist!
        self.__pool._refresh()

    def _circle(self,radius,angle=None,draw=True):
        """For documentation see method circle()."""
        if not self.__animate and not draw: return  # nothing to do
        if abs(radius)<0.99:
            raise Exception("Radius of a circle must be at least 1 px")
        fullcircle = True if angle is None or abs(angle)==360 else False
        if not self.__animate and fullcircle: # circle without animation
            self._fullcircle(radius)
            return
        if fullcircle:
            angle = float(angle) if angle else 360.0
        elif abs(angle)<0.1:
            raise Exception("Angle of arc must be at least 0.1 degrees")
        if radius<0:
            angle = -angle # for correct direction of moving
        q = angle/360.0
        n = min(18+4*int(abs(radius*q))//15,40) # number of steps for drawing
        phi = float(angle)/n
        d = q*radius*math.tan(2*math.pi/n)*0.99  # WHY *0.99 ?
        walk = lambda s : self._goto(self.__x+s*math.cos(self.__angle*Frog.PI180),
                self.__y+s*math.sin(self.__angle*Frog.PI180),draw=draw,drawarc=True)
        tempitems = walk(0.5*d) # move without appending itemlist
        for k in xrange(n-1):
            self.turn(phi) # nodelay etc. MISSING!
            tempitems.extend(walk(d))
        self.turn(phi)
        tempitems.extend(walk(0.5*d))
        if not draw: return # nothing more to do
        # replace connected arcs through fullcircle or one connected line-item
        if fullcircle:
            for item in tempitems:
                self.__pool.delete(item)
            self._fullcircle(radius)
        elif tempitems: # only part of a circle
            # Note: canv.coords() returns a map in Py3 -> convert to list!
            line = list(self.__pool.coords(tempitems[0]))[:2]
            for item in tempitems:
                line.extend(list(self.__pool.coords(item))[2:])
                self.__pool.delete(item)
            self._appendline(line)

    def _eventhandler(self,e,func):
        """Universal eventhandler that interprets real events catched by
        frog's method listen() and delivers a dictionary with all necessary
        event-data as only argument to func, which is the really handler.
        Only mouse-events are be handled by frog's listen()-methode.
        Key-, timer- and close-events are handled by pool's listen()-method.
        """
        if not e.type in ['4','5','6','7','8','38']: # only mouse-events allowed
            raise Exception("Event-type cannot be handled by listen()")
            return
        if e.type == "38": # MouseWheel - Windows only!
            name = "Up" if e.delta>0 else "Down"
        elif e.type == "4" and _LINUX and e.num in [4,5]:
            e.type = "38" # MouseWheel - simulate event on Linux
            name = "Up" if e.num == 4 else "Down"
        eventtype = {"4":"Button", "5":"ButtonRelease", "6":"Motion",
                     "7":"Enter", "8":"Leave", "38":"MouseWheel"}
        x, y = -self.__pool._dx+e.x, self.__pool._dy-e.y
        key = "" if e.keysym == "??" else e.keysym
        btn = "" if e.num == "??" else "Button-"+str(e.num)
        ch = "" if e.char == "??" else e.char
        name = key or btn if e.type != "38" else name
        event = {"type":eventtype[e.type], "name":name, "char":ch,
                 "pos":(x,y), "time":e.time, "object":self}
        func(event)


# --------- getter/setter bind to properties -----

    def getpool(self):
        """Return the pool the frog belongs to."""
        return self.__pool

    def getid(self):
        """Return the frog's ID (an integer)."""
        return self.__id

    def getx(self):
        """Return the x-value of frog's position."""
        return self.__x

    def setx(self,x):
        """Set the x-value of frog's position to x."""
        self.jumpto(x,self.__y,turn=False)

    def gety(self):
        """Return the y-value of frog's position."""
        return self.__y

    def sety(self,y):
        """Set the y-value of frog's position to y."""
        self.jumpto(self.__x,y,turn=False)

    def getpos(self):
        """Return frog's position in the pool as pair (x,y)."""
        return self.__x, self.__y

    def setpos(self,pos):
        """Set frog to position pos. Identical zu jumpto(pos)."""
        self.jumpto(pos,turn=False)

    def getangle(self):
        """Return frog's current angle."""
        return self.__angle

    def setangle(self,phi):
        """Set frog's direction to an absolute angle of phi degrees."""
        self.turnto(phi)

    def getway(self):
        """Return length of frog's way since last counter reset."""
        return self.__way

    def setway(self,way):
        """Reset length of way to 0 - other assignments lead to an error."""
        if abs(way)<0.0001:
            self.__way = 0.0
        else:
            raise Exception("Frog's way can only be reset to 0.")

    def getcolor(self):
        """Return current drawing color."""
        return self.__color

    def setcolor(self,col):
        """Set color for following drawing operations and frog's outline."""
        if col:
            rgbstr = Color.toRGBstr(col) # raises FrogError if col is invalid
        else:
            col = rgbstr = ""
        self.__color = col
        color = rgbstr if self.__borderwidth else ""
        if self.__visible and self.__animate and self.__shapetype=="polygon":
            self.__pool.itemconfigure(self.__itemID,outline=color)
            self.__pool.update()

    def getbodycolor(self):
        """Return frog's bodycolor."""
        return self.__bodycolor

    def setbodycolor(self,col):
        """Set frog's bodycolor. Value is set, even is frog is invisible."""
        if col:
            rgbstr = Color.toRGBstr(col) # raises FrogError if col is invalid
        else:
            col = rgbstr = ""
        self.__bodycolor = col
        if self.__visible and self.__animate and self.__shapetype=="polygon":
            self.__pool.itemconfigure(self.__itemID,fill=rgbstr)
            self.__pool.update()

    def getshapes(self):
        """Return list of all available frog shapes."""
        return Frog.__shapes.keys()

    def getshape(self):
        """Return name of frog's current shape."""
        return self.__shape

    def setshape(self,*args):
        """Set shape 'name'. If new shape, data gets tuple of points or name
        of imagefile; shape is automatically added to collection of shapes,
        which is hold in a class attribute of Frog.
        """
        # identify and handle different typs of arguments
        if len(args)==1: args = args[0]
        if isinstance(args,tuple):
            name, data = args[0], args[1:]
            if len(data)==1: data = data[0]
        else:
            name, data = args, None
        if data is None:
            if not name in Frog.__shapes:
                raise Exception("There is no shape named %s" %str(name))
            if name == self.__shape:
                return # nothing to do
        else: # data is given
            if name in Frog.__DEFAULTSHAPES:
                raise Exception("Shape %s cannot be overwritten" %name)
            if isinstance(data,tuple): # polygon type -> mirror y-Values
                data = tuple([(float(x),-float(y)) for (x,y) in data])
                Frog.__shapes[name] = data
            elif isinstance(data,str): # image type -> check it
                try:
                    Frog.__shapes[name] = tk.PhotoImage(file=data)
                    self.__shapetype = "image"
                except:
                    raise Exception("There's no imagefile named %s" %data)
            else:
                raise Exception("No valid data defined for shape %s" %str(data))
        self.__shape = name
        if isinstance(Frog.__shapes[name],tuple):
            self.__shapetype = "polygon"
        else:
            self.__shapetype = "image"
        if self.__visible: # show new shape
            self.setvisible(False)
            self.setvisible(True)

    def getborderwidth(self):
        """Return borderwidth of frog's shape if it's polygon."""
        return self.__borderwidth

    def setborderwidth(self,w):
        """Set borderwidth of frog's shape if it's a polygon."""
        if int(w)<0:
            raise Exception("%s is no valid borderwidth" %str(w))
        self.__borderwidth = int(w)
        if self.__visible and self.__animate and self.__shapetype=="polygon":
            self.__pool.itemconfigure(self.__itemID,width=self.__borderwidth)
            self.__pool.update()

    def getsize(self):
        """Return bounding-box of frog's shape."""
        bbox = self.__pool.bbox(self.__itemID)
        return (0,0) if bbox is None else (bbox[2]-bbox[0],bbox[3]-bbox[1])

    def getwidth(self):
        """Return width of frog's trace in px as a value >=1."""
        return self.__width

    def setwidth(self,w):
        """Set width of frog's trace in px as a value >=1."""
        if int(w)<1:
            raise Exception("%s is no valid width" %str(w))
        self.__width = int(w)

    def getvisible(self):
        """Return frog's visibilty state: True|False."""
        return self.__visible

    def setvisible(self,visible):
        """Set frog's visibility state: True|False. Default is True.
        If unbind is True, all event-bindings are unbound."""
        if not self.__animate:
            self.__visiblestate = visible # don't make frog visible
            return
        if visible == self.__visible: # nothing to do
            return
        if visible: # make frog visible
            if self.__shapetype == "polygon":
                self.__itemID = self.__pool.create_polygon(
                    Frog.__shapes[self.__shape],width=self.__borderwidth)
            else: # image
                self.__itemID = self.__pool.create_image(
                    0,0,image=Frog.__shapes[self.__shape])
            self.__pool.move(self.__itemID,self.__pool._dx+self.__x,
                                           self.__pool._dy-self.__y)
            self.__visible = True
            self.setcolor(self.__color)
            self.setbodycolor(self.__bodycolor)
            newangle = self.__angle
            self.__angle = self.__anglestate
            self._turnto(newangle, nodelay=True)
            self.__pool.addtag_withtag(self.__id,self.__itemID)
        else: # make frog invisible
            self.__pool.delete(self.__itemID)
            self.__itemID = 0
            self.__visible = False
            self.__angelstate = self.__angle
        self.__pool._rearrange()

    def getspeed(self):
        """Return frog's current speed as a value from 1.0 to 10.0."""
        return self.__speed

    def setspeed(self,v):
        """Set frog's speed as a value from 1.0 to 10.0 or 'max'.
        if speed is 'max' there will be no delay in any frog action.
        """
        v = "max" if str(v).lower() == "max" else float(v)
        if v == "max" or 0.99 <= v <= 10.01:
            self.__speed = v
        else:
            raise Exception("%s is no valid speed" %str(v))

    def getanimate(self):
        """Return frog's animation state: True|False."""
        return self.__animate

    def setanimate(self,animate):
        """Set frog's animation state. Default is True."""
        if animate == self.__animate: return
        if animate:
            self.__animate = animate
            if self.__visiblestate:
                self.__visible = False
                self.setvisible(True)
        else:
            self.__visiblestate = self.__visible
            self.setvisible(False)
            self.__animate = animate

    def getactive(self):
        """Return frog's state: actually moving/jumping/turning or not."""
        return self.__active

    def getitems(self):
        """Return number of frog's visible drawings (items)."""
        return len(self.__itemlist)

    def getfill(self):
        """Return state of fill flag."""
        return self.__fill

    def setfill(self,fill):
        """Set fill flag. If True, all following closed figures are filled."""
        if fill:
            self.__fill = True
            self.__fillinglist = list()
            self.__tempitems = list()
        else:
            self.__fill = False

    def getfillcolor(self):
        """Return current fillcolor used for filling operations."""
        return self.__fillcolor

    def setfillcolor(self,col):
        """Set fillcolor for following filling operations."""
        if col:
            Color.toRGBstr(col) # raises FrogError if col is invalid
        else:
            col = ""
        self.__fillcolor = col

    def getfont(self):
        """Return actual font."""
        return self.__font

    def setfont(self,name,size=None,style=None):
        """Set font for all following textoutput.
        size is int/float size in pt. Use negative value to set size in px.
        style is one of 'normal','bold','italic' or 'bolditalic'.
        If the given values are not realizable,
        set the font, the systems offers as solution.
        An error will only occur, if there's a type mismatch.
        """
        if isinstance(name,tuple):
            if len(name)==1:
                name += (None,None)
            elif len(name)==2:
                name += (None,)
            elif len(name)>3:
                raise Exception("Too many arguments to set a font.")
            name, size, style = name
        size = self.__font[1] if size is None else int(round(size))
        style = style or self.__font[2]
        font = self._toTkFont((name,size,style)).actual()
        style = font["weight"]+font["slant"].replace("roman","")
        style = "italic" if style=="normalitalic" else style
        self.__font = font["family"],font["size"],style

    def getfonts(self):
        """Return a list of all available fonts."""
        return sorted(tkFont.families())

    def getlastitem(self):
        """Return ID of last item created by the frog."""
        return len(self.__itemlist) and self.__itemlist[-1]

    # --------- properties ---------

    pool = property(getpool)
    id = property(getid)
    x, y = property(getx,setx), property(gety,sety)
    pos = property(getpos,setpos)
    angle = property(getangle,setangle)
    way = property(getway,setway)
    color = property(getcolor,setcolor)
    bodycolor = property(getbodycolor,setbodycolor)
    width = property(getwidth,setwidth)
    shape = property(getshape,setshape)
    shapes = property(getshapes)
    borderwidth = property(getborderwidth,setborderwidth)
    size = property(getsize)
    visible = property(getvisible,setvisible)
    speed = property(getspeed,setspeed)
    animate = property(getanimate,setanimate)
    active = property(getactive)
    items = property(getitems)
    fill = property(getfill,setfill)
    fillcolor = property(getfillcolor,setfillcolor)
    font = property(getfont,setfont)
    fonts = property(getfonts)
    lastitem = property(getlastitem)

    # --------- other public methods ----------

    def jumpto(self,x,y=None,turn=True):
        """Move frog to (x,y) without drawing"""
        if y is None:
            x,y = x
        if turn: # default: turn frog into jumping-direction
            oldangle = self.__angle
            self.turnto(self.angleto(x,y))
            self._goto(float(x),float(y))
            self.turnto(oldangle)
        else: # fast jumping - used by pos, x and y attributes
            self._goto(float(x),float(y))

    def jump(self,d):
        """Move frog d px forward without drawing"""
        phi = self.__angle*Frog.PI180
        self._goto(self.__x+d*math.cos(phi),self.__y+d*math.sin(phi))

    def moveto(self,x,y=None):
        """Move frog to (x,y) while drawing"""
        if y is None:
            x,y = x
        oldangle = self.__angle
        self.turnto(self.angleto(x,y))
        self._goto(float(x),float(y),draw=True)
        self.turnto(oldangle)

    def move(self,d):
        """Move frog d px forward while drawing"""
        phi = self.__angle*Frog.PI180
        self._goto(self.__x+d*math.cos(phi),self.__y+d*math.sin(phi),draw=True)

    def turnto(self,phi):
        """Rotate frog to angle a. - 0 degrees = East, use shortest way."""
        self._turnto(float(phi),optimize=True)

    def turn(self,phi):
        """Rotate frog phi degrees left according to current orientation."""
        self._turnto(float(self.__angle+phi))

    def home(self):
        """Move frog to (0,0) and 0 degrees without drawing."""
        self.turnto(self.angleto(0,0))
        self._goto(0.0,0.0)
        self.turnto(0)

    def circle(self,radius,angle=None,draw=True):
        """Draw (or, if draw=False, move along) a circle or an arc with an
        extent of angle degrees relativ to starting angle.
        If radius>0, center of circle is radius px left to the frog,
        if radius<0, center of circle is radius px right to the frog.
        If angle>0, frog moves forward, if angle<0, frog moves backward.
        If angle is None, draw a full circle moving forward.
        """
        self._circle(radius,angle,draw)

    def dot(self,width=8,fill=True):
        """Draw a dot in drawing color with given width.
        fill may be a color or True or False."""
        if width<1:
            raise Exception("%s is not a valid width for a dot" %str(width))
        r = 0.5*width
        x0, x1 = self.__pool._dx+self.__x-r, self.__pool._dx+self.__x+r
        y0, y1 = self.__pool._dy-self.__y-r, self.__pool._dy-self.__y+r
        col = Color.toRGBstr(self.__color)
        fillcol = "" if not fill else col if fill is True else fill
        dot = self.__pool.create_oval(x0,y0,x1,y1,
                                outline=col,fill=fillcol,width=self.__width)
        self.__itemlist.append(dot)
        self.__pool._refresh()

    def stamp(self):
        """Leave a copy of frog's shape at current position"""
        if self.__shapetype == "polygon":
            col = Color.toRGBstr(self.__color) if self.__borderwidth else ""
            bcol = Color.toRGBstr(self.__bodycolor)
            visible = self.visible
            if not visible: # make visible to set a stamp
                self.visible = True
            # Note: canv.coords() returns a map in Py3 -> convert to list!
            stamp = self.__pool.create_polygon(list(self.__pool.coords(self.__itemID)),
                    outline=col,fill=bcol,width=self.__borderwidth)
            if not visible: # reset former visibility state
                self.visible = False
        else: # image
            stamp = self.__pool.create_image(0,0,
                    image=Frog.__shapes[self.__shape])
            self.__pool.move(stamp,self.__pool._dx+self.__x,self.__pool._dy-self.__y)
        self.__itemlist.append(stamp)
        self.__pool._refresh()

    def button(self,text,func):
        """Create a button with text and func as command.
        Font, color etc. are taken from the frog's attributes.
        Bodycolor is the value for the normal background,
        fillcolor is the value used for the activebackground.
        func must have exactly one argument: It will be passend an
        event-dictionary with type 'ButtonWidget' and text as name.
        event-dictionary is the same as delivered by Pool's listen()-method.
        """
        col = Color.toRGBstr(self.__color) or "black"
        bgcol = Color.toRGBstr(self.__bodycolor) or "#fff"
        actcol = Color.toRGBstr(self.__fillcolor) or "#fff"
        font = self._toTkFont(self.__font)
        event = {"type":"ButtonWidget", "name":text, "char":"",
                 "pos":(0,0), "time":0}
        bt = tk.Button(text=text,font=font,fg=col,bg=bgcol,
                command = lambda e=event:func(e),cursor="hand1",
                activeforeground=col,activebackground=actcol)
        x, y = self.__pool._dx+self.__x+1, self.__pool._dy-self.__y
        button = self.__pool.create_window(x,y,window=bt,anchor=tk.SW)
        self.__itemlist.append(button)
        self.__pool._refresh()

    def buttonsize(self,text):
        """Return width and height of a button with text text in the
        frog's current font."""
        bt = tk.Button(text=text,font=self._toTkFont(self.__font))
        button = self.__pool.create_window(5000,5000,window=bt)
        x0,y0,x1,y1 = self.__pool.bbox(button)
        self.__pool.delete(button)
        return x1-x0+1, y1-y0+1

    def read(self,msg=""):
        """Open a tkSimpleDialog with an inputline.
        msg is an optional message for the user.
        If [cancel] is pressed, None will be returned.
        """
        s = tkSimpleDialog.askstring("Input",msg)
        self.__pool.focus_set() # necessary!
        if s is None: return
        if sys.version_info[0] == 2:
            # encoding avoids possible problems with german "Umlaute"
            s = s.encode("iso-8859-15")
        return s

    def message(self,msgtype,msg):
        """Show a toplevel-Window with msg as message.
        msgtype is one of "Info","Warning","Error","Question","Confirm".
        Return True if Button [OK] or [YES] was pressed, False otherwise.
        """
        msgfunc = {"Info":tkMessageBox.showinfo,
                   "Warning":tkMessageBox.showwarning,
                   "Error":tkMessageBox.showerror,
                   "Question":tkMessageBox.askyesno,
                   "Confirm":tkMessageBox.askokcancel}
        try:
            msgtype = msgtype[0].upper()+msgtype[1:].lower()
            return msgfunc[msgtype](msgtype,msg) and True
        except:
            raise Exception("Invalid messagetype %s" %msgtype)

    def write(self,text,width=None):
        """Write text at the frog's current position in frog's
        current color and font. Position of the frog is the lower left
        corner of the bounding-box of the text. If width is given,
        there will be linebreaks inserted so that the maximum is width px.
        """
        col = Color.toRGBstr(self.__color) or "black"
        x, y = self.__pool._dx+self.__x, self.__pool._dy-self.__y
        item = self.__pool.create_text(x,y,anchor=tk.SW,fill=col,
                    width=width,font=self._toTkFont(self.__font),text=text)
        self.__itemlist.append(item)
        self.__pool._refresh()

    def textsize(self,text,width=None):
        """Return width and height of text in px based on the frog's
        current font value."""
        item = self.__pool.create_text(5000,5000,width=width,
                                font=self._toTkFont(self.__font),text=text)
        x0,y0,x1,y1 = self.__pool.bbox(item)
        self.__pool.delete(item)
        return x1-x0-2,y1-y0-2

    def distanceto(self,arg,y=None):
        """arg maybe x value, or (x,y) or a frog object.
        Returns distance to that position resp. frog.
        """
        if isinstance(arg,Frog):
            x, y = arg.x, arg.y
        elif isinstance(arg,tuple):
            x, y = arg
        elif y is not None:
            x = arg
        else:
            raise Exception("%s is no valid argument for distanceto()" %str(arg))
        return math.hypot(self.__x-x,self.__y-y)

    def angleto(self,arg,y=None):
        """arg maybe x value, or (x,y) or a frog object.
        Returns angle towards that position resp. frog.
        """
        if isinstance(arg,Frog):
            x, y = arg.x, arg.y
        elif isinstance(arg,tuple):
            x, y = arg
        elif y is not None:
            x = arg
        else:
            raise Exception("%s is no valid argument for distanceto()" %str(arg))
        return (360+math.atan2(y-self.__y,x-self.__x)/math.pi*180) % 360

    def clear(self,item="all"):
        """Remove some or all of the frog's drawings.
        If item is None, all items are cleared - default.
        Item maybe a single ID (= int) or a list of IDs to be removed.
        """
        if not self.__itemlist or not item: return # nothing to remove
        if item == "all": # remove all items
            for item in self.__itemlist:
                self.__pool.delete(item)
            self.__itemlist = list()
        else:
            items = item if isinstance(item,list) else [item]
            for item in items: # remove selected items
                if item in self.__itemlist:
                    self.__pool.delete(item)
                    self.__itemlist.remove(item)
        self.__pool.update()

    def clone(self):
        """Return a complete copy of a frog, except the value in 'way'.
        Event-bindings are NOT copied."""
        nn = Frog(self.__pool, visible=False)
        nn.color, nn.bodycolor = self.color, self.bodycolor
        nn.shape, nn.borderwidth = self.shape, self.borderwidth
        nn.visible, nn.animate = self.visible, self.animate
        nn.speed, nn.width = self.speed, self.width
        nn.fill, nn.fillcolor = self.fill, self.fillcolor
        nn.font = self.font
        return nn

    def beep(self):
        """Make a short beep."""
        self.__pool.bell()

    def sing(self,song,background=False):
        """Play a song given as filename. Audiotype wav is supported on
        Linux and Windows, sometimes mp3-files will also work.
        On Linux the commandline-tool play (from package sox) is used,
        on Windows the winsound-module; Mac OS is not supported, yet.
        """
        try: # check if audiofile exists
            songfile = open(song,"rb")
            songfile.close()
        except:
            raise Exception("Audiofile %s not found." %song)
        if _LINUX:
            try:
                if background:
                    subprocess.Popen(["play",song],
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
                else:
                    subprocess.call(["play",song],
                            stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            except OSError:
                pass # package sox not installed -> no sound played
        if _WINDOWS:
            try:
                if background:
                    winsound.PlaySound(song,winsound.SND_ASYNC)
                else:
                    winsound.PlaySound(song,winsound.SND_NOSTOP)
            except RuntimeError:
                pass # some kind of Error -> no sound played

    def wait(self,ms):
        """Waiting for ms milliseconds."""
        s = 0.001*ms
        t0 = Pool._timecounter() # platform dependent time measurement!
        while Pool._timecounter()-t0<s: pass

    def listen(self,seq,func,add=False):
        """Create a binding between an event, specified by seq and a
        function func which has to provide exactly ONE parameter.
        The event is filtered and interpreted by the method _eventhandler(),
        that provides a dictionary with the needed event-data delivered
        to func. If func is None, unbind is executed.
        Bindings are unbound by changing the visibility-state or the shape.
        """
        if seq == "<Close>" or "Timer" in seq:
            raise Exception("Event-type can only be handled by pool.listen().")
        event = {"type":"undefined", "name":"", "char":"",
                 "pos":"", "time":"", "object":self}
        add = "+" if add else None
        if "MouseWheel" in seq and _LINUX:
            seq1 = seq.replace("MouseWheel","Button-4")
            seq2 = seq.replace("MouseWheel","Button-5")
            if func is None:
                self.__pool.tag_unbind(self.__id,seq1)
                self.__pool.tag_unbind(self.__id,seq2)
            else:
                self.__pool.tag_bind(self.__id,seq1,
                        lambda event,f=func:self._eventhandler(event,f),add)
                self.__pool.tag_bind(self.__id,seq2,
                        lambda event,f=func:self._eventhandler(event,f),"+")
        elif func is None:
            self.__pool.tag_unbind(self.__id,seq)
        else:
            self.__pool.tag_bind(self.__id,seq,
                        lambda event,f=func:self._eventhandler(event,f),add)

    def exit(self):
        """Remove frog from the pool and delete all his traces."""
        if self in self.__pool.frogs:
            self.clear()
            self.__pool.delete(self.__itemID)
            froglist = list(self.__pool._Pool__frogs)
            froglist.remove(self)
            self.__pool._Pool__frogs = tuple(froglist)
            for attr in dir(self):
                try: delattr(self,attr)
                except: pass

# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# ++++++++++++  main section: short demo ++++++++++++++++++++++++

# Want to see more? -> Look at frogdemo.py

if __name__ == "__main__":  # ------------------------------------------------

    print("\nModule: frog")
    print("Version: "+__version__+" ("+__date__+")")
    print("(C) by "+__author__)

    from random import random

    def drawrect(d):
        rect.pos = frog.pos
        rect.color = random(),random(),random()
        rect.fillcolor = random(), random(), random()
        for k in range(4):
            rect.move(d)
            rect.turn(90)

    pool = Pool(pos="center",width=600,height=400)
    frog = Frog(pool,visible=False)
    frog.shape = "frog"
    frog.color, frog.bodycolor = "darkgreen", "green"
    frog.pos = 140,-150
    frog.visible = True
    rect = Frog(pool,visible=False)
    rect.animate = False
    rect.fill = True
    for k in xrange(1,16):
        frog.turn(16)
        frog.jump(6*k)
        drawrect(6*k)
    frog.home()
    frog.width = 6
    frog.circle(-70)
    frog.turn(90)
    frog.jump(-70)
    frog.bodycolor = "red"
    frog.speed = 1
    frog.turn(360)
    frog.bodycolor = "green"
    pool.ready()
