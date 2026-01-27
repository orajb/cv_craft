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
        
        @page {
            margin: 0.5in 0.4in;
        }
        
        @page :first {
            margin-top: 0.4in;
        }
        
        @media print {
            body {
                padding: 0.4in;
                max-width: none;
                margin-bottom: 0.4in;
            }
            
            /* Prevent page breaks inside entries */
            .entry, article, .role-entry {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Avoid orphaned section headers */
            h2 {
                page-break-after: avoid;
                break-after: avoid;
            }
            
            /* Allow breaks between sections */
            section {
                page-break-before: auto;
            }
            
            /* Keep header on first page */
            header {
                page-break-after: avoid;
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


def get_modern_clean_template_html() -> str:
    """Return the Modern Clean template HTML - more visually appealing for human recruiters."""
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
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            font-size: 10.5pt;
            line-height: 1.6;
            color: #1f2937;
            background: #ffffff;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.6in 0.7in;
        }
        
        @page {
            margin: 0.5in 0.4in;
        }
        
        @page :first {
            margin-top: 0.4in;
        }
        
        @media print {
            body {
                padding: 0.4in;
                max-width: none;
                margin-bottom: 0.4in;
            }
            
            /* Prevent page breaks inside entries */
            .entry, article, .role-entry {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Avoid orphaned section headers */
            h2 {
                page-break-after: avoid;
                break-after: avoid;
            }
            
            /* Allow breaks between sections */
            section {
                page-break-before: auto;
            }
            
            /* Keep header on first page */
            header {
                page-break-after: avoid;
            }
        }
        
        header {
            margin-bottom: 1.75rem;
            padding-bottom: 1.25rem;
            border-bottom: 3px solid #166534;
        }
        
        h1 {
            font-size: 26pt;
            font-weight: 700;
            color: #166534;
            margin-bottom: 0.5rem;
            letter-spacing: -0.5px;
        }
        
        .contact-info {
            font-size: 9.5pt;
            color: #4b5563;
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem 1.5rem;
        }
        
        .contact-info a {
            color: #166534;
            text-decoration: none;
        }
        
        .contact-info a:hover {
            text-decoration: underline;
        }
        
        section {
            margin-bottom: 1.5rem;
        }
        
        h2 {
            font-size: 11pt;
            font-weight: 700;
            color: #166534;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 0.75rem;
            padding-left: 0.75rem;
            border-left: 3px solid #166534;
        }
        
        .summary {
            font-size: 10.5pt;
            color: #374151;
            line-height: 1.7;
        }
        
        .entry {
            margin-bottom: 1.25rem;
        }
        
        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            flex-wrap: wrap;
            margin-bottom: 0.2rem;
        }
        
        .entry-title {
            font-weight: 600;
            font-size: 11pt;
            color: #111827;
        }
        
        .entry-subtitle {
            color: #4b5563;
            font-weight: 500;
        }
        
        .entry-date {
            font-size: 9.5pt;
            color: #6b7280;
            font-weight: 500;
        }
        
        .entry-location {
            font-size: 9.5pt;
            color: #6b7280;
        }
        
        ul {
            margin-left: 1.25rem;
            margin-top: 0.4rem;
        }
        
        li {
            margin-bottom: 0.25rem;
            font-size: 10pt;
            color: #374151;
        }
        
        .skills-grid {
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
        }
        
        .skill-pill {
            background: #f0fdf4;
            color: #166534;
            padding: 0.25rem 0.6rem;
            border-radius: 4px;
            font-size: 9pt;
            font-weight: 500;
            border: 1px solid #bbf7d0;
        }
        
        .skill-category {
            width: 100%;
            font-weight: 600;
            color: #166534;
            font-size: 9.5pt;
            margin-top: 0.5rem;
            margin-bottom: 0.25rem;
        }
        
        .skill-category:first-child {
            margin-top: 0;
        }
        
        .projects-list, .certs-list {
            list-style: none;
            margin-left: 0;
        }
        
        .projects-list li, .certs-list li {
            margin-bottom: 0.6rem;
            padding-left: 0.75rem;
            border-left: 2px solid #d1fae5;
        }
        
        .project-name, .cert-name {
            font-weight: 600;
            color: #111827;
        }
        
        .project-tech {
            font-size: 9pt;
            color: #6b7280;
            font-style: italic;
        }
    </style>
</head>
<body>
    <header>
        <h1>{{CONTACT_NAME}}</h1>
        <div class="contact-info">
            <span>{{CONTACT_EMAIL}}</span>
            <span>{{CONTACT_PHONE}}</span>
            <span>{{CONTACT_LOCATION}}</span>
            {{CONTACT_LINKS}}
        </div>
    </header>
    
    <section id="summary">
        <h2>Summary</h2>
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
        {{SKILLS_PILLS}}
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
        <h2>Awards</h2>
        {{AWARDS}}
    </section>
</body>
</html>'''


def get_career_progression_template_html() -> str:
    """Return the Career Progression template HTML - groups roles by company."""
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
            font-size: 10.5pt;
            line-height: 1.55;
            color: #1a1a1a;
            background: #ffffff;
            max-width: 8.5in;
            margin: 0 auto;
            padding: 0.5in;
        }
        
        @page {
            margin: 0.5in 0.4in;
        }
        
        @page :first {
            margin-top: 0.4in;
        }
        
        @media print {
            body {
                padding: 0.4in;
                max-width: none;
                margin-bottom: 0.4in;
            }
            
            /* Prevent page breaks inside entries */
            .entry, article, .role-entry {
                page-break-inside: avoid;
                break-inside: avoid;
            }
            
            /* Avoid orphaned section headers */
            h2, .company-header {
                page-break-after: avoid;
                break-after: avoid;
            }
            
            /* Allow breaks between sections */
            section {
                page-break-before: auto;
            }
            
            /* Keep header on first page */
            header {
                page-break-after: avoid;
            }
        }
        
        header {
            text-align: center;
            margin-bottom: 1.5rem;
            padding-bottom: 1rem;
            border-bottom: 2px solid #374151;
        }
        
        h1 {
            font-size: 24pt;
            font-weight: 600;
            color: #111827;
            margin-bottom: 0.5rem;
        }
        
        .contact-info {
            font-size: 9.5pt;
            color: #4b5563;
        }
        
        .contact-info a {
            color: #374151;
            text-decoration: none;
        }
        
        .contact-info span {
            margin: 0 0.4rem;
        }
        
        section {
            margin-bottom: 1.25rem;
        }
        
        h2 {
            font-size: 11pt;
            font-weight: 600;
            color: #111827;
            text-transform: uppercase;
            letter-spacing: 1px;
            border-bottom: 1px solid #d1d5db;
            padding-bottom: 0.25rem;
            margin-bottom: 0.75rem;
        }
        
        .summary {
            font-size: 10.5pt;
            color: #374151;
            text-align: justify;
        }
        
        /* Company grouping styles */
        .company-group {
            margin-bottom: 1.25rem;
        }
        
        .company-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.5rem;
            padding-bottom: 0.25rem;
            border-bottom: 1px solid #e5e7eb;
        }
        
        .company-name {
            font-weight: 700;
            font-size: 11.5pt;
            color: #111827;
        }
        
        .company-tenure {
            font-size: 9.5pt;
            color: #6b7280;
            font-weight: 500;
        }
        
        .company-location {
            font-size: 9.5pt;
            color: #6b7280;
        }
        
        .role-entry {
            margin-left: 1rem;
            margin-bottom: 0.75rem;
            padding-left: 0.75rem;
            border-left: 2px solid #e5e7eb;
        }
        
        .role-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            margin-bottom: 0.15rem;
        }
        
        .role-title {
            font-weight: 600;
            font-size: 10.5pt;
            color: #1f2937;
        }
        
        .role-date {
            font-size: 9pt;
            color: #6b7280;
        }
        
        .role-entry ul {
            margin-left: 1rem;
            margin-top: 0.25rem;
        }
        
        .role-entry li {
            margin-bottom: 0.2rem;
            font-size: 10pt;
            color: #374151;
        }
        
        /* Standard entry for non-grouped items */
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
            font-size: 10.5pt;
            color: #1a1a1a;
        }
        
        .entry-subtitle {
            font-style: italic;
            color: #4b5563;
        }
        
        .entry-date {
            font-size: 9.5pt;
            color: #6b7280;
        }
        
        .entry-location {
            font-size: 9.5pt;
            color: #6b7280;
        }
        
        ul {
            margin-left: 1.25rem;
            margin-top: 0.25rem;
        }
        
        li {
            margin-bottom: 0.2rem;
            font-size: 10pt;
        }
        
        .skills-grid {
            display: grid;
            grid-template-columns: auto 1fr;
            gap: 0.25rem 1rem;
            font-size: 10pt;
        }
        
        .skill-category {
            font-weight: 600;
            color: #374151;
        }
        
        .skill-items {
            color: #4b5563;
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
            font-size: 9pt;
            color: #6b7280;
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
        {{EXPERIENCE_GROUPED}}
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

@page {
    margin: 0.5in 0.4in;
}

@page :first {
    margin-top: 0.4in;
}

@media print {
    body {
        padding: 0.4in;
        max-width: none;
        margin-bottom: 0.4in;
    }
    
    /* Prevent page breaks inside entries */
    .entry, article, .role-entry {
        page-break-inside: avoid;
        break-inside: avoid;
    }
    
    /* Avoid orphaned section headers */
    h2 {
        page-break-after: avoid;
        break-after: avoid;
    }
    
    /* Allow breaks between sections */
    section {
        page-break-before: auto;
    }
    
    /* Keep header on first page */
    header {
        page-break-after: avoid;
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


def get_compact_mode_css(level: str = "normal") -> str:
    """Return CSS adjustments for compact modes."""
    if level == "normal":
        return ""
    elif level == "compact":
        return '''
<style>
/* Compact Mode */
body {
    font-size: 9.5pt !important;
    line-height: 1.4 !important;
    padding: 0.4in !important;
}
h1 { font-size: 20pt !important; margin-bottom: 0.3rem !important; }
h2 { font-size: 10pt !important; margin-bottom: 0.5rem !important; }
header { margin-bottom: 1rem !important; padding-bottom: 0.75rem !important; }
section { margin-bottom: 0.9rem !important; }
.entry, article { margin-bottom: 0.7rem !important; }
.entry-header, .role-header { margin-bottom: 0.15rem !important; }
ul { margin-top: 0.2rem !important; margin-left: 1rem !important; }
li { margin-bottom: 0.1rem !important; font-size: 9.5pt !important; }
.summary { font-size: 9.5pt !important; }
.contact-info { font-size: 8.5pt !important; }
.entry-date, .entry-location, .role-date { font-size: 8.5pt !important; }
.skill-pill { padding: 0.15rem 0.4rem !important; font-size: 8pt !important; }
.company-group { margin-bottom: 0.9rem !important; }
.role-entry { margin-bottom: 0.5rem !important; padding-left: 0.5rem !important; }
</style>
'''
    elif level == "very_compact":
        return '''
<style>
/* Very Compact Mode */
body {
    font-size: 8.5pt !important;
    line-height: 1.3 !important;
    padding: 0.3in !important;
}
h1 { font-size: 18pt !important; margin-bottom: 0.2rem !important; }
h2 { font-size: 9pt !important; margin-bottom: 0.4rem !important; letter-spacing: 0.5px !important; }
header { margin-bottom: 0.75rem !important; padding-bottom: 0.5rem !important; }
section { margin-bottom: 0.7rem !important; }
.entry, article { margin-bottom: 0.5rem !important; }
.entry-header, .role-header { margin-bottom: 0.1rem !important; }
ul { margin-top: 0.15rem !important; margin-left: 0.9rem !important; }
li { margin-bottom: 0.05rem !important; font-size: 8.5pt !important; }
.summary { font-size: 8.5pt !important; }
.contact-info { font-size: 8pt !important; gap: 0.3rem 1rem !important; }
.entry-date, .entry-location, .role-date { font-size: 8pt !important; }
.entry-title, .role-title { font-size: 9.5pt !important; }
.entry-subtitle { font-size: 9pt !important; }
.skill-pill { padding: 0.1rem 0.3rem !important; font-size: 7.5pt !important; }
.skills-grid { gap: 0.3rem !important; }
.company-group { margin-bottom: 0.7rem !important; }
.company-header { margin-bottom: 0.3rem !important; padding-bottom: 0.15rem !important; }
.role-entry { margin-bottom: 0.4rem !important; margin-left: 0.75rem !important; padding-left: 0.5rem !important; }
.projects-list li, .certs-list li { margin-bottom: 0.3rem !important; padding-left: 0.5rem !important; }
</style>
'''
    return ""


def get_paginated_preview_css() -> str:
    """Return CSS for paginated preview display (simulates printed pages)."""
    return '''
<style>
/* Paginated Preview - simulates printed pages */
@media screen {
    html {
        background: #525659 !important;
    }
    body {
        background: white !important;
        width: 8.5in !important;
        min-height: 11in !important;
        margin: 0.5in auto !important;
        padding: 0.5in !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
        box-sizing: border-box !important;
    }
}
</style>
'''


def fill_template_with_experiences(
    template_html: str, 
    experiences: dict,
    compact_mode: str = "normal",
    show_page_preview: bool = False
) -> str:
    """Fill template placeholders with actual experience data.
    
    Args:
        template_html: The HTML template with placeholders
        experiences: Dict containing contact, work_experiences, education, etc.
        compact_mode: "normal", "compact", or "very_compact"
        show_page_preview: If True, adds CSS to simulate printed page appearance
    """
    
    html = template_html
    contact = experiences.get("contact", {})
    
    # Contact info
    html = html.replace("{{CONTACT_NAME}}", contact.get("name", "Your Name"))
    html = html.replace("{{CONTACT_EMAIL}}", contact.get("email", "email@example.com"))
    html = html.replace("{{CONTACT_PHONE}}", contact.get("phone", ""))
    html = html.replace("{{CONTACT_LOCATION}}", contact.get("location", ""))
    
    # Contact links - build URLs from usernames
    links = []
    if contact.get("linkedin"):
        linkedin_input = contact["linkedin"].strip()
        # Handle both username-only and full URL input (backwards compatibility)
        if "linkedin.com" in linkedin_input:
            # Already a URL - extract and rebuild
            linkedin_input = linkedin_input.replace("https://", "").replace("http://", "").replace("www.", "")
            if linkedin_input.startswith("linkedin.com/in/"):
                linkedin_input = linkedin_input.replace("linkedin.com/in/", "")
        # Build clean URL and display
        linkedin_url = f"https://www.linkedin.com/in/{linkedin_input}"
        linkedin_display = f"linkedin.com/in/{linkedin_input}"
        links.append(f'<a href="{linkedin_url}">{linkedin_display}</a>')
    
    if contact.get("github"):
        github_input = contact["github"].strip()
        # Handle both username-only and full URL input (backwards compatibility)
        if "github.com" in github_input:
            # Already a URL - extract and rebuild
            github_input = github_input.replace("https://", "").replace("http://", "").replace("www.", "")
            if github_input.startswith("github.com/"):
                github_input = github_input.replace("github.com/", "")
        # Build clean URL and display
        github_url = f"https://github.com/{github_input}"
        github_display = f"github.com/{github_input}"
        links.append(f'<a href="{github_url}">{github_display}</a>')
    
    if contact.get("website"):
        website_input = contact["website"].strip()
        # Ensure website has protocol
        if website_input and not website_input.startswith(("http://", "https://")):
            website_url = f"https://{website_input}"
        else:
            website_url = website_input
        # Display without protocol
        website_display = website_url.replace("https://", "").replace("http://", "").replace("www.", "")
        links.append(f'<a href="{website_url}">{website_display}</a>')
    
    links_html = ""
    if links:
        links_html = " | " + " | ".join(links)
    html = html.replace("{{CONTACT_LINKS}}", links_html)
    
    # For placeholders, provide the full formatted URLs
    linkedin_input = contact.get("linkedin", "").strip()
    github_input = contact.get("github", "").strip()
    html = html.replace("{{CONTACT_LINKEDIN}}", f"linkedin.com/in/{linkedin_input}" if linkedin_input else "")
    html = html.replace("{{CONTACT_GITHUB}}", f"github.com/{github_input}" if github_input else "")
    
    # Summary
    html = html.replace("{{SUMMARY}}", experiences.get("summary", ""))
    
    # Experience (standard)
    exp_html = _format_experience_html(experiences.get("work_experiences", []))
    html = html.replace("{{EXPERIENCE}}", exp_html)
    
    # Experience (grouped by company - for Career Progression template)
    exp_grouped_html = _format_experience_grouped_html(experiences.get("work_experiences", []))
    html = html.replace("{{EXPERIENCE_GROUPED}}", exp_grouped_html)
    
    # Education
    edu_html = _format_education_html(experiences.get("education", []))
    html = html.replace("{{EDUCATION}}", edu_html)
    
    # Skills (standard grid)
    skills_html = _format_skills_html(experiences.get("skills", {}))
    html = html.replace("{{SKILLS}}", skills_html)
    
    # Skills (pill style - for Modern Clean template)
    skills_pills_html = _format_skills_pills_html(experiences.get("skills", {}))
    html = html.replace("{{SKILLS_PILLS}}", skills_pills_html)
    
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
    
    # Build injected CSS
    injected_css = '''
<style>
/* Universal print styles - injected for all templates */
@page {
    margin: 0.5in 0.4in;
}

@page :first {
    margin-top: 0.4in;
}

@media print {
    body {
        margin-bottom: 0.4in;
    }
    
    /* Prevent page breaks inside entries */
    .entry, article, .role-entry {
        page-break-inside: avoid;
        break-inside: avoid;
    }
    
    /* Avoid orphaned section headers */
    h2, h3, .company-header {
        page-break-after: avoid;
        break-after: avoid;
    }
    
    /* Allow breaks between sections */
    section {
        page-break-before: auto;
    }
    
    /* Keep header on first page */
    header {
        page-break-after: avoid;
    }
}
</style>
'''
    
    # Add compact mode CSS if needed
    if compact_mode != "normal":
        injected_css += get_compact_mode_css(compact_mode)
    
    # Add paginated preview CSS if requested
    if show_page_preview:
        injected_css += get_paginated_preview_css()
    
    # Insert before </head> if exists, otherwise before </body>
    if '</head>' in html:
        html = html.replace('</head>', injected_css + '</head>')
    elif '</body>' in html:
        html = html.replace('</body>', injected_css + '</body>')
    
    return html


def _format_experience_html(experiences: list) -> str:
    """Format work experiences as HTML. Newest/current first."""
    if not experiences:
        return ""
    
    # Sort: current jobs first, then by created_at descending (newest first)
    sorted_exps = sorted(
        experiences,
        key=lambda x: (not x.get("is_current", False), x.get("created_at", "")),
        reverse=False  # is_current=True comes first, then newest created_at
    )
    # Actually reverse to get newest first (most recently added)
    sorted_exps = list(reversed(sorted_exps))
    
    html_parts = []
    for exp in sorted_exps:
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
    """Format education as HTML. Newest first."""
    if not education:
        return ""
    
    # Sort by created_at descending (newest first)
    sorted_edu = list(reversed(education))
    
    html_parts = []
    for edu in sorted_edu:
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


def _format_skills_pills_html(skills: dict) -> str:
    """Format skills as pill/tag style badges for Modern Clean template."""
    if not any(skills.values()):
        return ""
    
    html_parts = ['<div class="skills-grid">']
    
    for category, items in skills.items():
        if items:
            display_name = category.replace("_", " ").title()
            html_parts.append(f'<span class="skill-category">{display_name}</span>')
            for item in items:
                html_parts.append(f'<span class="skill-pill">{item}</span>')
    
    html_parts.append('</div>')
    return "\n".join(html_parts)


def _format_experience_grouped_html(experiences: list) -> str:
    """Format work experiences grouped by company for Career Progression template."""
    if not experiences:
        return ""
    
    # Sort: current jobs first, then by created_at descending
    sorted_exps = sorted(
        experiences,
        key=lambda x: (not x.get("is_current", False), x.get("created_at", "")),
        reverse=False
    )
    sorted_exps = list(reversed(sorted_exps))
    
    # Group by company (case-insensitive)
    from collections import OrderedDict
    company_groups = OrderedDict()
    
    for exp in sorted_exps:
        company_key = exp.get("company", "").strip().lower()
        if company_key not in company_groups:
            company_groups[company_key] = {
                "company": exp.get("company", ""),
                "location": exp.get("location", ""),
                "roles": []
            }
        company_groups[company_key]["roles"].append(exp)
    
    html_parts = []
    
    for company_key, group in company_groups.items():
        roles = group["roles"]
        company_name = group["company"]
        location = group["location"]
        
        # Calculate company tenure (earliest start to latest end)
        start_dates = [r.get("start_date", "") for r in roles]
        end_dates = [r.get("end_date", "") for r in roles]
        
        earliest_start = start_dates[-1] if start_dates else ""  # Last in list is earliest
        latest_end = end_dates[0] if end_dates else ""  # First in list is latest
        
        tenure = f"{earliest_start} - {latest_end}" if earliest_start else ""
        
        if len(roles) == 1:
            # Single role - use standard format
            exp = roles[0]
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
        else:
            # Multiple roles - group under company
            html_parts.append(f'''
            <div class="company-group">
                <div class="company-header">
                    <span class="company-name">{company_name}</span>
                    <span class="company-tenure">{tenure}</span>
                </div>
                <div class="company-location">{location}</div>
            ''')
            
            for exp in roles:
                bullets = "".join(f"<li>{b}</li>" for b in exp.get("bullets", []))
                html_parts.append(f'''
                <div class="role-entry">
                    <div class="role-header">
                        <span class="role-title">{exp.get("role", "")}</span>
                        <span class="role-date">{exp.get("start_date", "")} - {exp.get("end_date", "")}</span>
                    </div>
                    <ul>{bullets}</ul>
                </div>
                ''')
            
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
