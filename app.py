"""
Job Hunter - AI-Powered CV Generator
A local tool for creating machine-readable CVs with Gemini AI assistance.
"""

import streamlit as st
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from data_manager import (
    load_experiences, save_experiences, get_default_experiences_structure,
    add_work_experience, update_work_experience, delete_work_experience,
    add_education, update_education, delete_education,
    add_project, update_project, delete_project,
    add_certification, update_certification, delete_certification,
    add_award, update_award, delete_award,
    update_contact, update_summary, update_skills,
    load_templates, save_template, update_template, delete_template,
    set_default_template, get_template, get_default_template,
    load_applications, save_application, update_application, delete_application,
    get_application
)
from gemini_client import (
    GeminiClient, create_cv_prompt, create_template_prompt,
    SYSTEM_INSTRUCTION_CV, SYSTEM_INSTRUCTION_TEMPLATE
)
from cv_generator import (
    get_default_template_html, get_default_template_css,
    get_modern_clean_template_html, get_career_progression_template_html,
    fill_template_with_experiences, open_cv_in_browser,
    save_cv_html, extract_html_from_response,
    get_compact_mode_css, get_paginated_preview_css
)

# =============================================================================
# PAGE CONFIG
# =============================================================================

st.set_page_config(
    page_title="Job Hunter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# CUSTOM CSS - Dark Mode
# =============================================================================

st.markdown("""
<style>
    /* Dark theme overrides */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Accent color */
    :root {
        --accent: #00d4aa;
        --accent-dark: #00a080;
        --bg-secondary: #1a1f2e;
        --bg-tertiary: #252b3b;
        --text-primary: #fafafa;
        --text-secondary: #a0a0a0;
        --border-color: #2d3548;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: var(--text-primary) !important;
    }
    
    /* Cards */
    .card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 0.5rem;
    }
    
    .card-title {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
    }
    
    .card-subtitle {
        color: var(--text-secondary);
        font-size: 0.875rem;
    }
    
    /* Status badges */
    .badge {
        display: inline-block;
        padding: 0.25rem 0.5rem;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 500;
    }
    
    .badge-default {
        background: var(--accent);
        color: #000;
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-secondary);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: var(--bg-secondary);
        border-radius: 4px;
        padding: 8px 16px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: var(--accent) !important;
        color: #000 !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
    }
    
    .stButton > button[kind="primary"] {
        background-color: var(--accent);
        color: #000;
    }
    
    /* Text area styling */
    .stTextArea textarea {
        background-color: var(--bg-tertiary);
        border-color: var(--border-color);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--bg-secondary);
        border-radius: 4px;
    }
    
    /* Preview container */
    .preview-container {
        background: #fff;
        border-radius: 8px;
        padding: 1rem;
        max-height: 600px;
        overflow-y: auto;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize session state variables."""
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""
    if "gemini_client" not in st.session_state:
        st.session_state.gemini_client = None
    if "current_cv_html" not in st.session_state:
        st.session_state.current_cv_html = ""
    if "editing_exp_id" not in st.session_state:
        st.session_state.editing_exp_id = None
    if "editing_edu_id" not in st.session_state:
        st.session_state.editing_edu_id = None
    if "editing_proj_id" not in st.session_state:
        st.session_state.editing_proj_id = None
    # Form counters for clearing forms after submission
    if "work_exp_form_key" not in st.session_state:
        st.session_state.work_exp_form_key = 0
    if "edu_form_key" not in st.session_state:
        st.session_state.edu_form_key = 0
    if "proj_form_key" not in st.session_state:
        st.session_state.proj_form_key = 0
    if "cert_form_key" not in st.session_state:
        st.session_state.cert_form_key = 0
    if "award_form_key" not in st.session_state:
        st.session_state.award_form_key = 0
    # Editing state for certifications and awards
    if "editing_cert_id" not in st.session_state:
        st.session_state.editing_cert_id = None
    if "editing_award_id" not in st.session_state:
        st.session_state.editing_award_id = None
    # Template management
    if "editing_template_name" not in st.session_state:
        st.session_state.editing_template_name = None
    if "confirm_delete_template" not in st.session_state:
        st.session_state.confirm_delete_template = None
    # CV display options
    if "cv_compact_mode" not in st.session_state:
        st.session_state.cv_compact_mode = "normal"

init_session_state()

# =============================================================================
# SIDEBAR
# =============================================================================

with st.sidebar:
    st.title("🎯 Job Hunter")
    st.caption("AI-Powered CV Generator")
    
    st.divider()
    
    # API Key input
    st.subheader("🔑 Gemini API Key")
    api_key = st.text_input(
        "Enter your API key",
        type="password",
        value=st.session_state.api_key,
        help="Your API key is stored in session only, never saved to disk."
    )
    
    if api_key != st.session_state.api_key:
        st.session_state.api_key = api_key
        st.session_state.gemini_client = None
    
    if api_key:
        if st.button("Test Connection", use_container_width=True, key="test_api_connection"):
            with st.spinner("Testing..."):
                client = GeminiClient(api_key)
                success, message = client.test_connection()
                if success:
                    st.success(message)
                    st.session_state.gemini_client = client
                else:
                    st.error(message)
    
    st.divider()
    
    # Quick stats
    st.subheader("📊 Your Data")
    experiences = load_experiences()
    templates = load_templates()
    applications = load_applications()
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Experiences", len(experiences.get("work_experiences", [])))
        st.metric("Templates", len(templates.get("templates", [])))
    with col2:
        st.metric("Education", len(experiences.get("education", [])))
        st.metric("Applications", len(applications))
    
    st.divider()
    
    # Model info
    st.subheader("🤖 Models")
    st.caption("**Pro Tasks**: gemini-3-pro-preview")
    st.caption("**Fast Tasks**: gemini-2.0-flash")
    st.caption("Fallback: gemini-2.5-pro")

# =============================================================================
# MAIN CONTENT - TABS
# =============================================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📝 Experience Bank",
    "🎨 Template Editor", 
    "✨ CV Generator",
    "📚 Application History"
])

