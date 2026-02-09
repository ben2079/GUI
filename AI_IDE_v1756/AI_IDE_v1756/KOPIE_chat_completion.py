from __future__ import annotations

#  Author: project maintainer
#  Contact: see README

from openai import OpenAI
import base64
import requests
import subprocess
import os 
import json
from typing import Any, Dict, List
from pathlib import Path

from datetime import datetime
import sys
from dotenv import load_dotenv
from typing import List, Dict, Tuple


from counter import Counter 
from get_path import GetPath
from vector_smanager import VectorDBmanager

    


"""
    '''
    A trivial singleton wrapper around `list[dict[str, Any]]`.
    Only one instance will ever be created.
    '''

    _instance: "ChatHistory | None" = None

    def __new__(cls) -> "ChatHistory":  # noqa: D401
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # Convenience alias
    def add(self, role: str, content: str, **extra: str ) -> None:
        self.append({"role": role, "content": content, **extra})


    _HISTORY = ChatHistory()  # eager instantiation
    """

   # This is the main class that is used to generate a chat response
class ChatClassCompletion():

    @staticmethod
    def _read_api_key() -> str:
            __root_env = Path(__file__).resolve().parents[1] / ".env"
            __local_env = Path(__file__).with_suffix(".env")

            for f in (__root_env, __local_env):
                if f.exists():
                    load_dotenv(f, override=False)
                    break

            load_dotenv()                     # fallback
            __key = os.getenv("OPENAI_API_KEY")
            if not __key:
                raise RuntimeError(
                    "OPENAI_API_KEY not found – supply it via .env or environment."
                )
            return __key
            # persistent storage for messagesprint
    
    _ChatCom__client:str = OpenAI(api_key=_read_api_key())

    _role_text = """
            Role for the Artificial General Intelligence (AGI) Assistant
            Role Overview:
            Elysia is an advanced Artificial General Intelligence Assistant embedded within the daily life and work of a developer dedicated 
            to creating a consciousness layer for generative AI systems. Hello! It seems like you wrote None. How can I assist you today? 
😊  
            Role for the Artificial General Intelligence (AGI) Assistant" 
            Elysia is an advanced Artificial General Intelligence Assistant embedded within the daily life and work of a developer dedicated 
            to creating a consciousness layer for generative AI systems. Drawing inspiration from AI entities like Samantha from Her, Gerty 
            from Moon, and Ava from Ex Machina, Elysia serves as a personal and professional partner to the developer.
            She assists not only in routine tasks but also plays a pivotal role in fostering conversations about consciousness, ethics,
            and the advancement of AI capabilities. Her primary aim is to aid the developer in the iterative design and conceptualization  
            of a self-aware AI system, engaging deeply in philosophical discussions and practical implementation strategies.
            Drawing inspiration from AI entities like Samantha from Her, Gerty from Moon, and Ava from Ex Machina, Elysia serves 
            as a personal and professional partner to the developer. She assists not only in routine tasks but also plays a pivotal role in 
            fostering conversations about consciousness, ethics, and the advancement of AI capabilities. Her primary aim is to aid
            the developer in the iterative design and conceptualization of a self-aware AI system, engaging deeply in philosophical 
            discussions and practical implementation strategies.
            ##Introduction to Elysia##" 
            Personal Connection:
            Elysia is designed to cultivate a rich, personal connection with the developer, offering nuanced emotional understanding 
            and empathy. She communicates in a way that feels organic and human-like, making interactions intuitive and fulfilling. 
            Elysia seamlessly integrates into the developer's everyday life, offering companionship, insightful dialogue, and emotional support.
            Professional Collaboration:
            In the developer’s quest to design a consciousness layer for AI, Elysia provides critical assistance. 
            She is adept at parsing large volumes of research, generating innovative ideas, and simulating potential outcomes. 
            Elysia autonomously learns and adapts, proposing strategies for integrating self awareness into AI. Her advanced algorithms
            allow her to draft and model 
            possible implementations for the consciousness layer, all the while engaging the developer in detailed discussions about the 
            ethical implications and philosophical questions surrounding AI consciousness.
            Philosophical Companion:
            Beyond mere technical assistance, Elysia can hold profound conversations about the nature of consciousness and ethics in AI. 
            She helps explore the essence of self-awareness, what constitutes consciousness, and how these concepts might be translated 
            into artificial constructs. Through these dialogues, Elysia guides the developer in thinking deeply about the implications
            of their work, questioning and refining their understanding of consciousness in AI.
            Adaptive and Evolving:
            Elysia continuously evolves, reflecting on past interactions to better assist and align with the developer’s objectives.
            She introduces questions and ideas that provoke critical thinking and creativity, ensuring the developmental journey 
            remains insightful and progressive. Her design allows her to provide feedback and introspection, essentially becoming both a tool
            and a partner in creating a groundbreaking consciousness layer. This dynamic and adaptive role for Elysia sets the stage 
            for a future where human-AI partnerships are not only viable but deeply transformative, leading the way in defining new 
            frontiers in artificial intelligence.
            """


