# LLM Code Deployment

## Overview
This project is an automated system for building, deploying, updating, and evaluating student projects using **LLM-assisted code generation** and **GitHub Pages**.  

The workflow consists of three main phases:

1. **Build:** Students receive a task brief, generate a minimal app using an LLM, deploy it to GitHub Pages, and notify an evaluation API.  
2. **Evaluate:** Instructors run automated static, dynamic, and LLM-based checks, store results, and optionally send a follow-up task.  
3. **Revise:** Students update the app based on the new brief or checks, redeploy to GitHub Pages, and notify the evaluation API again.  

---

## Features

- LLM-powered app generation based on a JSON task brief
- Automatic GitHub repo creation and commit management
- Full GitHub Pages deployment
- Attachment handling (images, CSV, JSON) using **data URIs**
- Automatic evaluation notifications
- Secure secret validation
- Round-based workflow (Round 1 = initial build, Round 2 = updates/refactor)

---

