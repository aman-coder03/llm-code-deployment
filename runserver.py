#!/usr/bin/env python3
"""
Server startup script for the LLM Code Deployment API.
Starts FastAPI backend on port 7860, compatible with Hugging Face Spaces Docker deployments.
"""

import uvicorn
from pathlib import Path

if __name__ == "__main__":

    uvicorn.run(
        "app.main:app",    
        host="0.0.0.0",
        port=7860,
        reload=False,
        log_level="info"
    )
