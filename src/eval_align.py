import glob
import textgrids
import argparse
import statistics
import os
import numpy as np
import pandas as pd

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
	parser.add_argument("-p", "--pred_dir", type=str, help="folder of TextGrids with system (predicted) alignments. If more than one dir, separate with a comma")
	# optional args to specify exact evaluation setup (currently defaults to all)
	parser.add_argument("-w", "--window_msec", type=int, help="number of milliseconds to compute accuracy window evaluation")
	parser.add_argument("-c", "--command", type=str, help="main command to use", choices=['boundary_diff', 'accuracy_window', 'xx'])
	parser.add_argument("-n", "--natural_class_tsv", type=str, help="TSV file to evaluate based on natural classes")

	args = parser.parse_args()
	pred_dir = args.pred_dir
	gold_ext = args.gold_extension
	gold_dir = args.gold_dir

	gold_dict = {}
	pred_dict = {}

	# hack to debug file alignment loss from textgrid preds (i.e. panara)
	textgrid_utt_boundaries = {}

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

			if 'utterances' in grid:
				utt_boundary_list = []
				for utt_item in grid['utterances']:
					if not utt_item.text:
						continue
					utt_boundary_list.append((round(utt_item.xmin * 1000), round(utt_item.xmax * 1000)))
				textgrid_utt_boundaries[file_id_gold] = utt_boundary_list

		else:  # TIMIT dir (gold_extension=exp.phn)
			with open(phone_file, 'r') as f:
				# skip sil; convert frames to msec
				gold_dict[file_id_gold] = [(line.split()[2].strip(), round(int(line.split()[0])/16), round(int(line.split()[1])/16)) for line in f.readlines() if line.split()[2].strip() != 'sil']

	# read system predicted textgrids
	pred_dirs = pred_dir.split(',')
	for one_pred_dir in pred_dirs:
		for fname in glob.glob(f'{one_pred_dir}/**/*.TextGrid', recursive=True):

			if gold_ext == 'TextGrid':
				file_id_pred = os.path.basename(fname).split('.')[0]

			else:
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
	following_phones = []  # phone following the onset
	preceding_phones = []  # phone preceding the onset. Could be SIL

	for file_id, pred_list in pred_dict.items():
		if file_id not in gold_dict:
			continue

		gold_list = gold_dict[file_id]
		if len(gold_list) != len(pred_list):
			print(file_id, len(gold_list), len(pred_list))

			gold_offset_idx = 0
			current_utt_idx = 0

			# for utt_start, utt_end in textgrid_utt_boundaries[file_id]:
			for i_tup, pred_tup in enumerate(pred_list):
				utt_start = textgrid_utt_boundaries[file_id][current_utt_idx][0]
				utt_end = textgrid_utt_boundaries[file_id][current_utt_idx][1]
				# shift gold indices
				while pred_tup[1] > utt_end:
					current_utt_idx += 1
					utt_start = textgrid_utt_boundaries[file_id][current_utt_idx][0]
					utt_end = textgrid_utt_boundaries[file_id][current_utt_idx][1]

				# print(i_tup)
				# print(gold_offset_idx)
				while gold_list[i_tup + gold_offset_idx][2] < utt_start:
					gold_offset_idx += 1

				gold_tup = gold_list[i_tup + gold_offset_idx]

				# absolute diff of each phone's ONSET only
				# if want OFFSET, use tup[2]
				diff = abs(gold_tup[1] - pred_tup[1])
				diffs.append(diff)

				# update lists for following and preceding phones
				following_phones.append(gold_tup[0])
				if i_tup > 0:
					# check if preceding phone and current phone are touching
					if gold_list[i_tup + gold_offset_idx - 1][2] == gold_tup[1]:
						preceding_phones.append(gold_list[i_tup + gold_offset_idx - 1][0])
						continue

				preceding_phones.append('SIL')

			continue

		# when gold and pred lists are same length
		for i_tup, gold_tup in enumerate(gold_list):
			pred_tup = pred_list[i_tup]
			# absolute diff of each phone's ONSET only
			# if want OFFSET, use tup[2]
			diff = abs(gold_tup[1] - pred_tup[1])
			diffs.append(diff)

			# update lists for following and preceding phones
			following_phones.append(gold_tup[0])
			if i_tup > 0:
				if gold_list[i_tup - 1][2] == gold_tup[1]:  # check if preceding phone and current phone are touching
					preceding_phones.append(gold_list[i_tup - 1][0])
					continue

			preceding_phones.append('SIL')

	# evaluate

	# import natural classes list (for Panara only)
	df = pd.read_csv(args.natural_class_tsv, sep="\t", header=0)
	classes = list(df.columns)
	# long_vowels = df['Long Vowels'].dropna()
	class_dict = df.to_dict(orient='list')
	diffs_np = np.array(diffs)
	prec_np = np.array(preceding_phones)
	foll_np = np.array(following_phones)
	phone_set = set(following_phones)

	if not args.command or args.command == 'boundary_diff':

		print('Boundary Onset statistics:')
		print('** OVERALL **')
		print(f'MEAN: {statistics.mean(diffs):0.3f}')
		print(f'MEDIAN: {statistics.median(diffs)}')
		print(f'MIN: {min(diffs)}')
		print(f'MAX: {max(diffs)}')

		for phone_location, phone_list in {'PREC (offset)': prec_np, 'FOLL (onset)': foll_np}.items():
			print(f'\n{phone_location}\n')
			# for class_name in classes:
			for class_name in sorted(list(phone_set)):

				class_diffs = []
				within_window = 0
				window_msec = 20  # hard-coded for now
				for phone_i, phone in enumerate(phone_list):
					# if phone in class_dict[class_name]:
					if phone == class_name:  # fine-grained
						class_diffs.append(diffs_np[phone_i])
						if diffs_np[phone_i] < window_msec:
							within_window += 1

				print(f'\n** {class_name} **')

				try:
					print(f'WINDOW ({window_msec}ms): {float(within_window)*100/len(class_diffs):0.3f}\tCOUNT:{len(class_diffs)}')
					# print(f'{float(within_window)*100/len(class_diffs):0.2f}')
					print(f'MEAN: {statistics.mean(class_diffs):0.2f}')
					print(f'MEDIAN: {statistics.median(class_diffs)}')
					print(f'MIN: {min(class_diffs)}')
					print(f'MAX: {max(class_diffs)}')
				except:
					print('[none]')

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

			print(f'WINDOW ({window_msec}ms): {float(within_window)*100/len(diffs):0.3f}')
