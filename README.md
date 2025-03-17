# Ahrefs Traffic Scraper

This script automates the process of collecting organic traffic data from Ahrefs for a list of domains.

## Prerequisites

- Python 3.7 or higher
- Chrome browser installed
- Valid Ahrefs account with login credentials

## Installation

1. Clone this repository or download the files

2. (Optional) Create and activate a virtual environment:
   ```bash
   # On Windows
   python -m venv venv
   .\venv\Scripts\activate

   # On macOS/Linux
   python -m venv venv
   source venv/bin/activate
   ```


2. Install required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

## Setup

1. Create a CSV file named `sample_sheet.csv` with at least two columns:
   - `URL`: containing the domains you want to check
   - `Traffic`: can be empty, will be filled by the script
   - `Flag`: can be empty, will be filled by the script
See `sample_sheet.csv` for an example.

## Running the Script

1. Run the script:
```bash
python ahrefs.py
```

2. When the browser opens:
   - Log in to your Ahrefs account manually
   - Complete any Cloudflare verification if required
   - Press any key in the terminal to continue

3. The script will:
   - Process each domain in your CSV file
   - Save traffic data back to the CSV

## Notes

- The script uses human-like typing patterns to avoid detection
- Do not exit the browser window while the script is running (you can minimize it)
- Will flag domains showing organic traffic over 20,000

## Troubleshooting

If you encounter errors:
- Ensure your Ahrefs login is valid
- Check your internet connection
- Verify the CSV file format is correct
