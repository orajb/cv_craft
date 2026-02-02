"""
Data Manager - CRUD operations for JSON-based storage
Handles experiences, templates, and application history
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional
import uuid


# Data directory path
DATA_DIR = Path(__file__).parent.parent / "data"


def _ensure_data_dir():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def _load_json(filename: str) -> dict:
    """Load JSON file, return empty structure if doesn't exist."""
    filepath = DATA_DIR / filename
    if filepath.exists():
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def _save_json(filename: str, data: dict):
    """Save data to JSON file."""
    _ensure_data_dir()
    filepath = DATA_DIR / filename
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


# =============================================================================
# EXPERIENCES
# =============================================================================

EXPERIENCES_FILE = "experiences.json"


def get_default_experiences_structure() -> dict:
    """Return default structure for experiences."""
    return {
        "contact": {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "website": ""
        },
        "summary": "",
        "work_experiences": [],
        "education": [],
        "skills": {
            "technical": [],
            "soft": [],
            "languages": [],
            "tools": []
        },
        "projects": [],
        "certifications": [],
        "awards": [],
        "other": []
    }


def load_experiences() -> dict:
    """Load all experiences from storage."""
    data = _load_json(EXPERIENCES_FILE)
    if not data:
        data = get_default_experiences_structure()
        _save_json(EXPERIENCES_FILE, data)
    return data


def save_experiences(data: dict):
    """Save all experiences to storage."""
    _save_json(EXPERIENCES_FILE, data)


def add_work_experience(
    company: str,
    role: str,
    start_date: str,
    end_date: str,
    location: str,
    bullets: list[str],
    is_current: bool = False
) -> str:
    """Add a work experience entry. Returns the ID."""
    data = load_experiences()
    exp_id = str(uuid.uuid4())[:8]
    
    data["work_experiences"].append({
        "id": exp_id,
        "company": company,
        "role": role,
        "start_date": start_date,
        "end_date": end_date if not is_current else "Present",
        "location": location,
        "bullets": bullets,
        "is_current": is_current,
        "created_at": datetime.now().isoformat()
    })
    
    save_experiences(data)
    return exp_id


def update_work_experience(exp_id: str, updates: dict):
    """Update a work experience entry."""
    data = load_experiences()
    for exp in data["work_experiences"]:
        if exp["id"] == exp_id:
            exp.update(updates)
            exp["updated_at"] = datetime.now().isoformat()
            break
    save_experiences(data)


def delete_work_experience(exp_id: str):
    """Delete a work experience entry."""
    data = load_experiences()
    data["work_experiences"] = [
        exp for exp in data["work_experiences"] if exp["id"] != exp_id
    ]
    save_experiences(data)


def add_education(
    institution: str,
    degree: str,
    field: str,
    start_date: str,
    end_date: str,
    gpa: str = "",
    highlights: list[str] = None
) -> str:
    """Add an education entry. Returns the ID."""
    data = load_experiences()
    edu_id = str(uuid.uuid4())[:8]
    
    data["education"].append({
        "id": edu_id,
        "institution": institution,
        "degree": degree,
        "field": field,
        "start_date": start_date,
        "end_date": end_date,
        "gpa": gpa,
        "highlights": highlights or [],
        "created_at": datetime.now().isoformat()
    })
    
    save_experiences(data)
    return edu_id


def update_education(edu_id: str, updates: dict):
    """Update an education entry."""
    data = load_experiences()
    for edu in data["education"]:
        if edu["id"] == edu_id:
            edu.update(updates)
            edu["updated_at"] = datetime.now().isoformat()
            break
    save_experiences(data)


def delete_education(edu_id: str):
    """Delete an education entry."""
    data = load_experiences()
    data["education"] = [
        edu for edu in data["education"] if edu["id"] != edu_id
    ]
    save_experiences(data)


def add_project(
    name: str,
    description: str,
    technologies: list[str],
    url: str = "",
    bullets: list[str] = None
) -> str:
    """Add a project entry. Returns the ID."""
    data = load_experiences()
    proj_id = str(uuid.uuid4())[:8]
    
    data["projects"].append({
        "id": proj_id,
        "name": name,
        "description": description,
        "technologies": technologies,
        "url": url,
        "bullets": bullets or [],
        "created_at": datetime.now().isoformat()
    })
    
    save_experiences(data)
    return proj_id


