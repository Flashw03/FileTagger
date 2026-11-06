# File Tagger CLI - Technical Documentation

## Project Overview

**Project Name:** File Tagger CLI  
**Version:** 1.0  
**Type:** Command-line application  
**Platform:** Cross-platform (Windows, macOS, Linux)  
**Primary Language:** Python  
**Architecture:** Single-file application with SQLite database  

---

## Programming Language

### Python 3.8+

**Why Python?**
- Simple syntax for beginners
- Built-in SQLite support
- Excellent libraries for data handling (pandas)
- Cross-platform compatibility
- No compilation required

**Minimum Version:** Python 3.8  
**Recommended Version:** Python 3.10 or higher  
**Tested On:** Python 3.14

**Python Features Used:**
- Object-Oriented Programming (Classes)
- File I/O operations
- Database connectivity
- Exception handling
- String manipulation
- List comprehensions

---

## Dependencies

### External Libraries

#### 1. pandas (>=1.3.0)
**Purpose:** Data manipulation and display  
**Used For:**
- Creating DataFrames from database query results
- Displaying files in tabular format
- Data filtering and selection
- Column operations

**Installation:**
```bash
pip install pandas
```

**Why pandas?**
- Professional table formatting
- Easy data manipulation
- Industry-standard library
- Excellent for displaying structured data

**Specific Usage:**
- `pd.DataFrame()` - Create tables from file data
- `df.to_string()` - Format tables for terminal display
- `df.apply()` - Transform data (e.g., show "untagged" for empty keys)
- `df[condition]` - Filter files by filename

---

### Built-in Libraries (No Installation Required)

#### 1. os
**Purpose:** Operating system interface  
**Used For:**
- File path operations (`os.path.basename()`, `os.path.splitext()`)
- Directory validation (`os.path.isdir()`)
- Recursive directory traversal (`os.walk()`)
- Opening files in default applications (`os.startfile()` - Windows)
- File deletion (`os.remove()`)

#### 2. sqlite3
**Purpose:** Database management  
**Used For:**
- Creating and managing SQLite database
- Executing SQL queries (INSERT, UPDATE, SELECT, DELETE)
- Database connection management
- Transaction handling (commit, rollback)

#### 3. datetime
**Purpose:** Date and time operations  
**Note:** Currently not used in the simplified version (removed for minimalism)

---

## Database Technology

### SQLite 3

**Type:** Embedded relational database  
**File:** `files.db` (auto-created on first run)  
**Size:** Lightweight (few KB for hundreds of files)  

**Why SQLite?**
- No server setup required
- Built into Python
- Single file database
- ACID compliant
- Perfect for local applications
- Zero configuration

**Database Schema:**

```sql
CREATE TABLE IF NOT EXISTS files (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    filepath TEXT UNIQUE,
    file_type TEXT,
    keys TEXT
)
```

**Field Details:**
- `id` - Auto-incrementing primary key
- `filename` - Name of the file (e.g., "notes.pdf")
- `filepath` - Full absolute path (UNIQUE constraint)
- `file_type` - File extension (e.g., ".pdf", ".py")
- `keys` - Comma-separated tags (e.g., "python, project")

**SQL Operations Used:**
- `CREATE TABLE IF NOT EXISTS` - Initialize database
- `INSERT INTO ... VALUES` - Add new files
- `UPDATE ... SET ... WHERE` - Update tags
- `SELECT ... FROM ... WHERE` - Query files
- `DELETE FROM ... WHERE` - Remove records (removed in simplified version)
- `LIKE` operator - Case-insensitive search
- `LOWER()` function - Case normalization

**Constraints:**
- `PRIMARY KEY` - Unique identifier for each record
- `UNIQUE` - Prevents duplicate file paths
- `IntegrityError` handling - Graceful duplicate handling

---

## Virtual Environment

### What is a Virtual Environment?

A virtual environment is an isolated Python environment that keeps project dependencies separate from system-wide Python packages.

**Benefits:**
- Isolated dependencies (no conflicts with other projects)
- Reproducible environment
- Easy to share project requirements
- Clean uninstallation (just delete the folder)

### Setup Instructions

#### Windows

**Create virtual environment:**
```bash
python -m venv venv
```

**Activate:**
```bash
venv\Scripts\activate
```

