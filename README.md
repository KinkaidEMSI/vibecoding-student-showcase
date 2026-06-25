# VibeCoding 2026 - Student Project Showcase

✨ **Live Site:** https://kinkaidemsi.github.io/vibecoding-student-showcase/

A curated showcase of outstanding student projects from the **Engineer, Math & Science Institute** at Kinkaid School.

---

## 🎯 For Instructors: Full Control

You decide which projects appear on the showcase!

### Quick Workflow

```bash
# 1. Find all available projects
python3 manage-showcase.py discover

# 2. Edit showcase.json to control what shows
#    - Set "enabled": true for projects to show
#    - Set "enabled": false to hide
#    - Customize descriptions

# 3. Generate the showcase
python3 manage-showcase.py generate

# 4. Publish
git add showcase.json index.html
git commit -m "Update showcase"
git push
```

**See [CURATION-GUIDE.md](CURATION-GUIDE.md) for complete instructions.**

### What You Control

- ✅ Which projects appear (enable/disable any project)
- ✅ Project descriptions (write custom descriptions)
- ✅ Display order (reorder projects in showcase.json)
- ✅ Quality standards (preview before approving)

---

## 📝 For Students: Getting Your Project Showcased

### Step 1: Enable GitHub Pages

1. Go to your project repository on GitHub
2. Click **Settings** → **Pages**
3. Select **main** branch → **Save**
4. Wait for your site to build

### Step 2: That's It!

Your instructor will discover your project and may add it to the showcase if it meets the quality standards.

**Tip:** Make sure your project is polished and complete before enabling GitHub Pages!

---

## 📂 Repository Structure

- **`showcase.json`** - Curated list of projects (YOU CONTROL THIS)
- **`manage-showcase.py`** - Management script (discover/generate)
- **`index.html`** - Generated showcase page (auto-created)
- **`students.json`** - Student display names
- **`CURATION-GUIDE.md`** - Complete curation instructions

---

## 🔍 Discover vs Generate

### `discover` - Find What's Available
- Scans KinkaidEMSI and EMSI-Vibe-Coding orgs
- Shows all projects with GitHub Pages enabled
- Highlights NEW projects not yet in your showcase
- Gives you URLs to preview

### `generate` - Build the Showcase
- Reads your curated `showcase.json`
- Only shows projects with `"enabled": true`
- Creates `index.html` with your selections
- Ready to commit and publish

---

## 💡 Example showcase.json

```json
{
  "projects": {
    "project1": [
      {
        "username": "pavangud",
        "name": "Pavan",
        "description": "Interactive portfolio with smooth animations",
        "enabled": true
      },
      {
        "username": "incomplete-student",
        "name": "Student",
        "description": "Not ready yet",
        "enabled": false
      }
    ],
    "project2": []
  }
}
```

---

## 🎓 Organizations Tracked

- **KinkaidEMSI** (legacy)
- **EMSI-Vibe-Coding** (current)

The script automatically scans both organizations.

---

## 📚 Links

- **Showcase:** https://kinkaidemsi.github.io/vibecoding-student-showcase/
- **Course Materials:** https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/
- **Curation Guide:** [CURATION-GUIDE.md](CURATION-GUIDE.md)
- **Student Guide:** [STUDENT-GUIDE.md](STUDENT-GUIDE.md)

---

Built with 💜 for VibeCoding 2026 at **Kinkaid School - Engineer, Math & Science Institute**