def update_project(proj_id: str, updates: dict):
    """Update a project entry."""
    data = load_experiences()
    for proj in data["projects"]:
        if proj["id"] == proj_id:
            proj.update(updates)
            proj["updated_at"] = datetime.now().isoformat()
            break
    save_experiences(data)


def delete_project(proj_id: str):
    """Delete a project entry."""
    data = load_experiences()
    data["projects"] = [
        proj for proj in data["projects"] if proj["id"] != proj_id
    ]
    save_experiences(data)


def add_certification(
    name: str,
    issuer: str,
    date: str,
    url: str = "",
    expiry: str = ""
) -> str:
    """Add a certification entry. Returns the ID."""
    data = load_experiences()
    cert_id = str(uuid.uuid4())[:8]
    
    data["certifications"].append({
        "id": cert_id,
        "name": name,
        "issuer": issuer,
        "date": date,
        "url": url,
        "expiry": expiry,
        "created_at": datetime.now().isoformat()
    })
    
    save_experiences(data)
    return cert_id


def update_certification(cert_id: str, updates: dict):
    """Update a certification entry."""
    data = load_experiences()
    for cert in data["certifications"]:
        if cert["id"] == cert_id:
            cert.update(updates)
            cert["updated_at"] = datetime.now().isoformat()
            break
    save_experiences(data)


def delete_certification(cert_id: str):
    """Delete a certification entry."""
    data = load_experiences()
    data["certifications"] = [
        cert for cert in data["certifications"] if cert["id"] != cert_id
    ]
    save_experiences(data)


def add_award(text: str) -> str:
    """Add an award entry (free text). Returns the ID."""
    data = load_experiences()
    
    # Ensure awards list exists (for existing data files)
    if "awards" not in data:
        data["awards"] = []
    
    award_id = str(uuid.uuid4())[:8]
    
    data["awards"].append({
        "id": award_id,
        "text": text,
        "created_at": datetime.now().isoformat()
    })
    
    save_experiences(data)
    return award_id


def update_award(award_id: str, text: str):
    """Update an award entry."""
    data = load_experiences()
    if "awards" not in data:
        data["awards"] = []
    for award in data["awards"]:
        if award["id"] == award_id:
            award["text"] = text
            award["updated_at"] = datetime.now().isoformat()
            break
    save_experiences(data)


def delete_award(award_id: str):
    """Delete an award entry."""
    data = load_experiences()
    if "awards" in data:
        data["awards"] = [
            award for award in data["awards"] if award["id"] != award_id
        ]
    save_experiences(data)


def update_contact(contact_data: dict):
    """Update contact information."""
    data = load_experiences()
    data["contact"].update(contact_data)
    save_experiences(data)


def update_summary(summary: str):
    """Update professional summary."""
    data = load_experiences()
    data["summary"] = summary
    save_experiences(data)


def update_skills(skills_data: dict):
    """Update skills section."""
    data = load_experiences()
    data["skills"].update(skills_data)
    save_experiences(data)


# =============================================================================
# TEMPLATES
# =============================================================================

TEMPLATES_FILE = "templates.json"


def load_templates() -> dict:
    """Load all CV templates."""
    data = _load_json(TEMPLATES_FILE)
    if not data:
        data = {"templates": [], "default_id": None}
        _save_json(TEMPLATES_FILE, data)
    return data


def save_template(
    name: str,
    html_content: str,
    css_content: str,
    description: str = "",
    set_as_default: bool = False
) -> str:
    """Save a CV template. Returns the ID."""
    data = load_templates()
    template_id = str(uuid.uuid4())[:8]
    
    template = {
        "id": template_id,
        "name": name,
        "description": description,
        "html": html_content,
        "css": css_content,
        "created_at": datetime.now().isoformat()
    }
    
    data["templates"].append(template)
    
    if set_as_default or data["default_id"] is None:
        data["default_id"] = template_id
    
    _save_json(TEMPLATES_FILE, data)
    return template_id


def update_template(template_id: str, updates: dict):
    """Update an existing template."""
    data = load_templates()
    for template in data["templates"]:
        if template["id"] == template_id:
            template.update(updates)
            template["updated_at"] = datetime.now().isoformat()
            break
    _save_json(TEMPLATES_FILE, data)


