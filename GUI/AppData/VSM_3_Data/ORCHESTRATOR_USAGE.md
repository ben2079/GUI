# Primary Agent Orchestrator - Usage Guide

## Overview

The **`_primary_agent`** (Orchestrator) is the user-facing entry point for the cover letter generation workflow. It coordinates all specialized agents and returns a complete, validated cover letter.

## Architecture

```
User
  ↓
_primary_agent (Orchestrator)
  ├─→ _profile_parser (if profile unavailable)
  ├─→ _data_dispatcher / _job_posting_parser (extract job posting)
  └─→ _cover_letter_generator (generate letter)
  ↓
User (with cover letter + metrics)
```

## Input Contract

The orchestrator accepts user requests in this format:

### Minimal Example
```json
{
    "action": "generate_cover_letter",
    "job_posting_path": "/path/to/job.pdf",
    "profile_id": "profile_abc123def456"
}
```

### Full Example
```json
{
    "action": "generate_cover_letter",
    "job_posting": {
        "source": "file",
        "value": "/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/job_posting.pdf"
    },
    "applicant_profile": {
        "source": "file",
        "value": "/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/cv.pdf"
    },
    "options": {
        "language": "de",
        "tone": "modern",
        "max_words": 350,
        "include_enclosures": true,
        "city": "Berlin",
        "date": "2026-01-21"
    }
}
```

### Alternative: Stored Profile
```json
{
    "action": "generate_cover_letter",
    "job_posting": {
        "source": "text",
        "value": "<job posting text here>"
    },
    "applicant_profile": {
        "source": "stored_id",
        "value": "profile_sha256hash"
    },
    "options": {
        "language": "de"
    }
}
```

## Workflow Steps

### Phase 1: Input Validation
- Orchestrator validates the request structure
- Checks for required fields: `action`, `job_posting` source
- Sets defaults for `options` (language: "de", tone: "modern", max_words: 350)

### Phase 2: Profile Resolution
**If profile is provided:**
- If `source: "stored_id"`: Load from persistent DB
- If `source: "file"`: Route to `_profile_parser` for extraction
- If `source: "text"`: Route to `_profile_parser` for extraction
- If missing: Check `AppData/VSM_4_Data/applicant_profile.json` for default
- If still unavailable: Ask user to provide profile

**Example:**
```json
{
    "action": "generate_cover_letter",
    "job_posting": {...},
    "status": "awaiting_profile",
    "message": "Please provide applicant profile (file path, text, or stored ID)"
}
```

### Phase 3: Job Posting Extraction
Route to appropriate parser:
```python
route_to_agent(
    target_agent="_job_posting_parser",
    message_text={
        "type": "job_posting_pdf",
        "correlation_id": "<sha256>",
        "file": {...},
        "requested_actions": ["parse", "extract_text", "store_job_posting"]
    }
)
```

### Phase 4: Result Aggregation
Collect outputs:
- Profile JSON from `_profile_parser` (if needed)
- Job posting JSON from `_job_posting_parser`
- Validate extraction quality (high/medium/low)

### Phase 5: Cover Letter Generation
Forward aggregated data:
```python
route_to_agent(
    target_agent="_cover_letter_generator",
    message_text={
        "job_posting_result": {...},
        "profile_result": {...},
        "options": {...}
    }
)
```

### Phase 6: Result Presentation
Return structured output to user:

```json
{
    "status": "success",
    "cover_letter": {
        "full_text": "Sehr geehrte Damen und Herren,\n\n...",
        "format": "text",
        "word_count": 342,
        "language": "de"
    },
    "metadata": {
        "job_posting_id": "job_sha256hash",
        "profile_id": "profile_sha256hash",
        "generated_at": "2026-01-21T10:30:00Z",
        "generation_time_ms": 3421
    },
    "quality_metrics": {
        "matched_requirements": [
            "Python",
            "FastAPI",
            "PostgreSQL",
            "Team leadership"
        ],
        "highlighted_skills": [
            "Python (5+ years)",
            "PySide6 UI Development",
            "API Design (REST/GraphQL)",
            "Team Mentoring"
        ],
        "red_flags": [],
        "tone_achieved": "modern",
        "extraction_quality": "high"
    },
    "next_actions": [
        "Download as PDF",
        "Edit and refine",
        "Store in database",
        "Send to recipient"
    ]
}
```

