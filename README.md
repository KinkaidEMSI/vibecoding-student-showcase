# VibeCoding 2026 - Student Project Showcase

This repository showcases student projects from the VibeCoding 2026 course at Kinkaid School.

## 🌐 View the Showcase
Visit: **https://kinkaidemsi.github.io/vibecoding-student-showcase/**

## 📚 Course Materials
[VibeCoding 2026 Course Materials](https://kinkaidemsi.github.io/vibecoding-2026-materials/docs/)

## 🎯 Projects

### Project 1: Personal Website
Students create their own personal websites to showcase their interests, skills, and projects.

### Project 2: Interactive App
Students build interactive web applications with creative features and animations.

## ➕ How to Add Your Project

### Option 1: Submit via Pull Request (Recommended)

1. **Fork this repository**
2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/vibecoding-student-showcase.git
   cd vibecoding-student-showcase
   ```

3. **Edit `index.html`** - Add your project card:
   
   For **Project 1** (Personal Website), add this inside `<div class="projects-grid" id="project1-grid">`:
   ```html
   <div class="project-card">
       <h3>Your Name</h3>
       <p class="student-name">@your-github-username</p>
       <p class="project-description">
           Brief description of your personal website (1-2 sentences).
       </p>
       <div class="project-links">
           <a href="https://your-username.github.io/your-repo-name/" class="btn btn-primary" target="_blank">View Site</a>
           <a href="https://github.com/KinkaidEMSI/your-repo-name" class="btn btn-secondary" target="_blank">Code</a>
       </div>
   </div>
   ```
   
   For **Project 2** (Interactive App), add this inside `<div class="projects-grid" id="project2-grid">`:
   ```html
   <div class="project-card">
       <h3>Your App Name</h3>
       <p class="student-name">@your-github-username</p>
       <p class="project-description">
           Brief description of your interactive app (1-2 sentences).
       </p>
       <div class="project-links">
           <a href="https://your-username.github.io/your-app-repo/" class="btn btn-primary" target="_blank">View App</a>
           <a href="https://github.com/KinkaidEMSI/your-app-repo" class="btn btn-secondary" target="_blank">Code</a>
       </div>
   </div>
   ```

4. **Commit and push**
   ```bash
   git add index.html
   git commit -m "Add my project to showcase"
   git push origin main
   ```

5. **Create a Pull Request** on GitHub

### Option 2: Submit via Issue

Create an issue with your project information:
- Project type (1 or 2)
- Your name
- GitHub username
- Project GitHub Pages URL
- Repository URL
- Brief description

---

## 🛠️ For Instructors

### Enable GitHub Pages
1. Go to repository **Settings** > **Pages**
2. Set **Source** to `main` branch, `/` (root)
3. Save

### Review Student Submissions
Check pull requests and merge approved projects.

---

Built with 💜 for VibeCoding 2026
