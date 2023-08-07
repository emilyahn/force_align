import glob
import textgrids
import argparse
import statistics

""" Evaluate forced alignment output, compare to gold standard

	To run:
		python src/eval_align.py --timit_dir {timit_dir} --pred_dir {pred_dir} --gold_extension {gold_extension} --command {command}
	Example run:
		py src/eval_align.py --timit_dir data/LDC93S1/TIMIT/TRAIN/DR7 --pred_dir data/out/ldc_pilot_dr7 --gold_extension exp.phn --command boundary_diff
"""

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-c", "--command", type=str, help="main command to use", choices=['boundary_diff', 'accuracy_window', 'xx'])
	parser.add_argument("-t", "--timit_dir", type=str, help="TIMIT folder, containing gold files")
	parser.add_argument("-g", "--gold_extension", type=str, help="file extension of gold files (originally '.PHN'). E.g. 'exp.phn")
	parser.add_argument("-p", "--pred_dir", type=str, help="folder of TextGrids with system (predicted) alignments")
	parser.add_argument("-w", "--window_msec", type=int, help="number of milliseconds to compute accuracy window evaluation")

	args = parser.parse_args()
	timit_dir = args.timit_dir
	pred_dir = args.pred_dir
	gold_ext = args.gold_extension

	gold_dict = {}
	pred_dict = {}

	# read gold files
	for phone_file in glob.glob(f'{timit_dir}/**/*.{gold_ext}', recursive=True):
		file_id_gold = phone_file.replace(timit_dir, '').replace('/', '_').split('.')[0]
		if file_id_gold.startswith('_'):
			file_id_gold = file_id_gold[1:]

		with open(phone_file, 'r') as f:
			# skip sil; convert frames to msec
			gold_dict[file_id_gold] = [(line.split()[2].strip(), round(int(line.split()[0])/16), round(int(line.split()[1])/16)) for line in f.readlines() if line.split()[2].strip() != 'sil']

	# read system predicted textgrids
	for fname in glob.glob(f'{pred_dir}/**/*.TextGrid', recursive=True):

		file_id_pred = fname.replace(pred_dir, '').replace('/', '_').split('.')[0]
		if file_id_pred.startswith('_'):
			file_id_pred = file_id_pred[1:]

		utt_list = []
		grid = textgrids.TextGrid(fname)
		for item in grid['phones']:
			phone = item.text
			if not phone:  # ''
				continue

			# convert sec to msec
			start = round(item.xmin * 1000)
			end = round(item.xmax * 1000)
			utt_list.append((phone, start, end))

		pred_dict[file_id_pred] = utt_list

	diffs = []
	for file_id, gold_list in gold_dict.items():
		pred_list = pred_dict[file_id]
		# if len(gold_list) != len(pred_list):
		# 	print(file_id)  # all good!
		for i_tup, gold_tup in enumerate(gold_list):
			pred_tup = pred_list[i_tup]
			# absolute diff of each phone's ONSET only
			# if want OFFSET, use tup[2]
			diff = abs(gold_tup[1] - pred_tup[1])
			diffs.append(diff)

	# evaluate
	if not args.command or args.command == 'boundary_diff':

		print(f'MEAN: {statistics.mean(diffs):0.2f}')
		print(f'MEDIAN: {statistics.median(diffs)}')
		print(f'MIN: {min(diffs)}')
		print(f'MAX: {max(diffs)}')

	if not args.command or args.command == 'accuracy_window':
		if not args.window_msec:
			windows = [10, 20]

		else:
			windows = [args.window_msec]

		for window_msec in windows:
			within_window = 0
			for diff_item in diffs:
				if diff_item < window_msec:
					within_window += 1

			print(f'WINDOW ({window_msec}ms): {float(within_window/len(diffs)):0.2f}')
