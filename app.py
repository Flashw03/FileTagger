import os
import sqlite3
import pandas as pd

#  DATABASE CLASS 
class FileDatabase:
    def __init__(self, db_name='files.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.init_db()
    
    def init_db(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS files (
                id INTEGER PRIMARY KEY,
                filename TEXT,
                filepath TEXT UNIQUE,
                file_type TEXT,
                keys TEXT
            )
        ''')
        self.conn.commit()
    
    def insert_file(self, filepath, keys=''):
        filename = os.path.basename(filepath)
        file_type = os.path.splitext(filename)[1] or 'no-type'
        
        try:
            self.cursor.execute('''
                INSERT INTO files (filename, filepath, file_type, keys)
                VALUES (?, ?, ?, ?)
            ''', (filename, filepath, file_type, keys))
            self.conn.commit()
        except sqlite3.IntegrityError:
            pass
    
    def update_keys(self, filepath, keys):
        self.cursor.execute('UPDATE files SET keys = ? WHERE filepath = ?', (keys, filepath))
        self.conn.commit()
    
    def get_files_by_key(self, key):
        self.cursor.execute('''
            SELECT filename, file_type, keys, filepath
            FROM files WHERE LOWER(keys) LIKE ?
        ''', (f'%{key.lower()}%',))
        return self.cursor.fetchall()
    
    def get_file_metadata(self, filepath):
        self.cursor.execute('SELECT filename, file_type, keys, filepath FROM files WHERE filepath = ?', (filepath,))
        return self.cursor.fetchone()
    
    def close(self):
        self.conn.close()

#  DISPLAY FUNCTIONS 
def display_files_dataframe(file_data):
    if not file_data:
        print("\nNo files found")
        return None
    
    df = pd.DataFrame(file_data, columns=['Filename', 'Type', 'Keys', 'Filepath'])
    df['Keys'] = df['Keys'].apply(lambda x: x if x else 'untagged')
    print("\n" + "="*80)
    print(df[['Filename', 'Type', 'Keys']].to_string(index=False))
    print("="*80)
    return df

def select_file_from_list(df):
    while True:
        choice = input("\nEnter filename to select (or 'back' to go back): ").strip()
        if choice.lower() == 'back':
            return None
        
        matching = df[df['Filename'] == choice]
        if not matching.empty:
            return matching.iloc[0]['Filepath']
        print("Filename not found. Try again.")

#  FILE OPERATIONS 
def open_file(filepath):
    try:
        os.startfile(filepath)
        print(f"Opening {os.path.basename(filepath)}...")
    except Exception as e:
        print(f"Error opening file: {e}")

def add_keys_to_file(db, filepath):
    print(f"\nAdding keys to: {os.path.basename(filepath)}")
    print("Enter keys separated by comma (e.g., college, python, sem3, project)")
    keys_input = input("Keys: ").strip()
    
    keys = ', '.join([k.strip() for k in keys_input.split(',') if k.strip()])
    db.update_keys(filepath, keys)
    print(f"Keys updated: {keys if keys else 'untagged'}")

def file_action_menu(db, filepath):
    while True:
        print(f"\n{'='*50}")
        print(f"Selected: {os.path.basename(filepath)}")
        print(f"{'='*50}")
        print("1. Open file")
        print("2. Add/Update keys")
        print("3. Back to main menu")
        print(f"{'='*50}")
        
        choice = input("\nChoose action (1-3): ").strip()
        
        if choice == '1':
            open_file(filepath)
        elif choice == '2':
            add_keys_to_file(db, filepath)
        elif choice == '3':
            break
        else:
            print("Invalid option")

#  MENU OPERATIONS 
def get_all_files_recursive(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for filename in filenames:
            if not filename.startswith('.'):
                files.append(os.path.join(root, filename))
    return files

def browse_files_action(db):
    print(f"\n{'='*50}")
    print("BROWSE & SELECT FILES")
    print(f"{'='*50}")
    
    path = input("\nEnter directory path to browse: ").strip()
    
    if not os.path.isdir(path):
        print("Invalid directory path")
        return
    
    filepaths = get_all_files_recursive(path)
    
    if not filepaths:
        print("No files found in directory")
        return
    
    file_data = []
    for filepath in filepaths:
        metadata = db.get_file_metadata(filepath)
        if metadata:
            file_data.append(metadata)
        else:
            db.insert_file(filepath)
            metadata = db.get_file_metadata(filepath)
            file_data.append(metadata)
    
    df = display_files_dataframe(file_data)
    if df is not None:
        selected_filepath = select_file_from_list(df)
        if selected_filepath:
            file_action_menu(db, selected_filepath)

def search_files_action(db):
    print(f"\n{'='*50}")
    print("SEARCH FILES BY KEY")
    print(f"{'='*50}")
    
    key = input("\nEnter key to search (e.g., python): ").strip()
    
    if not key:
        print("Please enter a search key")
        return
    
    file_data = db.get_files_by_key(key)
    df = display_files_dataframe(file_data)
    
    if df is not None:
        selected_filepath = select_file_from_list(df)
        if selected_filepath:
            file_action_menu(db, selected_filepath)

def show_main_menu():
    print(f"\n{'='*50}")
    print("FILE TAGGER CLI - MAIN MENU")
    print(f"{'='*50}")
    print("1. Browse & Select Files")
    print("2. Search Files by Key")
    print("3. Exit")
    print(f"{'='*50}")

#  MAIN FUNCTION 
def main():
    print("\nWELCOME TO FILE TAGGER CLI")
    db = FileDatabase()
    
    try:
        while True:
            show_main_menu()
            choice = input("\nChoose option (1-3): ").strip()
            
            if choice == '1':
                browse_files_action(db)
            elif choice == '2':
                search_files_action(db)
            elif choice == '3':
                print("\nGoodbye!")
                break
            else:
                print("Invalid option")
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    finally:
        db.close()

if __name__ == '__main__':
    main()
