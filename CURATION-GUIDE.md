# 🎯 Showcase Curation Guide

You now have **full control** over which projects appear on the showcase!

## How It Works

1. **`discover` mode** - Finds all available student projects
2. **`showcase.json`** - You edit this to control what shows
3. **`generate` mode** - Builds the showcase from your curated list

---

## Quick Start

### 1. Discover Available Projects

```bash
python3 manage-showcase.py discover
```

This shows:
- All projects with GitHub Pages enabled
- Which ones are NEW (not in your showcase yet)
- Their URLs so you can preview them

Example output:
```
🆕 New Project 1 websites (not in showcase):
   • Sammy (@smpwell)
     https://example.github.io/project/
```

### 2. Edit showcase.json

Open `showcase.json` and add/edit projects:

```json
{
  "projects": {
    "project1": [
      {
        "username": "smpwell",
        "name": "Sammy",
        "description": "Creative website with amazing animations",
        "enabled": true
      },
      {
        "username": "another-student",
        "name": "Another Student",
        "description": "Cool project",
        "enabled": false
      }
    ],
    "project2": []
  }
}
```

**Control options:**
- `"enabled": true` - Project shows on showcase
- `"enabled": false` - Project hidden (but saved for later)
- `"description"` - Custom description (be specific!)
- `"name"` - Display name for the student

### 3. Generate the Showcase

```bash
python3 manage-showcase.py generate
```

This builds `index.html` with ONLY the enabled projects.

### 4. Publish

```bash
git add showcase.json index.html
git commit -m "Update showcase: added 3 new projects"
git push
```

Done! Live in ~2 minutes.

---

## Common Workflows

### Adding a New Project

1. Run `discover` to see new projects
2. Preview the project URL in your browser
3. If it's good, add it to `showcase.json` with `"enabled": true`
4. Run `generate`
5. Commit and push

### Hiding a Project (Without Deleting It)

In `showcase.json`, set:
```json
"enabled": false
```

The project stays in your file but won't show on the site.

### Changing Project Description

Edit the `"description"` field in `showcase.json`:
```json
"description": "Interactive quiz about space with score tracking"
```

Be descriptive! This is what visitors see.

### Reordering Projects

Projects appear in the order they're listed in `showcase.json`. Just move them around:

```json
"project1": [
  {"username": "third-to-show", ...},
  {"username": "first-to-show", ...},
  {"username": "second-to-show", ...}
]
```

---

## Tips

### Preview Before Adding
Always visit the project URL before enabling it. Check:
- Does it load properly?
- Is it complete enough to showcase?
- Is the quality up to standard?

### Use Good Descriptions
Instead of: "Personal website by Sarah"
Write: "Creative portfolio with interactive photo gallery and blog"

### Keep Disabled Projects
When you set `"enabled": false`, the project info stays in the file. This is useful for:
- Projects that aren't quite ready yet
- Projects you want to rotate in/out
- Keeping a record of all submissions

### Regular Updates
Run `discover` periodically to find new projects:
```bash
# Every few days or when students submit
python3 manage-showcase.py discover
```

---

## Example showcase.json

```json
{
  "projects": {
    "project1": [
      {
        "username": "pavangud",
        "name": "Pavan",
        "description": "Interactive portfolio with smooth animations and project gallery",
        "enabled": true
      },
      {
        "username": "NIcolechen977",
        "name": "Nicole Chen",
        "description": "Clean, modern design with blog and contact form",
        "enabled": true
      },
      {
        "username": "student-incomplete",
        "name": "Student",
        "description": "Work in progress - not ready yet",
        "enabled": false
      }
    ],
    "project2": [
      {
        "username": "ajarkyn",
        "name": "Ajarkyn",
        "description": "Interactive quiz game about world geography with score tracking",
        "enabled": true
      }
    ]
  }
}
```

---

## Troubleshooting

**Q: A project shows in discover but won't generate**
- Check that GitHub Pages is actually enabled on their repo
- Verify the username matches exactly (case-sensitive)

**Q: I want to add a project manually (not via discover)**
- Just add it to `showcase.json` with all required fields
- Make sure the username exactly matches their GitHub repo name

**Q: How do I remove a project completely?**
- Delete the entire entry from `showcase.json`
- Or set `"enabled": false` to hide it

**Q: Can I change the order projects appear?**
- Yes! Just reorder them in `showcase.json`

---

## Commands Summary

```bash
# Find new projects
python3 manage-showcase.py discover

# Build showcase from your curated list
python3 manage-showcase.py generate

# Publish changes
git add showcase.json index.html
git commit -m "Update showcase"
git push
```

---

**You're in control!** Only the projects you approve and enable will appear on the showcase.
