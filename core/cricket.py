import requests
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

API_KEY=os.getenv("CRICKET_API_KEY")
# API Key and URL
API_URL = f"https://api.cricapi.com/v1/currentMatches?apikey={API_KEY}&offset=0"

def fetch_live_matches():
    """Fetch live cricket match data from CricAPI"""
    try:
        response = requests.get(API_URL)
        data = response.json()
        
        if data["status"] != "success":
            print("Error fetching data:", data.get("message", "Unknown error"))
            return []
        
        return data.get("data", [])
    
    except Exception as e:
        print("Error fetching match data:", str(e))
        return []

def display_matches(matches):
    """Display match details in a readable format"""
    print("\n===== Live Cricket Matches =====\n")
    
    if not matches:
        print("No live matches found.")
        return

    for match in matches:
        teams = " vs ".join(match["teams"])
        status = match["status"]
        venue = match["venue"]
        match_type = match["matchType"].upper()
        
        print(f"🏏 {teams} ({match_type})")
        print(f"📍 Venue: {venue}")
        print(f"📢 Status: {status}")

        if "score" in match and match["score"]:
            for s in match["score"]:
                print(f"  🔹 {s['inning']}: {s['r']} runs / {s['w']} wickets in {s['o']} overs")
        
        print("-" * 50)

if __name__ == "__main__":
    matches = fetch_live_matches()
    display_matches(matches)