## Error Handling

### Missing Profile
```json
{
    "status": "incomplete",
    "message": "Applicant profile required",
    "required_input": {
        "type": "profile",
        "format": "file path | text | stored profile ID"
    },
    "retry_instruction": "Please provide profile and resubmit"
}
```

### Job Posting Parse Error
```json
{
    "status": "partial_failure",
    "job_posting": {
        "parse_status": "failed",
        "errors": [
            "Could not extract text from PDF"
        ],
        "suggested_action": "Paste job posting text directly"
    },
    "retry_with": {
        "job_posting": {
            "source": "text",
            "value": "<paste text here>"
        }
    }
}
```

### Low Extraction Quality
```json
{
    "status": "success_with_warnings",
    "cover_letter": {...},
    "warnings": [
        "Job posting extraction quality is MEDIUM - some information may be incomplete",
        "Missing salary information",
        "Could not identify hiring manager name - using generic salutation"
    ],
    "quality_metrics": {
        "extraction_quality": "medium",
        "red_flags": [
            "Job title unclear",
            "Company address missing"
        ]
    }
}
```

## Tool Usage

The `_primary_agent` has access to:

| Tool | Purpose |
|------|---------|
| `route_to_agent` | Delegate to specialized agents |
| `load_dispatcher_db` | Check DB for existing profiles/postings |
| `read_document` | Load profile from file system |
| `write_document` | Save final cover letter to file system |

Example tool calls:

### Load stored profile
```python
load_dispatcher_db()
# Returns: { "documents": { "profile_sha256": {...} } }
```

### Route to parser
```python
route_to_agent(
    target_agent="_profile_parser",
    message_text={
        "type": "applicant_profile_file",
        "correlation_id": null,
        "file": {
            "path": "/path/to/cv.pdf",
            "name": "cv.pdf",
            "content_sha256": "..."
        }
    }
)
```

### Save cover letter
```python
write_document(
    content="Sehr geehrte Damen und Herren...",
    path="/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/Cover_letters/letter_001.txt",
    doc_id="letter_sha256",
    filename="cover_letter_TechCorp_2026-01-21.txt"
)
```

## Configuration

### Default Paths
```python
JOB_POSTINGS_DIR = "/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/"
PROFILE_DEFAULT = "/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/applicant_profile.json"
LETTERS_OUTPUT_DIR = "/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/Cover_letters/"
DB_PATH = "/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/ai_ide/AppData/dispatcher_doc_db.json"
```

### Language Support
- `de` (German) - default, full support
- `en` (English) - full support
- Other: Defaults to German with warning

### Tone Options
- `modern` - Dynamic, contemporary phrasing
- `professional` - Traditional, formal tone
- `creative` - Storytelling, personality-driven

## Best Practices

1. **Reuse Profiles**: For multiple applications to the same company, load stored profile (faster)
2. **Validation**: Always review `quality_metrics.red_flags` before sending
3. **Language Consistency**: If job is in German, use `language: "de"` for letter
4. **Tone Matching**: Match company culture (startup = "modern", law firm = "professional")
5. **Proofreading**: Download and review before sending to recruiter

## Performance

Expected execution times:
- Profile parsing: 2-5 seconds
- Job posting parsing: 2-4 seconds
- Cover letter generation: 3-6 seconds
- Total workflow: 5-15 seconds (depending on reuse)

## Troubleshooting

### "Profile not found"
→ Check: `/home/ben/Vs_Code_Projects/Projects/GUI/AI_IDE_v1756/AppData/VSM_4_Data/applicant_profile.json`
→ Provide: file path, text, or stored ID

### "PDF extraction failed"
→ Check: File is readable and valid PDF
→ Retry: Paste text directly (use `source: "text"`)

### "Cover letter is too short/long"
→ Adjust: `options.max_words` (default: 350)
→ Review: Check `quality_metrics.word_count`

### "Wrong tone in letter"
→ Set: `options.tone` ("modern" | "professional" | "creative")
→ Regenerate: Submit new request with corrected tone

## Version
- **Orchestrator Version**: 1.0
- **Last Updated**: 21 January 2026
- **Model**: gpt-4o-mini
