"""
Gemini API Client with model fallback support
Primary: gemini-3-pro-preview
Fallback: gemini-2.5-pro
Fast/Cheap: gemini-2.0-flash
"""

import google.generativeai as genai
from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configurations
MODELS = {
    "pro": {
        "primary": "gemini-3-pro-preview",
        "fallback": "gemini-2.5-pro"
    },
    "flash": "gemini-2.0-flash"
}


class GeminiClient:
    """Gemini API client with automatic fallback."""
    
    def __init__(self, api_key: str):
        """Initialize the client with API key."""
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self._pro_model = None
        self._flash_model = None
    
    def _get_pro_model(self):
        """Get or create pro model with fallback."""
        if self._pro_model is None:
            # Try primary model first
            try:
                self._pro_model = genai.GenerativeModel(MODELS["pro"]["primary"])
                # Test the model with a simple request
                logger.info(f"Using primary model: {MODELS['pro']['primary']}")
            except Exception as e:
                logger.warning(f"Primary model unavailable: {e}. Falling back...")
                self._pro_model = genai.GenerativeModel(MODELS["pro"]["fallback"])
                logger.info(f"Using fallback model: {MODELS['pro']['fallback']}")
        return self._pro_model
    
    def _get_flash_model(self):
        """Get or create flash model."""
        if self._flash_model is None:
            self._flash_model = genai.GenerativeModel(MODELS["flash"])
        return self._flash_model
    
    def generate_pro(self, prompt: str, system_instruction: str = None) -> str:
        """
        Generate content using the pro model (with fallback).
        Use for: CV generation, content assessment, final polish.
        """
        model = self._get_pro_model()
        
        try:
            if system_instruction:
                model = genai.GenerativeModel(
                    model_name=model.model_name,
                    system_instruction=system_instruction
                )
            
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            # If primary fails during generation, try fallback
            if MODELS["pro"]["primary"] in str(model.model_name):
                logger.warning(f"Primary model failed: {e}. Trying fallback...")
                self._pro_model = genai.GenerativeModel(MODELS["pro"]["fallback"])
                if system_instruction:
                    fallback = genai.GenerativeModel(
                        model_name=MODELS["pro"]["fallback"],
                        system_instruction=system_instruction
                    )
                else:
                    fallback = self._pro_model
                response = fallback.generate_content(prompt)
                return response.text
            raise
    
    def generate_flash(self, prompt: str, system_instruction: str = None) -> str:
        """
        Generate content using the flash model.
        Use for: Quick drafts, template generation, previews.
        """
        model = self._flash_model
        
        if model is None or system_instruction:
            model = genai.GenerativeModel(
                model_name=MODELS["flash"],
                system_instruction=system_instruction
            ) if system_instruction else self._get_flash_model()
        
        response = model.generate_content(prompt)
        return response.text
    
    def test_connection(self) -> tuple[bool, str]:
        """Test API connection and return (success, message)."""
        try:
            model = genai.GenerativeModel(MODELS["flash"])
            response = model.generate_content("Say 'API Connected' in exactly 2 words.")
            return True, f"Connected successfully. Response: {response.text.strip()}"
        except Exception as e:
            return False, f"Connection failed: {str(e)}"


# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

SYSTEM_INSTRUCTION_CV = """You are an expert CV/resume writer specializing in ATS-optimized, 
machine-readable resumes for tech professionals. You understand modern 2026 hiring practices.

Your writing style:
- Concise, action-oriented bullet points
- Quantified achievements where possible
- Industry-relevant keywords naturally integrated
- Professional yet personable tone

Format requirements:
- Output clean, semantic HTML only (no markdown)
- Use proper heading hierarchy (h1, h2, h3)
- Use <section> tags for major sections
- Use <ul> and <li> for bullet points
- No tables for layout
- Include appropriate CSS classes for styling

Content ordering rules:
- Experience MUST be ordered from newest/latest to oldest (reverse chronological)
- Group multiple roles at the same company together under one company heading
- Education should also be reverse chronological

Link display rules (MUST follow exactly):
- LinkedIn: href="https://www.linkedin.com/in/USERNAME" with display text "linkedin.com/in/USERNAME"
- GitHub: href="https://github.com/USERNAME" with display text "github.com/USERNAME"
- Do NOT use generic text like "LinkedIn" or "GitHub" - always show the readable URL path
- Do NOT modify or override these link formats - they are provided pre-formatted
"""

