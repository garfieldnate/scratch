# Randomizes entries in german_freq.html
import sys
import random
# make shuffling deterministic between runs
random.seed(0)

def main(argv):
	if len(argv) != 2:
		print('Usage: randomize_entries.py <german_freq.html>')
		sys.exit(1)

	all_entries = []
	with open(argv[1]) as f:
		in_entries = False
		current_entry = []
		for row in f:
			if row.startswith("<div class='entry'>"):
				if in_entries:
					all_entries.append(current_entry)
				in_entries = True
				current_entry = [row]
			elif in_entries:
				current_entry.append(row)
			else:
				print(row, end='')
		all_entries.append(current_entry)

	random.shuffle(all_entries)
	for entry in all_entries:
		for row in entry:
			print(row, end='')
	# print(len(all_entries))


if __name__ == '__main__':
	main(sys.argv)