from __future__ import annotations
import json
import os
import atexit
import ast
import dis
import inspect
import sys
import typing
from typing import Any
from datetime import datetime
from pyexpat import model
from get_path import GetPath
from KOPIE_chat_completion import ChatComE, ChatHistory
from vector_smanager import VectorDBmanager

_MAX_TOOL_DEPTH = 30 
_TOOL_CACHE: dict[str, str] = {}
_MODEL = "gpt-4.1-mini-2025-04-14"
model = _MODEL
_DEFAULT_SAVE_DIR = os.path.expanduser("/home/ben/Applications/Cover_letters")
# Minimal, robust triage/dispatcher script.
# Config
ChatHistory._FINAL_PATH = GetPath()._parent(parg=f"{__file__}") + "/AppData/memory_db.json"

history = ChatHistory()
ChatHistory._history_ = history._load()
# Load existing history if needed

_initial_history_length = len(ChatHistory._history_)

# Flush on exit only when new entries were added
def _cleanup_on_exit():
    if len(ChatHistory._history_) > _initial_history_length:
        history._flush()


atexit.register(_cleanup_on_exit)

# Vector DB tool wrappers
def memorydb(query: str, k: int = 1) -> str:

    store_path = GetPath()._parent(parg=f"{__file__}") + "AppData/VSM_4_Data"
    manifest_file = GetPath()._parent(parg=f"{__file__}") + "AppData/VSM_4_Data/manifest.json"
    db = VectorDBmanager(store_path=store_path, manifest_file=manifest_file)
    db.build(GetPath().get_path(
    parg = "home ben Vs_Code_Projects Projects GUI AI_IDE_v1756 AppData", opt = "s"))
    result = db.query(query, k=k)
    return str(result) if result else "No results found in memory database"


def VectorDB(query: str, k: int = 1) -> str:
    try:
        store_path = GetPath()._parent(parg=f"{__file__}") + "AppData/VSM_2_Data"
        manifest_file = GetPath()._parent(parg=f"{__file__}") + "AppData/VSM_2_Data/manifest.json"
        db = VectorDBmanager(store_path=store_path, manifest_file=manifest_file)
        db.build(GetPath().get_path(
        parg = " home ben Applications Job_offers", opt = "s"))
        result = db.query(query, k=k)
        return str(result) if result else "No results found in vector database"
    except Exception as e:
        return f"VectorDB error: {e}"


# return data from T, with key:type or with key:type where key:type,from (SQL/NoSQL) data structure
def retrieve_data(data:list[ Any|str, Any]) -> Any:
        Any = str | int | float | bool | list | dict | tuple | None
        dat:Any 
        structure:list = []
        idx:str = []
        dtx:list
        data = data[0] if isinstance(data, 
            list) and len(data) == 1 else [
            data for data in data]
        for typ in Any:
            if isinstance(data, typ):
                structure.append(typ)
            if isinstance( data, dict):
                for key, val in data.items():
                    idx.append(key)
                    dtx = retrieve_data([val])
                    structure.append(
                    {key:dtx})
                    return 
        structure if structure else "unknown"


        '''
        if isinstance(data, Any):
        try:
            payload = json.loads(payload)
        except Exception:
            return payload

    if not isinstance(payload, dict):
        return str(payload)

    document = payload.get('document')
    if isinstance(document, dict):
        page_content = document.get('page_content')
        if isinstance(page_content, str) and page_content.strip():
            return page_content.strip()

    content = payload.get('content')
    if isinstance(content, dict):
        text = content.get('text')
        if isinstance(text, str) and text.strip():
            return text.strip()

    return json.dumps(payload, ensure_ascii=False)
    '''

def _write(text: str, path: str | None = None, job_offer: str | None = None) -> str:
    """Persist document to disk with timestamped filename."""
    target_dir = os.path.expanduser(path or _DEFAULT_SAVE_DIR)
    os.makedirs(target_dir, exist_ok=True)

    prefix = (job_offer or "cover_letter").strip()
    # save prefix generation with safe characters
    safe_prefix = "".join(ch if ch.isalnum() or ch in ("-", "_") else "_" for ch in prefix) 
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{safe_prefix}_{timestamp}.md"
    file_path = os.path.join(target_dir, filename)

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text.rstrip() + "\n")
    return file_path

