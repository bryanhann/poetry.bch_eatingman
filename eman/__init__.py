__version__ = '0.1.0'

import sys
from pathlib import Path
from urllib.request import Request, urlopen

ROOT=Path(__file__).parent.parent
INDEX=ROOT/'index'
BACKSPACE='\b'

def lfilter(*a,**b): return list(filter(*a,**b))
def is_url(x): return x.startswith('http')
def fsplit(f): return f.read_text().split()
def pad(n): return str(n+10000)[-4:]
def stderr(msg): sys.stderr.write(msg), sys.stderr.flush()
def back(msg): stderr( f'{BACKSPACE*50}{msg}' )
def urls4file(fpath): return filter(is_url, fsplit(fpath))

def wget(url,dst):
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    if not dst.exists():
        (dst.parent).mkdir(exist_ok=True)
        dst.write_bytes(urlopen(Request(url, headers=HEADERS)).read())

class EnumeratedSequence:
    def __init__(self,seq, text='anon'):
        self._seq = list(seq)
        self._ii = 0
        self._text = text
        self.cb_first  = lambda self : None
        self.cb_next   = lambda self : None
        self.cb_last   = lambda self : None

    def withself(self):
        with self:
            yield from self


    @property
    def cb_next(self): return self._cb_next
    @cb_next.setter
    def cb_next(self,val): self._cb_next = val

    @property
    def cb_last(self): return self._cb_last
    @cb_last.setter
    def cb_last(self,val): self._cb_last = val
    @property
    def cb_first(self): return self._cb_first
    @cb_first.setter
    def cb_first(self,val): self._cb_first = val

    def total(self): return len(self._seq)
    def ii(self): return self._ii

    def text(self): return self._text
    def set_text(self,val): self._text = val

    def __bool__    (self): return self.ii() < self.total()
    def __inc       (self): self._ii += 1
    def __enter__   (self): self.cb_first(self); return self
    def __iter__    (self): return self
    def __exit__    (self,*a): self.cb_last(self)

    def __next__(self):
        if self:
            ii = self.ii()
            self.__inc()
            self.cb_next(self)
            return ii, self._seq[ii]
        else:
            raise StopIteration




