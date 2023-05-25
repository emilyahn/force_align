import glob
import textgrids
from argparse import ArgumentParser

""" Evaluate forced alignment output, compare to gold standard

	To run:
		python src/eval_align.py --timit_dir {timit_dir} --phone_map_file {phone_map_file} --outf {dict_out_file}
	Example run:
		py src/eval_align.py --timit_dir data/LDC93S1/TIMIT --phone_map_file data/notes/timit-map-phones-explicit.txt --outf data/notes/timit-explicit-lex.txt
"""

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--command", type=str, help="main command to use", choices=['boundary_diff', 'accuracy_window', 'xx'])
	parser.add_argument("-t", "--timit_dir", type=str, help="TIMIT folder, containing gold files")
	parser.add_argument("-g", "--gold_extension", type=str, help="file extension of gold files (originally '.PHN'). E.g. 'exp.phn")
	parser.add_argument("-p", "--pred_dir", type=str, help="folder of TextGrids with system (predicted) alignments")

	args = parser.parse_args()
	timit_dir = args.timit_dir
	pred_dir = args.pred_dir
	gold_ext = args.gold_extension

	# read system predicted textgrids
	for fname in sorted(glob.glob(tg_files)):
		if not fname.endswith('TextGrid'):
			continue

		utt_list = []
		grid = textgrids.TextGrid(fname)
		for item in grid['phones']:
			phone = item.text
			# convert sec to msec
			start = int(item.xmin * 1000)
			end = int(item.xmax * 1000)
			utt_list.append((phone, start, end))

		# TODO: store utt_list into larger dict/list

	# read gold files
	for phone_file in glob.glob(f'{timit_dir}/**/*.{gold_ext}', recursive=True):
		with open(phone_file, 'r') as f:
			lines = [(line.split()[2].strip(), int(line.split()[0]), int(line.split()[1])) for line in f.readlines()]

		# TODO: store lines into larger dict/list

	# evaluate
	if args.command == 'boundary_diff':
		pass
		# use math.abs(x)

	elif args.command == 'accuracy_window':
		pass

