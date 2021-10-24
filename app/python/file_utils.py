		
def read_file(path, mode):
	file = open(path, mode)
	content = file.read()
	file.close()
	return content

def save_file(path, mode, content):
	file = open(path, mode)
	file.write(content)
	file.close()

#returns a new path, if no filename, takes the original name from a path
def determine_path(filename, base_path, old_path):
	if filename is None:
		return base_path + (lambda x: x.split('/')[-1]) (old_path)
	else:
		return base_path + filename

#returns a the content of a file, if file is none, returns content of old path
def determine_content(file_content, path_to_old_content):
	if file_content != None:
		return file_content.read()   #read it, and store its content
	else:
		return read_file(path_to_old_content, "rb")
	