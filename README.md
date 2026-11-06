# File Tagger CLI

A command-line file management tool that lets you tag files with custom metadata and search them easily.

## Features

- Tag files with custom keys without opening them
- Store metadata in SQLite database
- Display files in formatted tables
- Search files by tags (case-insensitive, partial match)
- Browse directories recursively
- Open files in default applications

## Installation

### Prerequisites
- Python 3.8 or higher
- pip

### Setup

1. **Clone or download this project**
   ```bash
   cd FileTagger
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   ```

3. **Activate virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:
```bash
python app.py
```

### Main Menu Options

1. **Browse & Select Files**
   - Enter a directory path
   - View all files (including subdirectories)
   - Select a file to open or tag

2. **Search Files by Key**
   - Search for files by tags
   - Case-insensitive partial matching
   - Select from results

3. **Exit**
   - Close the application

### File Actions

When you select a file, you can:
- **Open file**: Opens in default application
- **Add/Update keys**: Add comma-separated tags (e.g., `college, python, project`)
- **Back**: Return to main menu

## Examples

### Tagging a file
```
Keys: college, python, sem3, project
Keys updated: college, python, sem3, project
```

### Searching
```
Enter key to search: python
```
Shows all files tagged with "python" (case-insensitive)

## Database

Files are stored in `files.db` with the following structure:
- filename
- filepath (unique)
- file_type
- keys (comma-separated tags)

## Notes

- Hidden files (starting with `.`) are ignored
- Files with no tags show as "untagged"
- Subdirectories are scanned recursively
- Search is case-insensitive and supports partial matches

## Troubleshooting

**Error: "No module named 'pandas'"**
```bash
pip install pandas
```

**Error: "Invalid directory path"**
- Make sure the path exists
- Use absolute paths or correct relative paths
- On Windows, use backslashes: `C:\Users\YourName\Documents`

## License

Free to use for educational purposes.
