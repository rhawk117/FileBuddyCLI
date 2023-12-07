# Rhawk117 - File Organizer
import os
import shutil
import threading
from dataclasses import dataclass, field
import traceback as debug
import click 

class Organize:
    @staticmethod
    def browse_files(dir_path):
        all_files = [os.path.join(root, file) for root, _, files in os.walk(
            dir_path) for file in files]
        unique_types = set()  # Use set to automatically filter out duplicates
        for file in all_files:
            _, file_type = os.path.splitext(file)
            # Remove period to create file name later
            file_type = file_type[1:]
            if file_type and os.path.isfile(file):
                unique_types.add(file_type)
        return all_files, list(unique_types)

    @staticmethod
    def files_of(target_type, dir_contents):
        return [file for file in dir_contents if file.endswith('.' + target_type)]

    @staticmethod
    def move_all(target_files,  output_dir):
        for file in target_files:
            try:
                file_source = file
                file_destination = os.path.join(output_dir, os.path.basename(file))
                print(f'\t\t> Moving -> {file} to {output_dir}')
                shutil.move(file_source, file_destination)
            except Exception:
                print(f'[!] Failed to Move {file} to -> {output_dir}')
                


    @staticmethod
    def create_threads(unique_types, postfix, dl_path, dl_contents):
        dirs = []  # Directory names being created
        threads = []  # Threads for cleaning
        for extension in unique_types:
            # New / old output directory
            new_dir = os.path.join(dl_path, extension + postfix)
            if not os.path.exists(new_dir):
                os.mkdir(new_dir)
            target_files = Organize.files_of(extension, dl_contents)
            thread = threading.Thread(target=Organize.move_all,
                    args=(target_files, new_dir),
                    name='file_cleaner')
            threads.append(thread)
            thread.start()  # Start Thread
            dirs.append(new_dir)
        return threads

    @staticmethod
    def process_threads(all_threads):
        for thread in all_threads:
            thread.join()  # Start file cleaning

    @staticmethod
    def header():
        print('***\t\t[*] File Buddy [*]\t\t***')
        print('***\t***developed by: rhawk117***\t\t***\n\n')

    @staticmethod
    def main(dl_path):
        Organize.header()
        print(f'[!] NOTICE: The downloads folder is set to {dl_path} [!]')
        os.chdir(dl_path)
        print(f'\n***\t\tCreating Downloads Folder Data\t\t***\n')
        try:
            dl_contents, unique_types = Organize.browse_files(dl_path)
            dir_delimit = '_files'
            print(f'***\t\tDownload Contents\t\t***')
            for file in dl_contents:
                print(f'\n\t > {file}')

            print(f'\n***\t\tUnique File Types Found\t\t***')
            print('\t>'.join(unique_types))

            print('\t[*] Starting File Cleaning Threads.. [*]\t\t')
            threads = Organize.create_threads(
                unique_types, dir_delimit, dl_path, dl_contents)
            Organize.process_threads(threads)
            print('\n\n***\t\t[*] PROCESSING COMPLETE [*]\t\t***\n\n')

        except Exception as ex:
            print(f'An Error Occurred during the download cleaning process.')
            print(f'\n\nFormatted Exception\n\n')
            print(debug.format_exc())


# WORK IN PROGRESS 
# @dataclass
# class File:
#     '''
#     Represents a single File
#     '''
#     file_path: str
#     name: str = ""
#     extension: str = ""
#     size: int = 0
#     creation_date: str = ""

#     def __post_init__(self):
#         self.name, self.extension = os.path.splitext(os.path.basename(self.file_path))
#         self.size = os.path.getsize(self.file_path)
#         creation_time = os.path.getctime(self.file_path)
#         self.creation_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(creation_time))
    
#     @property
#     def json_export(self) -> dict:
#         return {
#             "file_path": self.file_path,
#             "name": self.name,
#             "extension": self.extension,
#             "size": self.size,
#             "creation_date": self.creation_date
#         }
    


# @dataclass
# class Directory:
#     '''
#     Represents a single directory
#     '''
#     path: str # Folder Path
#     files: list = field(default_factory=list) # List of all File Objects
#     unique_file_types: set = field(default_factory=set) # List of unique typs
#     sub_dirs: list = field(default_factory=list) # List of Subdirectories 

#     def __post_init__(self):
#         self.set_data()

#     def set_data(self):
#         """Populates the files, unique_file_types, and sub_dirs attributes based on the directory path."""
#         if not os.path.isdir(self.path) or not os.path.exists(self.path):
#             raise ValueError(f"{self.path} is not a valid directory")
        
#         self.has_files : bool 
#         self.has_sub_dirs : bool
#         self.file_count : int
#         for root, dirs, files in os.walk(self.path):
#             if root == self.path:  # Only consider immediate subdirectories and files, thank god lol
#                 for dir_name in dirs:
#                     sub_dir_path = os.path.join(root, dir_name)
#                     sub_dir = Directory(sub_dir_path)
#                     self.sub_dirs.append(sub_dir)
#                     self.has_sub_dirs = True
#                 for file in files:
#                     full_path = os.path.join(root, file)
#                     file_obj = File(full_path)
#                     self.files.append(file_obj)
#                     self.unique_file_types.add(file_obj.extension.lower())
#         self.file_count = len(self.files)
#         self.empty = not self.has_files and not self.sub_dirs # checking if the folder is empty

#     @property
#     def folder_size(self):
#         """Calculates and returns the total size of all files in the directory."""
#         return sum(file.size for file in self.files)
    
