#------------------------------------------#
# Title: Assignmen08.py
# Desc: Assignnment 08 - Working with classes
# Change Log: (Who, When, What)
# JHsu, 2020-Mar-13, started file
# JHsu, 2020-Mar-15, finished file
#------------------------------------------#

# -- DATA -- #
strFileName = 'CDInventory.txt'
lstOfCDObjects = []

class ValueToLowError(Exception):
    def __str__(self):
        return 'ID cannot be in the negatives.'

class ValueWrongError(Exception):
    def __str__(self):
        return 'ID cannot be a letter.'

class ValueIncorrectError(Exception):
    def __str__(self):
        return 'Option entered is invalid. Please choose a valid option.'

class CD:
    """Stores data about a CD:

    properties:
        cd_id: (int) with CD ID
        cd_title: (string) with the title of the CD
        cd_artist: (string) with the artist of the CD
    methods:

    """

    def __init__(self, cd_id, cd_title, cd_artist):
        self.__cd_id = cd_id
        self.__cd_title = cd_title
        self.__cd_artist = cd_artist
        
    @property
    def cd_id(self):
        return self.__cd_id
 
    @property
    def cd_title(self):
        return self.__cd_title
 
    @property
    def cd_artist(self):
        return self.__cd_artist
  
    @cd_id.setter
    def cd_id(self, cd_id):
     try:
      self.cd_id = int(cd_id)
     except Exception:
      raise Exception("Must be an int")
   
    
# -- PROCESSING -- #
class DataProcessor:

    """Allows user to delete entries with valid CD IDs and add additional CD entries

    properties:

    methods:
        delete_entry
        insert_entry

    """
    @staticmethod
    def delete_entry(cd_id, list):
        cdRemoved = False
        for cd in list:
            if int(cd.cd_id) == cd_id:
                list.remove(cd)
                cdRemoved = True
        if cdRemoved:
            print('The CD was removed')

    @staticmethod
    def insert_entry(cd, list):
        list.append(cd)

class FileIO:
    """Processes data to and from file:

    properties:

    methods:
        save_inventory(file_name, lst_Inventory): -> None
        load_inventory(file_name): -> (a list of CD objects)

    """
    @staticmethod
    def load_inventory(file_name):
     try:
        cdList = []
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            cd = CD(data[0], data[1], data[2])
            cdList.append(cd)
        objFile.close()
        return cdList
     except FileNotFoundError:
         print("The file {} could not be loaded".format(file_name))
         print('You must create a \'CDInventory.txt\' file for the program to work')
 

    @staticmethod
    def save_inventory(file_name, list):
        objFile = open(file_name, 'w')
        for cd in list:
            objFile.write(cd.cd_id + ', ' + cd.cd_title + ', ' + cd.cd_artist + '\n')
        objFile.close()

    pass

# -- PRESENTATION (Input/Output) -- #
class IO:
    """Handling Input / Output as entered by the user"""
    @staticmethod
    def print_menu():

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        while True:
            try:
                choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
                if choice not in ['l', 'a', 'i', 'd', 's', 'x']:
                    raise ValueIncorrectError()
                return choice
            except Exception as e:
                print(e)
                continue

    @staticmethod
    def add_entry():
       while True:
        try:
            cd_id = input('Enter ID:').strip()
            intNum = str(cd_id)
            if  intNum.isalpha():
                raise ValueWrongError()
            intNum = int(cd_id)
            if intNum < 0:
                raise ValueToLowError()
            cd_title = input('Enter CD Title:').strip()
            cd_artist = input('Enter Artist Name:').strip()
            return CD(cd_id, cd_title, cd_artist)
        except Exception as e:
            print(e)
            continue

    @staticmethod
    def show_inventory(table):
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for cd in table:
            print (cd.cd_id, cd.cd_title, cd.cd_artist)
        return table

        print('======================================')


# -- Main Body of Script -- #
lstOfCDObjects = FileIO.load_inventory(strFileName)

while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':

        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            lstOfCDObjects = FileIO.load_inventory(strFileName)
            IO.show_inventory(lstOfCDObjects)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        cd = IO.add_entry()
        DataProcessor.insert_entry(cd, lstOfCDObjects)
        # 3.3.2 Add item to the table

        IO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstOfCDObjects)
        # 3.5.1.2 ask user which ID to remove
        while True:
            try:
                intIDDel = int(input('Which ID would you like to delete? ').strip())
                break
            except ValueError:
                print("Please enter an int value")

        DataProcessor.delete_entry(intIDDel, lstOfCDObjects)
        IO.show_inventory(lstOfCDObjects)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstOfCDObjects)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileIO.save_inventory(strFileName, lstOfCDObjects)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