**Deactivate:**
```bash
deactivate
```

#### macOS/Linux

**Create virtual environment:**
```bash
python3 -m venv venv
```

**Activate:**
```bash
source venv/bin/activate
```

**Deactivate:**
```bash
deactivate
```

### Virtual Environment Structure

```
venv/
├── Scripts/          (Windows) or bin/ (Unix)
│   ├── activate      # Activation script
│   ├── python.exe    # Isolated Python interpreter
│   └── pip.exe       # Isolated package manager
├── Lib/              # Installed packages
│   └── site-packages/
│       └── pandas/   # pandas library
└── pyvenv.cfg        # Configuration
```

### Requirements File

**File:** `requirements.txt`  
**Purpose:** Lists all project dependencies  
**Content:**
```
pandas>=1.3.0
```

**Install all dependencies:**
```bash
pip install -r requirements.txt
```

**Generate requirements file:**
```bash
pip freeze > requirements.txt
```

---

## Project Structure

```
FileTagger/
├── app.py                      # Main application (single file)
├── files.db                    # SQLite database (auto-created)
├── requirements.txt            # Python dependencies
├── README.md                   # Setup and usage guide
├── USER_GUIDE.md              # Complete user documentation
├── TECHNICAL_DOCUMENTATION.md  # This file
├── .gitignore                 # Git ignore rules
├── setup_venv.bat             # Windows setup script
└── venv/                      # Virtual environment (if created)
```

---

## Application Architecture

### Design Pattern

**Pattern:** Procedural with Object-Oriented Database Layer  
**Structure:** Single-file application for simplicity

### Components

#### 1. Database Layer (Class)
**Class:** `FileDatabase`  
**Responsibility:** All database operations  
**Methods:**
- `__init__()` - Initialize connection and create table
- `init_db()` - Create database schema
- `insert_file()` - Add new file records
- `update_keys()` - Update file tags
- `get_files_by_key()` - Search by tags
- `get_file_metadata()` - Retrieve single file info
- `close()` - Close database connection

#### 2. Display Layer (Functions)
**Functions:**
- `display_files_dataframe()` - Show files in table format
- `select_file_from_list()` - User file selection

#### 3. File Operations Layer (Functions)
**Functions:**
- `open_file()` - Open file in default app
- `add_keys_to_file()` - Add/update tags
- `file_action_menu()` - File action menu loop

#### 4. Menu Layer (Functions)
**Functions:**
- `get_all_files_recursive()` - Scan directories
- `browse_files_action()` - Browse and select workflow
- `search_files_action()` - Search workflow
- `show_main_menu()` - Display main menu

#### 5. Main Entry Point
**Function:** `main()`  
**Responsibility:** Application lifecycle management

---

## Data Flow

### Browse Files Flow

```
User Input (directory path)
    ↓
get_all_files_recursive() → List of file paths
    ↓
For each file:
    get_file_metadata() → Check if in database
    ↓
    If not found: insert_file() → Add to database
    ↓
    Collect metadata
    ↓
display_files_dataframe() → Show table
    ↓
select_file_from_list() → User selects file
    ↓
file_action_menu() → User actions (open/tag)
```

### Search Files Flow

```
User Input (search keyword)
    ↓
get_files_by_key() → SQL query with LIKE
    ↓
display_files_dataframe() → Show matching files
    ↓
select_file_from_list() → User selects file
    ↓
file_action_menu() → User actions (open/tag)
```

### Tag Update Flow

```
User selects file
    ↓
add_keys_to_file() → Prompt for tags
    ↓
Parse and clean input (strip spaces, join with commas)
    ↓
update_keys() → SQL UPDATE query
    ↓
Confirmation message
```

---

## Key Algorithms

### Recursive Directory Scanning

**Function:** `get_all_files_recursive()`  
**Algorithm:** Depth-first traversal using `os.walk()`  
**Logic:**
1. Start at root directory
2. For each directory level:
   - Filter out hidden directories (starting with '.')
   - For each file:
     - Skip hidden files (starting with '.')
     - Add full path to results list
3. Return complete list of file paths

**Time Complexity:** O(n) where n = total files  
**Space Complexity:** O(n) for storing file paths

### Case-Insensitive Search

