"""
AI Client with support for both Google Gemini and Anthropic Claude APIs.
Automatically detects which API key is provided and uses the appropriate backend.

Gemini Models:
- Pro (expensive): gemini-3-pro-preview → fallback: gemini-2.5-pro
- Flash (cheap): gemini-2.0-flash

Claude Models:
- Pro (expensive): claude-sonnet-4-20250514
- Flash (cheap): claude-3-5-haiku-20241022
"""

from typing import Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Model configurations
GEMINI_MODELS = {
    "pro": {
        "primary": "gemini-3-pro-preview",
        "fallback": "gemini-2.5-pro"
    },
    "flash": "gemini-2.0-flash"
}

CLAUDE_MODELS = {
    "pro": "claude-sonnet-4-20250514",
    "flash": "claude-3-5-haiku-20241022"
}


def detect_api_provider(api_key: str) -> str:
    """Detect whether the API key is for Gemini or Claude."""
    if not api_key:
        return "unknown"
    
    # Claude API keys typically start with "sk-ant-"
    if api_key.startswith("sk-ant-"):
        return "claude"
    
    # Gemini API keys typically start with "AI" and are ~39 characters
    if api_key.startswith("AI") and len(api_key) > 30:
        return "gemini"
    
    # Default to gemini for other patterns (older key formats)
    # Could also try to make a test call, but that uses tokens
    return "gemini"


class AIClient:
    """Unified AI client supporting both Gemini and Claude APIs."""
    
    def __init__(self, api_key: str):
        """Initialize the client with API key. Automatically detects provider."""
        self.api_key = api_key
        self.provider = detect_api_provider(api_key)
        self._initialized = False
        self._client = None
        
        logger.info(f"AI Client initialized with provider: {self.provider}")
    
    def _init_gemini(self):
        """Initialize Gemini client."""
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self._genai = genai
        self._initialized = True
    
    def _init_claude(self):
        """Initialize Claude client."""
        import anthropic
        self._client = anthropic.Anthropic(api_key=self.api_key)
        self._initialized = True
    
    def _ensure_initialized(self):
        """Ensure the appropriate client is initialized."""
        if self._initialized:
            return
        
        if self.provider == "claude":
            self._init_claude()
        else:
            self._init_gemini()
    
    def generate_pro(self, prompt: str, system_instruction: str = None) -> str:
        """
        Generate content using the expensive/pro model.
        Use for: CV generation, content assessment, final polish.
        """
        self._ensure_initialized()
        
        if self.provider == "claude":
            return self._claude_generate(prompt, system_instruction, model=CLAUDE_MODELS["pro"])
        else:
            return self._gemini_generate_pro(prompt, system_instruction)
    
    def generate_flash(self, prompt: str, system_instruction: str = None) -> str:
        """
        Generate content using the cheap/fast model.
        Use for: Quick drafts, template generation, previews.
        """
        self._ensure_initialized()
        
        if self.provider == "claude":
            return self._claude_generate(prompt, system_instruction, model=CLAUDE_MODELS["flash"])
        else:
            return self._gemini_generate_flash(prompt, system_instruction)
    
    def _claude_generate(self, prompt: str, system_instruction: str, model: str) -> str:
        """Generate using Claude API."""
        messages = [{"role": "user", "content": prompt}]
        
        kwargs = {
            "model": model,
            "max_tokens": 8192,
            "messages": messages
        }
        
        if system_instruction:
            kwargs["system"] = system_instruction
        
        response = self._client.messages.create(**kwargs)
        return response.content[0].text
    
    def _gemini_generate_pro(self, prompt: str, system_instruction: str = None) -> str:
        """Generate using Gemini pro model with fallback."""
        # Try primary model first
        try:
            model_name = GEMINI_MODELS["pro"]["primary"]
            if system_instruction:
                model = self._genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
            else:
                model = self._genai.GenerativeModel(model_name)
            
            response = model.generate_content(prompt)
            logger.info(f"Generated with {model_name}")
            return response.text
        except Exception as e:
            logger.warning(f"Primary model failed: {e}. Trying fallback...")
            
            # Try fallback model
            model_name = GEMINI_MODELS["pro"]["fallback"]
            if system_instruction:
                model = self._genai.GenerativeModel(
                    model_name=model_name,
                    system_instruction=system_instruction
                )
            else:
                model = self._genai.GenerativeModel(model_name)
            
            response = model.generate_content(prompt)
            logger.info(f"Generated with fallback {model_name}")
            return response.text
    
    def _gemini_generate_flash(self, prompt: str, system_instruction: str = None) -> str:
        """Generate using Gemini flash model."""
        model_name = GEMINI_MODELS["flash"]
        if system_instruction:
            model = self._genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
        else:
            model = self._genai.GenerativeModel(model_name)
        
        response = model.generate_content(prompt)
        return response.text
    
    def test_connection(self) -> tuple[bool, str]:
        """Test API connection and return (success, message)."""
        self._ensure_initialized()
        
        try:
            if self.provider == "claude":
                response = self._client.messages.create(
                    model=CLAUDE_MODELS["flash"],
                    max_tokens=50,
                    messages=[{"role": "user", "content": "Say 'API Connected' in exactly 2 words."}]
                )
                return True, f"Claude connected! Response: {response.content[0].text.strip()}"
            else:
                model = self._genai.GenerativeModel(GEMINI_MODELS["flash"])
                response = model.generate_content("Say 'API Connected' in exactly 2 words.")
                return True, f"Gemini connected! Response: {response.text.strip()}"
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
- Use <section> tags for major sections with id attributes
- Use <ul> and <li> for bullet points
- No tables for layout

MANDATORY HTML STRUCTURE (must follow exactly for editing compatibility):

1. Summary section:
   <section id="summary">
     <h2>...</h2>
     <p class="summary">Summary text here</p>
   </section>

2. Each work experience entry:
   <article class="entry" data-type="experience">
     <div class="entry-header">
       <span class="entry-title">Role/Title</span>
       <span class="entry-date">Date Range</span>
     </div>
     <div class="entry-header">
       <span class="entry-subtitle">Company Name</span>
       <span class="entry-location">Location</span>
     </div>
     <ul>
       <li>Bullet point</li>
     </ul>
   </article>

3. Education entries use same structure with data-type="education"

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
