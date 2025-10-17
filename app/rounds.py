from .models import TaskRequest
from .deployer import create_github_repo, notify_evaluation_url, push_files_to_github_repo, enable_github_pages
from .llm import generate_code_with_llm

def round2():
    print("inside round 2")


async def round1(request: TaskRequest):
    try:
        repo_response = await create_github_repo(repo_name=request.task)
        repo_url = repo_response.get("html_url", "")

        files = await generate_code_with_llm(request)

        commit_sha = await push_files_to_github_repo(repo=request.task, files=files)
        
        pages_response = await enable_github_pages(repo=request.task)
        pages_url = pages_response.get("pages_url")

        # Prepare payload
        payload = {
            "email": request.email,
            "task": request.task,
            "round": request.round,
            "nonce": request.nonce,
            "repo_url": repo_url,
            "commit_sha": commit_sha,
            "pages_url": pages_url,
        }
        await notify_evaluation_url(request.evaluation_url, payload)
    except Exception as e:
        print(f"Error in background task: {e}")