# Tools metadata (kept for model prompts but handled locally)
vector_tools = [
    {
        "type": "function",
        "function": {
            "name": "vectordb_tool",
            "description": (
                "Use this tool to query the vector database for relevant documents "
                "based on the user's query."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "vector_tools": {
                        "type": "string",
                        "enum": ["VectorDB", "memorydb"],
                        "description": "Select the source to query"
                    },
                    "Query": {
                        "type": "string",
                        "description": "Filename or free-text query to look up"
                    }
                },
                "required": ["Query", "vector_tools"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write",
            "description": (
                "Persist the generated document to disk. Provide the text via 'content' and"
                " optionally override the default save directory or include the job offer title"
                " for the filename prefix."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "document content to write to disk."
                    },
                    "path": {
                        "type": "string",
                        "description": "Directory to store the file. Defaults to /home/ben/Applications/Cover_letters."
                    },
                    "doc_title": {
                        "type": "string",
                        "description": "Optional doctitle used to build the filename prefix."
                    }
                },
                "required": ["content"]
            }
        }  
    } 
]
# Triage tool to route to specialized agents
triage_tools = [
    {
        "type": "function",
        "function": {
        'name':"route_to_agent",
            "description": "Route the request to a specialized agent.",
            "parameters": {
                "type": "object",
                "properties": {
                    "target_agent": {"type": "string", "enum": ["cover_letter_agent", "Mail_agent"]},
                    "user_question": {"type": "string"}
                },
                "required": ["user_question", "target_agent"]
            }
        }
    }
]
# System prompts
sys0mi = [
   {
        "role": "system",
        "content": (
            " You are a cover_letter_agent specialized in generating cover letters for job applications in IT/Applicationdevelopment. "
            " You get all necessary information from the vector database to generate a personal cover letter: "
            " 1. Retrieve the AGENTS.md from the vector database. Use the function VectorDB with Query string AGENTS.md."
            " 2. Retrieve files from AGENTS.md where job_offers are marked OFFEN; provide filename as a query to VectorDB tool."
            " 3. Use the memorydb function to retrieve relevant conversation history only if needed."
            " 4. If you can generate the cover letter with the information you have, do so."
            " Generiere  **structured output** nach folgendem dictionary Schema  "
            " {'content':{'text':'**your message text**'},{'document':{'page_content':'**das generierte Anschreiben**'},"
            " {'metadata':{'job_offer':'**titel des Stellenangebots**'} }}"
            "you have the cabbility to call the following tools: vectordb_tool, cover_letter_tool "
            " write_document, calendar, send_email, @ny_url, fetch_data, call_api, call, accept_call, reject_call"
                   )
    }
]
sys1mi = [
    {"role": "system",
        "content": (
            "You are an triage agent. "
            "1. Use the memorydb function to retrieve relevant conversation history if needed."
            "2. Ask clarifying questions if information is missing. "
            "3. If you can answer the question independently, do so. "
            "4. If a specialized agent is clearly better suited, "
            "   call the function route_to_agent with the appropriate 'target_agent'."

        )
    }
]

def _validate_message_sequence(messages: list[dict]) -> list[dict]:
    """Ensure tool messages are always preceded by assistant messages with tool_calls.
    
    OpenAI API requires: assistant (with tool_calls) -> tool (with matching tool_call_id)
    If the sequence is broken (e.g., due to slicing), we drop orphaned tool messages.
    """
    validated = []
    pending_tool_call_ids: set[str] = set()
    
    for msg in messages:
        role = msg.get("role")
        
        if role == "assistant":
            # Track tool_calls from this assistant message
            tool_calls = msg.get("tool_calls")
            if tool_calls:
                for tc in tool_calls:
                    if hasattr(tc, 'id'):
                        pending_tool_call_ids.add(tc.id)
                    elif isinstance(tc, dict) and tc.get('id'):
                        pending_tool_call_ids.add(tc['id'])
            validated.append(msg)
            
        elif role == "tool":
            # Only include tool messages if we have a matching pending tool_call
            tool_call_id = msg.get("tool_call_id")
            if tool_call_id and tool_call_id in pending_tool_call_ids:
                validated.append(msg)
                pending_tool_call_ids.discard(tool_call_id)
            # else: skip orphaned tool message
            
        else:
            # user, system messages pass through
            validated.append(msg)
    
    return validated