#     @property
#     def largest_file(self) -> tuple:
#         if self.empty or not self.has_files:
#             raise Exception("Folder is empty")
#         best = -1
#         best_name = ''
#         best_file 
#         for file_objs in self.files:
#             if(file_objs.size > best):
#                 best = file_objs.size
#                 best_name = file_objs.name
#                 best_file = file_objs
#         return (best_file, best_name)
        

    
#     @property
#     def json_export(self) -> dict:
#         return {
#             "Folder Path": self.path,
#             "All File Info": [file.json_export() for file in self.files],
#             "Unique File Types": list(self.unique_file_types),
#             "Subfolders": [sub_dir.json_export() for sub_dir in self.sub_dirs],
#             "Folder Empty": self.empty,
#             "Folder Size": self.folder_size
#         }



@click.group()
def cli():
    pass

@click.command()
@click.argument('folder',type=click.Path(exists=True, dir_okay=True, file_okay=False))
def organize(folder):
    try:
        if os.path.exists(folder) and os.path.isdir(folder):
            Organize.main(folder)
        else:
            raise Exception("File Path provided doesn't exist or isn't a directory")
    except Exception as error:
        print(f'\n[!] An exception occured details below [!]\n')
        debug.print_exc(error)

cli.add_command(organize)

if __name__ == '__main__':
    cli()


# Commands 
# --filter <dir_path> -d: organizes the directory path 
# --scan <dir_path> (-s, -p): scan the directory path and get information and data about all the files 







# def get_input(prompt: str, options: list) -> None:
#     usr_input = input(f'{prompt}\nEnter Here: ')
#     if usr_input not in options:
#         print(
#             f'\n\n[!] Input ({usr_input}) invalid [!]\nPick One of the following: {" , ".join(options)}')
#         return get_input(prompt, options)
#     else:
#         return usr_input
    
# def browse_files(path):
#     all_files = [items for _, __, file in os.walk(path) for items in file]
#     unique_types = set() # use set to automatically filter out duplicates 
#     for file in all_files:
#          _, file_type = os.path.splitext(file)
#          file_type = file_type[1:].lower() # remove period to create file name later 
#          if os.path.isfile(file):
#              unique_types.add(file_type)
#     return (all_files, list(unique_types)) # set to filter out duplicates

# # Finds all Files with the corresponding target_type
# def files_of(target_type, dir_contents):
#     return [file for file in dir_contents if file.endswith(target_type)]

# def move_all(target_files: list, source, output_dir, lock) -> None:
#     for file in target_files:
#         file_source = os.path.join(source, file)
#         with lock:
#             print(f'\t\t> Moving -> {file} to {output_dir}')
#             shutil.move(file_source, output_dir)

# def create_threads(unique_types, postfix, dl_path, dl_contents):
#     dirs = [] # directory names being created
#     threads = []
#     new_dir = extension + postfix
#     thread_lock = threading.Lock()
#     for extension in unique_types:
#         print(f'\t\t > [*] PROCESSING FOLDER -> {new_dir} {extension}')
#         target_files = files_of(extension, dl_contents)
#         thread = threading.Thread(target=move_all, 
#             args=(target_files, dl_path, new_dir, thread_lock), name='file_cleaner'
#         )
#         threads.append(thread)
#         if not os.path.exists(new_dir):
#             os.mkdir(new_dir)
#         thread.start() # Start Thread
#         dirs.append(new_dir)
#         return (dirs, threads)
    
# def main() -> None:
#     print('***\t\t[*] File Buddy [*]\t\t***')
#     print('***\t***developed by: rhawk117***\t\t***\n\n')
#     dl_path = r'C:\Users\Beast\Desktop\Downloads'
#     print(f'[!] NOTICE: The downloads folder is set to {dl_path} [!]')
#     print('[*] If you wish to change the downloads folder' +
#               ' path modify the settings.json file\n[*] Ending program...')
#     os.chdir(dl_path)
#     print(f'[*]  ')
#     usr_choices = ['y','n']
#     choice = get_input('[?] Proceed with file organization (y/n) [?]', options=usr_choices)
#     if choice == 'n':
#         print('[*] If you wish to change the downloads folder' +
#               ' path modify the settings.json file\n[*] Ending program...')
#         return
#     preference = get_input('[?] Delete old File after organization', options=usr_choices)
       

#     # Example of using threads to process directories concurrently
#     print(f'\n***\t\tCreating Downloads Folder Data\t\t***\n')
#     try:
#         dl_contents, unique_types = browse_files(dl_path)
#         dir_delimit = '_files'
#         print(f'***\t\tDownload Contents\t\t***')
#         for file in dl_contents:
#             print(f'\n\t > {file}')
        
#         print(f'\n***\t\tUnique File Types Found\t\t***')
#         print('\n\t>'.join(unique_types))
        
#         print('\t\t[*] Starting File Cleaning [*]\t\t')
#         # Wait for all threads to finish
#         threads = create_threads(unique_types, dir_delimit)
#         for thread in threads:
#             print(f'\n***\t\t[!] PROCESSING -> {thread}\t\t***\n\n')
#             thread.join() # start file cleaning 
#         print('\n\n***\t\t[*] PROCESSING COMPLETE [*]\t\t***\n\n')
#     except Exception as ex:
#         print(f'An Error Occured during download cleaning process.')
#         debug.print_exception(ex)
#         print(f'\n\nFormatted Exception\n\n')
#         debug.format_exception(ex)