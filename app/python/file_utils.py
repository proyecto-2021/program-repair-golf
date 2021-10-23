
def temporary_save(new_names, code_file, tests_file, old_code_path, old_test_path):
	temp_path = "public/temp/"      #path to temp directory
	
	code_path = determine_path(new_names.get('source_code_file_name'), temp_path, old_code_path)
	test_path = determine_path(new_names.get('test_suite_file_name'), temp_path, old_test_path)

	source_code = None
    if code_file != None:
        source_code = code_file.read()   #read it, and store its content
    else:
        source_code = read_file(old_code_path, "rb")
    save_file(code_path, "wb", source_code)

    source_code_tests = None
    if tests_file != None:
        source_code_tests = tests_file.read()   #read it, and store its content
    else:
        source_code_tests = read_file(old_test_path, "rb")
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