# Helper: handle tool calls produced by the model
def _handle_tool_calls(agent_msg, depth: int = 0, 
                       agent_label: str = 'cover_letter_agent') -> Any:
    # router
    """Execute supported tool calls locally and continue the conversation."""
    if depth >= _MAX_TOOL_DEPTH:
        warning = "Aborting: tool-call depth exceeded."
        history._log(_role='assistant', 
                     _content=warning, 
                     _name='dispatcher_agent', 
                     _thread_name='chat',
                     _obj='chat')
        return warning
    
    if not hasattr(agent_msg, 'tool_calls') or not agent_msg.tool_calls:
        return None

    # Log assistant message once if recursive
    if depth > 0:
        history._log(_role='assistant',
                     _content=agent_msg.content or '',
                     _name=agent_label,
                     _thread_name='chat', _obj='chat',
                     _tool_calls=agent_msg.tool_calls)

    routed_request = None

    for tc in agent_msg.tool_calls:
        name = tc.function.name
        result:str = ""
        try:
            args = json.loads(tc.function.arguments or "{}")
        except Exception:
            args = {}
        
        if name == 'vectordb_tool':
            query = (args.get('Query') or args.get('query') or '').strip()
            tool_name = args.get('vector_tools') or 'VectorDB'
            cache_key = f"{tool_name}:{query.lower()}"

            if cache_key in _TOOL_CACHE:
                result = _TOOL_CACHE[cache_key]
            else:
                if tool_name == 'memorydb':  
                    result = memorydb(query)
                else:
                    result = VectorDB(query)
                _TOOL_CACHE[cache_key] = result
            
        elif name == 'write':
            content = (args.get('content') or '').strip()
            path = (args.get('path') or _DEFAULT_SAVE_DIR).strip() 
            job_offer = (args.get('job_offer') or '').strip() or None

            if not content:
                result = "write error: content is required"
            else:
                try:
                    saved_path = _write(content, path, job_offer)
                    result = f"Cover letter saved to {saved_path}"
                except Exception as exc:
                    result = f"write error: {exc}"
           
        elif name == 'route_to_agent':
            target = args.get('target_agent') or ''
            usr_quest = args.get('user_question') or ''
            result = f"Routing to {target}"

            if target == 'cover_letter_agent':
                routed_request = {
                    'messages': sys0mi + [{"role":"user","content":usr_quest}],
                    'agent_label': 'cover_letter_agent'
                }
            else:
                result = f'Unknown target agent: {target}'

        # Log tool output
        print(f"DEBUG: Logging tool output for {name}, id={tc.id}")
        history._log(_role='tool', _tool_call_id=tc.id, _name_tool=name,
                     _content=str(result), _thread_name='chat', _obj='chat')

    # After processing all tools, decide next step
    response = None
    next_agent_label = agent_label

    if routed_request:
        print(f"\n\nROUTED RESPONSE STARTING...")
        response = ChatComE(_model=model, 
                            _messages=routed_request['messages'], 
                            tools=vector_tools, 
                            tool_choice='auto')._response()
        next_agent_label = routed_request['agent_label']
    else:
        # Continuation
        print(f"DEBUG: History length: {len(history._history_)}")
        last_msgs = history._insert(tool=True, f_deph=-10)
        print(f"DEBUG: Last 10 messages from history: {[m.get('role') for m in last_msgs]}")
        
        raw_history = history._insert(tool=True, f_deph=-50)
        validated_history = _validate_message_sequence(raw_history)
        follow_up = sys0mi + validated_history
        # print(f"DEBUG: follow_up messages: {json.dumps(follow_up, indent=2)}")
        response = ChatComE(_model=model, _messages=follow_up, 
                            tools=vector_tools, tool_choice='auto'
                            )._response()
        # print("\n\nFOLLOW UP MESSAGES:\n\n" + str(follow_up))
        print("\n\nFOLLOW UP RESPONSE:\n\n" + str(response))

    if hasattr(response, 'choices') and len(response.choices) > 0:  
        next_msg = response.choices[0].message
        if hasattr(next_msg, 'tool_calls') and next_msg.tool_calls:
            return _handle_tool_calls(next_msg, depth + 1, 
                agent_label=next_agent_label)
        
        history._log(_role='assistant', 
            _content=next_msg.content or '', 
            _name=next_agent_label, 
            _thread_name='chat', _obj='chat')
        return next_msg.content

    return None
# start
# Entrypoint: ask triage agent
text = """fuege die Anschrift des Arbeitgebers in den Briefkopf ein und generiere ein Anschreiben auf eine offene Stelle basierend auf meinem Profil und der Stellenanzeige."""
user_msg = text
history._log(_role='user', _content=user_msg, 
             _name='dispatcher_agent',
             _thread_name='chat', _obj='chat')
triage = ChatComE(_model=model, 
                  _messages=sys1mi + [{"role":"user",
                  "content":user_msg}], 
                  tools=triage_tools, 
                  tool_choice='auto')
rspn = triage._response()
if hasattr(rspn, 'choices') and len(rspn.choices) > 0:
    msg = rspn.choices[0].message
    history._log(_role='assistant', 
                 _content=msg.content or '', 
                 _name='triage_agent', 
                 _thread_name='chat', 
                 _obj='chat', 
                 _tool_calls=msg.tool_calls if hasattr
                 (msg, 'tool_calls') else None)
    # If the triage agent asked to call a tool or route, handle it
    result = _handle_tool_calls(msg, agent_label='triage_agent')
    if result:
  
        print("\n\nCOVER LETTER:\n\n" + result)
      
    else:
        # final content
        print('\n\nFINAL CONTENT:\n\n' + (msg.content or ''))
else:
    print('\n\nRESPONSE:\n\n' + str(rspn))
