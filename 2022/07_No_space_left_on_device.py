class MyFile():
    def __init__(self, name, size):
        self.name = name
        self.size = size

class MyFolder():
    def __init__(self, name, parent, contents):
        self.name = name
        self.parent = parent
        self.contents = contents


def read_file(filename):
    with open(filename, 'r') as file:
        return file.read().split('\n')


def create_filesystem_from_commands(commands):

    filesystem = MyFolder("/", None, [])
    current_dir = filesystem
    for row in commands:
        words = row.split()
        if words[0] == '$':
            # user input
            if words[1] == 'cd':
                # TODO cd
                if words[2] == '/':
                    current_dir = filesystem
                elif words[2] == '..':
                    current_dir = current_dir.parent
                else:
                    current_dir.contents.append(MyFolder(words[2], current_dir, []))
                    current_dir = current_dir.contents[-1]
            elif words[1] == 'ls':
                # TODO ls
                pass
            
        else:
            # system output
            if words[0] == 'dir':
                current_dir.contents.append(MyFolder(words[1], current_dir, []))
            else:
                current_dir.contents.append(MyFile(words[1], int(words[0])))
    
    return filesystem


def print_filesystem(fs, indent="-"):
    print(indent, fs.name, "(dir)")
    for item in fs.contents:
        if type(item) is MyFile:
            print("      "+indent, item.name, f"(file, size={item.size})")
        else:
            print_filesystem(item, indent="  "+indent)


def print_filesystem_folders_only(fs, indent="-"):
    print(indent, fs.name, "(dir)", "size: ", filesystem_size(fs))
    for item in fs.contents:
        if type(item) is MyFolder:
            print_filesystem_folders_only(item, indent="  "+indent)


def filesystem_size(fs):
    size = 0
    for item in fs.contents:
        if type(item) is MyFile:
            size += item.size
        else:
            size += filesystem_size(item)
    return size


def sum_of_folders_lte_x(fs, x):
    total = 0
    fssize = filesystem_size(fs)
    if fssize <= x:
        total += fssize

    for item in fs.contents:
        if type(item) is MyFolder:
            total += sum_of_folders_lte_x(item, x)

    return total

def create_test_fs():
    files = [MyFile("test.txt", 5000), MyFile("foo.bar", 1000)]
    root = MyFolder("/", None, files)
    return root
    

def find_folder_to_delete(fs, used_disk_space, best_candidate=70000000, total_disk_space=70000000, needed_disk_space=30000000):
    free_disk_space = total_disk_space - used_disk_space
    fssize = filesystem_size(fs)
    if free_disk_space + fssize >= needed_disk_space and fssize < best_candidate:
        best_candidate = fssize
    for item in fs.contents:
        if type(item) is MyFolder:
            candidate = find_folder_to_delete(item, used_disk_space, best_candidate=best_candidate, total_disk_space=total_disk_space, needed_disk_space=needed_disk_space)
            if candidate < best_candidate:
                best_candidate = candidate
    return best_candidate

    

def main():
    filename = 'inputs/07_input.txt'
    commands = read_file(filename)
    fs = create_filesystem_from_commands(commands)    
    #test_fs = create_test_fs()
    
    #print_filesystem_folders_only(fs)
    print(sum_of_folders_lte_x(fs, 100000))
    print(find_folder_to_delete(fs, used_disk_space=filesystem_size(fs), best_candidate=70000000, total_disk_space=70000000, needed_disk_space=30000000))

if __name__ == "__main__":
    main()