SYSTEM_INSTRUCTION_TEMPLATE = """You are a professional web designer specializing in 
CV/resume templates. You create clean, ATS-friendly, modern templates.

Requirements:
- Single-column layout (ATS-friendly)
- Clean typography
- Semantic HTML5
- Print-friendly CSS
- Placeholder sections using {{PLACEHOLDER}} syntax
- Professional appearance suitable for tech industry

Content ordering rules (build template structure to support):
- Experience section should display newest/latest first (reverse chronological)
- Template should allow grouping multiple roles under one company
- Education should also be reverse chronological

Link display rules (MUST follow exactly):
- LinkedIn format: <a href="https://www.linkedin.com/in/USERNAME">linkedin.com/in/USERNAME</a>
- GitHub format: <a href="https://github.com/USERNAME">github.com/USERNAME</a>
- Do NOT use generic text like "LinkedIn" or "GitHub" - always show the readable URL path
- The {{CONTACT_LINKS}} placeholder will be pre-formatted - do NOT modify link formats
"""


def create_cv_prompt(
    experiences: dict,
    job_description: str,
    user_instructions: str = "",
    template_html: str = "",
    limit_one_page: bool = False
) -> str:
    """Create the prompt for CV generation."""
    
    # Format experiences into readable text
    exp_text = _format_experiences(experiences)
    
    # Page length guidance
    if limit_one_page:
        page_guidance = """STRICT 1-PAGE LIMIT:
- Be highly concise - this CV MUST fit on a single page
- Use 2-3 bullet points per role maximum
- Focus only on the most impactful achievements
- Keep descriptions brief but powerful
- Omit less relevant experiences entirely"""
    else:
        page_guidance = """PAGE LENGTH:
- Target 1-2 pages
- Include comprehensive details for relevant experiences
- 3-5 bullet points per role is acceptable"""
    
    prompt = f"""Based on the candidate's experience and the target job description, 
create a tailored CV that highlights the most relevant qualifications.

## CANDIDATE'S FULL EXPERIENCE BANK:
{exp_text}

## TARGET JOB DESCRIPTION:
{job_description}

## ADDITIONAL INSTRUCTIONS FROM USER:
{user_instructions if user_instructions else "None provided."}

## {page_guidance}

## TASK:
1. Select the most relevant experiences, skills, and achievements for this specific role
2. Tailor bullet points to match the job requirements
3. Optimize for ATS keyword matching
4. Use professional, impactful language

"""
    
    if template_html:
        prompt += f"""
## TEMPLATE TO USE:
Fill in this template structure, replacing placeholders with tailored content:

{template_html}

Output the complete HTML with all placeholders filled in.
"""
    else:
        prompt += """
## OUTPUT FORMAT:
Generate complete, valid HTML for the CV. Include embedded CSS in a <style> tag.
Use semantic HTML5 elements. Make it print-friendly.
"""
    
    return prompt


