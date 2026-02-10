from datetime import datetime
import json
try:
    from .chat_completion import ChatCom  # type: ignore
except Exception:
    from ALDE.ALDE.alde.chat_completion import ChatCom  # type: ignore

try:
    from . import agents_factory  # type: ignore
except Exception:
    import alde.agents_factory as agents_factory  # type: ignore
from langchain_community.document_loaders import PyPDFLoader
from alde.apply_agent_prompts import _SYSTEM_PROMPT

def run_agent(job_data: dict, applicant_profile: dict) -> str:
    """
    Führt den Cover Letter Generator Agenten aus.
    Args:
        job_data (dict): Strukturierte Job Posting Daten.
        applicant_profile (dict): Strukturierte Bewerberprofil Daten.
    Returns:
        str: Generiertes Bewerbungsanschreiben im strukturierten Format.
    """
    # Erst Job Posting parsen
    parsed_job = ChatCom(
        _model="gpt-4.1",
        _input_text=f"{_SYSTEM_PROMPT['_JOB_POSTING_PARSER']}\n\n{job_data}"
    ).get_response()
    
    # Dann Cover Letter generieren mit geparstem Job + Profil
    prompt = f"""{_SYSTEM_PROMPT['_COVER_LETTER']}

**Aktuelles Datum:** {datetime.now().strftime("%d. %B %Y")} 

**Job Posting Daten:**
{parsed_job}

**Bewerber Profil:**
{json.dumps(applicant_profile, indent=2, ensure_ascii=False)}
"""
    response = ChatCom(_model="gpt-4.1", _input_text=prompt).get_response()
    return response


if __name__ == "__main__":
    # Applicant Profile laden
    applicant_profile = _SYSTEM_PROMPT['_PROFILE_PARSER']
    # Job PDF laden
    job_data = PyPDFLoader(
        "/home/ben/Applications/Job_offers/IT - Administrator (m_w_d) bei ME Saar e.V. Verband d.Metall-u.Elektroind_.pdf"
    ).load()
    
    # Cover Letter generieren
    result = run_agent(job_data, applicant_profile)
    
    # Response ist ein JSON-String, muss erst geparsed werden
    try:
        result_dict = json.loads(result.strip())
        print(result_dict['cover_letter']['full_text'])
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        # Falls kein JSON oder falsches Format, ganzen Text ausgeben
        print(result)