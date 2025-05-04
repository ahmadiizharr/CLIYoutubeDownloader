import requests
import json
from datetime import datetime
import os
from tqdm import tqdm

class YouTubeDownloader:
    def __init__(self):
        self.search_url = "https://ssvid.net/api/ajax/search"
        self.convert_url = "https://ssvid.net/api/ajax/convert"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def get_video_info(self, url: str) -> dict:
        """Get video information from ssvid.net"""
        try:
            data = {
                "query": url,
                "vt": "home"
            }
            
            response = requests.post(self.search_url, data=data, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            # Get available MP4 qualities
            mp4_links = result['links']['mp4']
            first_quality = list(mp4_links.keys())[0]
            
            return {
                'k': mp4_links[first_quality]['k'],
                'vid': result['vid'],
                'title': result['title']
            }
            
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None

    def get_download_link(self, vid: str, k: str) -> str:
        """Get download link from convert API"""
        try:
            data = {
                'vid': vid,
                'k': k
            }
            
            response = requests.post(self.convert_url, data=data, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            return result.get('dlink')
            
        except Exception as e:
            print(f"Error getting download link: {str(e)}")
            return None

    def download_video(self, url: str, filename: str) -> bool:
        """Download video file"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            with open(filename, 'wb') as file, tqdm(
                desc=filename,
                total=total_size,
                unit='iB',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for data in response.iter_content(chunk_size=1024):
                    size = file.write(data)
                    pbar.update(size)
            
            return True
            
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            return False

    def process_single_url(self, url: str) -> bool:
        """Process a single YouTube URL"""
        print(f"\nProcessing: {url}")
        
        # Get video information
        info = self.get_video_info(url)
        if not info:
            return False
            
        # Get download link
        download_url = self.get_download_link(info['vid'], info['k'])
        if not download_url:
            return False
            
        # Generate filename and download
        # Create date folder and generate filename
        folder = self._get_date_folder()
        filename = os.path.join(folder, self._get_unique_filename(folder, info['title']))
        return self.download_video(download_url, filename)

    def _get_date_folder(self) -> str:
        """Get or create date-based folder for downloads"""
        folder_name = datetime.now().strftime("%d%m%Y")
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        return folder_name

    def _get_unique_filename(self, folder: str, title: str) -> str:
        """Generate unique filename for duplicate files"""
        base_filename = f"{title}.mp4"
        filepath = os.path.join(folder, base_filename)
        
        if not os.path.exists(filepath):
            return base_filename
            
        counter = 1
        while True:
            new_filename = f"{counter}_{title}.mp4"
            filepath = os.path.join(folder, new_filename)
            if not os.path.exists(filepath):
                return new_filename
            counter += 1

    def process_bulk_file(self) -> None:
        """Process multiple URLs from file.txt"""
        if not os.path.exists('file.txt'):
            print("Error: file.txt not found!")
            return
            
        with open('file.txt', 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
            
        print(f"\nFound {len(urls)} URLs in file.txt")
        
        for i, url in enumerate(urls, 1):
            print(f"\nProcessing URL {i}/{len(urls)}")
            self.process_single_url(url)

def main():
    downloader = YouTubeDownloader()
    
    while True:
        print("\nYouTube Downloader CLI")
        print("0. Support via Saweria")
        print("1. Download single video")
        print("2. Bulk download from file")
        print("3. Debug mode (show JSON response)")
        print("4. Exit")
        
        choice = input("\nEnter your choice (0-4): ").strip()
        
        if choice == "0":
            print("\nOpening Saweria donation page...")
            os.system("start https://saweria.co/ahmadiizhar")
            
        elif choice == "1":
            url = input("\nEnter YouTube URL: ").strip()
            if url:
                downloader.process_single_url(url)
            else:
                print("Error: URL cannot be empty!")
                
        elif choice == "2":
            downloader.process_bulk_file()
                
        elif choice == "3":
            url = input("\nEnter YouTube URL: ").strip()
            if url:
                try:
                    # Get search API response
                    data = {
                        "query": url,
                        "vt": "home"
                    }
                    search_response = requests.post(downloader.search_url, data=data, headers=downloader.headers)
                    search_response.raise_for_status()
                    search_result = search_response.json()
                    
                    print("\nAPI Response:")
                    print("-" * 50)
                    print(json.dumps({
                        'title': search_result.get('title', ''),
                        'dlink': search_result.get('dlink', ''),
                        'vid': search_result.get('vid', ''),
                        'links': search_result.get('links', {})
                    }, indent=2))
                    print("-" * 50)
                    
                except Exception as e:
                    print(f"\nError in debug mode: {str(e)}")
            else:
                print("Error: URL cannot be empty!")
                
        elif choice == "4":
            print("\nExiting...")
            break
            
        else:
            print("\nInvalid choice! Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
