'(c) Copyright 2012, Juan Sebastian Casallas'
from os import environ # Environment variables
from subprocess import check_output # Make system calls (returning their output)
import re # regex

path = [environ['HOME']]
cmd = ['duff']
params = ['-r'] # Recursive (read directories)
params = params + ['-l','1'] # Minimum size 1 (don't check 0-sized files)
print ' '.join(cmd + params + path)
d_out = check_output(cmd + params + path)
# \d+ : one or more digits, \s : space, \( : parentheses
num_dupes = [int(n) for n in re.findall('(\d+)\sfile[s]\sin\scluster\s\d+\s\(',d_out)]
max_dupe = max(num_dupes)
dupes = re.split('\d+\sfile[s]\sin\scluster\s\d+\s\(',d_out)
out_csv = open('out.csv','w')

sep = '|'

header = ['file','size','num']
# Generate the adequate number of instances to the header
header = header+['instance'+str(i) for i in range(max_dupe)]
header = sep.join(header)
print header # Print the header to the console in case something goes wrong with the file
out_csv.write(header)
out_csv.write('\n')

# \s : space, [0-9a-f]+ : a hexadecimal number, \\n : line break
# Compile since we'll be using it many times
regex = re.compile('\sbyte[s],\sdigest\s[0-9a-f]+\)\\n')
for i in range(1,len(dupes)):
	try:
		splt = regex.split(dupes[i])
		size = splt[0] # First part of the split should be the size
		files = splt[1].split('\n') # Second part of the split should be the files
		file_name = files[0].rpartition('/')[2]
		line = [file_name,size,str(len(files))]+files
		line = sep.join(line)
		print line # Print the lines to the console in case something goes wrong with the file
		out_csv.write(line)
		out_csv.write('\n')
	except:
		pass

out_csv.close()
