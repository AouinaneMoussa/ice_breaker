import os
import requests
from dotenv import load_dotenv

load_dotenv()



def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Mannually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/AouinaneMoussa/a62768bfdfa5fb74db86e790b4234559/raw/2428616fd8eb06e502898777253e04fafafbde94/moussa-aouinane-scrapin.json"
        response = requests.get(
            linkedin_profile_url, 
            timeout=10,
        )
    else:
        api_endpoint = "https://api.scrapin.io/enrichment/profile"
        params = {
            "apikey": os.environ["SCRAPIN_API_KEY"],
            "linkedInUrl": linkedin_profile_url,
        }
        response = requests.get(
            api_endpoint,
            params=params,
            timeout=10,
        )

    data = response.json().get("person")
    data = {
        k: v 
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["certifications"]
    }
    
    return data

        


if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/moussa-aouinane-37a27616a/", mock=True
        )
    )