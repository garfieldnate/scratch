# add simple TOC to existing HTML file
import sys


def add_toc(lines):
	toc_lines = []
	new_lines = []
	entry_counter = 0
	space_counter = 0
	for line in lines:
		if "<div class='entry'" in line:
			entry_counter += 1
			space_counter += 1
			if space_counter % 50 == 0:
				space_counter = 0
				new_lines.append(f'<span id="{entry_counter}">Entry number {entry_counter} (<a href="#top">top</a>)</span>')
				toc_lines.append(f'<a href="#{entry_counter}">{entry_counter}</a><br/>')
		new_lines.append(line)

	return new_lines[0:3] + ['<div id="top"></div>'] + toc_lines + new_lines[3:]



def output_final(lines):
	for line in lines:
		print(line, end='')

def main(argv):
	if len(argv) != 2:
		raise ValueError("Usage: python3 make_toc.py <html file>")
	lines = open(argv[1]).readlines()
	lines_with_toc = add_toc(lines)
	output_final(lines_with_toc)

if __name__ == '__main__':
	main(sys.argv)