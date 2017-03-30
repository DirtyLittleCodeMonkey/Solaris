

def get_resolution():
    try:
        file = open('config.txt', 'r')
    except:
        with open('config.txt', 'w') as write_file:
            file_contents = 'resolution 800 600'
            write_file.writelines(file_contents)
        file = open('config.txt', 'r')
    lines = file.readlines()
    for line in lines:
        if line.startswith('resolution'):
            fields = line.split()
            return int(fields[1]), int(fields[2])