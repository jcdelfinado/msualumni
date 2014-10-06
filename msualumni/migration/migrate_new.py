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
			alum['last'] = data[0]
			alum['first'] = data[1]
			alum['middle'] = data[2]
			print alum
			alum['hometown'] = data[6]
			grad_list = []
			print "getting grad data"
			grad_list = get_grad_list(
					degrees =split_degree(data[3]),
					dates = split_date(data[4]),
					campus = (data[5][2:-1].split(','))
				)
			
			alum['id'] = get_alum_id(grad_list)
			#each grad dict in the list gets identified with an alum
			for g in grad_list:
				g['alum_id'] = alum['id']
				g['last'] = alum['last']
				g['first'] = alum['first']
				g['middle'] = alum['middle'] if alum.has_key('middle') else ''
				g['hometown'] = alum['hometown']
				save_to_file(g, 'alumni.csv', OrderedDict([('alum_id',None),
														('last',None),
														('first',None),
														('middle',None),
														('hometown',None),
														('course',None),
														('month',None),
														('year',None),
														('campus',None),
														]))
			data_count += 1
		except:
			print sys.exc_info()[0], sys.exc_info()[1]
			return -1

	return data_count

def save_to_file(data, filename, fields):

	with open(filename, 'a') as csvfile:
		file = csv.DictWriter(csvfile, fields, delimiter=';')
		file.writerow(data)
		csvfile.close()

def get_grad_list(degrees, dates, campus):

	"""
		returns a list of grad dicts
	"""
	less_campus = False
	if len(degrees) > len(campus):
		less_campus = True
	grads = []
	for i in range(len(degrees)):
		print "index", i
		course = degrees[i]
		year = dates[i]['year']		
		month = dates[i]['month'] if dates[i].has_key('month') else None
		print "here"
		camp = campus[0] if less_campus else campus[i]
		camp = camp.strip()
		print camp
		grads.append({
			'course':course,
			'year':year,
			'month':month,
			'campus':campus
			})
		print grads
	return grads
 
def get_alum_id(grad):
	try:
		global sequences
		year = grad[0]['year']
		for g in grad:
			if g['year'] < year:
				year = g['year']

		if sequences.has_key(year):
			next_id = sequences[year] + 1
			sequences[year] = next_id
		else:
			sequences[year] = 1
			next_id = 1
		return str(year) + get_string(next_id)
	except:
		print "@ ID"
		print sys.exc_info()[0], sys.exc_info()[1]
		return -1

def get_string(id):

	digits = len(str(id))
	zeros = 4 - digits
	id_string = ''
	for x in range(zeros):
		id_string += '0'
	id_string += str(id)
	return id_string

def split_date(full):

	try:
		dates = []
		full = full[2:-1]
		print "raw date", full
		separated = full.split(',')
		date = {}
		print separated
		print len(separated)
		for item in separated:
			print "ITEM", item
			if item.strip().isdigit():
				date['year'] = item.strip()
				print "from year", date
			else:
				print "splitting"
				split_item = item.strip().split(' ')
				print "SPLIT ITEM:", split_item
				if split_item[0].strip().isalpha():
					date['month'] = split_item[0].strip()
					print "from month", date
			if len(separated) < 2 or (date.has_key('month') and date.has_key('year')):
				print "APPENDED:", date
				dates.append(date)
				date = {}
			
		print dates
		return dates
	except:
		print sys.exc_info()[0], sys.exc_info()[1]
		return -1


def split_degree(data):

	degrees = []
	data = data[2:-1]
	raw = data.split(',')
	return raw

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
	print "BEGIN"
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