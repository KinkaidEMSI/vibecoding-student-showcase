# VibeCoding 2026 - Student Project Showcase

✨ **Live Site:** https://kinkaidemsi.github.io/vibecoding-student-showcase/

This page automatically shows all VibeCoding student projects that have GitHub Pages enabled!

---

## 🎯 For Students: How to Get Your Project on the Showcase

### The Simple Version

**Your project will automatically appear on the showcase once you enable GitHub Pages.** That's it!

### Step-by-Step:

1. **Finish your project** and make sure it's working in your Codespace

2. **Push your code to GitHub**
   ```bash
   git add .
   git commit -m "Final version"
   git push
   ```

3. **Enable GitHub Pages:**
   - Go to your repository on GitHub
   - Click **Settings** (top right)
   - Click **Pages** (left sidebar)
   - Under "Branch", select **main** branch
   - Click **Save**
   - Wait 1-2 minutes for your site to build

4. **That's it!** Within a few hours, your project will automatically appear on the showcase page.

### How It Works

The showcase page runs an automatic script that:
- Scans all student repositories in the KinkaidEMSI organization
- Finds projects with GitHub Pages enabled
- Displays them automatically

**You don't need to:**
- Fork anything
- Create pull requests  
- Edit any HTML
- Fill out forms

**You just need to:** Enable GitHub Pages on your project repository!

---

## 🛠️ For Instructors

### Update the Showcase Manually

When you want to refresh the showcase with the latest student projects:

```bash
# Clone the repo
git clone https://github.com/KinkaidEMSI/vibecoding-student-showcase.git
cd vibecoding-student-showcase

# Run the update script
python3 fetch-student-projects.py

# Commit and push
git add index.html
git commit -m "Update student projects showcase"
git push
```

The script automatically:
- Fetches all student repos from the KinkaidEMSI org
- Checks which ones have GitHub Pages enabled
- Generates an updated index.html with all projects
- Shows project counts and stats

### Customize Project Matching

Edit `fetch-student-projects.py` and modify the `get_student_repos()` function to change:
- Project name patterns (currently: `project-1-personal-website` and `project-2`)
- Which repos to include/exclude
- How student names are extracted from repo names

### Manual HTML Edits

If you need to manually add/edit a project, edit `index.html` directly. Find the appropriate section (`project1-grid` or `project2-grid`) and add:

```html
<div class="project-card">
    <h3>Student Name</h3>
    <p class="student-name">@username</p>
    <p class="project-description">
        Brief project description.
    </p>
    <div class="project-links">
        <a href="PAGES_URL" class="btn btn-primary" target="_blank">View Site</a>
        <a href="REPO_URL" class="btn btn-secondary" target="_blank">Code</a>
    </div>
</div>
```

---

## 📚 Links

- **Showcase:** https://kinkaidemsi.github.io/vibecoding-student-showcase/
- **Course Materials:** https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/
- **Repository:** https://github.com/KinkaidEMSI/vibecoding-student-showcase

---

Built with 💜 for VibeCoding 2026 at Kinkaid School
