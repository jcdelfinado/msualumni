import sys, re, pickle, csv
from datetime import datetime
from collections import OrderedDict

data_count = 0
error_count = 0
sequences = {}

class FormatError:

	def __init__(self, value):
		global error_count
		self.value = value
		report(value)
		error_count += 1

	def __str__(self):
		return repr(self.value)

def parse(file):

	
	for line in file:
		try:
			alum = {}
			global data_count
			data = line.split(';')
			alum = get_name_dict(data[0].strip())
			print data[0]
			campus = data[2]
			grad = []
			degrees = split_dual(data[1])
			for d in degrees:
				degree = {}
				date, degree['course'] = split_date_and_course(d)
				degree['month'], degree['year'] = get_date_dict(date.strip())
				degree['campus'] = campus
				grad.append(degree)
			alum['id'] = get_alum_id(grad)
			for g in grad:
				g['alum_id'] = alum['id']
				g['last'] = alum['last']
				g['first'] = alum['first']
				g['middle'] = alum['middle'] if alum.has_key('middle') else ''
				save_to_file(g, 'alumni.csv', OrderedDict([('alum_id',None),
														('last',None),
														('first',None),
														('middle',None),
														('course',None),
														('month',None),
														('year',None),
														('campus',None),
														]))
			data_count += 1
		except FormatError as e:
			print e.value
			print 'Skipping Data'
			continue
		except:
			report('ERROR ' + line )
			continue

	return data_count
def save_to_file(data, filename, fields):

	with open(filename, 'a') as csvfile:
		file = csv.DictWriter(csvfile, fields, delimiter=';')
		file.writerow(data)
		csvfile.close()
 
def get_alum_id(grad):

	global sequences

	if len(grad) > 1:
		if grad[0]['year'] < grad[1]['year']:
			year = grad[0]['year']
		else:
			year = grad[1]['year']
	else:
		year = grad[0]['year'] 

	if sequences.has_key(year):
		next_id = sequences[year] + 1
		sequences[year] = next_id
	else:
		sequences[year] = 1
		next_id = 1
	return str(year) + get_string(next_id)


def get_string(id):

	digits = len(str(id))
	zeros = 4 - digits
	id_string = ''
	for x in range(zeros):
		id_string += '0'
	id_string += str(id)
	return id_string

def get_name_dict(full):

	name = {}
	raw = full.split(',')
	name['last'] = raw[0].strip()
	raw_name = raw[1].strip()
	if len(raw) > 2: #has jr or other format errors
		raw_name = ' '.join(raw[1:])
	if raw_name[-1] == '.':
		name['first'] = raw_name[:-2].strip()
		name['middle'] = raw_name[-2]
	else:
		print '\nWARNING: No middle initial read.\n\tTaking all entries after comma as first name.'
		print '\nFIRST NAME:', raw_name
		choice = raw_input('Report as Format Error? [y/n]')
		if choice in ('y', 'Y'):
			#report(name['last'], 'Name Format Error')
			raise FormatError('NameFormat Error: '+ full)
		elif choice in ('n', 'N'):
			choice = raw_input('Use last word as middle name? [y/n]')
			if choice in ('y', 'Y'):
				split = raw_name.split(' ')
				name['middle'] = split.pop()
				raw_name = ' '.join(split)			
			name['first'] = raw_name.strip()
	return name

def get_date_dict(full):

	date = {}
	#print "raw date", full
	sep = full.split(',')
	if len(sep) > 1:
		if sep[-1].strip().isdigit():
			date['year'] = sep[-1].strip()
			date['month'] = sep[0].split(' ')[0]
		else:
			raise FormatError('Date Format Error: ' + full)
	else:
		sep = sep[0].split(' ')
		date['month'] = sep[0].strip()
		if sep[0].strip().isdigit():
			date['year'] = sep[0].strip()
		else:
			raise FormatError('Date Format Error: ' + full)
	return date['month'], date['year']


def split_dual(data):

	if is_dual(data):
		degrees = []
		raw = data.split(' and ')
	else:
		raw = [data]
	if len(raw) > 2:
		#has 'and' in course (e.g. Hotel and Restauran Mgt.)
		print raw
		new_raw = []
		for index, value in enumerate(raw):
			if not index%2 or index == 0:
				print index
				new_raw.append(raw[index] + ' and ' + raw[index+1])
		raw = new_raw
	return raw

def split_date_and_course(data):

	reverse = data[::-1]
	reverse = reverse.split('-')
	date = reverse[0][::-1]
	course = reverse[1]
	print course
	if len(reverse) > 2:
		course = course + ' ' + reverse[2]
	course = course[::-1]
	return date, course.strip()

def is_dual(data):

	match = re.search(r'\d\sand\s', data)
	return match

def open_file(filename, flag='rU'):

	try:
		file = open(filename, flag)
		return file
	except:
		print sys.exc_info()[1]
		sys.exit(1)

def report(error):

	log = open_file('errors.log', 'a')
	line = str(datetime.today()) + '\t' + error +'\n'
	log.write(line)
	log.close()

def save_obj(obj, name):
    with open(name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open(name + '.pkl') as f:
        return pickle.load(f)

def main():
	global error_count
	global data_count 
	global sequences
	if len(sys.argv) > 1:
		filename = sys.argv[1]
		print filename
	else:
		filename = raw_input('Enter filename or path: ')

	file = open_file(filename)
	try:
		sequences = load_obj('sequences')
	except:
		sequences = {}
		save_obj(sequences, 'sequences')
	data_count = parse(file)
	print str(data_count) + ' processed.'
	if error_count:
		print str(error_count) + " error(s). Check 'errors.log' for details."

	sys.exit(0)

if __name__ == '__main__':
  main()