**Function:** `get_files_by_key()`  
**Algorithm:** SQL LIKE with LOWER()  
**Logic:**
1. Convert search term to lowercase
2. Convert database keys to lowercase
3. Use LIKE with wildcards: `%search%`
4. Return matching records

**SQL Query:**
```sql
SELECT * FROM files 
WHERE LOWER(keys) LIKE '%python%'
```

### Tag Parsing

**Function:** `add_keys_to_file()`  
**Algorithm:** Split, strip, filter, join  
**Logic:**
1. Split input by comma: `"a, b, c"` → `["a", " b", " c"]`
2. Strip whitespace: `["a", " b", " c"]` → `["a", "b", "c"]`
3. Filter empty strings: `["a", "", "b"]` → `["a", "b"]`
4. Join with comma-space: `["a", "b"]` → `"a, b"`

**Python Code Pattern:**
```python
', '.join([k.strip() for k in input.split(',') if k.strip()])
```

---

## Error Handling

### Exception Types Handled

#### 1. sqlite3.IntegrityError
**Cause:** Duplicate filepath (UNIQUE constraint violation)  
**Handling:** Silent pass (file already in database)  
**Location:** `insert_file()`

#### 2. FileNotFoundError
**Cause:** File doesn't exist (moved/deleted)  
**Handling:** Removed in simplified version  
**Previous Use:** Delete operations

#### 3. PermissionError
**Cause:** No permission to access file  
**Handling:** Generic exception catch in `open_file()`

#### 4. KeyboardInterrupt
**Cause:** User presses Ctrl+C  
**Handling:** Graceful exit with goodbye message  
**Location:** `main()` try-except block

#### 5. General Exception
**Cause:** Any unexpected error  
**Handling:** Error message display  
**Location:** `open_file()`

### Error Handling Pattern

```python
try:
    # Operation
except SpecificError:
    # Handle specific case
except Exception as e:
    # Handle general case
finally:
    # Cleanup (close database)
```

---

## Performance Considerations

### Database Performance

**Indexing:**
- Primary key on `id` (automatic)
- UNIQUE constraint on `filepath` (creates index)
- No additional indexes needed for small datasets

**Query Optimization:**
- Use parameterized queries (prevents SQL injection)
- LIKE queries are fast for small datasets (<10,000 files)
- For large datasets, consider full-text search

**Connection Management:**
- Single connection per session
- Commit after each write operation
- Close connection on exit

### Memory Usage

**Minimal Memory Footprint:**
- Database queries return tuples (memory efficient)
- pandas DataFrames created only for display
- File paths stored as strings (not file contents)

**Estimated Memory:**
- Base app: ~50 MB (Python + pandas)
- Per 1000 files: ~100 KB (database + DataFrame)

### Scalability

**Current Limits:**
- Tested with: Hundreds of files
- Practical limit: ~10,000 files
- Bottleneck: pandas DataFrame display

**For Larger Datasets:**
- Implement pagination
- Add database indexes
- Use chunked queries

---

## Security Considerations

### SQL Injection Prevention

**Method:** Parameterized queries  
**Example:**
```python
# SAFE (parameterized)
cursor.execute('SELECT * FROM files WHERE filepath = ?', (filepath,))

# UNSAFE (string concatenation)
cursor.execute(f'SELECT * FROM files WHERE filepath = {filepath}')
```

**All queries use parameterized format**

### File System Access

**Restrictions:**
- Only reads file metadata (not contents)
- User must have read permissions
- No automatic file modifications
- No network access

### Data Privacy

**Local Storage:**
- Database stored locally
- No cloud sync
- No internet connection required
- No telemetry or tracking

---

## Platform-Specific Features

### Windows

**File Opening:**
- Uses `os.startfile()` (Windows-specific)
- Opens files in default applications
- Fully supported

**Path Format:**
- Backslashes: `C:\Users\Name\Documents`
- Forward slashes also work: `C:/Users/Name/Documents`

### macOS/Linux

**File Opening:**
- Would need `subprocess.Popen(['open', filepath])` (macOS)
- Would need `subprocess.Popen(['xdg-open', filepath])` (Linux)
- Currently optimized for Windows

**Path Format:**
- Forward slashes: `/home/user/documents`
- Backslashes don't work

