import os, sys  # Importing necessary libraries
import hashlib  # Importing hashlib for checksum creation

class tripwire:
    folder = ''  # Folder to monitor
    record_file = ''  # File to store checksums
    opt = ''  # Option to either create or check checksums

    def __init__(self, check_folder, save_file, opt):
        # Constructor initializes the instance variables
        self.folder = check_folder
        self.record_file = save_file
        self.opt = opt

    def run(self):
        # Depending on the option, either save or check checksums
        if self.opt == 'c':
            self.save_checksum()
        else:
            self.checksum()

    def save_checksum(self):
        # Save checksums of all files in the folder to the record file
        ret = self.get_all_files_hash()
        try:
            
            with open(self.record_file, 'w+') as fp:
                print(f"Attempting to write to {self.record_file}...")
                fp.write(f"Folder: {os.path.abspath(self.folder)}\n") # Add full length path of the tripwireDir as heading
                for name, hash in ret.items():
                    fp.write(name + ' ' + hash + '\n')
            print(self.record_file, 'Checksum file has been created')
        except IOError as e:
            print('Error writing to file:', e)
            sys.exit(1)

    def checksum(self):
        # Check the current checksums against the saved ones and report changes
        get_current_sum = self.get_all_files_hash()
        check_sum_arr = self.get_check_sum_arr()

        for cn, ch in get_current_sum.items():
            try:
                if not check_sum_arr[cn]:
                    pass
            except:
                print('Added', cn)
                continue
            if check_sum_arr[cn] != ch:
                print('Modified', cn)
        for name in check_sum_arr:
            try:
                get_current_sum[name]
            except:
                print('Removed', name)

    def get_check_sum_arr(self):
        # Retrieve saved checksums from the record file
        fp = open(self.record_file, 'r')
        filecon = fp.readlines()
        check_sum_arr = {}
        for line in filecon:
            lr = line.split(' ')
            lr_name = lr[0]
            hash = lr.pop(-1)
            lr_name = ' '.join(lr)
            check_sum_arr[lr_name] = hash.strip()
        return check_sum_arr

    def get_all_files_hash(self):
        # Calculate checksums for all files in the folder
        file_list = os.listdir(self.folder)
        files = {}
        for file in file_list:
            if os.path.isdir(self.folder + '\\' + file):
                continue
            hash = self.get_check_sum(self.folder + '\\' + file)
            files[file] = hash
        return files

    def get_check_sum(self, file):
        # Calculate the MD5 checksum of a file
        fp = open(os.path.abspath(file), 'rb')
        data = fp.read()
        fileHash = hashlib.md5(data).hexdigest()
        fp.close()
        return fileHash

# Start of script execution
check_folder = ''
save_file = ''
opt = ''
args = sys.argv[1:]  # Get command-line arguments

if len(args) < 2:
    # If not enough arguments, display usage message and exit
    print('Usage:')
    print('      python tripwire.py monitorFolder checksumFile [type letter c to create checksumFile]')
    exit(0)

# Assign command-line arguments to variables
check_folder = args[0]
save_file = args[1]
try:
    opt = args[2]
except:
    pass

# Create a tripwire object and run the monitoring/checking process
tripwireObj = tripwire(check_folder, save_file, opt)
tripwireObj.run()
