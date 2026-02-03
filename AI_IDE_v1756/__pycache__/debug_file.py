'''class_Caller 
''' 
'''debugging & code review
'''

from datetime import datetime
from ChatClassCompletion  import ChatComEditor
import os
import sys
import subprocess
from sys_Cmd import sys_Cmd


class Caller():
   
    
    def __init__(self):
     
        hms = '%H:%M:%S'
        dmY = '%d.%m.%Y'
        self.date = datetime.now().strftime(dmY)
        self.dateTime = datetime.now()
        self.unix_t = self.dateTime.timestamp()
        self.now = datetime.now()
        self.date = self.now.strftime(dmY)
        self.time = self.now.strftime(hms)
        self.dateTime = self.now
        
        self.s_ID = self.unix_t
        self.vn = float(0.0)
        self.vn = 0.0  
        self.fileTl = "debug_file.txt"
        self.path_read = os.path.join("/",sys.argv[1])
        self.path_write = "home/benjamin/Debugger"
          
        f"SessionID='{self.s_ID}'"
        f"Originpath='{self.path_write}'"


    def __repr__(self):
        return (f"Caller(date='{self.date}', time='{self.time}',"
                f"dateTime={self.dateTime}, unix_t={self.unix_t}',"
                f"vn={self.vn}, path='{self.path_read}',"
                f"SessionID='{self.s_ID}', Originpath='{self.path_write}')")
                
                

class CallerDebugger(ChatComEditor,Caller):

    def __init__(self):
        super()
        w = None

    def read_write(self):
        
        try:
            path_file = f"{self.path_write}{self.fileTl}_{self.date}_{self.vn}_{self.s_ID}"
            pfile = f"{self.fileTl}_{self.path_read}_{self.vn}_{self.s_ID}"
            with open(path_file,"a") as file:
             file.write("Debugg session python3")
        except Exception as e:
               print(f"Error (file write): {e}")
        
        try: 
            # - shell command debugger.py /path/to/execute
            run = sys_Cmd
            capture_output = run.CmdSys(f"python3 {self.path_read}")
            stdout = capture_output.stdout.decode("UTF-8")
            stderr = capture_output.stderr.decode("UTF-8")
            print(f"{stdout}{stderr}")
            with open(path_file,"a") as file:
             repeat_pattern = lambda x: "\n".join(["text"] * len(x))
             file.write(f"{repeat_pattern(stdout)}\n\n\n## {stdout}\n\n\n{repeat_pattern(stderr)}\n\n\n## {stderr}\n\n\n")  
        except Exception as e: print(e)

        try:  
            chatcomeditor_instance = ChatComEditor(self.path_read,pfile,self.input_text)
            w = chatcomeditor_instance.get_response({w})
        except Exception as e:
                print(f"Error (ChatComEditor read): {e}")
        print(f"input_text: {self.input_text} response: {w}")
        try:
            ChatComEditor().get_writeedit(w=f'## {w}\n')
        except Exception as e:
                print(f"Error (ChatComEditor write): {e}")










class CallerExecute:
    def __init__(self):
        super()
    
class Config:
    def __init__(self):
        Config

class Session:
    def __init__(self):
        Session

class Versioner():
    def __init__(self):
      Versioner

class Counter():
    def __init__(self):
      Counter

class ProcessingHistory():
    def __init__(self):
      ProcessingHistory 



Traceback (most recent call last):
  File "/home/benjamin/Vs_Code_Projects/PyToolbox/Caller.py", line 7, in <module>
    from ChatClassCompletion  import ChatComEditor
  File "/home/benjamin/Vs_Code_Projects/PyToolbox/ChatClassCompletion.py", line 2, in <module>
    from openai import OpenAI
ModuleNotFoundError: No module named 'openai'


