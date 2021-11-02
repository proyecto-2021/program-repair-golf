		
def read_file(path, mode):
	file = open(path, mode)
	content = file.read()
	file.close()
	return content

def save_file(path, mode, content):
	file = open(path, mode)
	file.write(content)
	file.close()

#gets the filename from a path containing it
def get_filename(path):
	return path.split('/')[-1]

#returns a new path, if no filename, takes the original name from a path
def determine_path(filename, base_path, old_path):
	if filename is None:
		return base_path + get_filename(old_path)
	else:
		return base_path + filename

#returns a the content of a file, if file is none, returns content of old path
def determine_content(file_content, path_to_old_content):
	if file_content != None:
		return file_content.read()   #read it, and store its content
	else:
		return read_file(path_to_old_content, "rb")
	
#saves a file with new name and new content
#if not a new name it uses the old one, same for content
def save_changes(new_name, file_content, old_file_path, base_path):
	new_path = determine_path(new_name, base_path, old_file_path)
	#gets new or old content
	source_code = determine_content(file_content, old_file_path)
	save_file(new_path, "wb", source_code)
	return new_path
