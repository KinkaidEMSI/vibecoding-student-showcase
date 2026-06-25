# VibeCoding 2026 - Student Project Showcase

✨ **Live Site:** https://kinkaidemsi.github.io/vibecoding-student-showcase/

This page automatically shows all VibeCoding student projects from the **Engineer, Math & Science Institute** at Kinkaid School that have GitHub Pages enabled!

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

4. **That's it!** Your project will automatically appear on the showcase page within a few hours.

### How It Works

The showcase page runs an automatic script that:
- Scans student repositories in **both** KinkaidEMSI and EMSI-Vibe-Coding organizations
- Finds projects with GitHub Pages enabled
- Displays them automatically with your proper name

**You don't need to:**
- Fork anything
- Create pull requests  
- Edit any HTML
- Fill out forms

**You just need to:** Enable GitHub Pages on your project repository!

---

## 🛠️ For Instructors

### Update the Showcase

When you want to refresh the showcase with the latest student projects:

```bash
# Clone the repo (first time only)
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
- Scans **KinkaidEMSI** and **EMSI-Vibe-Coding** organizations
- Finds repos matching project patterns
- Checks which ones have GitHub Pages enabled
- Uses proper student names from `students.json`
- Generates an updated index.html with all projects
- Shows project counts and stats

### Update Student Names

Edit `students.json` to add or update student display names:

```json
{
  "github-username": "Display Name",
  "pavangud": "Pavan",
  "NIcolechen977": "Nicole Chen"
}
```

### Customize Project Matching

Edit `fetch-student-projects.py` and modify the patterns in `get_student_repos()`:

```python
# Current patterns
if project_num == 1:
    patterns = ["project-1-personal-website", "project1"]
else:
    patterns = ["project-2", "project2", "interactive"]
```

### Add/Remove Organizations

Edit the `ORGS` list at the top of `fetch-student-projects.py`:

```python
ORGS = ['KinkaidEMSI', 'EMSI-Vibe-Coding', 'AnotherOrg']
```

---

## 📚 Links

- **Showcase:** https://kinkaidemsi.github.io/vibecoding-student-showcase/
- **Course Materials:** https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/
- **Repository:** https://github.com/KinkaidEMSI/vibecoding-student-showcase
- **Student Guide:** [STUDENT-GUIDE.md](STUDENT-GUIDE.md)

---

## 🎓 Current Students

The showcase automatically tracks projects from these students:

Ajarkyn, Amelie, Andy, Audrey, Aurora, Bryan, Diego, Emika, Francisco, GS Blackthorn, G Tran, Han, Kangkang Wang, Mezu Uwalaka, Naima Beye, Najma, N Hammen, Nicole Chen, Pavan, Ram, Rebecca, Saloni, Sammy, Vladimir Lopez

---

Built with 💜 for VibeCoding 2026 at **Kinkaid School - Engineer, Math & Science Institute**
