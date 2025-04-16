import os
import requests
from dotenv import load_dotenv

load_dotenv()



def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False):
    """scrape information from LinkedIn profiles,
    Mannually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url = "https://gist.githubusercontent.com/AouinaneMoussa/f80909ea4d5b14be411fbea8ead77f57/raw/920a3627318d722a79efaadc8c0cee2d0c93669a/moussa-aouinane.json"
        response = requests.get(
            linkedin_profile_url, 
            timeout=10,
        )
    else:
        api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
        header = {"Authorization": f'Bearer {os.environ.get("PROXYCURL_API_KEY")}'}
        response = requests.get(
            api_endpoint,
            params={
            "url": linkedin_profile_url
            },
            headers=header,
            timeout=10,
        )

    data = response.json()
    data = {
        k: v 
        for k, v in data.items()
        if v not in ([], "", "", None) and k not in ["people_also_viewed","certifications"]
    }

    if data.get("groups"):
        for group_dict in data.get("groups"):
            group_dict.pop("profile_pic_url")
    
    return data

        


#if __name__ == "__main__":
    print(
        scrape_linkedin_profile(
            linkedin_profile_url="https://www.linkedin.com/in/moussa-aouinane-37a27616a/", mock=True
        )
    )