import glob
import argparse
import pandas as pd

""" Iterate through TIMIT dir to generate:
		- .lab sentence transcripts (deposit in same dir)
		- a dictionary/lexicon based on a given phone mapping file
		- .exp.phn ('explicit phone') phone-level segment files, redone to account for merging and remapping of symbols
	To run:
		python src/get_timit_dict_lab.py --timit_dir {timit_dir} --phone_map_file {phone_map_file} --outf {dict_out_file}
	Example run:
		py src/get_timit_dict_lab.py --timit_dir data/LDC93S1/TIMIT --phone_map_file data/notes/timit-map-phones-explicit.txt --outf data/notes/timit-explicit-lex.txt
"""


# lines format: list of tuples (start_int, end_int, chars_str)
def parse_timit_wrd_phn_files(wrd_phn_file):
	with open(wrd_phn_file, 'r') as f:
		lines = [(int(line.split()[0]), int(line.split()[1]), line.split()[2]) for line in f.readlines()]

	return lines


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--timit_dir", type=str, help="main folder or infolder")
	parser.add_argument("-p", "--phone_map_file", type=str, help="main command to use")
	parser.add_argument("-o", "--outf", type=str, help="dictionary or lexicon outfile")
	# parser.add_argument("-l", "--labels", help="whether or not to write .lab files within timit dir", action='store_true')
	args = parser.parse_args()

	timit_dir = args.timit_dir
	phone_map_file = args.phone_map_file
	dict_out_file = args.outf

	# process phone map file
	phone_map = {}
	phone_map_duo = {}  # key: tuple(str1, str2) // value: str3
	out_lex = set()
	with open(phone_map_file, 'r') as f:
		phone_map_lines = []
		for line in f.readlines():
			if not line:
				continue
			if line.startswith('#'):
				continue

			if '\t' in line:
				line = line.strip()
				out_symbol = line.split('\t')[1]
				out_lex.add(out_symbol)
				if '+' in line:
					phone_map_duo[(line.split('\t')[0].split('+')[0], line.split('\t')[0].split('+')[1])] = out_symbol
				else:
					phone_map[line.split('\t')[0]] = out_symbol

			else:
				out_lex.add(line.strip())

	# print(phone_map)
	# print(phone_map_duo)
	duo_first_symbols = set([duo[0] for duo in phone_map_duo])
	# print(duo_first_symbols)

	# note: not utilizing sentence conventions from '.TXT' files
	#		like punctuation or caps
	for phone_file in glob.glob(f'{timit_dir}/**/*.PHN', recursive=True):
		lab_out_file = phone_file.replace('.PHN', '.lab')
		new_phone_out_file = phone_file.replace('.PHN', '.exp.phn')
		phone_lines = parse_timit_wrd_phn_files(phone_file)
		phone_seq = [phone_tup[2] for phone_tup in phone_lines]

		# BEGIN special modifications
		new_phone_seq = []

		# MOD 1: handle merges b/w consecutive symbols (e.g. tcl+t -> t)
		phone_idx = 0
		while phone_idx < len(phone_seq) - 1:  # excludes last symbol
			phone = phone_seq[phone_idx]
			found_match = False
			if any(phone == duo_sym for duo_sym in duo_first_symbols):
				# get all phone maps keys for the matched phone
				matched_phone_maps = [phone_tup for phone_tup in phone_map_duo if phone_tup[0] == phone]
				for matched_phone_map in matched_phone_maps:
					if matched_phone_map[1] == phone_seq[phone_idx + 1]:
						new_phone_seq.append((phone_idx, phone_map_duo[matched_phone_map]))
						phone_idx += 1
						found_match = True
						break

			# if no match, add phone to newphoneseq as regular
			if not found_match:
				new_phone_seq.append((phone_idx, phone))
			phone_idx += 1

		new_phone_seq.append((phone_idx, phone_seq[-1]))

		# MOD 2: single substitutions
		for i in range(len(new_phone_seq)):
			if new_phone_seq[i][1] in phone_map:
				new_phone_seq[i] = (new_phone_seq[i][0], phone_map[new_phone_seq[i][1]])

		# END special modifications
		# print(new_phone_seq)
		# print(phone_lines)

		# print(lab_out_file)
		sentence = ' '.join([phon_tup[1] for phon_tup in new_phone_seq])
		with open(lab_out_file, 'w') as w:
			w.write(sentence + '\n')

		# write new PHN files
		new_start_end_phones = []
		last_phone_i = len(new_phone_seq) - 1
		for new_phone_seq_i, (phone_i, phone) in enumerate(new_phone_seq):
			phone_start = phone_lines[phone_i][0]
			new_start_end_phones.append([phone, phone_start])
			if phone_i > 0:
				# print(new_start_end_phones)
				new_start_end_phones[-2].append(phone_start)  # append phone_end
			if new_phone_seq_i == last_phone_i:
				new_start_end_phones[-1].append(phone_lines[phone_i][1])

		# print(new_start_end_phones)
		# print(new_phone_out_file)
		with open(new_phone_out_file, 'w') as w:
			for phone_trio in new_start_end_phones:
				w.write(f'{phone_trio[1]} {phone_trio[2]} {phone_trio[0]}\n')

		# break

	# print(out_lex)
	with open(dict_out_file, 'w') as w:
		for phone in sorted(list(out_lex)):
			if not phone:
				continue
			w.write(f"{phone}\t{phone}\n")