# =============================================================================
# TAB 1: EXPERIENCE BANK
# =============================================================================

with tab1:
    st.header("Experience Bank")
    st.caption("Store all your experiences, skills, and achievements here. The AI will select the most relevant ones for each application.")
    
    experiences = load_experiences()
    
    # Contact Information
    with st.expander("👤 Contact Information", expanded=True):
        contact = experiences.get("contact", {})
        
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", value=contact.get("name", ""))
            email = st.text_input("Email", value=contact.get("email", ""))
            phone = st.text_input("Phone", value=contact.get("phone", ""))
            location = st.text_input("Location (City, Country)", value=contact.get("location", ""))
        
        with col2:
            linkedin = st.text_input(
                "LinkedIn Username",
                value=contact.get("linkedin", ""),
                placeholder="johndoe",
                help="Just your username, e.g., 'johndoe' → linkedin.com/in/johndoe"
            )
            github = st.text_input(
                "GitHub Username",
                value=contact.get("github", ""),
                placeholder="johndoe",
                help="Just your username, e.g., 'johndoe' → github.com/johndoe"
            )
            website = st.text_input("Website/Portfolio", value=contact.get("website", ""))
        
        if st.button("Save Contact Info", key="save_contact", type="primary"):
            update_contact({
                "name": name, "email": email, "phone": phone,
                "location": location, "linkedin": linkedin,
                "github": github, "website": website
            })
            st.toast("✅ Contact information saved!", icon="👤")
            st.rerun()
    
    # Professional Summary
    with st.expander("📋 Professional Summary"):
        summary = st.text_area(
            "Your professional summary (can be tailored by AI for each application)",
            value=experiences.get("summary", ""),
            height=100
        )
        if st.button("Save Summary", key="save_summary", type="primary"):
            update_summary(summary)
            st.toast("✅ Summary saved!", icon="📋")
            st.rerun()
    
    # Work Experience
    with st.expander("💼 Work Experience", expanded=True):
        work_exps = experiences.get("work_experiences", [])
        
        # Check if we're editing an existing experience
        editing_exp = None
        if st.session_state.editing_exp_id:
            editing_exp = next((e for e in work_exps if e["id"] == st.session_state.editing_exp_id), None)
        
        # Form header changes based on mode
        if editing_exp:
            st.subheader(f"✏️ Editing: {editing_exp['role']} at {editing_exp['company']}")
            if st.button("Cancel Edit", type="secondary", key="cancel_exp_edit"):
                st.session_state.editing_exp_id = None
                st.session_state.work_exp_form_key += 1
                st.rerun()
        else:
            st.subheader("Add New Experience")
        
        # Form with pre-filled values when editing
        with st.form(f"add_work_exp_{st.session_state.work_exp_form_key}"):
            col1, col2 = st.columns(2)
            with col1:
                new_company = st.text_input("Company", value=editing_exp["company"] if editing_exp else "")
                new_role = st.text_input("Role/Title", value=editing_exp["role"] if editing_exp else "")
                new_location = st.text_input("Location", value=editing_exp.get("location", "") if editing_exp else "")
            with col2:
                new_start = st.text_input("Start Date (e.g., Jan 2023)", value=editing_exp["start_date"] if editing_exp else "")
                default_end = editing_exp["end_date"] if editing_exp and editing_exp["end_date"] != "Present" else ""
                new_end = st.text_input("End Date (e.g., Dec 2024)", value=default_end)
                default_current = editing_exp.get("is_current", False) if editing_exp else False
                new_current = st.checkbox("Currently working here", value=default_current)
            
            default_bullets = "\n".join(editing_exp.get("bullets", [])) if editing_exp else ""
            new_bullets = st.text_area(
                "Bullet Points (one per line)",
                value=default_bullets,
                help="Each line becomes a bullet point. Use action verbs and quantify achievements.",
                height=150
            )
            
            button_label = "Update Experience" if editing_exp else "Add Experience"
            if st.form_submit_button(button_label, use_container_width=True, type="primary"):
                if new_company and new_role:
                    bullets = [b.strip() for b in new_bullets.split("\n") if b.strip()]
                    
                    if editing_exp:
                        # Update existing
                        update_work_experience(editing_exp["id"], {
                            "company": new_company,
                            "role": new_role,
                            "start_date": new_start,
                            "end_date": "Present" if new_current else new_end,
                            "location": new_location,
                            "bullets": bullets,
                            "is_current": new_current
                        })
                        st.session_state.editing_exp_id = None
                        st.session_state.work_exp_form_key += 1
                        st.toast(f"✅ Updated experience at {new_company}!", icon="✏️")
                    else:
                        # Add new
                        add_work_experience(
                            company=new_company,
                            role=new_role,
                            start_date=new_start,
                            end_date=new_end if not new_current else "Present",
                            location=new_location,
                            bullets=bullets,
                            is_current=new_current
                        )
                        st.session_state.work_exp_form_key += 1
                        st.toast(f"✅ Added experience at {new_company}!", icon="🎉")
                    st.rerun()
                else:
                    st.error("Company and Role are required.")
        
        # List existing experiences
        st.subheader("Your Experiences")
        for exp in work_exps:
            with st.container():
                # Highlight if currently being edited
                is_editing = st.session_state.editing_exp_id == exp["id"]
                card_style = "border: 2px solid #00d4aa;" if is_editing else ""
                
                st.markdown(f"""
                <div class="card" style="{card_style}">
                    <div class="card-header">
                        <span class="card-title">{exp['role']} at {exp['company']}</span>
                    </div>
                    <div class="card-subtitle">{exp.get('location', '')} | {exp['start_date']} - {exp['end_date']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Bullet points display
                for bullet in exp.get("bullets", []):
                    st.markdown(f"• {bullet}")
                
                col1, col2, col3 = st.columns([1, 1, 4])
                with col1:
                    if st.button("✏️ Edit", key=f"edit_exp_{exp['id']}"):
                        st.session_state.editing_exp_id = exp["id"]
                        st.session_state.work_exp_form_key += 1  # Reset form to load new values
                        st.rerun()
                with col2:
                    if st.button("🗑️ Delete", key=f"del_exp_{exp['id']}"):
                        delete_work_experience(exp['id'])
                        if st.session_state.editing_exp_id == exp["id"]:
                            st.session_state.editing_exp_id = None
                        st.rerun()
                
                st.divider()
    
    # Education
    with st.expander("🎓 Education"):
        edu_list = experiences.get("education", [])
        
        # Check if editing
        editing_edu = None
        if st.session_state.editing_edu_id:
            editing_edu = next((e for e in edu_list if e["id"] == st.session_state.editing_edu_id), None)
        
        if editing_edu:
            st.subheader(f"✏️ Editing: {editing_edu['degree']} at {editing_edu['institution']}")
            if st.button("Cancel Edit", key="cancel_edu_edit", type="secondary"):
                st.session_state.editing_edu_id = None
                st.session_state.edu_form_key += 1
                st.rerun()
        else:
            st.subheader("Add Education")
        
        with st.form(f"add_education_{st.session_state.edu_form_key}"):
            col1, col2 = st.columns(2)
            with col1:
                edu_institution = st.text_input("Institution", value=editing_edu["institution"] if editing_edu else "")
                edu_degree = st.text_input("Degree (e.g., Bachelor's, Master's)", value=editing_edu["degree"] if editing_edu else "")
                edu_field = st.text_input("Field of Study", value=editing_edu.get("field", "") if editing_edu else "")
            with col2:
                edu_start = st.text_input("Start Year", value=editing_edu["start_date"] if editing_edu else "")
                edu_end = st.text_input("End Year (or Expected)", value=editing_edu["end_date"] if editing_edu else "")
                edu_gpa = st.text_input("GPA (optional)", value=editing_edu.get("gpa", "") if editing_edu else "")
            
            default_highlights = "\n".join(editing_edu.get("highlights", [])) if editing_edu else ""
            edu_highlights = st.text_area("Highlights (one per line, optional)", value=default_highlights)
            
            button_label = "Update Education" if editing_edu else "Add Education"
            if st.form_submit_button(button_label, use_container_width=True, type="primary"):
                if edu_institution and edu_degree:
                    highlights = [h.strip() for h in edu_highlights.split("\n") if h.strip()]
                    
                    if editing_edu:
                        update_education(editing_edu["id"], {
                            "institution": edu_institution,
                            "degree": edu_degree,
                            "field": edu_field,
                            "start_date": edu_start,
                            "end_date": edu_end,
                            "gpa": edu_gpa,
                            "highlights": highlights
                        })
                        st.session_state.editing_edu_id = None
                        st.session_state.edu_form_key += 1
                        st.toast("✅ Education updated!", icon="✏️")
                    else:
                        add_education(
                            institution=edu_institution,
                            degree=edu_degree,
                            field=edu_field,
                            start_date=edu_start,
                            end_date=edu_end,
                            gpa=edu_gpa,
                            highlights=highlights
                        )
                        st.session_state.edu_form_key += 1
                        st.toast("✅ Education added!", icon="🎓")
                    st.rerun()
        
        # List education
        for edu in edu_list:
            is_editing = st.session_state.editing_edu_id == edu["id"]
            if is_editing:
                st.markdown(f"**{edu['degree']}** in {edu['field']} — {edu['institution']} 📝")
            else:
                st.markdown(f"**{edu['degree']}** in {edu['field']} — {edu['institution']}")
            st.caption(f"{edu['start_date']} - {edu['end_date']}" + (f" | GPA: {edu['gpa']}" if edu.get('gpa') else ""))
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✏️ Edit", key=f"edit_edu_{edu['id']}"):
                    st.session_state.editing_edu_id = edu["id"]
                    st.session_state.edu_form_key += 1
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_edu_{edu['id']}"):
                    delete_education(edu['id'])
                    if st.session_state.editing_edu_id == edu["id"]:
                        st.session_state.editing_edu_id = None
                    st.rerun()
            st.divider()
    
    # Skills
    with st.expander("🛠️ Skills"):
        skills = experiences.get("skills", {})
        
        col1, col2 = st.columns(2)
        with col1:
            technical = st.text_area(
                "Technical Skills (comma-separated)",
                value=", ".join(skills.get("technical", [])),
                height=100
            )
            tools = st.text_area(
                "Tools & Software (comma-separated)",
                value=", ".join(skills.get("tools", [])),
                height=100
            )
        with col2:
            soft = st.text_area(
                "Soft Skills (comma-separated)",
                value=", ".join(skills.get("soft", [])),
                height=100
            )
            languages = st.text_area(
                "Languages (comma-separated)",
                value=", ".join(skills.get("languages", [])),
                height=100
            )
        
        if st.button("Save Skills", key="save_skills", type="primary"):
            update_skills({
                "technical": [s.strip() for s in technical.split(",") if s.strip()],
                "tools": [s.strip() for s in tools.split(",") if s.strip()],
                "soft": [s.strip() for s in soft.split(",") if s.strip()],
                "languages": [s.strip() for s in languages.split(",") if s.strip()]
            })
            st.toast("✅ Skills saved!", icon="🛠️")
            st.rerun()
    
    # Projects
    with st.expander("🚀 Projects"):
        projects = experiences.get("projects", [])
        
        # Check if editing
        editing_proj = None
        if st.session_state.editing_proj_id:
            editing_proj = next((p for p in projects if p["id"] == st.session_state.editing_proj_id), None)
        
        if editing_proj:
            st.subheader(f"✏️ Editing: {editing_proj['name']}")
            if st.button("Cancel Edit", key="cancel_proj_edit", type="secondary"):
                st.session_state.editing_proj_id = None
                st.session_state.proj_form_key += 1
                st.rerun()
        else:
            st.subheader("Add Project")
        
        with st.form(f"add_project_{st.session_state.proj_form_key}"):
            proj_name = st.text_input("Project Name", value=editing_proj["name"] if editing_proj else "")
            proj_desc = st.text_area("Description", value=editing_proj.get("description", "") if editing_proj else "", height=80)
            default_tech = ", ".join(editing_proj.get("technologies", [])) if editing_proj else ""
            proj_tech = st.text_input("Technologies (comma-separated)", value=default_tech)
            proj_url = st.text_input("URL (optional)", value=editing_proj.get("url", "") if editing_proj else "")
            default_bullets = "\n".join(editing_proj.get("bullets", [])) if editing_proj else ""
            proj_bullets = st.text_area("Key Achievements (one per line)", value=default_bullets)
            
            button_label = "Update Project" if editing_proj else "Add Project"
            if st.form_submit_button(button_label, use_container_width=True, type="primary"):
                if proj_name:
                    bullets = [b.strip() for b in proj_bullets.split("\n") if b.strip()]
                    tech_list = [t.strip() for t in proj_tech.split(",") if t.strip()]
                    
                    if editing_proj:
                        update_project(editing_proj["id"], {
                            "name": proj_name,
                            "description": proj_desc,
                            "technologies": tech_list,
                            "url": proj_url,
                            "bullets": bullets
                        })
                        st.session_state.editing_proj_id = None
                        st.session_state.proj_form_key += 1
                        st.toast("✅ Project updated!", icon="✏️")
                    else:
                        add_project(
                            name=proj_name,
                            description=proj_desc,
                            technologies=tech_list,
                            url=proj_url,
                            bullets=bullets
                        )
                        st.session_state.proj_form_key += 1
                        st.toast("✅ Project added!", icon="🚀")
                    st.rerun()
        
        for proj in projects:
            is_editing = st.session_state.editing_proj_id == proj["id"]
            if is_editing:
                st.markdown(f"**{proj['name']}** 📝")
            else:
                st.markdown(f"**{proj['name']}**")
            st.caption(f"Technologies: {', '.join(proj.get('technologies', []))}")
            st.write(proj.get('description', ''))
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✏️ Edit", key=f"edit_proj_{proj['id']}"):
                    st.session_state.editing_proj_id = proj["id"]
                    st.session_state.proj_form_key += 1
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_proj_{proj['id']}"):
                    delete_project(proj['id'])
                    if st.session_state.editing_proj_id == proj["id"]:
                        st.session_state.editing_proj_id = None
                    st.rerun()
            st.divider()
    
    # Certifications
    with st.expander("📜 Certifications"):
        certs = experiences.get("certifications", [])
        
        # Check if editing
        editing_cert = None
        if st.session_state.editing_cert_id:
            editing_cert = next((c for c in certs if c["id"] == st.session_state.editing_cert_id), None)
        
        if editing_cert:
            st.subheader(f"✏️ Editing: {editing_cert['name']}")
            if st.button("Cancel Edit", key="cancel_cert_edit", type="secondary"):
                st.session_state.editing_cert_id = None
                st.session_state.cert_form_key += 1
                st.rerun()
        else:
            st.subheader("Add Certification")
        
        with st.form(f"add_cert_{st.session_state.cert_form_key}"):
            col1, col2 = st.columns(2)
            with col1:
                cert_name = st.text_input("Certification Name", value=editing_cert["name"] if editing_cert else "")
                cert_issuer = st.text_input("Issuing Organization", value=editing_cert["issuer"] if editing_cert else "")
            with col2:
                cert_date = st.text_input("Date Obtained", value=editing_cert.get("date", "") if editing_cert else "")
                cert_url = st.text_input("Credential URL (optional)", value=editing_cert.get("url", "") if editing_cert else "")
            
            button_label = "Update Certification" if editing_cert else "Add Certification"
            if st.form_submit_button(button_label, use_container_width=True, type="primary"):
                if cert_name and cert_issuer:
                    if editing_cert:
                        update_certification(editing_cert["id"], {
                            "name": cert_name,
                            "issuer": cert_issuer,
                            "date": cert_date,
                            "url": cert_url
                        })
                        st.session_state.editing_cert_id = None
                        st.session_state.cert_form_key += 1
                        st.toast("✅ Certification updated!", icon="✏️")
                    else:
                        add_certification(
                            name=cert_name,
                            issuer=cert_issuer,
                            date=cert_date,
                            url=cert_url
                        )
                        st.session_state.cert_form_key += 1
                        st.toast("✅ Certification added!", icon="📜")
                    st.rerun()
        
        for cert in certs:
            is_editing = st.session_state.editing_cert_id == cert["id"]
            if is_editing:
                st.markdown(f"**{cert['name']}** — {cert['issuer']} ({cert['date']}) 📝")
            else:
                st.markdown(f"**{cert['name']}** — {cert['issuer']} ({cert['date']})")
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✏️ Edit", key=f"edit_cert_{cert['id']}"):
                    st.session_state.editing_cert_id = cert["id"]
                    st.session_state.cert_form_key += 1
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_cert_{cert['id']}"):
                    delete_certification(cert['id'])
                    if st.session_state.editing_cert_id == cert["id"]:
                        st.session_state.editing_cert_id = None
                    st.rerun()
    
    # Awards
    with st.expander("🏆 Awards & Honors"):
        awards = experiences.get("awards", [])
        
        # Check if editing
        editing_award = None
        if st.session_state.editing_award_id:
            editing_award = next((a for a in awards if a["id"] == st.session_state.editing_award_id), None)
        
        if editing_award:
            st.subheader("✏️ Editing Award")
            if st.button("Cancel Edit", key="cancel_award_edit", type="secondary"):
                st.session_state.editing_award_id = None
                st.session_state.award_form_key += 1
                st.rerun()
        else:
            st.subheader("Add Award")
        
        with st.form(f"add_award_{st.session_state.award_form_key}"):
            # Get existing text - handle both old format (name/issuer/date) and new format (text)
            default_text = ""
            if editing_award:
                if "text" in editing_award:
                    default_text = editing_award["text"]
                else:
                    # Convert old format to text
                    parts = [editing_award.get("name", "")]
                    if editing_award.get("issuer"):
                        parts.append(f"— {editing_award['issuer']}")
                    if editing_award.get("date"):
                        parts.append(f"({editing_award['date']})")
                    if editing_award.get("description"):
                        parts.append(f": {editing_award['description']}")
                    default_text = " ".join(parts)
            
            award_text = st.text_area(
                "Award",
                value=default_text,
                height=80,
                placeholder="e.g., Dean's List, Fall 2023 — University of Example\nor: Best Paper Award — ACM Conference 2024 — For research on ML optimization",
                help="Free text format. Include award name, issuing organization, date, and any details you want."
            )
            
            button_label = "Update Award" if editing_award else "Add Award"
            if st.form_submit_button(button_label, use_container_width=True, type="primary"):
                if award_text.strip():
                    if editing_award:
                        update_award(editing_award["id"], award_text.strip())
                        st.session_state.editing_award_id = None
                        st.session_state.award_form_key += 1
                        st.toast("✅ Award updated!", icon="✏️")
                    else:
                        add_award(award_text.strip())
                        st.session_state.award_form_key += 1
                        st.toast("✅ Award added!", icon="🏆")
                    st.rerun()
                else:
                    st.error("Please enter award details.")
        
        # List awards
        for award in awards:
            is_editing = st.session_state.editing_award_id == award["id"]
            
            # Handle both old and new format
            display_text = award.get("text", "")
            if not display_text and award.get("name"):
                # Old format - build display text
                display_text = award["name"]
                if award.get("issuer"):
                    display_text += f" — {award['issuer']}"
                if award.get("date"):
                    display_text += f" ({award['date']})"
            
            if is_editing:
                st.markdown(f"• {display_text} 📝")
            else:
                st.markdown(f"• {display_text}")
            
            if award.get("description") and not award.get("text"):
                st.caption(f"  {award['description']}")
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button("✏️ Edit", key=f"edit_award_{award['id']}"):
                    st.session_state.editing_award_id = award["id"]
                    st.session_state.award_form_key += 1
                    st.rerun()
            with col2:
                if st.button("🗑️ Delete", key=f"del_award_{award['id']}"):
                    delete_award(award['id'])
                    if st.session_state.editing_award_id == award["id"]:
                        st.session_state.editing_award_id = None
                    st.rerun()

# =============================================================================
# TAB 2: TEMPLATE EDITOR
# =============================================================================

with tab2:
    st.header("Template Editor")
    st.caption("Create and manage CV templates. Use AI to generate new templates or edit existing ones.")
    
    templates_data = load_templates()
    templates_list = templates_data.get("templates", [])
    default_id = templates_data.get("default_id")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Your Templates")
        
        # List existing templates first
        if templates_list:
            for template in templates_list:
                is_default = template["id"] == default_id
                badge = " ⭐" if is_default else ""
                
                if st.button(
                    f"{template['name']}{badge}",
                    key=f"select_template_{template['id']}",
                    use_container_width=True
                ):
                    st.session_state.selected_template_id = template["id"]
                    st.rerun()
        else:
            st.caption("No templates yet. Add one below!")
        
        st.divider()
        
        # Built-in templates
        st.subheader("📦 Built-in Templates")
        
        # Check which built-in templates already exist
        existing_names = [t["name"].lower() for t in templates_list]
        
        builtin_templates = [
            {
                "name": "Classic Professional",
                "html_func": get_default_template_html,
                "description": "Clean, ATS-friendly single-column layout. Traditional and professional.",
                "icon": "📄"
            },
            {
                "name": "Modern Clean",
                "html_func": get_modern_clean_template_html,
                "description": "Visually appealing with subtle green accents. Great for human recruiters.",
                "icon": "✨"
            },
            {
                "name": "Career Progression",
                "html_func": get_career_progression_template_html,
                "description": "Groups multiple roles at the same company to showcase growth.",
                "icon": "📈"
            }
        ]
        
        for builtin in builtin_templates:
            if builtin["name"].lower() not in existing_names:
                col_btn, col_info = st.columns([2, 1])
                with col_btn:
                    if st.button(
                        f"{builtin['icon']} Add {builtin['name']}",
                        key=f"add_builtin_{builtin['name']}",
                        use_container_width=True
                    ):
                        template_id = save_template(
                            name=builtin["name"],
                            html_content=builtin["html_func"](),
                            css_content="",
                            description=builtin["description"],
                            set_as_default=len(templates_list) == 0
                        )
                        st.toast(f"✅ Added {builtin['name']}!", icon=builtin["icon"])
                        st.session_state.selected_template_id = template_id
                        st.rerun()
                with col_info:
                    st.caption(builtin["description"][:50] + "...")
        
        # Show if all built-in templates already added
        if all(b["name"].lower() in existing_names for b in builtin_templates):
            st.caption("✓ All built-in templates added")
        
        st.divider()
        
        # Generate new template with AI
        st.subheader("🤖 Generate Template")
        
        style_description = st.text_area(
            "Describe your desired style",
            placeholder="e.g., Minimalist and modern, single column, subtle blue accents, professional but not boring",
            height=100
        )
        
        template_name = st.text_input("Template Name", placeholder="Modern Blue")
        
        if st.button("Generate with AI", use_container_width=True, disabled=not st.session_state.api_key, key="template_generate_ai"):
            if style_description and template_name:
                with st.spinner("Generating template..."):
                    try:
                        client = GeminiClient(st.session_state.api_key)
                        prompt = create_template_prompt(style_description)
                        response = client.generate_flash(prompt, SYSTEM_INSTRUCTION_TEMPLATE)
                        html_content = extract_html_from_response(response)
                        
                        template_id = save_template(
                            name=template_name,
                            html_content=html_content,
                            css_content="",
                            description=style_description,
                            set_as_default=len(templates_list) == 0
                        )
                        st.success(f"Template '{template_name}' created!")
                        st.session_state.selected_template_id = template_id
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error generating template: {e}")
            else:
                st.warning("Please provide both style description and template name.")
        
        if not st.session_state.api_key:
            st.caption("⚠️ Enter API key in sidebar to use AI generation")
    
    with col2:
        st.subheader("Template Preview & Edit")
        
        # Get selected template
        selected_id = st.session_state.get("selected_template_id", default_id)
        selected_template = get_template(selected_id) if selected_id else None
        
        if selected_template:
            is_default = selected_template["id"] == default_id
            
            # Template name with edit capability
            col_name, col_actions = st.columns([2, 1])
            with col_name:
                # Check if we're editing the name
                if st.session_state.get("editing_template_name") == selected_template["id"]:
                    new_name = st.text_input(
                        "Template Name",
                        value=selected_template["name"],
                        key="template_name_input",
                        label_visibility="collapsed"
                    )
                    col_save, col_cancel = st.columns(2)
                    with col_save:
                        if st.button("Save Name", use_container_width=True, type="primary", key="template_save_name"):
                            if new_name.strip():
                                update_template(selected_template["id"], {"name": new_name.strip()})
                                st.session_state.editing_template_name = None
                                st.toast("✅ Template renamed!", icon="✏️")
                                st.rerun()
                    with col_cancel:
                        if st.button("Cancel", use_container_width=True, key="template_cancel_rename"):
                            st.session_state.editing_template_name = None
                            st.rerun()
                else:
                    default_badge = " ⭐" if is_default else ""
                    st.markdown(f"### {selected_template['name']}{default_badge}")
            
            with col_actions:
                if not st.session_state.get("editing_template_name"):
                    if st.button("✏️ Rename", use_container_width=True, key="template_rename"):
                        st.session_state.editing_template_name = selected_template["id"]
                        st.rerun()
            
            # Template management buttons
            col_default, col_delete = st.columns(2)
            with col_default:
                if not is_default:
                    if st.button("⭐ Set as Default", use_container_width=True, key="template_set_default"):
                        set_default_template(selected_template["id"])
                        st.toast("✅ Set as default template!", icon="⭐")
                        st.rerun()
                else:
                    st.caption("✓ Default template")
            with col_delete:
                if st.button("🗑️ Delete Template", use_container_width=True, key="template_delete"):
                    st.session_state.confirm_delete_template = selected_template["id"]
                    st.rerun()
            
            # Delete confirmation
            if st.session_state.get("confirm_delete_template") == selected_template["id"]:
                st.warning(f"Are you sure you want to delete '{selected_template['name']}'?")
                col_yes, col_no = st.columns(2)
                with col_yes:
                    if st.button("Yes, Delete", use_container_width=True, type="primary", key="template_confirm_delete"):
                        delete_template(selected_template["id"])
                        st.session_state.selected_template_id = None
                        st.session_state.confirm_delete_template = None
                        st.toast("✅ Template deleted!", icon="🗑️")
                        st.rerun()
                with col_no:
                    if st.button("Cancel", use_container_width=True, key="cancel_delete"):
                        st.session_state.confirm_delete_template = None
                        st.rerun()
            
            st.divider()
            
            # Edit mode toggle
            edit_mode = st.toggle("Edit HTML", value=False, key="template_edit_mode")
            
            if edit_mode:
                edited_html = st.text_area(
                    "HTML Content",
                    value=selected_template["html"],
                    height=400
                )
                
                if st.button("💾 Save HTML Changes", use_container_width=True, type="primary", key="template_save_html"):
                    update_template(selected_template["id"], {"html": edited_html})
                    st.toast("✅ Template HTML saved!", icon="💾")
                    st.rerun()
            else:
                # Preview with sample data
                experiences = load_experiences()
                preview_html = fill_template_with_experiences(
                    selected_template["html"],
                    experiences
                )
                
                st.components.v1.html(preview_html, height=600, scrolling=True)
                
                if st.button("🌐 Open in Browser", use_container_width=True, key="template_open_browser"):
                    filepath = open_cv_in_browser(preview_html, f"template_preview_{selected_id}.html")
                    st.info(f"Opened in browser. File saved at: {filepath}")
        else:
            st.info("Select a template from the left panel or create a new one.")

# =============================================================================
# TAB 3: CV GENERATOR
# =============================================================================

with tab3:
    st.header("CV Generator")
    st.caption("Paste a job description, add any specific instructions, and let AI create a tailored CV.")
    
    if not st.session_state.api_key:
        st.warning("⚠️ Please enter your Gemini API key in the sidebar to use the CV Generator.")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Job Details")
        
        # Job info
        job_company = st.text_input("Company Name", key="gen_company")
        job_role = st.text_input("Role/Position", key="gen_role")
        
        job_description = st.text_area(
            "Job Description",
            placeholder="Paste the full job description here...",
            height=250
        )
        
        user_instructions = st.text_area(
            "Additional Instructions (optional)",
            placeholder="e.g., Emphasize my Python experience, highlight leadership roles...",
            height=100
        )
        
        # Page length target
        limit_one_page = st.checkbox(
            "📄 Limit to 1 page",
            value=False,
            help="AI will be more concise. Compact mode will be auto-applied."
        )
        
        # Template selection
        templates_data = load_templates()
        templates_list = templates_data.get("templates", [])
        template_options = {t["name"]: t["id"] for t in templates_list}
        
        if template_options:
            selected_template_name = st.selectbox(
                "Select Template",
                options=list(template_options.keys())
            )
            selected_template_id = template_options[selected_template_name]
        else:
            st.warning("No templates found. Please create one in the Template Editor tab.")
            selected_template_id = None
        
        # Generate button
        st.divider()
        
        if st.button("🚀 Generate CV", use_container_width=True, type="primary", disabled=not st.session_state.api_key, key="generate_cv_btn"):
            if job_description and selected_template_id:
                with st.spinner("AI is crafting your CV..."):
                    try:
                        client = GeminiClient(st.session_state.api_key)
                        experiences = load_experiences()
                        template = get_template(selected_template_id)
                        
                        prompt = create_cv_prompt(
                            experiences=experiences,
                            job_description=job_description,
                            user_instructions=user_instructions,
                            template_html=template["html"] if template else "",
                            limit_one_page=limit_one_page
                        )
                        
                        response = client.generate_pro(prompt, SYSTEM_INSTRUCTION_CV)
                        generated_html = extract_html_from_response(response)
                        
                        st.session_state.current_cv_html = generated_html
                        st.session_state.cv_job_company = job_company
                        st.session_state.cv_job_role = job_role
                        st.session_state.cv_job_description = job_description
                        st.session_state.cv_template_id = selected_template_id
                        
                        # Auto-apply compact mode if 1-page limit was requested
                        if limit_one_page:
                            st.session_state.cv_compact_mode = "compact"
                        
                        st.success("CV generated successfully!")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"Error generating CV: {e}")
            else:
                st.warning("Please provide a job description and select a template.")
    
    with col2:
        st.subheader("Generated CV")
        
        if st.session_state.current_cv_html:
            # Display options row
            col_edit, col_compact = st.columns([1, 1])
            with col_edit:
                edit_cv_mode = st.toggle("Edit HTML", value=False, key="edit_cv_toggle")
            with col_compact:
                compact_mode = st.selectbox(
                    "Density",
                    options=["normal", "compact", "very_compact"],
                    format_func=lambda x: {"normal": "📄 Normal", "compact": "📑 Compact", "very_compact": "📃 Very Compact"}[x],
                    key="cv_compact_select",
                    help="Reduce margins and font sizes to fit more content"
                )
                if compact_mode != st.session_state.cv_compact_mode:
                    st.session_state.cv_compact_mode = compact_mode
            
            if edit_cv_mode:
                edited_cv = st.text_area(
                    "Edit CV HTML",
                    value=st.session_state.current_cv_html,
                    height=400
                )
                if st.button("Apply Changes", key="apply_cv_changes"):
                    st.session_state.current_cv_html = edited_cv
                    st.success("Changes applied!")
                    st.rerun()
            else:
                # Preview with compact mode and page simulation
                preview_html = st.session_state.current_cv_html
                
                # Inject compact mode CSS if not normal
                if st.session_state.cv_compact_mode != "normal":
                    compact_css = get_compact_mode_css(st.session_state.cv_compact_mode)
                    if '</head>' in preview_html:
                        preview_html = preview_html.replace('</head>', compact_css + '</head>')
                    elif '</body>' in preview_html:
                        preview_html = preview_html.replace('</body>', compact_css + '</body>')
                
                # Add page preview styling
                page_preview_css = get_paginated_preview_css()
                if '</head>' in preview_html:
                    preview_html = preview_html.replace('</head>', page_preview_css + '</head>')
                elif '</body>' in preview_html:
                    preview_html = preview_html.replace('</body>', page_preview_css + '</body>')
                
                # Show preview
                st.components.v1.html(
                    preview_html,
                    height=700,
                    scrolling=True
                )
                st.caption("📄 Preview shows approximate page layout. Use 'Open in Browser' for accurate print preview.")
            
            # Action buttons
            st.divider()
            col_a, col_b, col_c = st.columns(3)
            
            with col_a:
                if st.button("🌐 Open in Browser", use_container_width=True, key="cv_open_browser"):
                    # Apply compact mode when opening in browser too
                    final_html = st.session_state.current_cv_html
                    if st.session_state.cv_compact_mode != "normal":
                        compact_css = get_compact_mode_css(st.session_state.cv_compact_mode)
                        if '</head>' in final_html:
                            final_html = final_html.replace('</head>', compact_css + '</head>')
                        elif '</body>' in final_html:
                            final_html = final_html.replace('</body>', compact_css + '</body>')
                    filepath = open_cv_in_browser(final_html)
                    st.info(f"Opened! Use browser's Print → Save as PDF")
            
            with col_b:
                if st.button("💾 Save Application", use_container_width=True, key="cv_save_app"):
                    company = st.session_state.get("cv_job_company", "Unknown")
                    role = st.session_state.get("cv_job_role", "Unknown")
                    jd = st.session_state.get("cv_job_description", "")
                    template_id = st.session_state.get("cv_template_id", "")
                    
                    # Save with compact mode applied
                    final_html = st.session_state.current_cv_html
                    if st.session_state.cv_compact_mode != "normal":
                        compact_css = get_compact_mode_css(st.session_state.cv_compact_mode)
                        if '</head>' in final_html:
                            final_html = final_html.replace('</head>', compact_css + '</head>')
                        elif '</body>' in final_html:
                            final_html = final_html.replace('</body>', compact_css + '</body>')
                    
                    app_id = save_application(
                        company=company,
                        role=role,
                        job_description=jd,
                        generated_html=final_html,
                        template_id=template_id
                    )
                    st.success(f"Application saved! ID: {app_id}")
            
            with col_c:
                if st.button("🔄 Regenerate", use_container_width=True, key="cv_regenerate"):
                    st.session_state.current_cv_html = ""
                    st.session_state.cv_compact_mode = "normal"
                    st.rerun()
        else:
            st.info("Fill in the job details and click 'Generate CV' to create your tailored CV.")
            
            # Show preview of what's in experience bank
            st.divider()
            st.caption("**Experience Bank Preview:**")
            experiences = load_experiences()
            
            work_count = len(experiences.get("work_experiences", []))
            edu_count = len(experiences.get("education", []))
            skills_count = sum(len(v) for v in experiences.get("skills", {}).values())
            
            st.markdown(f"""
            - 💼 **{work_count}** work experiences
            - 🎓 **{edu_count}** education entries
            - 🛠️ **{skills_count}** skills
            """)
            
            if work_count == 0:
                st.warning("⚠️ Add some experiences in the Experience Bank tab first!")

# =============================================================================
# TAB 4: APPLICATION HISTORY
# =============================================================================

with tab4:
    st.header("Application History")
    st.caption("Track all your job applications and their generated CVs.")
    
    applications = load_applications()
    
    if not applications:
        st.info("No applications yet. Generate a CV and save it to start tracking!")
    else:
        # Search/filter
        search = st.text_input("🔍 Search applications", placeholder="Company or role...")
        
        filtered = applications
        if search:
            search_lower = search.lower()
            filtered = [
                app for app in applications
                if search_lower in app.get("company", "").lower()
                or search_lower in app.get("role", "").lower()
            ]
        
        st.caption(f"Showing {len(filtered)} of {len(applications)} applications")
        
        for app in filtered:
            with st.expander(
                f"**{app.get('company', 'Unknown')}** — {app.get('role', 'Unknown Role')} "
                f"({app.get('created_at', '')[:10]})"
            ):
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    st.markdown("**Job Description:**")
                    st.text_area(
                        "JD",
                        value=app.get("job_description", ""),
                        height=150,
                        key=f"jd_{app['id']}",
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    
                    # Status update
                    status_options = ["created", "applied", "interviewing", "rejected", "offer"]
                    current_status = app.get("status", "created")
                    new_status = st.selectbox(
                        "Status",
                        options=status_options,
                        index=status_options.index(current_status) if current_status in status_options else 0,
                        key=f"status_{app['id']}"
                    )
                    
                    if new_status != current_status:
                        if st.button("Update Status", key=f"update_status_{app['id']}"):
                            update_application(app["id"], {"status": new_status})
                            st.success("Status updated!")
                            st.rerun()
                
                with col2:
                    st.markdown("**Generated CV Preview:**")
                    if app.get("generated_html"):
                        st.components.v1.html(
                            app["generated_html"],
                            height=300,
                            scrolling=True
                        )
                        
                        if st.button("🌐 Open in Browser", key=f"open_{app['id']}"):
                            filepath = open_cv_in_browser(
                                app["generated_html"],
                                f"cv_{app['company']}_{app['id']}.html"
                            )
                            st.info("Opened in browser!")
                
                # Notes
                notes = st.text_area(
                    "Notes",
                    value=app.get("notes", ""),
                    key=f"notes_{app['id']}",
                    placeholder="Add notes about this application..."
                )
                
                col_a, col_b = st.columns([1, 5])
                with col_a:
                    if st.button("Save Notes", key=f"save_notes_{app['id']}"):
                        update_application(app["id"], {"notes": notes})
                        st.success("Notes saved!")
                
                with col_b:
                    if st.button("🗑️ Delete Application", key=f"delete_app_{app['id']}"):
                        delete_application(app["id"])
                        st.success("Application deleted!")
                        st.rerun()