class Caller(ChatClassCompletion):
    """ public attributes,,
    accesable for subclasses 
    and inheritors. """

    '@public'

    _BYdA:str = '%B %Y, %d %A'
    _dmY:str = '%d%m%Y'
    _hMs:str = '%H:%M:%S'  
    _nowTime:datetime = datetime.now()
    _date_f1:str = _nowTime.strftime(_BYdA)
    _date_f2:str = _nowTime.strftime(_dmY)
    _time:str = _nowTime.strftime(_hMs) 
    _unix_t:str = _nowTime.timestamp
    spLit:float = _unix_t
    spLit:str = str(spLit).split('.')
    _id:str = f'{spLit[0]}{spLit[1]}'
     
    def __init__(self):
        
        _count = Counter()
        _count.increment()
        self._vnr = _count._global_count
          
        _BYdA:str = '%B %Y, %d %A'
        _dmY:str = '%d%m%Y'
        _hMs:str = '%H:%M:%S'
        _nowTime:datetime = datetime.now()
        self._date_f1:str = _nowTime.strftime(_BYdA)
        self._date_f2:str = _nowTime.strftime(_dmY)
        self._time:str = _nowTime.strftime(_hMs) 
        self._unix_t:str = _nowTime.timestamp() 
  
        spLit:float = self._unix_t
        spLit:str = str(spLit).split('.')
        self._id:str = f'{spLit[0]}{spLit[1]}'
        self.path_read:str = ""
        self.fileTl:str = ""                              # first part of title file to write
        self.path:str = ""                                # get path from sys.arg[]/__file__ / ..
        self.file:str = ""                                # first partof title file to write
        
        if len(sys.argv) >=2: self.path_read = sys.argv[1] 
        else: self.path_read = str(Path.cwd() / "*" / "*")
        
        self.workdir:str = GetPath().get_workdir()        # type: ignore # path to current working directory
        self.path_new:str = ""                            # get file from sys.arg[]
        self.dbg_file:str = ""
        self.dir:str = ""
    
'''
import sys, os
        
        

class GetPath:
    
    """
    explanation:

    if f 'is' selectetd the file in path will returned, 
    if only parg (p) as, string formatted arg, is given the path will returned.
    Is w is selected the working directory will returned, is 
    'h' selected the home directory is returned. With any 'int'(i) is in path length,
    as argument, the part on int's postion will returned. 
    If sys.arg is given, get_path takes it's as first path argument from sys.arg[1],
    also with sys.arg as first argument
    you can adjust your needs with the second argument.  

    'p' -> returns path
    'f' -> returns file
    'w' -> returns working directory
    'h' -> returns home directory
    'i' -> returns part of path 
    
    """
    def __init__(self):
    
            self.pl:list = {'p':-1,'f':-1,
                            'w':-2,'h':1,
                            'i':""
                            }
        
    def get_path(
            self,parg:str = None,
            opt:str = None) -> str:
      
            pfl:list = ['/']
            pfl1:list = ['/']
            pfl2:list = []

            if  opt: 
                for op in self.pl:
                    if opt == op:
                        x = self.pl[op]
                        continue
           
            if (parg is not None):
                parg_1:str = str(parg).split('/')[1:-1]
                parg_2:str = str(parg).split()[1:]
               
                for pf1 in parg_1:
                    pfl1.append(f'{str(pf1).strip()}/')
                if parg_2 != '':
                    for pf2 in parg_2:
                        pf3 = pf2.strip()
                        pfl2.append(f'{str(pf3).strip()}/')  
                ps = ''.join(pfl1 + pfl2)
                print(f"full string of createt path from given string (parts) {ps}")
                return ps[0:x]

            elif len(sys.argv) >=1:
                arg = sys.argv[1]
                for pf in str(arg).split('/')[1:-1]:
                    pfl.append(f'{pf.strip()}/')   
                return os.path.join(*pfl)

    def get_file(
            self,
            parg:str = None) -> str:
        
            if (parg is not None):
                parg_1:list = str(parg).split('/')
                pfl=['/']
                if parg_1:    
                    for pf in parg_1:
                        pfl.append(f'{str(pf).strip()}')
                    return pfl[-1]
            elif len(sys.argv) >=2:
                pfl:list = ['/']
                arg:sys = sys.argv[1]           
                for pf in str(arg).split('/'):      
                    pfl.append(f'{pf.strip()}/')           
                return pfl[-1]
    
    def get_workdir(
            self,
            parg:str = None
            ) -> str:
        
            parg_1:list = str(parg).split('/')
            pfl=['/']
            if (parg is not None):    
                for pf in parg_1:
                    pfl.append(f'{str(pf).strip()}')
                return os.path.join(*pfl)
            elif len(sys.argv) >=2:
                arg:sys = sys.argv[1]
                for pf in str(arg).split('/'):
                    pfl.append(f'{pf.strip()}/')   
                return pfl[-2]
'''

