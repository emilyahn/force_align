import glob
import textgrids
import argparse
import statistics

""" Evaluate forced alignment output, compare to gold standard

	To run:
		python src/eval_align.py --gold_dir {gold_dir} --pred_dir {pred_dir} --gold_extension {gold_extension}
	Example run:
		py src/eval_align.py --gold_dir data/panara/gold_eval --pred_dir data/out/panara_explicit --gold_extension TextGrid
		py src/eval_align.py --gold_dir data/timit_mod --pred_dir data/out/timit_full_explicit --gold_extension exp.phn
"""

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-t", "--gold_dir", type=str, help="TIMIT or PANARA folder, containing gold files")
	parser.add_argument("-g", "--gold_extension", type=str, help="file extension of gold files (originally '.PHN'). E.g. 'exp.phn")
	parser.add_argument("-p", "--pred_dir", type=str, help="folder of TextGrids with system (predicted) alignments")
	# optional args to specify exact evaluation setup (currently defaults to all)
	parser.add_argument("-w", "--window_msec", type=int, help="number of milliseconds to compute accuracy window evaluation")
	parser.add_argument("-c", "--command", type=str, help="main command to use", choices=['boundary_diff', 'accuracy_window', 'xx'])

	args = parser.parse_args()
	pred_dir = args.pred_dir
	gold_ext = args.gold_extension
	gold_dir = args.gold_dir

	gold_dict = {}
	pred_dict = {}

	# read gold files
	for phone_file in glob.glob(f'{gold_dir}/**/*.{gold_ext}', recursive=True):
		file_id_gold = phone_file.replace(gold_dir, '').replace('/', '_').split('.')[0]
		if file_id_gold.startswith('_'):
			file_id_gold = file_id_gold[1:]

		if file_id_gold.endswith('_gold'):
			file_id_gold = file_id_gold.replace('_gold', '')

		if gold_ext == 'TextGrid':
			grid = textgrids.TextGrid(phone_file)
			utt_list = []
			for item in grid[file_id_gold.split('_')[0]]:  # 'sokriti' or 'turen'
				phone = item.text
				phone = phone.strip()
				if not phone or phone == "unk" or phone == "\s" or phone.isspace():
					continue
				start = round(item.xmin * 1000)
				end = round(item.xmax * 1000)
				utt_list.append((phone, start, end))
			gold_dict[file_id_gold] = utt_list

		else:  # TIMIT dir
			with open(phone_file, 'r') as f:
				# skip sil; convert frames to msec
				gold_dict[file_id_gold] = [(line.split()[2].strip(), round(int(line.split()[0])/16), round(int(line.split()[1])/16)) for line in f.readlines() if line.split()[2].strip() != 'sil']

	# read system predicted textgrids
	for fname in glob.glob(f'{pred_dir}/**/*.TextGrid', recursive=True):

		file_id_pred = fname.replace(pred_dir, '').replace('/', '_').split('.')[0]
		if file_id_pred.startswith('_'):
			file_id_pred = file_id_pred[1:]

		if 'train_no36' in file_id_gold:
			file_id_gold = file_id_gold.replace('train_no36', 'TRAIN')

		utt_list = []
		grid = textgrids.TextGrid(fname)
		# for item in grid['phones']:
		for item in grid['words']:
			phone = item.text
			if not phone:  # ''
				continue

			# convert sec to msec
			start = round(item.xmin * 1000)
			end = round(item.xmax * 1000)
			utt_list.append((phone, start, end))

		pred_dict[file_id_pred] = utt_list

	# compare differences, pairwise
	diffs = []
	for file_id, pred_list in pred_dict.items():
		if file_id not in gold_dict:
			continue

		gold_list = gold_dict[file_id]
		if len(gold_list) != len(pred_list):
			print(file_id, len(gold_list), len(pred_list))  # all good!
			#FOR DEBUGGING:
			# for item in gold_list:
			# 	print(item)
			# print('***')
			# for item in pred_list:
			# 	print(item)
		for i_tup, gold_tup in enumerate(gold_list):
			try:
				pred_tup = pred_list[i_tup]
				# absolute diff of each phone's ONSET only
				# if want OFFSET, use tup[2]
				diff = abs(gold_tup[1] - pred_tup[1])
				diffs.append(diff)
			except:
				import pdb; pdb.set_trace()
				foo=1

	# evaluate
	if not args.command or args.command == 'boundary_diff':

		print('Boundary Onset statistics:')
		print(f'MEAN: {statistics.mean(diffs):0.2f}')
		print(f'MEDIAN: {statistics.median(diffs)}')
		print(f'MIN: {min(diffs)}')
		print(f'MAX: {max(diffs)}')

	if not args.command or args.command == 'accuracy_window':
		if not args.window_msec:
			windows = [10, 20]

		else:
			windows = [args.window_msec]

		print('\n% of onset boundaries within X ms')
		for window_msec in windows:
			within_window = 0
			for diff_item in diffs:
				if diff_item < window_msec:
					within_window += 1

			print(f'WINDOW ({window_msec}ms): {float(within_window/len(diffs)):0.2f}')
