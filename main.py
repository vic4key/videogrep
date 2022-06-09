from videogrep.cli import *

try: cdir = sys._MEIPASS
except Exception: cdir = ""
import os
os.environ["cdir"] = cdir

if __name__ == "__main__": main()