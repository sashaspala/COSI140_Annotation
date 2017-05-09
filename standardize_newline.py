import os

def move_newline(input_path, output_path):
	with open(input_path) as xml_file, open(output_path, 'w') as out_file :
		temp = ''
		for line in xml_file:
			if str(line) == ']]></TEXT>\n':
				temp = temp.rstrip()
			temp += line
		out_file.write(temp)


path = '/Users/sspala2/Desktop/Annotation/meghan_4-24'
output = '/Users/sspala2/Desktop/Annotation/fixed/'
for file in os.listdir(path):
	if os.path.isfile(os.path.join(path, file)) and file != '.DS_Store':
		move_newline(os.path.join(path, file), output + file)
