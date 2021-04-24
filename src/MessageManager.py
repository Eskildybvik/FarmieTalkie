import os
from os import listdir
from os.path import isfile, join
import re
import math

# Creates folder if it does not already exist
def create_folder(folder_name: str):
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

def get_file_names(path: str) -> list[str]:
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

class MessageManager:
    """Class for helping keep track of the 10 messages in the log."""
    
    FOLDER_NAME = "messages"
    PATH = f"./{FOLDER_NAME}"
    MESSAGE_LIMIT = 10
    FILE_NAME_PATTERN_STRING = "\d+\.wav$"
    FILE_NAME_PATTERN = re.compile(FILE_NAME_PATTERN_STRING)
    FILE_NUMBER_PATTERN_STRING = "(\d)+\."
    FILE_NUMBER_PATTERN = re.compile(FILE_NUMBER_PATTERN_STRING)
     
    def __init__(self):
        create_folder(self.FOLDER_NAME)

    def get_current_messages(self) -> list[bytearray]:
        """ This method loads all the messages from the path into memory. 
        
        Path is standard './messages". This method should be called anew 
        every time a new message is added so that the data is never stale. 
        """

        file_names = get_file_names(self.PATH)
        clean_file_names = self.clean_file_names(file_names)
        files = []

        for fn in clean_file_names:
            path = f"{self.PATH}/{fn}"
            with open(path, "rb") as f:
                file = f.read()
                files.append(file)

        return files

    def message_amount_within_limit(self, file_names: list) -> bool:
        amount = len(file_names)

        if amount < self.MESSAGE_LIMIT:
            return True
        else:
            return False
    
    def find_largest_number(self, clean_file_names: list) -> int:
        largest = -math.inf

        for name in clean_file_names:
            number = self.FILE_NUMBER_PATTERN.search(name)
            group = number.group()
            group = group[:-1]
            possible_largest = int(group)
            largest = max(largest, possible_largest)
        
        return largest


    def find_smallest_number(self, clean_file_names:list) -> int:
        smallest = math.inf

        for name in clean_file_names:
            number = self.FILE_NUMBER_PATTERN.search(name)
            group = number.group()
            group = group[:-1]
            possible_smallest = int(group)
            smallest = min(smallest, possible_smallest)
        
        return smallest


    def new_message_name(self, clean_file_names: list) -> str:
        current_amount = len(clean_file_names)

        if current_amount <= 0:
            return f"{self.PATH}/0.wav"

        last_number = self.find_largest_number(clean_file_names)
        new_last_item_number = last_number + 1
        new_last_item_file_name = f"{self.PATH}/{new_last_item_number}.wav"
        
        return new_last_item_file_name

    def write_message(self, path: str, message: bytearray):
        with open(path, "wb") as f:
            f.write(message)

    def clean_file_names(self, file_names):
        names = [x for x in file_names if self.FILE_NAME_PATTERN.match(x)]
        return names

    def new_message(self, message: bytearray):
        """ Saves message to persistent storage. If the new message increases the total count above the limit, then the message with lowest count (effectivly the oldest message) is deleted. The new message will be named like: "x.wav" where x is a number. This number is found by finding the message with the largest number and then increment it by one. 

        Eg. if the file with filename "36.wav" is the number which is largest, then the new message will be called "37.wav". 

        Limit is 9223372036854775807. 
        """
        
        file_names = get_file_names(self.PATH)
        clean_file_names = self.clean_file_names(file_names)
        is_within_limit = self.message_amount_within_limit(clean_file_names)

        if is_within_limit:
            new_last_item_file_name = self.new_message_name(clean_file_names)
            #print(f"Is within limit and: {new_last_item_file_name}")

            self.write_message(new_last_item_file_name, message)

        else:
            first_file_name = self.find_smallest_number(clean_file_names)
            first_file_path = f"{self.PATH}/{first_file_name}.wav"  
            new_last_item_file_name = self.new_message_name(clean_file_names)
            print(f"Is not within limit and new: {new_last_item_file_name}, remove: {first_file_path}")

            os.remove(first_file_path)
            self.write_message(new_last_item_file_name, message)
        

m = MessageManager()

f = get_file_names(m.PATH)
print(f)
c = m.clean_file_names(f)
print(c)
last = m.new_message_name(c)
print(last)

# with open("./assets/confirmation.wav", "rb") as f:
#     file = f.read()

#     for i in range(10):
#         m.new_message(file)

s = m.get_current_messages()
print("hello")