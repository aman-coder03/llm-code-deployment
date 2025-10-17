import logging
from typing import List
from pydantic_ai import Agent
from .models import TaskRequest, FileContext

# Configure module-level logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


async def generate_code_with_llm(request: TaskRequest) -> List[FileContext]:
    """
    Generates a complete static website project based on the task request
    using the LLM Agent from pydantic-ai-slim.
    Returns a list of FileContext objects with filenames and content.
    """

    # Prepare brief and attachment context
    attachments_text = ""
    if request.attachments:
        attachments_text = "\nAttachments:\n" + "\n".join(
            [f"- {att.name}: {att.url[:80]}..." for att in request.attachments]
        )
    else:
        attachments_text = "\n(No attachments were provided with the request)"

    prompt = f"""
Generate a complete static website project that is deployable on GitHub Pages.

Brief: {request.brief}

attachments (if any): {attachments_text}

Checks to be satisfied:
{f"{request.checks}" if getattr(request, "checks", None) else "(No explicit checks provided)"}

Requirements:
- Use attachments as data URIs where applicable.
- Include index.html and all necessary assets.
- Write a thorough README.md with project summary, setup, usage, code explanation, and MIT license.
- Fulfill all JS-based checks in the 'checks' section.
- Return a JSON array of objects with 'file_name' and 'file_content'.
"""

    system_prompt = """
You are a senior developer specializing in GitHub Pages static websites.

Create all necessary files (HTML, CSS, JS, assets) for deployment.
Use attachments properly.
Write a professional README.md.
Ensure all JS-based checks pass.
Return only a JSON array of objects with 'file_name' and 'file_content'.
"""

    try:
        agent = Agent(
            model="openai:gpt-5-nano",
            result_type=list,  # use plain list for async agent
            system_prompt=system_prompt
        )

        result = await agent.run(prompt)

        logger.info("Successfully generated code with LLM")

        # result.data might already be a list of dicts; convert to FileContext if needed
        files: List[FileContext] = [FileContext(**f) for f in result]
        return files

    except Exception as e:
        logger.error(f"Error generating code with LLM: {e}", exc_info=True)
        raise RuntimeError(f"LLM code generation failed: {e}") from e
