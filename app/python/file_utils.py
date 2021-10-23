
def temporary_save(new_names, code_file, tests_file, old_code_path, old_test_path):
	temp_path = "public/temp/"      #path to temp directory
	
	code_path = determine_path(new_names.get('source_code_file_name'), temp_path, old_code_path)
	test_path = determine_path(new_names.get('test_suite_file_name'), temp_path, old_test_path)

	#gets new or old content
	source_code = determine_content(code_file, old_code_path)
	save_file(code_path, "wb", source_code)
	#gets new or old content
	source_code_tests = determine_content(tests_file, old_test_path)
	save_file(test_path, "wb", source_code_tests)
		
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
	