def create_template_prompt(style_description: str) -> str:
    """Create the prompt for template generation."""
    
    return f"""Create a CV/resume HTML template based on this style description:

{style_description}

Requirements:
1. Use semantic HTML5 (<header>, <section>, <article>)
2. Single-column layout for ATS compatibility
3. Clean, professional appearance
4. Print-friendly (white background, dark text)
5. Include embedded CSS in a <style> tag

Use these exact placeholders for content sections:
- {{{{CONTACT_NAME}}}} - Full name
- {{{{CONTACT_EMAIL}}}} - Email address
- {{{{CONTACT_PHONE}}}} - Phone number
- {{{{CONTACT_LOCATION}}}} - City, Country
- {{{{CONTACT_LINKEDIN}}}} - LinkedIn URL
- {{{{CONTACT_GITHUB}}}} - GitHub URL
- {{{{SUMMARY}}}} - Professional summary paragraph
- {{{{EXPERIENCE}}}} - Work experience section (will be filled with HTML)
- {{{{EDUCATION}}}} - Education section (will be filled with HTML)
- {{{{SKILLS}}}} - Skills section (will be filled with HTML)
- {{{{PROJECTS}}}} - Projects section (will be filled with HTML)
- {{{{CERTIFICATIONS}}}} - Certifications section (will be filled with HTML)
- {{{{AWARDS}}}} - Awards & honors section (will be filled with HTML)

Output only the HTML template, nothing else.
"""


def _format_experiences(experiences: dict) -> str:
    """Format experiences dict into readable text for the prompt."""
    
    lines = []
    
    # Contact
    contact = experiences.get("contact", {})
    if any(contact.values()):
        lines.append("### CONTACT INFORMATION:")
        for key, value in contact.items():
            if value:
                lines.append(f"- {key.title()}: {value}")
        lines.append("")
    
    # Summary
    if experiences.get("summary"):
        lines.append("### PROFESSIONAL SUMMARY:")
        lines.append(experiences["summary"])
        lines.append("")
    
    # Work Experience
    work = experiences.get("work_experiences", [])
    if work:
        lines.append("### WORK EXPERIENCE:")
        for exp in work:
            lines.append(f"\n**{exp['role']}** at **{exp['company']}**")
            lines.append(f"   {exp.get('location', '')} | {exp['start_date']} - {exp['end_date']}")
            for bullet in exp.get("bullets", []):
                lines.append(f"   • {bullet}")
        lines.append("")
    
    # Education
    education = experiences.get("education", [])
    if education:
        lines.append("### EDUCATION:")
        for edu in education:
            lines.append(f"\n**{edu['degree']}** in {edu['field']}")
            lines.append(f"   {edu['institution']} | {edu['start_date']} - {edu['end_date']}")
            if edu.get("gpa"):
                lines.append(f"   GPA: {edu['gpa']}")
            for highlight in edu.get("highlights", []):
                lines.append(f"   • {highlight}")
        lines.append("")
    
    # Skills
    skills = experiences.get("skills", {})
    if any(skills.values()):
        lines.append("### SKILLS:")
        for category, skill_list in skills.items():
            if skill_list:
                lines.append(f"   {category.title()}: {', '.join(skill_list)}")
        lines.append("")
    
    # Projects
    projects = experiences.get("projects", [])
    if projects:
        lines.append("### PROJECTS:")
        for proj in projects:
            lines.append(f"\n**{proj['name']}**")
            lines.append(f"   {proj['description']}")
            if proj.get("technologies"):
                lines.append(f"   Technologies: {', '.join(proj['technologies'])}")
            for bullet in proj.get("bullets", []):
                lines.append(f"   • {bullet}")
        lines.append("")
    
    # Certifications
    certs = experiences.get("certifications", [])
    if certs:
        lines.append("### CERTIFICATIONS:")
        for cert in certs:
            lines.append(f"   • {cert['name']} - {cert['issuer']} ({cert['date']})")
        lines.append("")
    
    # Awards
    awards = experiences.get("awards", [])
    if awards:
        lines.append("### AWARDS & HONORS:")
        for award in awards:
            # Handle both new format (text) and old format (name/issuer/date)
            if award.get("text"):
                lines.append(f"   • {award['text']}")
            else:
                desc = f" - {award['description']}" if award.get('description') else ""
                lines.append(f"   • {award.get('name', '')} - {award.get('issuer', '')} ({award.get('date', '')}){desc}")
        lines.append("")
    
    return "\n".join(lines)
