import glob
import sys
import textgrids
from collections import defaultdict


''' Input: directory of TextGrid files
	Print out the counts of each word/phone, per file
	To run: python src/get_tg_word_counts.py {textgrid_directory}
'''

if __name__ == '__main__':

	tg_dir = sys.argv[1]

	all_dict = {}
	phone_set = set()
	for fname in glob.glob(f'{tg_dir}/**/*.TextGrid', recursive=True):

		file_id_pred = fname.replace(tg_dir, '').replace('/', '_').split('.')[0]
		# print(file_id_pred)

		phone_counts = defaultdict(int)

		grid = textgrids.TextGrid(fname)
		# for item in grid['words']:
		for item in grid['phones']:
			phone = item.text
			if not phone:  # ''
				continue

			phone_counts[phone] += 1

		all_dict[file_id_pred] = phone_counts
		phone_set.update(phone_counts.keys())

	ordered_phone_list = sorted(list(phone_set))
	for file_id, file_counts in all_dict.items():
		print(file_id)
		for phone in ordered_phone_list:
			try:
				print(f'{file_counts[phone]}\t{phone}')
			except:
				print(f'0\t{phone}')
