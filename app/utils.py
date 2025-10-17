import os
import httpx
import logging
import asyncio
API_SECRET = os.getenv("API_SECRET", "aman2005")


logger = logging.getLogger(__name__)

def validate_secret(secret: str) -> bool:
    from hmac import compare_digest
    return compare_digest(secret, API_SECRET)


async def retry_request(func, *args, retries=3, delay=3, **kwargs):
    last_exc = None
    for attempt in range(retries):
        try:
            return await func(*args, **kwargs)
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            last_exc = e
            logger.warning(f"Request failed on attempt {attempt + 1}/{retries}: {e}")
            if attempt < retries - 1:
                await asyncio.sleep(delay)
            else:
                logger.error("Max retries reached.")
                raise last_exc
    if last_exc:
        raise last_exc
