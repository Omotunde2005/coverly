from firecrawl import FirecrawlApp
from dotenv import load_dotenv
from pydantic import BaseModel, Field
import os


# SCHEMA FOR FIRECRAWL SCRAPER 
class ResponseModel(BaseModel):
    job_details: str = Field(description="All the details about the job listing including experience, requirements, etc.")
    is_valid: bool = Field(description="A boolean value to determine if the URL is valid or it actually contains job related information. True if it does, False if otherwise.")


load_dotenv()

app = FirecrawlApp(api_key=os.environ.get("FIRECRAWL_KEY"))

# SCRAPE JOB DESCRIPTION
def scrape(url):

    url = url
    data = app.scrape_url(
        url,
        params={
            "formats": ["extract"],
            "extract": {
                "schema": ResponseModel.model_json_schema(),
                "prompt": "Return details about the job description/job listing on this page. Other information on the page should be excluded.",
                "systemPrompt": "You are a helpful assistant that extracts a job listing and its related details from a page"
            }
        })

    scraped_response = data["extract"]
    return scraped_response