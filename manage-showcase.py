#!/usr/bin/env python3
"""
VibeCoding Student Showcase Manager
Two modes:
  1. discover - Find all available projects with GitHub Pages
  2. generate - Build showcase from curated showcase.json
"""

import json
import subprocess
import sys
from typing import List, Dict
from datetime import datetime

ORGS = ['KinkaidEMSI', 'EMSI-Vibe-Coding']

def run_gh_command(args: List[str]) -> str:
    """Run a gh CLI command and return the output."""
    try:
        result = subprocess.run(
            ['gh'] + args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}", file=sys.stderr)
        return ""

def load_student_names() -> Dict[str, str]:
    """Load student name mappings."""
    try:
        with open('students.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def discover_projects(project_num: int, student_names: Dict[str, str]) -> List[Dict[str, str]]:
    """Discover all available projects with GitHub Pages enabled."""
    print(f"🔍 Discovering Project {project_num} repositories...")
    
    if project_num == 1:
        patterns = ["project-1-personal-website", "project1"]
    else:
        patterns = ["project-2", "project2", "interactive"]
    
    projects = []
    seen = set()
    
    for org in ORGS:
        print(f"   Scanning {org}...")
        output = run_gh_command(['api', f'/orgs/{org}/repos', '--paginate'])
        if not output:
            continue
        
        repos = json.loads(output)
        
        for repo in repos:
            name = repo.get('name', '').lower()
            repo_name = repo.get('name', '')
            
            if any(skip in name for skip in ['starter', 'template', 'materials', 'setup-and-first-push']):
                continue
            
            if any(pattern in name for pattern in patterns):
                parts = repo_name.split('-')
                if len(parts) >= 2:
                    username = parts[-1]
                    
                    if username in seen:
                        continue
                    
                    pages_output = run_gh_command(['api', f'/repos/{org}/{repo_name}/pages'])
                    has_pages = bool(pages_output and 'html_url' in pages_output)
                    
                    if has_pages:
                        pages_data = json.loads(pages_output)
                        pages_url = pages_data.get('html_url', '')
                        display_name = student_names.get(username, username.replace('-', ' ').title())
                        
                        projects.append({
                            'username': username,
                            'name': display_name,
                            'repo_name': repo_name,
                            'org': org,
                            'pages_url': pages_url,
                            'description': f"{'Personal website' if project_num == 1 else 'Interactive app'} by {display_name}"
                        })
                        
                        seen.add(username)
                        print(f"  ✓ {display_name} (@{username})")
    
    return sorted(projects, key=lambda x: x['name'])

def discover_mode():
    """Discover all available projects and show what can be showcased."""
    print("🚀 VibeCoding Showcase - Discovery Mode")
    print(f"📚 Scanning: {', '.join(ORGS)}\n")
    
    student_names = load_student_names()
    
    project1 = discover_projects(1, student_names)
    project2 = discover_projects(2, student_names)
    
    print(f"\n📊 Discovery Summary:")
    print(f"   • Project 1: {len(project1)} websites available")
    print(f"   • Project 2: {len(project2)} apps available")
    print(f"   • Total: {len(project1) + len(project2)} projects\n")
    
    # Load current showcase config
    try:
        with open('showcase.json', 'r') as f:
            showcase = json.load(f)
    except FileNotFoundError:
        showcase = {'projects': {'project1': [], 'project2': []}}
    
    # Show new projects not in showcase
    current_p1 = {p['username'] for p in showcase['projects']['project1']}
    current_p2 = {p['username'] for p in showcase['projects']['project2']}
    
    new_p1 = [p for p in project1 if p['username'] not in current_p1]
    new_p2 = [p for p in project2 if p['username'] not in current_p2]
    
    if new_p1:
        print("🆕 New Project 1 websites (not in showcase):")
        for p in new_p1:
            print(f"   • {p['name']} (@{p['username']})")
            print(f"     {p['pages_url']}")
        print()
    
    if new_p2:
        print("🆕 New Project 2 apps (not in showcase):")
        for p in new_p2:
            print(f"   • {p['name']} (@{p['username']})")
            print(f"     {p['pages_url']}")
        print()
    
    if not new_p1 and not new_p2:
        print("✅ All available projects are already in showcase.json")
        print()
    
    print("💡 To add projects to the showcase:")
    print("   1. Edit showcase.json")
    print("   2. Set 'enabled': true for projects you want to show")
    print("   3. Customize descriptions")
    print("   4. Run: python3 manage-showcase.py generate")

def load_showcase_config() -> Dict:
    """Load curated project list from showcase.json."""
    try:
        with open('showcase.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: showcase.json not found!")
        print("   Run 'python3 manage-showcase.py discover' first")
        sys.exit(1)

def get_project_url(username: str, project_num: int) -> tuple:
    """Find the GitHub Pages URL and repo for a username."""
    if project_num == 1:
        patterns = ["project-1-personal-website", "project1"]
    else:
        patterns = ["project-2", "project2", "interactive"]
    
    for org in ORGS:
        output = run_gh_command(['api', f'/orgs/{org}/repos', '--paginate'])
        if not output:
            continue
        
        repos = json.loads(output)
        
        for repo in repos:
            repo_name = repo.get('name', '')
            if username.lower() in repo_name.lower() and any(p in repo_name.lower() for p in patterns):
                pages_output = run_gh_command(['api', f'/repos/{org}/{repo_name}/pages'])
                if pages_output and 'html_url' in pages_output:
                    pages_data = json.loads(pages_output)
                    return pages_data.get('html_url', ''), f"https://github.com/{org}/{repo_name}"
    
    return None, None

def generate_project_cards(projects: List[Dict], project_num: int) -> str:
    """Generate HTML for curated project cards."""
    cards_html = []
    
    for project in projects:
        if not project.get('enabled', True):
            continue
        
        # Use direct URLs from showcase.json if available, otherwise query GitHub
        if 'pages_url' in project and 'repo' in project:
            pages_url = project['pages_url']
            repo_url = f"https://github.com/{project['repo']}"
        else:
            # Get current URLs from GitHub
            pages_url, repo_url = get_project_url(project['username'], project_num)
        
        if not pages_url:
            print(f"  ⚠️  Warning: No GitHub Pages found for {project['name']} (@{project['username']})")
            continue
        
        card_html = f"""                <div class="project-card">
                    <h3>{project['name']}</h3>
                    <p class="student-name">@{project['username']}</p>
                    <p class="project-description">
                        {project['description']}
                    </p>
                    <div class="project-links">
                        <a href="{pages_url}" class="btn btn-primary" target="_blank">View {'Site' if project_num == 1 else 'App'}</a>
                        <a href="{repo_url}" class="btn btn-secondary" target="_blank">Code</a>
                    </div>
                </div>"""
        cards_html.append(card_html)
    
    # Add "add your project" card
    cards_html.append("""                <div class="project-card add-project-card">
                    <div class="add-icon">+</div>
                    <p>Add Your Project</p>
                    <p class="add-instructions">Enable GitHub Pages on your repo!</p>
                </div>""")
    
    return "\n".join(cards_html)

def generate_html(project1_cards: str, project2_cards: str, update_time: str, p1_count: int, p2_count: int) -> str:
    """Generate the complete HTML file."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeCoding 2026 - Student Projects</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=IBM+Plex+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --gold: #FFC61E;
            --gold-dark: #E5A800;
            --purple: #59118E;
            --purple-light: #7B2FBE;
            --dark: #1A1A1A;
            --mid: #555;
            --border: #E0E0E0;
            --white: #fff;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: var(--dark);
            background: var(--white);
        }}

        nav {{
            background: var(--purple);
            padding: 0 2rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
            height: 52px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}

        .nav-brand {{
            font-weight: 800;
            font-size: 0.9rem;
            color: var(--gold);
            letter-spacing: 0.04em;
            text-decoration: none;
        }}

        .nav-links {{
            display: flex;
            gap: 1rem;
        }}

        .nav-links a {{
            color: rgba(255,255,255,0.8);
            text-decoration: none;
            font-size: 0.82rem;
            font-weight: 500;
            padding: 6px 12px;
            border-radius: 4px;
            transition: all 0.15s;
        }}

        .nav-links a:hover {{
            background: rgba(255,255,255,0.12);
            color: var(--white);
        }}

        .hero {{
            background: var(--purple);
            padding: 3rem 2rem 2.5rem;
            text-align: center;
            border-bottom: 4px solid var(--gold);
        }}

        .hero h1 {{
            font-size: clamp(2rem, 4vw, 2.8rem);
            font-weight: 900;
            color: var(--white);
            margin-bottom: 0.5rem;
        }}

        .hero .emoji {{
            color: var(--gold);
        }}

        .hero p {{
            color: rgba(255,255,255,0.7);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto;
        }}

        .hero-stats {{
            display: flex;
            gap: 3rem;
            justify-content: center;
            margin-top: 2rem;
            flex-wrap: wrap;
        }}

        .stat {{
            text-align: center;
        }}

        .stat-num {{
            font-size: 2.5rem;
            font-weight: 900;
            color: var(--gold);
            line-height: 1;
        }}

        .stat-label {{
            font-size: 0.75rem;
            color: rgba(255,255,255,0.6);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-top: 4px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}

        .projects-section {{
            margin-bottom: 4rem;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 2rem;
            padding-bottom: 0.75rem;
            border-bottom: 3px solid var(--gold);
        }}

        .section-icon {{
            background: var(--gold);
            color: var(--dark);
            font-size: 1.5rem;
            width: 42px;
            height: 42px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .section-title {{
            font-size: 1.5rem;
            font-weight: 800;
            color: var(--purple);
            text-transform: uppercase;
            letter-spacing: 0.02em;
        }}

        .projects-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }}

        .project-card {{
            background: var(--white);
            border: 2px solid var(--border);
            border-radius: 12px;
            padding: 1.5rem;
            transition: all 0.3s ease;
        }}

        .project-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 24px rgba(89, 17, 142, 0.15);
            border-color: var(--purple-light);
        }}

        .project-card h3 {{
            color: var(--purple);
            margin-bottom: 0.3rem;
            font-size: 1.3rem;
            font-weight: 700;
        }}

        .student-name {{
            color: var(--mid);
            font-size: 0.85rem;
            margin-bottom: 1rem;
            font-family: 'IBM Plex Mono', monospace;
        }}

        .project-description {{
            margin-bottom: 1.25rem;
            color: var(--mid);
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .project-links {{
            display: flex;
            gap: 0.75rem;
        }}

        .btn {{
            padding: 0.6rem 1.1rem;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
            display: inline-block;
            text-align: center;
            flex: 1;
        }}

        .btn-primary {{
            background: var(--purple);
            color: var(--white);
        }}

        .btn-primary:hover {{
            background: var(--purple-light);
        }}

        .btn-secondary {{
            background: var(--gold);
            color: var(--dark);
        }}

        .btn-secondary:hover {{
            background: var(--gold-dark);
        }}

        .add-project-card {{
            border: 3px dashed var(--border);
            background: #fafafa;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            min-height: 200px;
            cursor: pointer;
            transition: all 0.3s ease;
        }}

        .add-project-card:hover {{
            background: #f0f0f0;
            border-color: var(--purple);
        }}

        .add-icon {{
            font-size: 3rem;
            color: var(--gold);
            margin-bottom: 0.5rem;
            font-weight: 300;
        }}

        .add-project-card p {{
            color: var(--mid);
            font-weight: 600;
            margin-bottom: 0.25rem;
        }}

        .add-instructions {{
            font-size: 0.8rem;
            color: var(--mid);
            opacity: 0.7;
        }}

        footer {{
            background: var(--purple);
            color: white;
            text-align: center;
            padding: 2rem;
            margin-top: 3rem;
        }}

        footer p {{
            margin-bottom: 0.5rem;
        }}

        footer a {{
            color: var(--gold);
            text-decoration: none;
            font-weight: 600;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .hero h1 {{
                font-size: 1.8rem;
            }}

            .projects-grid {{
                grid-template-columns: 1fr;
            }}

            .nav-links {{
                gap: 0.5rem;
            }}
        }}
    </style>
</head>
<body>
    <nav>
        <a href="https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/" class="nav-brand">
            VIBECODING 2026
        </a>
        <div class="nav-links">
            <a href="https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/">Course Home</a>
            <a href="https://github.com/KinkaidEMSI/vibecoding-student-showcase">GitHub</a>
        </div>
    </nav>

    <div class="hero">
        <h1><span class="emoji">🎨</span> Student Project Showcase</h1>
        <p>Curated projects from VibeCoding 2026 students</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; opacity: 0.6;">Engineer, Math & Science Institute • Kinkaid School</p>
        <div class="hero-stats">
            <div class="stat">
                <div class="stat-num">{p1_count}</div>
                <div class="stat-label">Personal Websites</div>
            </div>
            <div class="stat">
                <div class="stat-num">{p2_count}</div>
                <div class="stat-label">Interactive Apps</div>
            </div>
        </div>
    </div>

    <div class="container">
        <section class="projects-section">
            <div class="section-header">
                <div class="section-icon">📄</div>
                <h2 class="section-title">Project 1: Personal Websites</h2>
            </div>
            <div class="projects-grid" id="project1-grid">
{project1_cards}
            </div>
        </section>

        <section class="projects-section">
            <div class="section-header">
                <div class="section-icon">🎮</div>
                <h2 class="section-title">Project 2: Interactive Apps</h2>
            </div>
            <div class="projects-grid" id="project2-grid">
{project2_cards}
            </div>
        </section>
    </div>

    <footer>
        <p><strong>VibeCoding 2026</strong> | Kinkaid School</p>
        <p>Engineer, Math & Science Institute</p>
        <p><a href="https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/">View Course Materials</a></p>
        <p style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.7;">
            Last updated: {update_time}
        </p>
    </footer>
</body>
</html>'''

def generate_mode():
    """Generate showcase from curated showcase.json."""
    print("🚀 VibeCoding Showcase - Generate Mode")
    print("📝 Building from showcase.json...\n")
    
    showcase = load_showcase_config()
    
    project1_list = [p for p in showcase['projects']['project1'] if p.get('enabled', True)]
    project2_list = [p for p in showcase['projects']['project2'] if p.get('enabled', True)]
    
    print(f"📊 Curated projects:")
    print(f"   • Project 1: {len(project1_list)} websites (enabled)")
    print(f"   • Project 2: {len(project2_list)} apps (enabled)")
    print()
    
    # Generate HTML
    project1_cards = generate_project_cards(project1_list, 1)
    project2_cards = generate_project_cards(project2_list, 2)
    
    update_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    html_content = generate_html(project1_cards, project2_cards, update_time, len(project1_list), len(project2_list))
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated index.html successfully!")
    print(f"\n💡 Next: git add index.html && git commit -m 'Update showcase' && git push")

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 manage-showcase.py discover   # Find all available projects")
        print("  python3 manage-showcase.py generate   # Build showcase from showcase.json")
        sys.exit(1)
    
    mode = sys.argv[1]
    
    if mode == 'discover':
        discover_mode()
    elif mode == 'generate':
        generate_mode()
    else:
        print(f"Unknown mode: {mode}")
        print("Use 'discover' or 'generate'")
        sys.exit(1)

if __name__ == '__main__':
    main()
