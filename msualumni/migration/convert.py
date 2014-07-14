def convert(infile, outfile):

	file = open(infile)
	converted = open(outfile, 'w')
	text = file.read()
	lines = text.split('\n')
	new_lines = []
	for index, line in enumerate(lines[:50]):
		if index%2:
			prev = lines[index-1]
			#print 'PREV: ', prev
			new_line = str(lines[index-1]) + line
			converted.write(new_line+'\n')
			new_lines.append(new_line)

def main():

	file = open('test.dat')
	converted = open('converted.dat', 'w')
	text = file.read()
	lines = text.split('\n')
	new_lines = []
	for index, line in enumerate(lines):
		if index%2:
			prev = lines[index-1]
			#print 'PREV: ', prev
			new_line = str(lines[index-1]) + line
			converted.write(new_line+'\n')
			new_lines.append(new_line)


if __name__ == '__main__':
	main()