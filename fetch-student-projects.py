#!/usr/bin/env python3
"""
Automatically fetch and display student projects from GitHub Classroom repositories.
This script scans the KinkaidEMSI organization for student project repositories
and generates an updated showcase page.
"""

import json
import subprocess
import sys
from typing import List, Dict
import re

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
        print(f"Error running gh command: {e.stderr}", file=sys.stderr)
        return ""

def get_student_repos(project_num: int) -> List[Dict[str, str]]:
    """Fetch all student repositories for a specific project."""
    print(f"🔍 Fetching Project {project_num} repositories...")
    
    # Search patterns for both project types
    if project_num == 1:
        pattern = "project-1-personal-website"
    else:
        pattern = "project-2"
    
    # Get all repos from the org
    output = run_gh_command(['api', '/orgs/KinkaidEMSI/repos', '--paginate'])
    if not output:
        return []
    
    repos = json.loads(output)
    student_projects = []
    
    for repo in repos:
        name = repo.get('name', '')
        
        # Skip template/starter repos
        if 'starter' in name.lower() or 'template' in name.lower():
            continue
        
        # Match project pattern
        if pattern in name.lower():
            # Extract student username from repo name
            # Format: project-1-personal-website-USERNAME
            parts = name.split('-')
            if len(parts) >= 4:
                username = parts[-1]
                
                # Check if GitHub Pages is enabled
                pages_output = run_gh_command(['api', f'/repos/KinkaidEMSI/{name}/pages'])
                has_pages = bool(pages_output and 'html_url' in pages_output)
                
                if has_pages:
                    pages_data = json.loads(pages_output)
                    pages_url = pages_data.get('html_url', '')
                    
                    student_projects.append({
                        'name': username.replace('-', ' ').title(),
                        'username': username,
                        'repo_name': name,
                        'repo_url': f"https://github.com/KinkaidEMSI/{name}",
                        'pages_url': pages_url,
                        'description': f"A creative {'website' if project_num == 1 else 'interactive app'} by {username}"
                    })
                    print(f"  ✓ Found: {username}")
    
    print(f"✅ Found {len(student_projects)} projects with GitHub Pages enabled\n")
    return student_projects

def generate_project_cards(projects: List[Dict[str, str]], project_num: int) -> str:
    """Generate HTML for project cards."""
    cards_html = []
    
    for project in projects:
        card_html = f"""
                <div class="project-card">
                    <h3>{project['name']}</h3>
                    <p class="student-name">@{project['username']}</p>
                    <p class="project-description">
                        {project['description']}
                    </p>
                    <div class="project-links">
                        <a href="{project['pages_url']}" class="btn btn-primary" target="_blank">View {'Site' if project_num == 1 else 'App'}</a>
                        <a href="{project['repo_url']}" class="btn btn-secondary" target="_blank">Code</a>
                    </div>
                </div>"""
        cards_html.append(card_html)
    
    # Add "add your project" card
    cards_html.append("""
                <div class="project-card add-project-card">
                    <div class="add-icon">+</div>
                    <p>Add Your Project</p>
                    <p class="add-instructions">Enable GitHub Pages on your repo!</p>
                </div>""")
    
    return "\n".join(cards_html)

def generate_html(project1_cards: str, project2_cards: str) -> str:
    """Generate the complete HTML file."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>VibeCoding 2026 - Student Projects</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
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

        /* Navigation */
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

        /* Hero */
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

        /* Container */
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }}

        /* Projects Section */
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

        /* Project Cards Grid */
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

        /* Add Project Card */
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

        /* Footer */
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

        /* Responsive */
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
    <!-- Navigation -->
    <nav>
        <a href="https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/" class="nav-brand">
            VIBECODING 2026
        </a>
        <div class="nav-links">
            <a href="https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/">Course Home</a>
            <a href="https://github.com/KinkaidEMSI/vibecoding-student-showcase">GitHub</a>
        </div>
    </nav>

    <!-- Hero -->
    <div class="hero">
        <h1><span class="emoji">🎨</span> Student Project Showcase</h1>
        <p>Amazing work from VibeCoding 2026 students at Kinkaid School</p>
        <div class="hero-stats">
            <div class="stat">
                <div class="stat-num" id="project1-count">0</div>
                <div class="stat-label">Personal Websites</div>
            </div>
            <div class="stat">
                <div class="stat-num" id="project2-count">0</div>
                <div class="stat-label">Interactive Apps</div>
            </div>
        </div>
    </div>

    <!-- Main Content -->
    <div class="container">
        <!-- Project 1 Section -->
        <section class="projects-section">
            <div class="section-header">
                <div class="section-icon">📄</div>
                <h2 class="section-title">Project 1: Personal Websites</h2>
            </div>
            <div class="projects-grid" id="project1-grid">
{project1_cards}
            </div>
        </section>

        <!-- Project 2 Section -->
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

    <!-- Footer -->
    <footer>
        <p><strong>VibeCoding 2026</strong> | Kinkaid School</p>
        <p><a href="https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/">View Course Materials</a></p>
        <p style="margin-top: 1rem; font-size: 0.85rem; opacity: 0.7;">
            Last updated: <span id="update-time">{{UPDATE_TIME}}</span>
        </p>
    </footer>

    <script>
        // Update project counts
        const project1Cards = document.querySelectorAll('#project1-grid .project-card:not(.add-project-card)');
        const project2Cards = document.querySelectorAll('#project2-grid .project-card:not(.add-project-card)');
        
        document.getElementById('project1-count').textContent = project1Cards.length;
        document.getElementById('project2-count').textContent = project2Cards.length;

        // Add project card click handler
        document.querySelectorAll('.add-project-card').forEach(card => {{
            card.addEventListener('click', () => {{
                window.open('https://github.com/KinkaidEMSI/vibecoding-student-showcase#-how-to-add-your-project', '_blank');
            }});
        }});
    </script>
</body>
</html>'''

def main():
    """Main function to generate the showcase page."""
    print("🚀 VibeCoding Student Showcase Generator\n")
    
    # Fetch projects
    project1_repos = get_student_repos(1)
    project2_repos = get_student_repos(2)
    
    # Generate HTML cards
    print("📝 Generating HTML...")
    project1_cards = generate_project_cards(project1_repos, 1)
    project2_cards = generate_project_cards(project2_repos, 2)
    
    # Get current timestamp
    from datetime import datetime
    update_time = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    # Generate complete HTML
    html_content = generate_html(project1_cards, project2_cards)
    html_content = html_content.replace('{update_time}', update_time)
    
    # Write to file
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Generated index.html successfully!")
    print(f"   • Project 1: {len(project1_repos)} websites")
    print(f"   • Project 2: {len(project2_repos)} apps")
    print(f"   • Total: {len(project1_repos) + len(project2_repos)} student projects\n")
    print("💡 Next step: git commit and push to update the live site!")

if __name__ == '__main__':
    main()