---

## Development Environment

### Recommended Setup

**IDE/Editor:**
- VS Code (recommended)
- PyCharm
- Sublime Text
- Any text editor

**Python Installation:**
- Official Python from python.org
- Anaconda (includes pandas)
- System package manager

**Terminal:**
- Windows: Command Prompt or PowerShell
- macOS/Linux: Terminal

### Development Tools

**Package Manager:**
- pip (comes with Python)
- Used for installing pandas

**Version Control:**
- Git (optional)
- .gitignore provided

**Testing:**
- Manual testing (no automated tests)
- Test with sample directories

---

## Installation Requirements

### System Requirements

**Operating System:**
- Windows 7 or higher
- macOS 10.12 or higher
- Linux (any modern distribution)

**Disk Space:**
- Python: ~100 MB
- pandas: ~50 MB
- App + database: <1 MB
- Total: ~150 MB

**RAM:**
- Minimum: 512 MB
- Recommended: 2 GB

**Processor:**
- Any modern CPU (no intensive operations)

### Software Requirements

**Required:**
- Python 3.8 or higher
- pip (Python package manager)

**Optional:**
- Virtual environment (venv)
- Git (for version control)

---

## Deployment

### Distribution Methods

#### Method 1: Source Code
**Files to share:**
- `app.py`
- `requirements.txt`
- `README.md`

**User setup:**
1. Install Python
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python app.py`

#### Method 2: With Virtual Environment
**Files to share:**
- Entire project folder (including venv)
- Platform-specific (Windows venv won't work on Mac)

**User setup:**
1. Activate venv
2. Run: `python app.py`

#### Method 3: Executable (Future)
**Tool:** PyInstaller or cx_Freeze  
**Benefit:** No Python installation required  
**Drawback:** Large file size (~100 MB)

---

## Future Enhancements (Technical)

### Potential Improvements

**Database:**
- Add full-text search index
- Implement database migrations
- Add file hash for duplicate detection

**Performance:**
- Implement pagination for large datasets
- Add caching for frequent queries
- Optimize recursive scanning

**Features:**
- Multi-tag search (AND/OR logic)
- Tag autocomplete
- Export tags to CSV/JSON
- Import tags from file

**Cross-Platform:**
- Detect OS and use appropriate file opener
- Handle path separators automatically
- Test on all platforms

**UI/UX:**
- Add color output (colorama library)
- Progress bars for scanning (tqdm library)
- Better table formatting

---

## Troubleshooting (Technical)

### Common Issues

**Import Error: No module named 'pandas'**
- Cause: pandas not installed
- Solution: `pip install pandas`

**Database Locked Error**
- Cause: Multiple instances accessing database
- Solution: Close other instances

**UnicodeEncodeError**
- Cause: Terminal doesn't support UTF-8
- Solution: Use `chcp 65001` on Windows

**Path Not Found**
- Cause: Incorrect path format
- Solution: Use raw strings `r"C:\path"` or escape backslashes

---

## Code Metrics

**Total Lines:** ~220 lines  
**Functions:** 11  
**Classes:** 1  
**Imports:** 3 libraries  
**Complexity:** Low (beginner-friendly)  

**Code Distribution:**
- Database layer: ~30%
- Display layer: ~15%
- File operations: ~20%
- Menu operations: ~25%
- Main/utility: ~10%

---

## License & Credits

**License:** Free for educational purposes  
**Author:** Student project  
**Dependencies:**
- Python (PSF License)
- pandas (BSD License)
- SQLite (Public Domain)

---

## Version History

**v1.0 (Current)**
- Initial release
- Core features: browse, search, tag
- Windows support
- SQLite database
- pandas display

**Planned:**
- v1.1: Cross-platform file opening
- v1.2: Advanced search features
- v2.0: GUI version

---

## Contact & Support

**Documentation:**
- README.md - Setup guide
- USER_GUIDE.md - User documentation
- TECHNICAL_DOCUMENTATION.md - This file

**For Issues:**
- Check troubleshooting sections
- Verify Python and pandas versions
- Test with sample directory

---

**Last Updated:** 2025  
**Python Version:** 3.8+  
**Dependencies:** pandas>=1.3.0  
**Platform:** Cross-platform (Windows optimized)
