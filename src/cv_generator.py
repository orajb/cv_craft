"""
CV Generator - Combines templates with content and handles HTML output
"""

import re
import tempfile
import webbrowser
from pathlib import Path
from typing import Optional


def get_default_template_html() -> str:
    """Return the default CV template HTML."""
    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{CONTACT_NAME}} - CV</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #1a1a1a;
            background: #ffffff;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
        }
        
        @media print {
            body {
                padding: 0;
                max-width: none;
            }
        }
        
        header {
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #2c3e50;
        }
        
        h1 {
            font-size: 24pt;
            font-weight: 600;
            color: #2c3e50;
            margin-bottom: 0.5rem;
            letter-spacing: 0.5px;
        }
        
        .contact-info {
            font-size: 10pt;
            color: #555;
        }
        
        .contact-info a {
            color: #2c3e50;
            text-decoration: none;
        }
        
        .contact-info span {
            margin: 0 0.5rem;
        }
        
        section {
            margin-bottom: 1.25rem;
        }
        
        h2 {
            font-size: 12pt;
            font-weight: 600;
            color: #2c3e50;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #bdc3c7;
            padding-bottom: 0.25rem;
            margin-bottom: 0.75rem;
        }
        
        .summary {
            font-size: 10.5pt;
            color: #333;
            text-align: justify;
        }
        
        .entry {
            margin-bottom: 1rem;
        }
        
        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            margin-bottom: 0.25rem;
        }
        
        .entry-title {
            font-weight: 600;
            font-size: 11pt;
            color: #1a1a1a;
        }
        
        .entry-subtitle {
            font-style: italic;
            color: #555;
        }
        
        .entry-date {
            font-size: 10pt;
            color: #666;
        }
        
        .entry-location {
            font-size: 10pt;
            color: #666;
        }
        
        ul {
            margin-left: 1.25rem;
            margin-top: 0.25rem;
        }
        
        li {
            margin-bottom: 0.2rem;
            font-size: 10.5pt;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.25rem 1rem;
            font-size: 10.5pt;
        }
        
        .skill-category {
            font-weight: 600;
            color: #2c3e50;
        }
        
        .skill-items {
            color: #333;
        }
        
        .projects-list, .certs-list {
            list-style: none;
            margin-left: 0;
        }
        
        .projects-list li, .certs-list li {
            margin-bottom: 0.5rem;
        }
        
        .project-name, .cert-name {
            font-weight: 600;
        }
        
        .project-tech {
            font-size: 9.5pt;
            color: #666;
            font-style: italic;
        }
    </style>
</head>
<body>
    <header>
        <h1>{{CONTACT_NAME}}</h1>
        <div class="contact-info">
            <span>{{CONTACT_EMAIL}}</span> |
            <span>{{CONTACT_PHONE}}</span> |
            <span>{{CONTACT_LOCATION}}</span>
            {{CONTACT_LINKS}}
        </div>
    </header>
    
    <section id="summary">
        <h2>Professional Summary</h2>
        <p class="summary">{{SUMMARY}}</p>
    </section>
    
    <section id="experience">
        <h2>Experience</h2>
        {{EXPERIENCE}}
    </section>
    
    <section id="education">
        <h2>Education</h2>
        {{EDUCATION}}
    </section>
    
    <section id="skills">
        <h2>Skills</h2>
        {{SKILLS}}
    </section>
    
    <section id="projects">
        <h2>Projects</h2>
        {{PROJECTS}}
    </section>
    
    <section id="certifications">
        <h2>Certifications</h2>
        {{CERTIFICATIONS}}
    </section>
    
    <section id="awards">
        <h2>Awards & Honors</h2>
        {{AWARDS}}
    </section>
</body>
</html>'''


def get_default_template_css() -> str:
    """Return default CSS (embedded in template, but stored separately for editing)."""
    return '''/* CV Styles - ATS Friendly */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #1a1a1a;
    background: #ffffff;
    max-width: 8.5in;
    margin: 0 auto;
    padding: 0.5in;
}

@media print {
    body {
        padding: 0;
        max-width: none;
    }
}

header {
    text-align: center;
    margin-bottom: 1.5rem;
    padding-bottom: 1rem;
    border-bottom: 2px solid #2c3e50;
}

h1 {
    font-size: 24pt;
    font-weight: 600;
    color: #2c3e50;
}

