import os
import shutil
import sys
import time
from random import randint
import commands as cmd1

# ------------------------------------------------------------------------------------------

OUTPUT_DECOR = ">> "
INPUT_DECOR = "<< "
ERROR_DECOR = "<< WARNING >> "

file_path = os.getcwd()

SYSTEM_FOLDER_NAME = "System_Files"
SYSTEM_USER_FILE_NAME = "user_data.txt"
SYSTEM_HELP_FILE_NAME = "help.txt"
SYSTEM_UNKNOWN_FOLDER_NAME = "Unsupported"

SYSTEM_FOLDER_PATH = f"{file_path}\\{SYSTEM_FOLDER_NAME}"
SYSTEM_USER_FILE_PATH = f"{SYSTEM_FOLDER_PATH}\\{SYSTEM_USER_FILE_NAME}"
SYSTEM_HELP_FILE_PATH = f"{SYSTEM_FOLDER_PATH}\\{SYSTEM_HELP_FILE_NAME}"

# ------------------------------------------------------------------------------------------


class Controller:
    def __init__(self):
        self.user_name = ""
        self.run_diagnostic = Diagnosis()
        self.run_configuration = Configure()
        self.run_organizer = Organizer()

    def start(self):
        """
        THIS IS THE START OF THE ENTIRE PROGRAM.
        IT STARTS WITH A SYSTEM DIAGNOSIS TO ENSURE ALL SYSTEM FILES ARE PRESENT.
        THEN IT STARTS THE INTERACTION PROCESS WHICH ALLOWS THE USER TO ACCESS ALL THE OTHER CLASSES.
        """
        self.run_diagnostic.start()
        self.get_info()
        self.interact_with_user()

    def greet(self):
        time_str = int(time.strftime("%H", time.localtime()))
        if time_str in range(00, 12):
            return "Good morning"
        elif time_str in range(12, 18):
            return "Good afternoon"
        else:
            return "Good evening"    

    def interact_with_user(self):
        """
        GETS INPUT FROM THE USER AND CALLS THE REQUIRED METHODS.
        """
        greeting = self.greet()
        print(f"{OUTPUT_DECOR}{greeting}, {self.user_name}")

        while True:
            i, user_input = 0, input(f"{INPUT_DECOR}Tell me what to do: ").lower()
           
            while i < len(cmd1.input_data):
                if len(user_input) != 0 and user_input in cmd1.input_data[i]:
                    self.display_output_function(cmd1.input_data[i][0])
                    break
                elif len(user_input) == 0:
                    print(f"{ERROR_DECOR}Please enter a command.")
                    break
                else:
                    i += 1

    @staticmethod
    def display_output_text(key_word):
        """
        DISPLAYS TEXT OUTPUT FOR ALL THE FUNCTION CALLS AND MORE.
        """
        for item in cmd1.output_data:
            if key_word == item[0]:

                # PRINTS A RANDOM VALUE FROM THE 'OUTPUT_DATA' LIST IN THE COMMANDS FILE
                # randint(1, len(item) - 1) --> RANDOM NUMBER FROM 1 TO (LENGTH OF LIST) - 1 TO AVOID AN INDEXING ERROR.
                print(f"{OUTPUT_DECOR}{item[randint(1, len(item) - 1)]}\n")
                break
                
    def display_output_function(self, key_word):
        """
        CALLS THE NECESSARY METHODS WHEN THE KEY WORD IS ENCOUNTERED.
        """
        self.display_output_text(key_word)  # DISPLAYS TEXT OUTPUT FOR BEFORE FUNCTION CALL.

        if key_word == "start":
            self.run_organizer.start()
        elif key_word == "config":
            self.run_configuration.write_user_file()
        elif key_word == "diagnose":
            self.run_diagnostic.start()
        elif key_word == "help":
            self.render_help_file()
        elif key_word == "exit":
            time.sleep(0.5)
            sys.exit()

    def get_info(self):
        with open(SYSTEM_USER_FILE_PATH, "r") as f:
            self.user_name = f.readline()

    @staticmethod
    def render_help_file():
        with open(SYSTEM_HELP_FILE_PATH, "r") as f:
            print(f"\n{f.read()}\n")


class Diagnosis:
    def __init__(self):
        self.run_configuration = Configure()

    def start(self):
        """
        CALLS FUNCTIONS TO CHECK FOR SYSTEM FILES.
        """
        self.run_diagnosis(path=SYSTEM_FOLDER_PATH, option="dir")  # SYSTEM FOLDER
        self.run_diagnosis(path=SYSTEM_HELP_FILE_PATH)  # HELP FILE
        self.run_diagnosis(path=SYSTEM_USER_FILE_PATH, option="user file")  # USER FILE
        print(f"{OUTPUT_DECOR}System files located\n{'-'*80}\n")

    def run_diagnosis(self, path, option=None):
        """
        CHECKS TO SEE IF THE REQUIRED FILES AND DIRECTORIES(FOLDERS) ARE PRESENT AND CALLS METHODS
        TO ENSURE THEY ARE GENERATED.
        """
        if not os.path.exists(path):
            print(f"{ERROR_DECOR}Unable to locate --> {path}")
            if option == "dir":
                self.generate_folder()
            elif option == "user file":
                self.generate_file(path=path)
                self.run_configuration.write_user_file()
            else:
                self.generate_file(path=path)
        else:
            print(f"{OUTPUT_DECOR}Located --> {path}")

    @staticmethod
    def generate_folder(path=SYSTEM_FOLDER_PATH):
        os.mkdir(path)
        print(f"{OUTPUT_DECOR}Successfully generated --> {path}\n")

    @staticmethod
    def generate_file(path):
        open(path, "x").close()
        print(f"{OUTPUT_DECOR}Successfully generated --> {path} \n")


