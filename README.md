---
title: LLM Code Deployment API
emoji: 🚀
colorFrom: indigo
colorTo: red
sdk: docker
sdk_version: "0.0.1"
app_file: app/main.py
pinned: false
---

Check out the configuration reference at [https://huggingface.co/docs/hub/spaces-config-reference](https://huggingface.co/docs/hub/spaces-config-reference)

## LLM Code Deployment API

This Space provides a production-grade FastAPI backend for automated application generation and deployment, as described in the LLM Code Deployment project. It supports secure secret-based access, LLM-driven app generation, automated deployment to GitHub Pages, and evaluation callbacks—built with best practices for industry and Hugging Face Spaces Docker deployments.

### Key Features

- **POST `/handle-task`**: Receives and processes app brief requests, verifies secrets, and triggers app generation workflows.
- **Dockerized Deployment**: Secure, reproducible builds using a custom Dockerfile following Hugging Face recommendations.
- **Secrets Management**: Reads secrets via Hugging Face Spaces environment for maximum security (never hardcoded).
- **GitHub Automation**: Automatically creates public repos, populates README and LICENSE, and enables GitHub Pages.

### Usage

1. Set up required Space secrets (secrets and tokens via the Spaces UI).
2. Deploy or push your code to this Space.
3. POST a task request (see `/handle-task` endpoint documentation).

### Development

See `requirements.txt` for dependencies.  
Your FastAPI entry point should be specified in `app/main.py`.

---

For further configuration options, please visit the [Spaces Configuration Reference](https://huggingface.co/docs/hub/spaces-config-reference).
