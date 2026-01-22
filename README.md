# 🎯 Job Hunter

**AI-Powered CV Generator** — A local tool for creating machine-readable, ATS-friendly CVs with Gemini AI assistance.

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red)
![Gemini](https://img.shields.io/badge/Gemini-API-yellow)

---

## ✨ Features

- **📝 Experience Bank** — Store all your work experiences, education, skills, and projects in one place
- **🎨 Template Editor** — Create and customize CV templates with AI assistance
- **✨ CV Generator** — Paste a job description and let AI create a tailored CV
- **📚 Application History** — Track all your applications with their generated CVs
- **🤖 Gemini AI Integration** — Uses `gemini-3-pro-preview` with fallback to `gemini-2.5-pro`
- **🔒 Local-First** — All data stored locally, API key never saved to disk

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+** — [Download here](https://www.python.org/downloads/) if not installed
- **Gemini API Key** — [Get one free](https://makersuite.google.com/app/apikey)

### One-Command Launch

**macOS/Linux:**
```bash
cd "Job Hunter"
./run.sh
```

**Windows:**
```
Double-click run.bat
```

That's it! The script automatically:
- ✓ Creates a virtual environment
- ✓ Installs all dependencies  
- ✓ Launches the app

The app opens in your browser at `http://localhost:8501`

### Manual Installation (Alternative)

```bash
cd "Job Hunter"
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

### 4. First-Time Setup

1. **Enter your Gemini API key** in the sidebar
2. **Click "Test Connection"** to verify it works
3. **Go to Experience Bank** and add your information
4. **Create a template** in Template Editor (or use the default)
5. **Generate your first CV!**

---

## 📖 Usage Guide

### Experience Bank

Store all your professional information:
- **Contact Info** — Name, email, phone, LinkedIn, GitHub
- **Work Experience** — Companies, roles, dates, bullet points
- **Education** — Degrees, institutions, highlights
- **Skills** — Technical, soft skills, tools, languages
- **Projects** — Personal/professional projects with tech stack
- **Certifications** — Professional certifications

> 💡 **Tip**: Add ALL your experiences here. The AI will select the most relevant ones for each job application.

### Template Editor

Create and manage CV templates:
- **Generate with AI** — Describe your desired style and let Gemini create a template
- **Edit HTML** — Directly modify the template code
- **Preview** — See how the template looks with your data
- **Set Default** — Choose which template to use by default

### CV Generator

Create tailored CVs:
1. Enter the **company name** and **role**
2. **Paste the job description**
3. Add any **specific instructions** (optional)
4. Select a **template**
5. Click **Generate CV**
6. **Preview** and **edit** if needed
7. **Open in browser** and print to PDF
8. **Save Application** to track it

### Application History

Track your job applications:
- View all past applications with their CVs
- Update application **status** (created, applied, interviewing, rejected, offer)
- Add **notes** for each application
- **Search** by company or role

---

## 🖨️ Exporting to PDF

The app uses browser-based PDF export for maximum ATS compatibility:

1. Click **"Open in Browser"**
2. Press `Cmd+P` (Mac) or `Ctrl+P` (Windows)
3. Select **"Save as PDF"**
4. Adjust margins if needed (usually 0.5in works well)

---

## 🔧 Configuration

### Models Used

| Task | Model | Fallback |
|------|-------|----------|
| CV Generation | `gemini-3-pro-preview` | `gemini-2.5-pro` |
| Template Generation | `gemini-2.0-flash` | — |
| Connection Test | `gemini-2.0-flash` | — |

### Data Storage

All data is stored locally in JSON files:

```
data/
├── experiences.json    # Your experience bank
├── templates.json      # CV templates
└── applications.json   # Application history
```

> ⚠️ **Note**: These files are in `.gitignore` by default. Back them up if needed!

---

## 🛠️ Development

### Project Structure

```
Job Hunter/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .gitignore               # Git ignore rules
├── data/                    # User data (JSON files)
├── src/
│   ├── __init__.py
│   ├── data_manager.py      # CRUD operations for JSON storage
│   ├── gemini_client.py     # Gemini API client with fallback
│   └── cv_generator.py      # HTML generation utilities
├── templates/               # (Reserved for future use)
└── styles/                  # (Reserved for future use)
```

### Adding New Features

The codebase is modular:
- **Data operations** → `src/data_manager.py`
- **AI integration** → `src/gemini_client.py`
- **HTML/CV logic** → `src/cv_generator.py`
- **UI/UX** → `app.py`

---

## 📝 ATS Optimization Tips

The generated CVs are optimized for Applicant Tracking Systems:

- ✅ Single-column layout
- ✅ Semantic HTML5 structure
- ✅ Standard section headers
- ✅ No images or graphics
- ✅ Clean, parseable text
- ✅ Proper heading hierarchy

---

## 🐛 Troubleshooting

### "API Connection Failed"
- Verify your API key is correct
- Check your internet connection
- Ensure the Gemini API is available in your region

### "No templates found"
- Go to Template Editor and click "Create Default Template"

### CV looks different in PDF
- Use Chrome for best PDF export results
- Set margins to 0.5 inches
- Disable headers/footers in print settings

---

## 📄 License

MIT License — Feel free to use and modify for your job search!

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) — For the amazing Python web framework
- [Google Gemini](https://deepmind.google/technologies/gemini/) — For the AI capabilities
- You — For taking control of your job search! 💪
