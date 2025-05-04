import requests
import json
from datetime import datetime

def get_video_info(url: str) -> None:
    """
    Get and display video information from ssvid.net API
    """
    try:
        # API endpoint and headers
        api_url = "https://ssvid.net/api/ajax/search"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Prepare request data
        data = {
            "query": url,
            "vt": "home"
        }
        
        # Make API request
        print("\nFetching video information...")
        response = requests.post(api_url, data=data, headers=headers)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        
        # Get available MP4 qualities
        mp4_links = result['links']['mp4']
        
        # Get the first available quality
        first_quality = list(mp4_links.keys())[0]
        
        # Extract required information
        video_info = {
            'k': mp4_links[first_quality]['k'],
            'vid': result['vid'],
            'title': result['title'],
            'quality': first_quality
        }
        
        # Display information
        print("\nVideo Information:")
        print("-" * 50)
        print(f"Title: {video_info['title']}")
        print(f"Video ID: {video_info['vid']}")
        print(f"Quality: {video_info['quality']}")
        print(f"Key: {video_info['k']}")
        print("-" * 50)
        
        return video_info
        
    except requests.RequestException as e:
        print(f"\nError making API request: {str(e)}")
    except (KeyError, IndexError) as e:
        print(f"\nError parsing response: {str(e)}")
    except Exception as e:
        print(f"\nUnexpected error: {str(e)}")
    
    return None

def main():
    while True:
        print("\nYouTube Video Info CLI")
        print("1. Get video information")
        print("2. Exit")
        
        choice = input("\nEnter your choice (1-2): ").strip()
        
        if choice == "1":
            url = input("\nEnter YouTube URL: ").strip()
            if url:
                get_video_info(url)
            else:
                print("\nError: URL cannot be empty!")
                
        elif choice == "2":
            print("\nExiting...")
            break
            
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
