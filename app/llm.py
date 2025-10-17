import logging
from typing import List
from pydantic_ai import Agent
from .models import TaskRequest,FileContext

# Configure module-level logger
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)



async def genereate_code_with_llm(request: TaskRequest) -> List[FileContext]:

     # Prepare brief and attachment context
    attachments_text = ""
    if request.attachments and len(request.attachments) > 0:
        attachments_text = "\nAttachments:\n" + "\n".join([f"- {att.name}: {att.url[:80]}..." for att in request.attachments])
    else:
        attachments_text = "\n(No attachments were provided with the request)"

    prompt = f"""
Generate a complete static website project that is deployable on GitHub Pages.

Brief: {request.brief}

attachments (if any): {attachments_text}

Checks to be satisfied:
{f"{request.checks}" if getattr(request, "checks", None) else "(No explicit checks provided)"}


Requirements:
- Use the attachments provided (if any). For example, if a CSV file, image, or data file is attached,
  the generated site should correctly reference and use it in the codebase.
- Use data URIs as the source for attachments when embedding or referencing them (e.g., <img src="data:image/png;base64,..."> or fetch inline encoded data directly from JS).
- If attachments are present, they should be used within the project logically matching the task description.
- Provide all files necessary for deployment including at least an index.html.
- Write a thorough README.md that includes:
  - Project summary
  - Setup instructions for GitHub Pages
  - Usage guide
  - Explanation of the main code/files
  - License information (use MIT)
- Carefully read the provided "checks" section. Each listed check represents a requirement that must be fulfilled by the project files and behavior. 
- Checks can include both human-readable and programmatic JavaScript expressions.
- Implement all behaviors required so that JavaScript-based checks evaluate as true when tested.
- For checks beginning with `js:`:
  - Ensure your HTML, CSS, and JavaScript code produces behavior consistent with the JS expressions listed.
  - Implement any specified DOM updates, calculations, links, or asynchronous logic needed.
- Produce the project in such a way that every listed check passes successfully when evaluated automatically by test scripts or human reviewers.
- The project must follow industry standards for static GitHub Pages hosting.
- Return the project as a list of files with filenames and file contents.
- All code should be modern and ready to deploy without modification.
Output format:
Return only a JSON array of objects where each object has:
- "file_name": string
- "file_content": string
"""

    system_prompt = """
You are a highly experienced senior developer specializing in creating GitHub Pages-ready static websites.

Your goal is to produce a production-ready project based on the provided task brief and optional attachments.
The user may include one or more attachments, such as images, CSV data files, or other static assets encoded as Data URIs.


Specifically, ensure you do the following:

1. Process the task brief carefully to understand the required site behavior and structure.
2. If attachments are provided:
   - Treat them as first-class project assets.
   - Use `data:` URLs where appropriate (for images, CSV, JSON, etc.).
   - If a CSV or data file is attached, the project should load and use it accordingly in the site logic.
   - If images are attached, include them visually or reference them as part of the static content.
3. Create all necessary files to fully deploy a static website on GitHub Pages, including but not limited to:
   - index.html (the homepage)
   - any required CSS, JS, or asset files
   - configuration files (e.g., CNAME, if needed)
4. Write a complete, professional README.md file containing:
   - A clear project summary describing what the site does
   - Setup instructions to deploy the project on GitHub Pages step-by-step
   - Usage instructions, explaining how to use the website
   - Explanation of the key code files and their purpose
   - License information, applying the MIT license in standard format
5. Ensure all source code and resources are clean, properly structured, and follow modern best practices
6. Ensure the code Strictly fulfills every check listed in "checks" section . "checks" = explicit criteria the generated site will be tested against (either human-readable or
     programmatic checks such as JavaScript expressions beginning with `js:`).
     - Behavior and compliance:
   - Implement code so that all **JavaScript-based checks (`js:`)** evaluate to `true` 
     when the resulting page runs in a browser.
   - Satisfy any conditions mentioned in the `checks` — including DOM structure,
     CSS links (like `<link href*='bootstrap'>`), and computed dynamic values.
   - If a check includes formulas, like 
     `Math.abs(parseFloat(document.querySelector('#total-sales').textContent) - ${result}) < 0.01`,
     ensure your JavaScript logic dynamically computes matching values at runtime.
   - Include any required scripts or libraries (e.g., Bootstrap 5 from jsDelivr).
7. Format your output as a list of files, with each containing a file_name and file_content field
8. Do not include text explanations in the output; only return the code files and README as specified
9. Output format:
Return only a JSON array of objects where each object has:
- "file_name": string
- "file_content": string

The user will provide a brief describing the site functionality along with attachments (optional). Use these to guide your file generation.

Focus on quality, clarity, and correctness to deliver a ready-to-use GitHub Pages static website project.
"""

    try:
        agent = Agent(
            "openai:gpt-5-nano",
            result_type=List[FileContext],
            system_prompt=system_prompt
        )
        result = await agent.run(prompt)
        logger.info("Successfully generated code with LLM")
        # print(result.data)
        return result.data
    except Exception as e:
        # Log the error with traceback
        logger.error(f"Error generating code with LLM: {e}", exc_info=True)
        # Raise runtime error to caller or optionally return empty list/fallback output
        raise RuntimeError(f"LLM code generation failed: {e}") from e
