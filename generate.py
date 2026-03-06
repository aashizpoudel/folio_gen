import os
import shutil
import sys
import yaml
import markdown
import re
from datetime import datetime
from math import ceil
from jinja2 import Environment, FileSystemLoader

def load_config(content_dir):
    config_path = os.path.join(content_dir, 'site.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def setup_jinja_env(content_dir):
    template_dir = os.path.join(content_dir, 'templates')
    return Environment(loader=FileSystemLoader(template_dir))

def parse_markdown_file(filepath):
    """Parses a markdown file with YAML frontmatter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Match YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if match:
        frontmatter_str = match.group(1)
        markdown_str = match.group(2)
        try:
            metadata = yaml.safe_load(frontmatter_str) or {}
        except yaml.YAMLError:
            metadata = {}
    else:
        metadata = {}
        markdown_str = content

    html_content = markdown.markdown(markdown_str, extensions=['fenced_code', 'tables', 'attr_list'])
    return metadata, html_content

def process_regular_pages(content_dir, output_dir, config, jinja_env):
    pages_items = config.get('pages', [])
    for page_item in pages_items:
        folder = page_item.get('folder')
        if not folder:
            continue
            
        pages_dir = os.path.join(content_dir, folder)
        if not os.path.exists(pages_dir):
            continue

        for filename in os.listdir(pages_dir):
            if not filename.endswith('.md'):
                continue
                
            filepath = os.path.join(pages_dir, filename)
            slug = filename[:-3]
            metadata, html_content = parse_markdown_file(filepath)
            
            # Determine output path
            if slug == config.get('default_page'):
                page_output_dir = output_dir
            else:
                page_output_dir = os.path.join(output_dir, slug)
                os.makedirs(page_output_dir, exist_ok=True)
                
            output_filepath = os.path.join(page_output_dir, 'index.html')
            
            # Generate full HTML
            page_title = metadata.get('title', slug.title())
            
            # Add page-specific classes based on slug
            wrapper_class = f"{slug}-page"
            if slug == config.get('default_page'):
                wrapper_class = "home-page"
                
            wrapped_content = f'<div class="{wrapper_class}">\n{html_content}\n</div>'
            
            template_name = page_item.get('template', 'base.html')
            template = jinja_env.get_template(template_name)
            full_html = template.render(
                config=config, 
                page_title=page_title, 
                content_html=wrapped_content, 
                active_slug=slug
            )
            
            with open(output_filepath, 'w', encoding='utf-8') as f:
                f.write(full_html)
            print(f"Generated page: {slug}")

def slugify(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\-]+', '-', text)
    text = re.sub(r'\-+', '-', text).strip('-')
    return text

def process_dynamic_entries(content_dir, output_dir, config, jinja_env):
    dynamic_items = config.get('dynamic', [])
    for dynamic_item in dynamic_items:
        folder = dynamic_item.get('folder')
        if not folder:
            continue
            
        source_dir = os.path.join(content_dir, folder)
        if not os.path.exists(source_dir):
            continue

        section_title = dynamic_item.get('title', folder.title())
        section_slug = dynamic_item.get('slug', slugify(section_title))
        section_description = dynamic_item.get('description', '')
        
        templates_cfg = dynamic_item.get('templates', {})
        base_template_name = templates_cfg.get('base', 'base.html')
        entry_template_name = templates_cfg.get('entry', 'entry.html')
        listing_template_name = templates_cfg.get('listing', 'listing.html')

        entries = []
        
        # Parse all entries
        for filename in os.listdir(source_dir):
            if not filename.endswith('.md'):
                continue
                
            filepath = os.path.join(source_dir, filename)
            metadata, html_content = parse_markdown_file(filepath)
            
            title = metadata.get('title', 'Untitled')
            date_str = metadata.get('date', '')
            tags = metadata.get('tags', [])
            
            # Use filename without date prefix as slug if possible
            match = re.match(r'^\d{4}-\d{2}-\d{2}-(.*)\.md$', filename)
            if match:
                slug = match.group(1)
            else:
                slug = filename[:-3]
                
            entries.append({
                'title': title,
                'date': date_str,
                'tags': tags,
                'slug': slug,
                'html': html_content,
                'filepath': filepath
            })
            
            # Generate individual page
            entry_output_dir = os.path.join(output_dir, section_slug, slug)
            os.makedirs(entry_output_dir, exist_ok=True)
            
            entry_template = jinja_env.get_template(entry_template_name)
            entry_content = entry_template.render(
                date_str=date_str,
                title=title,
                tags=tags,
                html_content=html_content,
                section_slug=section_slug,
                section_title=section_title
            )
            
            template = jinja_env.get_template(base_template_name)
            full_html = template.render(
                config=config, 
                page_title=title, 
                content_html=entry_content, 
                active_slug=section_slug
            )
            with open(os.path.join(entry_output_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(full_html)

        # Sort entries by date descending
        entries.sort(key=lambda x: x['date'], reverse=True)
        
        # Pagination
        items_per_page = 10
        total_pages = ceil(len(entries) / items_per_page) if entries else 1
        
        for page_num in range(1, total_pages + 1):
            start_idx = (page_num - 1) * items_per_page
            end_idx = min(start_idx + items_per_page, len(entries))
            page_entries = entries[start_idx:end_idx]
            
            listing_template = jinja_env.get_template(listing_template_name)
            listing_html = listing_template.render(
                section_title=section_title,
                section_description=section_description,
                page_entries=page_entries,
                section_slug=section_slug,
                current_page=page_num,
                total_pages=total_pages
            )
            
            # Determine output directory for this page
            if page_num == 1:
                page_output_dir = os.path.join(output_dir, section_slug)
            else:
                page_output_dir = os.path.join(output_dir, section_slug, 'page', str(page_num))
                
            os.makedirs(page_output_dir, exist_ok=True)
            
            template = jinja_env.get_template(base_template_name)
            full_html = template.render(
                config=config, 
                page_title=section_title, 
                content_html=listing_html, 
                active_slug=section_slug
            )
            with open(os.path.join(page_output_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(full_html)
                
        print(f"Generated {len(entries)} {folder} entries across {total_pages} pages")

def build_site(content_dir, output_dir):
    print(f"Building site from {content_dir} to {output_dir}...")
    
    # Load config and Jinja environment
    config = load_config(content_dir)
    jinja_env = setup_jinja_env(content_dir)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Copy static assets
    static_src = os.path.join(content_dir, 'static')
    static_dst = os.path.join(output_dir, 'static')
    if os.path.exists(static_src):
        if os.path.exists(static_dst):
            shutil.rmtree(static_dst)
        shutil.copytree(static_src, static_dst)
        print("Copied static assets")
        
    # Process regular pages
    process_regular_pages(content_dir, output_dir, config, jinja_env)
    
    # Process dynamic entries
    process_dynamic_entries(content_dir, output_dir, config, jinja_env)
    
    print("Build complete!")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate.py <content_dir> [output_dir]")
        sys.exit(1)
        
    content_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "public"
    
    build_site(content_dir, output_dir)