def delete_template(template_id: str):
    """Delete a template."""
    data = load_templates()
    data["templates"] = [t for t in data["templates"] if t["id"] != template_id]
    
    # Reset default if deleted
    if data["default_id"] == template_id:
        data["default_id"] = data["templates"][0]["id"] if data["templates"] else None
    
    _save_json(TEMPLATES_FILE, data)


def set_default_template(template_id: str):
    """Set a template as the default."""
    data = load_templates()
    data["default_id"] = template_id
    _save_json(TEMPLATES_FILE, data)


def get_template(template_id: str) -> Optional[dict]:
    """Get a specific template by ID."""
    data = load_templates()
    for template in data["templates"]:
        if template["id"] == template_id:
            return template
    return None


def get_default_template() -> Optional[dict]:
    """Get the default template."""
    data = load_templates()
    if data["default_id"]:
        return get_template(data["default_id"])
    return None


# =============================================================================
# APPLICATIONS
# =============================================================================

APPLICATIONS_FILE = "applications.json"


def load_applications() -> list:
    """Load all application history."""
    data = _load_json(APPLICATIONS_FILE)
    if not data:
        data = {"applications": []}
        _save_json(APPLICATIONS_FILE, data)
    return data.get("applications", [])


def save_application(
    company: str = "Untitled Focus",
    role: str = "General",
    job_description: str = "",
    generated_html: str = "",
    template_id: str = "",
    notes: str = "",
    status: str = "created",
    role_url: str = ""
) -> str:
    """Save an application entry. Returns the ID."""
    data = _load_json(APPLICATIONS_FILE)
    if not data:
        data = {"applications": []}
    
    app_id = str(uuid.uuid4())[:8]
    
    application = {
        "id": app_id,
        "company": company or "Untitled Focus",
        "role": role or "General",
        "job_description": job_description,
        "generated_html": generated_html,
        "template_id": template_id,
        "notes": notes,
        "status": status,
        "role_url": role_url,
        "created_at": datetime.now().isoformat()
    }
    
    data["applications"].insert(0, application)  # Most recent first
    _save_json(APPLICATIONS_FILE, data)
    return app_id


def save_or_update_draft(
    company: str = "Untitled Focus",
    role: str = "General",
    job_description: str = "",
    generated_html: str = "",
    template_id: str = "",
    existing_draft_id: str = None,
    role_url: str = ""
) -> str:
    """Save a new draft or update existing draft. Returns the draft ID."""
    data = _load_json(APPLICATIONS_FILE)
    if not data:
        data = {"applications": []}
    
    # If we have an existing draft ID, update it
    if existing_draft_id:
        for app in data.get("applications", []):
            if app["id"] == existing_draft_id and app.get("status") == "draft":
                app["company"] = company or "Untitled Focus"
                app["role"] = role or "General"
                app["job_description"] = job_description
                app["generated_html"] = generated_html
                app["template_id"] = template_id
                app["role_url"] = role_url
                app["updated_at"] = datetime.now().isoformat()
                _save_json(APPLICATIONS_FILE, data)
                return existing_draft_id
    
    # Create new draft
    return save_application(
        company=company,
        role=role,
        job_description=job_description,
        generated_html=generated_html,
        template_id=template_id,
        status="draft",
        role_url=role_url
    )


def update_application(app_id: str, updates: dict):
    """Update an application entry."""
    data = _load_json(APPLICATIONS_FILE)
    for app in data.get("applications", []):
        if app["id"] == app_id:
            app.update(updates)
            app["updated_at"] = datetime.now().isoformat()
            break
    _save_json(APPLICATIONS_FILE, data)


def delete_application(app_id: str):
    """Delete an application entry."""
    data = _load_json(APPLICATIONS_FILE)
    data["applications"] = [
        app for app in data.get("applications", []) if app["id"] != app_id
    ]
    _save_json(APPLICATIONS_FILE, data)


def get_application(app_id: str) -> Optional[dict]:
    """Get a specific application by ID."""
    applications = load_applications()
    for app in applications:
        if app["id"] == app_id:
            return app
    return None
