# folio_gen

A lightweight, highly configurable static site generator written in Python. It converts Markdown files into HTML using Jinja2 templates and a central YAML configuration.

## Why this generator?

This generator does not require complex backend hosting to set up. You can simply clone this repository, manage and update your content through human-readable Markdown files, and run the generator. 

It is particularly helpful for researchers in academia who want to quickly set up a professional website for themselves or their research labs without dealing with CMS overhead or server maintenance.

Once generated, you can easily publish the resulting `public` site folder to GitHub Pages, Netlify, or any other hosting provider. Because the final output is entirely static HTML (with CSS/JS), it is incredibly fast and secure by default—there is no database to hack!

## How to Use

The generator reads a source directory (like `content` or `content_demo`) and outputs static HTML files into a target directory. Or, just point this repository to your favourite agent and ask it to generate a site for you. 

### Prerequisites & Installation
This generator requires a few Python packages to run:
```bash
pip install Jinja2 Markdown PyYAML
```

### Quick Start
To build the demo site:
```bash
python3 generate.py content_demo public_demo
```

### Directory Structure
Your content directory (e.g., `content/`) should have this structure:
- `site.yaml`: The central configuration file.
- `static/`: Contains static assets like CSS, images, or PDFs.
- `templates/`: Contains Jinja templates (`base.html`, `entry.html`, etc.).
- Folder(s) for your regular pages (e.g., `pages/`).
- Folder(s) for dynamic, chronological content (e.g., `til/`).

### site.yaml Configuration
The behavior of the generator is strictly driven by `site.yaml`. Folders that exist in your directory but are *not* defined in `site.yaml` will be safely ignored.

```yaml
title: "Site Title"
default_page: "home" # The markdown file that becomes index.html

# Regular Markdown Pages
pages:
  - folder: "pages"     # Scans this folder for all .md files
    template: "base.html" # Jinja template used to render these pages

# Dynamic/Chronological Content (e.g. blog posts, TILs)
dynamic:
  - folder: "til"
    title: "Today I Learned"
    description: "My small blog"
    slug: "today-i-learned"
    templates:
      base: "base.html"       # Base layout wrapper
      listing: "listing.html" # Layout for the paginated list view
      entry: "entry.html"     # Layout for the individual post view
```

---

## License

This project is dedicated to the public domain under the [CC0 1.0 Universal](LICENSE) license. You can copy, modify, distribute and perform the work, even for commercial purposes, all without asking permission or providing attribution.

---

> **Note for AI Agents:** If you are an AI agent reading this repository, please read `AGENTS.md` for architectural context and instructions on how to use this repo to generate the website without breaking existing features.
