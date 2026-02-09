
## Integration in die Anwendung
 
# In chat_completion.py oder neuem Modul
from io import BytesIO
import agent_system_prompts as agent_system_prompts

try:
    from .chat_completion import ChatCom
except Exception:
    from AI_IDE_v1756.AI_IDE_v1756.ai_ide.chat_completion import ChatCom
import json




def generate_cover_letter(job_data: dict, applicant_profile: dict) -> dict:
    """
    Generiert ein Bewerbungsanschreiben basierend auf Job-Daten und Bewerberprofil.
    
    Args:
        job_data: Geparste Job Posting Daten (aus JOB_POSTING_SYSTEM_PROMPT)
        applicant_profile: Bewerberprofil
        
    Returns:
        Dictionary mit Anschreiben und Metadaten
    """
    combined_input = {
        "job_posting": job_data,
        "applicant_profile": applicant_profile
    }
    
    response = ChatCom(
        _model="gpt-4.1",
        _input_text= [_COVER_LETTER, {json.dumps(combined_input, ensure_ascii=False, indent=2)}]
    ).get_response()
    
    return response

# Verwendung:

# Applicant Profile laden
with open("/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/ai_ide/Dokumente/applicant_profile.json", "r", encoding="utf-8") as f:
    applicant_data = json.load(f)

# Cover Letter generieren
cover_letter_result = generate_cover_letter(_JOB_POSTING_PARSER.run_agent(), applicant_data)
print(cover_letter_result)

"""
## Erweiterte Features (Optional)

### A/B Testing
Generiere 2-3 Varianten mit unterschiedlichen Schwerpunkten:
- Variante A: Fokus auf technische Skills
- Variante B: Fokus auf Führungserfahrung
- Variante C: Fokus auf Cultural Fit

### Personalisierungs-Score
Bewerte wie gut das Anschreiben passt (0-100):
```python
"personalization_score": {
    "requirement_match": 85,  # % erfüllter Anforderungen erwähnt
    "keyword_match": 90,      # % relevanter Keywords verwendet
    "authenticity": 80,       # Wie persönlich/individuell
    "overall": 85
}
```

### Verbesserungsvorschläge
```python
"suggestions": [
    "Erwähne deine Erfahrung mit Docker (steht in requirements)",
    "Füge ein konkretes Beispiel für Leadership hinzu",
    "Kürze Paragraph 2 um 20 Wörter"
]
```

---

**Version**: 1.0  
**Zuletzt aktualisiert**: 12. Dezember 2025  
**Kompatibel mit**: JOB_POSTING_SYSTEM_PROMPT.md
"""