h2 {
    font-size: 12pt;
    font-weight: 600;
    color: #2c3e50;
    text-transform: uppercase;
    letter-spacing: 1px;
    border-bottom: 1px solid #bdc3c7;
    padding-bottom: 0.25rem;
    margin-bottom: 0.75rem;
}
'''


def fill_template_with_experiences(template_html: str, experiences: dict) -> str:
    """Fill template placeholders with actual experience data."""
    
    html = template_html
    contact = experiences.get("contact", {})
    
    # Contact info
    html = html.replace("{{CONTACT_NAME}}", contact.get("name", "Your Name"))
    html = html.replace("{{CONTACT_EMAIL}}", contact.get("email", "email@example.com"))
    html = html.replace("{{CONTACT_PHONE}}", contact.get("phone", ""))
    html = html.replace("{{CONTACT_LOCATION}}", contact.get("location", ""))
    
    # Contact links
    links = []
    if contact.get("linkedin"):
        links.append(f'<a href="{contact["linkedin"]}">LinkedIn</a>')
    if contact.get("github"):
        links.append(f'<a href="{contact["github"]}">GitHub</a>')
    if contact.get("website"):
        links.append(f'<a href="{contact["website"]}">Portfolio</a>')
    
    links_html = ""
    if links:
        links_html = " | " + " | ".join(links)
    html = html.replace("{{CONTACT_LINKS}}", links_html)
    html = html.replace("{{CONTACT_LINKEDIN}}", contact.get("linkedin", ""))
    html = html.replace("{{CONTACT_GITHUB}}", contact.get("github", ""))
    
    # Summary
    html = html.replace("{{SUMMARY}}", experiences.get("summary", ""))
    
    # Experience
    exp_html = _format_experience_html(experiences.get("work_experiences", []))
    html = html.replace("{{EXPERIENCE}}", exp_html)
    
    # Education
    edu_html = _format_education_html(experiences.get("education", []))
    html = html.replace("{{EDUCATION}}", edu_html)
    
    # Skills
    skills_html = _format_skills_html(experiences.get("skills", {}))
    html = html.replace("{{SKILLS}}", skills_html)
    
    # Projects
    projects_html = _format_projects_html(experiences.get("projects", []))
    html = html.replace("{{PROJECTS}}", projects_html)
    
    # Certifications
    certs_html = _format_certs_html(experiences.get("certifications", []))
    html = html.replace("{{CERTIFICATIONS}}", certs_html)
    
    # Awards
    awards_html = _format_awards_html(experiences.get("awards", []))
    html = html.replace("{{AWARDS}}", awards_html)
    
    # Remove empty sections
    html = _remove_empty_sections(html)
    
    return html


def _format_experience_html(experiences: list) -> str:
    """Format work experiences as HTML."""
    if not experiences:
        return ""
    
    html_parts = []
    for exp in experiences:
        bullets = "".join(f"<li>{b}</li>" for b in exp.get("bullets", []))
        html_parts.append(f'''
        <article class="entry">
            <div class="entry-header">
                <span class="entry-title">{exp.get("role", "")}</span>
                <span class="entry-date">{exp.get("start_date", "")} - {exp.get("end_date", "")}</span>
            </div>
            <div class="entry-header">
                <span class="entry-subtitle">{exp.get("company", "")}</span>
                <span class="entry-location">{exp.get("location", "")}</span>
            </div>
            <ul>{bullets}</ul>
        </article>
        ''')
    
    return "\n".join(html_parts)


def _format_education_html(education: list) -> str:
    """Format education as HTML."""
    if not education:
        return ""
    
    html_parts = []
    for edu in education:
        highlights = ""
        if edu.get("highlights"):
            bullets = "".join(f"<li>{h}</li>" for h in edu["highlights"])
            highlights = f"<ul>{bullets}</ul>"
        
        gpa = f" | GPA: {edu['gpa']}" if edu.get("gpa") else ""
        
        html_parts.append(f'''
        <article class="entry">
            <div class="entry-header">
                <span class="entry-title">{edu.get("degree", "")} in {edu.get("field", "")}</span>
                <span class="entry-date">{edu.get("start_date", "")} - {edu.get("end_date", "")}</span>
            </div>
            <div class="entry-header">
                <span class="entry-subtitle">{edu.get("institution", "")}{gpa}</span>
            </div>
            {highlights}
        </article>
        ''')
    
    return "\n".join(html_parts)


def _format_skills_html(skills: dict) -> str:
    """Format skills as HTML grid."""
    if not any(skills.values()):
        return ""
    
    html_parts = ['<div class="skills-grid">']
    
    for category, items in skills.items():
        if items:
            display_name = category.replace("_", " ").title()
            html_parts.append(f'<span class="skill-category">{display_name}:</span>')
            html_parts.append(f'<span class="skill-items">{", ".join(items)}</span>')
    
    html_parts.append('</div>')
    return "\n".join(html_parts)


def _format_projects_html(projects: list) -> str:
    """Format projects as HTML."""
    if not projects:
        return ""
    
    html_parts = ['<ul class="projects-list">']
    
    for proj in projects:
        tech = ""
        if proj.get("technologies"):
            tech = f'<span class="project-tech">({", ".join(proj["technologies"])})</span>'
        
        bullets = ""
        if proj.get("bullets"):
            bullet_items = "".join(f"<li>{b}</li>" for b in proj["bullets"])
            bullets = f"<ul>{bullet_items}</ul>"
        
        html_parts.append(f'''
        <li>
            <span class="project-name">{proj.get("name", "")}</span> {tech}
            <p>{proj.get("description", "")}</p>
            {bullets}
        </li>
        ''')
    
    html_parts.append('</ul>')
    return "\n".join(html_parts)


def _format_certs_html(certifications: list) -> str:
    """Format certifications as HTML."""
    if not certifications:
        return ""
    
    html_parts = ['<ul class="certs-list">']
    
    for cert in certifications:
        html_parts.append(f'''
        <li>
            <span class="cert-name">{cert.get("name", "")}</span> - 
            {cert.get("issuer", "")} ({cert.get("date", "")})
        </li>
        ''')
    
    html_parts.append('</ul>')
    return "\n".join(html_parts)


def _format_awards_html(awards: list) -> str:
    """Format awards as HTML."""
    if not awards:
        return ""
    
    html_parts = ['<ul class="certs-list">']  # Reuse certs-list styling
    
    for award in awards:
        # Handle both new format (text) and old format (name/issuer/date)
        if award.get("text"):
            display_text = award["text"]
        else:
            # Old format - build display text
            display_text = award.get("name", "")
            if award.get("issuer"):
                display_text += f" — {award['issuer']}"
            if award.get("date"):
                display_text += f" ({award['date']})"
            if award.get("description"):
                display_text += f": {award['description']}"
        
        html_parts.append(f'''
        <li>{display_text}</li>
        ''')
    
    html_parts.append('</ul>')
    return "\n".join(html_parts)


def _remove_empty_sections(html: str) -> str:
    """Remove sections that have no content."""
    # Pattern to match empty sections
    patterns = [
        r'<section id="summary">.*?<p class="summary">\s*</p>\s*</section>',
        r'<section id="experience">.*?<h2>Experience</h2>\s*</section>',
        r'<section id="education">.*?<h2>Education</h2>\s*</section>',
        r'<section id="skills">.*?<h2>Skills</h2>\s*</section>',
        r'<section id="projects">.*?<h2>Projects</h2>\s*</section>',
        r'<section id="certifications">.*?<h2>Certifications</h2>\s*</section>',
        r'<section id="awards">.*?<h2>Awards & Honors</h2>\s*</section>',
    ]
    
    for pattern in patterns:
        html = re.sub(pattern, '', html, flags=re.DOTALL)
    
    return html


def open_cv_in_browser(html_content: str, filename: str = "cv_preview.html") -> str:
    """Save HTML to temp file and open in browser. Returns the file path."""
    
    # Create temp directory if needed
    temp_dir = Path(tempfile.gettempdir()) / "job_hunter"
    temp_dir.mkdir(exist_ok=True)
    
    filepath = temp_dir / filename
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    # Open in default browser
    webbrowser.open(f"file://{filepath}")
    
    return str(filepath)


def save_cv_html(html_content: str, filepath: str) -> str:
    """Save CV HTML to specified path."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    return str(path)


def extract_html_from_response(response: str) -> str:
    """Extract HTML from AI response, handling markdown code blocks."""
    
    # Try to find HTML in code blocks
    code_block_pattern = r'```(?:html)?\s*(<!DOCTYPE.*?</html>)\s*```'
    match = re.search(code_block_pattern, response, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # Try to find raw HTML
    html_pattern = r'(<!DOCTYPE.*?</html>)'
    match = re.search(html_pattern, response, re.DOTALL | re.IGNORECASE)
    
    if match:
        return match.group(1).strip()
    
    # If no full HTML document, check for body content
    if '<body>' in response.lower() or '<div' in response.lower():
        return response.strip()
    
    # Return as-is
    return response