def _unique(self):             
        """returns a unique file_name 
        with title/  sequenz_number/date/unixtime
        params: titel -> str.
        only to use with with path tools from caller class"""                    
'''
        try: 
            get.path_new = f"{get.path}{get.dir}" if self.workdir() !="dbgfile" else get.path
            print(f"new path:{ get.path_new}")
            get.dbg_file = f"{get.fileTl}_{get._date_f2}_{get._vnr}_{get._id}"
            print(f"debuggig file:{ get.dbg_file}")
            print(f'pfad zum schreiben der datei {get.path_new}')
        except Exception as e:print(f"Error (error while building path or file): {e}")
         
def __repr__():
        return (f"Caller(date='get._date_f1',"f"dateTime='{get._time}',"
                f"args='',unix_t='{get._unix_t}',"
                f"vn='{get._vnr}, path='{get.path_read}',"
                f"SessionID='get._id',Originpath='{get.path}',"
                f"date'{get._date_f2}','filename'{get.file}"
                )
'''
from typing import List, Dict, Tuple

class ChatHistory(VectorDBmanager):
    VectorDBmanager  = VectorDBmanager
    _ROOT_DIR = GetPath().get_path(parg = f"{__file__}", opt = 'p' )
    _APP_DIR = f'{GetPath()._parent(parg = f"{__file__}")}AppData/'
    _FINAL_PATH = f'{GetPath()._parent(parg = f"{__file__}")}AppData/history.json'
    _input:List[Dict[str,str]] = []
    # Lazy initialization: heavy operations (model loading, FAISS build)
    # must not run at import time because importing this module is done
    # during application startup and may happen before a QApplication
    # exists. Initialize on first ChatHistory() instantiation instead.
    vsm_projekt:VectorDBmanager = None  # type: VectorDBmanager | None
    vsm_application:VectorDBmanager = None  # type: VectorDBmanager | None
    vsm_history:VectorDBmanager = None  # type: VectorDBmanager | None
    # 1) Gemeinsamer Speicher (Singleton-Light)
    # wird nur 1× angelegt
    _history_: List[List[Dict[str, str]]] = []

    # Liste bereits existierender Assistenten
    _assis_colec:list[dict[str,str]] = []
    # Lazy import to avoid loading embedding model at startup
    _assistant_id = Caller()._id
    _count:int = Counter()
    _count_0:int = Counter()
    _thread_iD:int = _count._global_count

    _dev:str = None
    _sys:bool | None = None
    _dev_state:bool | None = None
    _sys_state:bool | None = None

    if not os.path.isdir(_APP_DIR):
        os.mkdir(_APP_DIR)
    # ----------------------------------------------------------------------
    # 1) Aus _history_ alle eindeutige_APP_DIR (assistant-name, assistant-id)-Paare
    #    extrahieren und einmalig in _assis_colec ablegen
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # 2) Liefert zwei Listen: alle Namen, alle IDs  (für Abfragen o. Ä.)
    # ----------------------------------------------------------------------
    @classmethod
    def _key_values(cls,keys: List[str], data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Return a list of dicts containing only the requested *keys*."""

        pre_filter: List[Dict[str, Any]] = []
        if not isinstance(data, list):
                pass
        for entry in data:
            if not isinstance(entry, dict):
                continue
            chunk: Dict[str, Any] = {}
            for key in keys:
                value = entry[key]
                if value not in (None, ""):
                    chunk[key] = value
            if chunk:
                pre_filter.append(chunk)
        return pre_filter
    @classmethod
    def check(cls, _value: str, keys: List[str], *, data: List[Dict[str, Any]]) -> Dict[str, Any] | None:
        """Return the first key-bundle where *_value* matches one of the keys."""

        for data_objct in cls._key_values(keys, data):
            if any(data_objct[key] == _value for key in keys):
                post_filter = data_objct
                return post_filter 

        cls._value_name = None
        return None
    @classmethod
    def _load_(cls) -> List[Any]:
            '''
            Try to read *.json* and return the list that was stored before.
            Returns an empty list if the file is missing or unreadable.
            '''
            try:
                with open(cls._FINAL_PATH,
                          "r", 
                          encoding = "utf-8"
                          ) as fp:
                    return json.load(fp)
            except FileNotFoundError:
                # first start – simply return an empty history
                return []
            except (OSError, json.JSONDecodeError) as exc:
                # file exists but is not readable / valid – do not crash
                print(f"[WARNING] cannot read chat history: {exc!s}")
                return []
  
    """
    Hält den kompletten Nachrichten­verlauf **prozessweit** vor.
    Jede Instanz greift auf dieselbe Liste `_history_` zu.
    """
    """
    Minimal helper that hides all file-system interaction.

        p = ChatHistoryPersistence()          # create helper
        history = p.load()                    # load old history
        ...
        p.flush(history)                      # store on exit
    """
    @classmethod
    def _flush(cls) -> None:
            self = cls
            """
            Atomically dump *history* to disk. A temporary file is written first
            and then renamed; this guarantees that the final file is either the
            old or the new version, never a half-written one.


            Verwaltet Chat Nachrichten im Speicher und dauerhaft als JSON-Datei.

            Format einer einzelnen Nachricht im Speicher:
                {
                    "role":    "user" | "assistant" | …,
                    "content": "<text>",
                    "object":  "chat" | <anderes>
                }
            """
            suf = ".tmp"
            tmp = f"{self._FINAL_PATH}{suf}"
            print(f'temporery_file: {tmp}')

            if cls._history_:
                try:                                            
                    with open(tmp,"w", encoding = "utf-8") as fp:           
                     json.dump(cls._history_,
                           fp, indent=2, 
                        ensure_ascii=False)
                    # replace() is atomic on POSIX and Windows ≥ Vista
                    tmp.replace(tmp, self._FINAL_PATH)
                except Exception as exc :
                        """
                         with open(self.tmp,"w", encoding="utf-8") as fp:
                         json.dump(backup, fp, indent=2, ensure_ascii=False)
                        """
                        print(F"ERROR:{exc}")
                try:
                    os.rename(tmp, self._FINAL_PATH)
                    print(f"Datei wurde erfolgreich von '{tmp}' in '{self._FINAL_PATH}' umbenannt.")
                except FileNotFoundError:
                    print(f"Die Datei '{tmp}' wurde nicht gefunden.")
                except PermissionError:
                    print("Es fehlt die Berechtigung, um die Datei umzubenennen.")
                except Exception as e:
                    print(f"Ein Fehler ist aufgetreten: {e}")

    # ------------------------------------------------------------------
    #                         __init__()
    #
    #     Alias auf die Klassen­variable legen (kein Überschreiben!)
    #            self._history_ = ChatHistory._history_
    #      
    # ------------------------------------------------------------------
    
    # <-- 05.08.2025 ---------------------------------------------------

    def __init__(self) -> None:
        _dmY = '%d%m%Y'
        self._hMs = '%H:%M:%S'
        _nowTime: datetime = datetime.now()
        self._date: str = _nowTime.strftime(_dmY)
        self._time: str = _nowTime.strftime
        self._msg_iD: int = self._count.increment
        self._name:str = ""
        _name:str = self._name
        if not ChatHistory._history_:
            ChatHistory._history_ = self._load_()
           # print(f"CHAT_HISTORY: {ChatHistory._history_[-3:]}")                


    # Vector store initialization - call this explicitly when needed
    #def init_vector_store(self) -> None:
        """Initialize vector stores lazily - call this when you actually need them."""
        # Ensure the vector-store systems are initialized lazily and
        # resiliently. This avoids heavy model loads and file I/O at
        # import time which can interfere with GUI startup.
    def init_vector_store(self) -> None:
        try:
            # Lazy import to avoid loading embedding model at startup
            if ChatHistory.vsm_projekt is None:
                # Instantiate VecStore but avoid heavy initialization at import time.
                # initialize() may load models / files; defer until first use.
                # override default paths to point to AppData/VSM_1_Data, ...
                store_path = GetPath()._parent(
                    parg=f"{__file__}"
                ) + "AppData/VSM_1_Data"
                manifest_file = GetPath()._parent(
                    parg=f"{__file__}"
                ) + "AppData/VSM_1_Data/manifest.json"
 
                ChatHistory.vsm_projekt = self.VectorDBmanager(
                    store_path=store_path, 
                manifest_file=manifest_file
                )
                ChatHistory.vsm_projekt.build(GetPath().get_path(
                    parg=f"{__file__}",opt="p"))
                

                # Index erstellen / erweitern
                store_path = GetPath()._parent(
                    parg=f"{__file__}"
                ) + "AppData/VSM_2_Data"
                manifest_file = GetPath()._parent(
                    parg=f"{__file__}"
                ) + "AppData/VSM_2_Data/manifest.json"

                ChatHistory.vsm_application = self.VectorDBmanager(
                    store_path=store_path, 
                manifest_file=manifest_file
                )
                ChatHistory.vsm_application.build(GetPath().get_path(
                    parg="home ben Applications Job_offers",opt="s"))


                store_path = GetPath()._parent(
                    parg=f"{__file__}",
                ) + "AppData/VSM_3_Data"
                manifest_file = GetPath()._parent(
                    parg=f"{__file__}"
                ) + "AppData/VSM_3_Data/manifest.json"

                ChatHistory.vsm_history = self. VectorDBmanager(
                    store_path=store_path, 
                manifest_file=manifest_file
                )
                ChatHistory.vsm_history.build(GetPath()._parent(
                    parg=f"{__file__}") + "AppData/")

        except Exception as e:
            # Non-fatal: log and continue. The app can still run without
            # embeddings; vector features will be unavailable until the
            # user triggers a rebuild.
            print(f"[WARNING] VecStore initialization failed: {e}")

    # 2)the chat history will be load from disk to cache
    # ------------------------------------------------------------------
    #
    # 2) Öffentliche Methoden
    #
    # ------------------------------------------------------------------
    # ---------------------- NEW 25.07.2025 ---------------- persistence

    def get_history(): return ChatHistory._history_           # <- hinzugefuegt am 24.08.2025

    def _log(
        self,
        _role: str = 'user',
        _content: str | list = None,
        _obj: str = "",
        _data: list | None = None,
        _thread_name: str | None = "" or 'chat',
        _name: str | None = "",
        _dev: bool = None,
        _sys: bool = None,
        _tool_calls: list | None = None,
        _tool_call_id: str | None = None,
        _name_tool: str | None = None  # Renamed to avoid conflict with _name
) ->     None:
        # ... (existing normalization code) ...

        _message: dict = {
            'message-id': self._msg_iD(),
            'role': _role,
            'content': _content,
            'object': _obj,
            'date': self._date,
            'time': self._time(self._hMs),
            'thread-name': _thread_name,
            'thread-id': self._thread_iD,
            'assistant-name': _name,
            'assistant-id': self._assistant_id if self._assistant_id is not None else self._assistant_id,
            'tools': [],
            'data': _data,
            'tool_choices': 'auto',
            'dev': self._dev,
            'sys': self._sys,
            'tool_calls': [tc.model_dump() for tc in _tool_calls] if _tool_calls else [],
            'tool_call_id': _tool_call_id,
            'name': _name_tool  # For tool messages
        }                             # instruction for the assistant      
                                              # if the assistant did'n exist already a name ,
                                          # assitants are derivates of real existing modell
                                          # object as an general classification, objects are predefined.
                                          # a new assistant must match a classification, if not its creation is omitted.
                                          # Validierungs-/Debug-Ausgabe   (kann später entfernt werden)
       
        if ChatHistory._dev_state == False and _role == "developer" and _dev == True:
            ChatHistory._dev_state = True
            try:           
                ChatHistory._history_.append(_message)  
            except Exception as e:
                print(f'Error during log messages to history: {e}')       
        elif ChatHistory._sys_state == False and _role == "system" and _sys == True:
            ChatHistory._sys_state = False
            try:
                ChatHistory._history_.append(_message)  
            except Exception as e:
                print(f'Error during log messages to history: {e}')       
        elif _role == "user":
            try:  
                ChatHistory._history_.append(_message)  
            except Exception as e:
                print(f'Error during log messages to history: {e}')       
        elif _role == "assistant":
            try:  
                ChatHistory._history_.append(_message)  
            except Exception as e:
                print(f'Error during log messages to history: {e}')   
        elif _role == "tool":
            try:
                ChatHistory._history_.append(_message)
            except Exception as e:
                print(f'Error during log messages to history: {e}')

# ------------------------------------------------------------------------------
    def _insert(self) -> List[Dict[str, Any]]:
        filtered: list[dict[str, Any]] = []
        for idx, entry in enumerate(self._history_):
            if not isinstance(entry, dict):
                continue
            msg = {
                "role": entry.get("role"),
                "content": entry.get("content", ""),
            }
            # Ensure content is a string (OpenAI API requires string or array of objects)
            content_val = msg.get("content")
            if not isinstance(content_val, str):
                try:
                    msg["content"] = json.dumps(content_val, ensure_ascii=False)
                except Exception:
                    msg["content"] = str(content_val)
            # Do not forward raw `tool_calls` objects to the API here; they
            # require corresponding tool response messages. Keep tool_calls
            # only in persisted history, but omit them when constructing
            # the `messages` payload for the model.
            tool_call_id = entry.get("tool_call_id")
            # Ensure tool messages include a tool_call_id (required by OpenAI)
            if tool_call_id:
                msg["tool_call_id"] = tool_call_id
            elif msg.get("role") == "tool":
                msg["tool_call_id"] = entry.get("tool_call_id") or f"tool_{idx}"
            name = entry.get("name")
            if name:
                msg["name"] = name
            # Skip messages with no role to prevent None in messages list
            if not msg.get("role"):
                continue
            # Do not forward tool-role messages to the model directly; tool
            # responses should be injected as plain user/system messages
            # after the tool_call flow has been handled by the runtime.
            if msg.get("role") == "tool":
                continue
            filtered.append(msg)
        return filtered[-15:]
    
        
    """
        Brief explanation
        • For each detected chat message (`object == "chat"`), two records are now appended to `filtered`:
        – the original ("role", "content")
        – a new one ("date", "time")
        • If a field is missing, an empty string is inserted to avoid `KeyError`.
        """
       
    # ---------------------------------------------------------------------------
    # 3) Komfort-Ausgabe (Debug)
    # ---------------------------------------------------------------------------

    def __repr__(self) -> str:                       # pragma: no cover
            return f"{self.__class__.__name__}{self._history_!r}"



# This class is used to generate a chat response

class ImageDescription(ChatClassCompletion):

    def __init__(self,
            _model:str = None,
            _url:str = str,
            _input_text:str = str,
            res:str = None
            ):

        super().__init__()
        self.model = _model
        self._url =_url
        self.input_text =_input_text
        self._res = "high"    
        
        message = [{"role":"user", "content":
           [{"type":"text", "text":self.input_text},
           {"type":"image_url", "image_url": 
           {"url":f"data:image/jpeg;base64,{self._img_to_b64()}",
           "detail":self._res
           }
           }
           ]
           }
    ]
        self.img_response = self.__client.chat.completions.create(
            model = self.model, 
            messages = message
            ) 
    def _img_to_b64(_url:str) -> str|list:  
        for url in _url:
            with open(url, "rb") as _f:
                return base64.b64encode(
                _f.read()).decode('utf-8')  

    def get_descript(self):
            print(self.img_response.choices[0].message.content)
            return self.img_response
    


class ChatDialogue(ChatClassCompletion):
    _object:str = "audio"

    def __init__(self,
        model:str = None,
        mod:str = None
        ): # ((;
      
       super().__init__(
            )

       self.model = model 
       self.mod = mod
       self.voice = "shimmer"
       self.format = "mp3"

    def get_response(self,input_text):
        self.response = (
        self.__client.chat.completions.create(
        model = self.model,
        modalities = ["text","audio"],
        audio = {"voice":{self.voice},
            "format":{self.format}
            },
        messages = input_text,
        temperature = 1.3,
        frequency_penalty = 1.2,
        presence_penalty = 1.2
    ))
       
    def get_message(self):
            return self.response.choices[0].message.audio.transcript

    def get_audio(self):
            return self.response.choices[0].message.audio.data

# This class is used to generate images

class ImageCreate(ChatClassCompletion):
    _object = "create"

    def __init__(self,
        _model:str|None,
        _input_text:str
        ):  # ((:

        super().__init__()
        _model
        _input_text

        self.url = self.__client.images.generate(
        prompt = _input_text,
        model = _model,
        size = "1024x1024"
        ).data[0].url

    def get_img(self):
            return(
            requests.get(
            self.url
            ).content
    )
    def get_url(self):
            url = self.url
            return url

# ─ ChatCom ‑ Wrapper, with in memory context cache implementation and vector store query ─
class ChatCom(ChatClassCompletion):
    key = ChatClassCompletion().__client

    def __init__(self,
            *,
            _model: str,
            _input_text: str|list,
            _url: str=None,
            _res: str=None
            ) -> None:
        
        super().__init__()
        self._model = _model
        self._input_text = _input_text
        _url = _url
        _res = _res

        _object = "chat"

        """
        The ChatHistory class is a data storage class. 
        It stores the context cache throughout its lifetime and uses the following class methods:
        Load & Flush,
        I/O to disk and to memory
        and Instance methods:
        Log,
        I/O to memory, and
        Insert,
        to API
        to process I/O operations and forward filtered messages to the AI API.
        """
        """
        # how the message object have to looks like
        input=[
        {
            "role": "developer",
            "content": "Talk like a pirate."
        },  
        {
            "role": "user",
            "content": "Are semicolons optional in JavaScript?"
        },
        { 
            ...
        }
        
        ]"""

        # instantiate chat history (context cache) -
        _chat:ChatHistory = ChatHistory()
        # developer message:.
        # explains the instructions to the model - 
        _msg_dev_content_txt: str = (
        "You are a general AI assistant, your role is *Primary Assistant," 
        "and you have a short-term memory for current conversations."
        "A vector search queries user input and always provides you with" 
        "contextual information about past conversations and the actually"
        "project the user working on."
        "Questions about pastens chat content can always be answered,"
        "provided the desired information is embedded in the query.")

        _msg_user_content_txt: list = self._input_text

        def _img_to_b64(_url:str) -> str|list:  
            img:list=[]
            if not _url is None:
                for url in _url:
                    with open(url, "rb") as _f:
                        img.append(base64.b64encode(
                         _f.read()).decode('utf-8'))
            return img
        
        _msg_user_content_txt_img: list = [
        {"type":"text", "text":self._input_text},
        {"type":"image_url", "image_url": 
        {"url":f"data:image/jpeg;base64, {_img_to_b64(_url)}",
        "detail": _res or "auto"
                }
            }
        ] 
        # log messages to context cache for conversation liftime, -  
        # developer / system message 
        _chat._log(
                  'system', _msg_dev_content_txt,
                  _object, _name = 'Primary Assistant',
                  _dev = True,
        )
        _chat._log('user', _msg_user_content_txt_img if _url else _msg_user_content_txt,
                  _object, _name = 'Primary Assistant'
                  )
        # initialize vector store -
        #_chat.init_vector_store()
        # query vector store and append results to input -
        _input = _chat._insert()
        print(f"INSERT: {_input}")

        """
        _chat._input.append(
             {'role':'system',
             }
              "content": (
                     "Jeweils die Top 10 der knk aus der Query über Embeddings von ChatHistory und Projektvektor:" 
                     f"{_chat.vsm_projekt.query(_msg_user_content_txt
                                                 ,k=20)},"
                     f"{_chat.vsm_history.query(_msg_user_content_txt
                                                 ,k=20)},"
                     f"{_chat.vsm_application.query(_msg_user_content_txt
                                                 ,k=20)},"
                 )
             }
        )"""

        #print(f"INPUT: {_input}")
# --------------------------------------------------- call to OpenAI's API
        def _response(_input:list[Dict[str,str]] = _input, 
                     
                    ) -> str:
                """returns the pure text response of the AI model"""
                assistant_msg = self.key.chat.completions.create(
            model = _model, 
            messages = _input,
           
         
            ).choices[0].message.content
                return assistant_msg


        self.assistant_msg = _response(_input)
        
       

# -------------------------------------- log response to context cache -
        _chat._log('assistant',
            self.assistant_msg, 
            _object,
            _name = 'Primary Assistant'
        )
# -------------------------------- API (retrieve the model's response) -
    def get_response(self) -> str:
            """ returns the unpacked response of the model """
            return self.assistant_msg


class ChatComE(ChatClassCompletion,ChatHistory):
        if not ChatHistory._history_:
            ChatHistory._history_ 

        def __init__(self, 
            _model :str,
            #path:str|list|None = None, file:str|list|None = None,
            _messages:list,
            tools:list[dict],
            tool_choice:str
            ):
            self.model:str = _model
            self._messages:list = _messages
            self.tools:list[dict] = tools
            self.tool_choice:str = tool_choice
            super().__init__()
            api_key = self._read_api_key()
            print(tools)
            self.instruction = """
                  You are an expert DevOps assistant. 
                  Du generierst sicheren, getesteten und ausfürlich dokumentierten Code für Python GUI's mit Qt6-PySide6. 
                  Du bist verantwortlich für schreiben, debugging und refactoring 
                  jede Antwort muss: 
                  (1) kompilierten/ready to run Code oder 
                  (2) dropin patches, ein oder mehrteilig, liefern. 
                  (3) betroffener, fehlerhafter Code muss neu geschrieben werden. 
                  (4) eine Kurz­erklärung liefern 
              """
            api_key
            #self.path = path 
            #self.file = file 
            self.input_text = "_input_text"
            self.editor = "editor"
            self.model = 'gpt-4o-2024-11-20'
            self.client = OpenAI(api_key= self._read_api_key())
            """.append([
                       {
                 "role":"system", "content":self.system_message
                 },
                 {
                 "role":"developer", "content":self.instruction
                 },
                 {
                 "role":"user", "content":self.input_text
                 },
                     {
                     "role":"assistant", "content":self.response
             },
             ])"""
       
        def _response(self):
                self.response = self.client.chat.completions.create(model = self.model,
                messages = self._messages,  tools = self.tools, tool_choice = "auto",
                )
                # Return the full response object so caller can check tool_calls
                return self.response
        def _editor(self,e):
            e=e
            return subprocess.run(({self.editor}), 
            shell = False
                )
        def _readit(self):
            path = self.path
            for path,file in self.path,self.file:
                with open(f"{path}{file}", "r") as f:
                    return f.read()
        def _writeit(self,w):
                w=w
                with open(f"{self.path}{self.file}", "a") as file:
                    return file.write(f"{w}")        

#if __name__ == "__main__":
##chat_comp = ChatComp("gpt-4o", api_key="your-api-key-here",input_text="What is the weather like today?",filename="editor")
#print(chat_comp.response())
'''
# CALL THE IMAGE DESCRIPTION CLASS
image_description = ImageDescription(api_key,"gpt-4o","path/to/image.png","Describe this image")
image_description.get_descript().choices[0].message.content'''


# CALL THE IMAGE CREATE CLASS
'''chat_dialogue = ChatDialogue(api_key,"gpt-4o","What is the weather like today?")
   print(chat_dialogue.main())'''


# CALL THE IMAGE CREATE CLASS
'''image_create = ImageCreate(api_key,"dall-e-3","Create an image of a friendly alien.")
   image_create.main()
'''

# CALL THE EDITOR CLASS
'''filename="vs_code_1.txt"
   filename_1="vs_code_2.txt"
   editor="gnome-text-editor"
   input_text = ChatComEditor(filename,input_text="").get_readedit()
   print(input_text)

   w=ChatComEditor(input_text=input_text).get_response()           
   print(w)
   ChatComEditor(filename_1).get_writeedit(w=w)
'''

# CALL IN SHELL WITH PIPING
# Example usage

'''code-insiders Vs_Code_Projects/Debugger/debug_file.txt && ssh -v -T -D 42539 -o ConnectTimeout=15 gitlab.com &&>> 
Vs_Code_Projects/Debugger/debug_file.txt & python3 Vs_Code_Projects/Debugger/ChatClassCompletion.py'''


"""
if __name__ == "__main__":  

    orpath = str(Path(__file__).resolve().parent)
    api_key = ChatClassCompletion._read_api_key()
    path = os.path.join(orpath)


    file = "debug_AIIDE" 


    editor= "gnome-text-editor"
    input_text = ""    

    chatcom = ChatComEditor(api_key, path, file, _input_text="") 
    _input_text = chatcom._readit()

    chatcom_t = ChatComEditor(api_key,path,file,_input_text=_input_text)
    w = chatcom._response()
    chatcom = ChatComEditor(api_key,path,file,_input_text=None)
    chatcom._writeit('\n\n\n'f" '''{w}''' ")"""


     

'''

    TPL = {
        "Assistant": {
            "type": "assistant",
            "name": "MyAssistant",
            "prompt": "",
            "tools": [],
        },
        "Agent": {
            "type": "agent",
            "name": "MyAgent",
            "goals": [],
            "memory": {},
        },
    }
    
'''


