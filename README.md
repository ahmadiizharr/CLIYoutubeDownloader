# YouTube Video Downloader CLI

A command-line interface tool for downloading YouTube videos using ssvid.net API.

## Features

- Download single YouTube videos
- Bulk download from file.txt (multiple URLs)
- Automatic date-based folder organization (e.g., "04052025")
- Automatic handling of duplicate filenames (adds number prefix)
- Debug mode to view API responses
- Progress bar for downloads
- Error logging

## Requirements

- Python 3.6+
- Required packages (install using `pip install -r requirements.txt`):
  - requests
  - tqdm

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the downloader:
```bash
python youtube_downloader.py
```

3. Choose from available options:
   - Option 1: Single video download
     - Enter YouTube URL
     - Video will be saved in date-based folder
   
   - Option 2: Bulk download
     - Create `file.txt`
     - Add YouTube URLs (one per line)
     - All videos will be downloaded to date-based folder
   
   - Option 3: Debug mode
     - Shows API response details
   
   - Option 4: Exit

### File Organization

- Downloads are organized in date-based folders (e.g., "04052025")
- Files are named using video titles
- Duplicate filenames are handled by adding number prefixes:
  - First file: `title.mp4`
  - Duplicates: `1_title.mp4`, `2_title.mp4`, etc.

## Credits

This tool uses the ssvid.net API for video processing and downloading.

### API Endpoints Used:
- Search API: `https://ssvid.net/api/ajax/search`
- Convert API: `https://ssvid.net/api/ajax/convert`

## Support the Project

If you find this tool useful, consider supporting the development:

[![Saweria](https://img.shields.io/badge/Donate-Saweria-orange)](https://saweria.co/ahmadiizhar)

You can donate through [Saweria](https://saweria.co/ahmadiizhar)

## License

This project is open source and available under the MIT License.
