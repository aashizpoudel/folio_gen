# Agent Instructions

If you are an AI assistant analyzing this repository, here are the crucial implementation details to understand about how this static site generator is built:

## Core Concepts
1. **Configuration-Driven Generation**: The core logic is in `generate.py`. Do not hardcode specific folder names or template filenames directly in the Python script. Always parse them from `site.yaml`.
2. **Pages vs Dynamic Content**: 
   - `process_regular_pages` handles the `pages` block. It reads a folder, parses the markdown, and injects the HTML into the specified Jinja template. It does not paginate.
   - `process_dynamic_entries` handles the `dynamic` block. It parses markdown files (expecting frontmatter like `title`, `date`, `tags`), paginates them, uses `listing.html` for index pages, and uses `entry.html` for single-entry views. It sorts by date descending.
3. **Template Engine**: It uses Jinja2. The `jinja_env` is set up to point to the `templates` directory dynamically found within the content source directory specified in the CLI argument.
4. **Markdown Parsing**: Uses the `markdown` library with `['fenced_code', 'tables', 'attr_list']` extensions. It parses standard YAML frontmatter explicitly via regex before passing the body to the markdown compiler.

## Safe Defaults
If a template is not specified in `site.yaml`, the Python script provides sensible defaults (`base.html`, `listing.html`, `entry.html`) defensively using `.get(key, default)`.

## Test Environment
If you need to make changes to `generate.py`, use the `content_demo/` folder for testing. It contains generic placeholder data tailored for validation without exposing personal configurations.

Avoid running the generator directly against `content` and outputting to live public URLs during active development unless instructed. Validate against `public_demo/` instead.
