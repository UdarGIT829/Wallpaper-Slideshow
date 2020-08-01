#Check if file exists
def file_exists(path):
    try:
        with open(path) as f:
            return True
        # Do something with the file
    except FileNotFoundError:
        print("File not accessible")
        return False

def read_file(path):
    paths_list = list()
    with open(path) as f:
        for line in f:
            if line != "\n":
                item = line[:-1]
                paths_list.append(item)
    return paths_list

def write_to_file(path, output_list):
    with open(path, "a+") as f:
        for element in output_list:
            f.write(element)
            f.write("\n")