class Configure:

    def write_user_file(self):
        path, data = SYSTEM_USER_FILE_PATH, input(f"{INPUT_DECOR}Please enter your name: ")

        if self.probe_input(data):
            with open(SYSTEM_USER_FILE_PATH, "w") as f:
                f.write(data)
            print(f"{OUTPUT_DECOR}Successfully configured --> {path}\n")
        else:
            print(f"{ERROR_DECOR}Invalid entry.")
            self.write_user_file()

    @staticmethod
    def probe_input(data):
        if len(data) == 0:
            return False
        else:
            return True


class Organizer:
    def __init__(self):
        self.directory = ""

    @staticmethod
    def get_directory():
        return input(f"{INPUT_DECOR}Please enter the directory: ")

    def probe_directory(self, directory):
        if len(directory) != 0 and "\\" in directory:
            return True
        else:
            return False

    def change_directory(self, directory):
        if self.probe_directory(directory):
            try:
                os.chdir(directory)
                print(f"{OUTPUT_DECOR}Successfully changed directory to --> {directory}.\n")
            except FileNotFoundError as e:
                print(f"{ERROR_DECOR}An error occurred: {e}\n")
                self.start()
        else:
            self.start()

    def generate_folders(self):
        """
        CONTAINS A DICTIONARY WITH THE FILE NAME AND THE CORRESPONDING FILE EXTENSIONS.
        IT WILL GENERATE FOLDERS BASED ON THE FILES THAT ARE PRESENT IN THE DIRECTORY.
        """
        global folder_names, file_extensions
        folder_types = {
            "Text": ".txt",
            "Images": [".jpg", ".png", ".jpeg", ".PNG", ".JPG", ".JPEG", ".gif", ".webp", ".tiff", ".psd",
                       ".GIF", ".WEBP", ".TIFF", ".PSD", "JPEG 2000"],
            "Python": ".py",
            "Audio": ".mp3",
            "Video": ".mp4",
            "HTML": ".html",
            "PDF": ".pdf",
            "Word_Document": ".docx",
            "Word_Template_Files": [".dotx", ".dotm"],
            "XML": ".xml",
            "Executables": [".exe", ".bat"],
            "JavaScript": ".js",
            "Java": ".java",
            "CSS": ".css",
            "C, C++": ".c",
            "Icons": ".ico",
            "7-Zip_Compressed_File": ".7z",
            "Zip": ".zip",
            "Tarball_Compressed_File": ".tar.gz",
            "ISO_Disk_Image": ".iso",
            "CSV": ".csv",
            "Database_Files": [".db", "dbf"],
            "Log_File": ".log",
            "SQL": ".sql",
            "GIF": ".gif",
            "Scalable_Vector_Graphics(SVG)": ".svg",
            "PHP": ".php",
            "PowerPoint_Slide_Show": ".pps",
            "PowerPoint_Presentation": ".ppt",
            "Microsoft_Excel_File": ".xls",
        }

        folder_names = [item for item in folder_types.keys()]
        file_extensions = [item for item in folder_types.values()]

        for file_ext in self.get_file_extensions():
            for x, y in zip(folder_names, file_extensions):
                if type(y) == list:
                    if file_ext in y:
                        if not os.path.exists(x):
                            os.mkdir(x)
                elif file_ext == y:
                    if not os.path.exists(x):
                        os.mkdir(x)

        print(f"{OUTPUT_DECOR}Successfully generated --> folders\n")

    def move_files(self):
        """
        WILL MOVE FILES INTO THEIR RESPECTIVE FOLDERS AND WILL CALL THE: handle_unknown_files()
        METHOD IF THE EXTENSION FOR THAT FILE IS UNSUPPORTED.
        """
        print(f"{OUTPUT_DECOR}Initiating file transfer program...\n")
        for item in self.get_files():
            if os.path.isfile(item):
                file_ext = os.path.splitext(item)[1]

                for x, y in zip(folder_names, file_extensions):
                    if type(y) == list and file_ext in y:
                        print(f"{OUTPUT_DECOR}Moving --> {item} : {x}...")
                        shutil.move(item, x)
                    elif file_ext == y:
                        print(f"{OUTPUT_DECOR}Moving --> {item} : {x}...")
                        shutil.move(item, x)


        print(f"{OUTPUT_DECOR}Files successfully transferred\n")

    def get_file_extensions(self):
        extensions = [os.path.splitext(item)[1] for item in os.listdir(self.directory)]
        return extensions

    def get_files(self):
        files = [item for item in os.listdir(self.directory)]
        return files

    def start(self):
        print(file_path)
        print(f"{OUTPUT_DECOR}Enter Ctrl + c to end process (Ignore messy output).")
        self.directory = self.get_directory()
        self.change_directory(self.directory)
        self.generate_folders()
        self.move_files()
        print(file_path)


obj1 = Controller()
obj1.start()