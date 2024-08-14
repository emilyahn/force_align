import epitran
import argparse
import js2py
import re
import glob
import os
from praatio import textgrid  # module used to be 'tgio'
# import textgrids
# import statistics

""" 1. Takes a folder with Transcribed ELAN (in tab-sep .txt, in Panãra orthography) files,
	2. Conducts G2P (Grapheme-to-Phoneme) for Panãra,
	3. Outputs TextGrids with phone sequences (treating phones as words)
	4. Outputs dictionary

	Notes:
	Mostly uses Teela Huff's javascript G2P, and applies some post-processing rules.
	Includes a Portuguese G2P (from Epitran).
	Alternately takes in a wordlist (tab-separated words of orth & phonetic sequence), for testing.

	To run:
		python src/g2p_panara.py
	Example run:
		py src/g2p_panara.py --jsfile src/panara_orth_to_phon.js --wordlist data/panara/wordlist_g2p_gold.tsv
		py src/g2p_panara.py --jsfile src/panara_orth_to_phon.js --input_dir data/panara/intvw_input --dictfile data/panara/dict_panara_phone_narrow.txt
"""

orth_dict = {'ï': 'ĩ', 'ÿ': 'ỹ', 'ü': 'ũ', 'ë': 'ẽ', 'ä': 'ã', 'ö': 'õ', 'á': 'a', 'í': 'i'}
out_nasal_dict = {'ỹ': 'ɯ̃', 'ã': 'ɤ̃'}
# nasal_dict = {'ï': 'ĩ', 'ÿ': 'ɯ̃', 'ü': 'ũ', 'ë': 'ẽ', 'ä': 'ɤ̃', 'ö': 'õ'}

def post_process(orig_str):
	out_str = orig_str
	# 1. convert umlaut vowels to nasal vowels
	double_nasal_dict = {'ĩĩ': 'ĩː', 'ɯ̃ɯ̃': 'ɯ̃ː', 'ũũ': 'ũː', 'ẽẽ': 'ẽː', 'ɤ̃ɤ̃': 'ɤ̃ː', 'õõ': 'õː'}
	for umlaut_char, nasal_char in out_nasal_dict.items():
		out_str = out_str.replace(umlaut_char, nasal_char)

	# 2. remove stress and syllables marks
	out_str = out_str.replace('.', '').replace('ˈ', '')

	# 3. convert colon into length mark, and remove duplicate length mark
	out_str = out_str.replace(':', 'ː')
	out_str = out_str.replace('ːː', 'ː')

	# 4. convert double consonants into geminates
	out_str = re.sub(r'(\D)\1+', r'\1ː', out_str)
	for double_char, single_char in double_nasal_dict.items():
		out_str = out_str.replace(double_char, single_char)

	return out_str


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-w", "--wordlist", type=str, help="tab-delimited word list of orthography to IPA, manually defined. used as input for checking G2P post-processing rules.")
	parser.add_argument("-j", "--jsfile", type=str, help="name of Teela's G2P javascript file")
	parser.add_argument("-i", "--input_dir", type=str, help="folder with Transcribed ELAN (in tab-sep .txt, in Panãra orthography) files")
	parser.add_argument("-d", "--dictfile", type=str, help="filename of output dictionary for MFA")

	args = parser.parse_args()
	js_file = args.jsfile
	eval_res, tempfile = js2py.run_file(js_file)

	if args.dictfile:
		phone_set = set()

	# return list of IPA phones
	def eval_g2p(txt_input):
		g2p_input = f'//[]<{txt_input.replace(" ", "")}>(){{}}||'
		g2p_output = tempfile.PHONFILL(g2p_input)
		# out_phoneme = g2p_output.split('/')[1]
		out_phones = g2p_output.split('[')[1].split(']')[0]
		post_processed_str = post_process(out_phones).replace(' ', '')
		out_str_space_sep = post_processed_str[0]
		for out_i in range(1, len(post_processed_str)):
			if post_processed_str[out_i] == '̃' or post_processed_str[out_i] == 'ː':
				out_str_space_sep += post_processed_str[out_i]
			else:
				out_str_space_sep += ' ' + post_processed_str[out_i]

		return out_str_space_sep.split()

	if args.input_dir:
		epi = epitran.Epitran('por-Latn')

		for elan_txt_file in glob.glob(f'{args.input_dir}/*.txt',):
			# for now, skip pnr_hist_snake file
			if elan_txt_file.endswith('pnr_hist_snake.txt'):
				continue

			file_basename = os.path.basename(elan_txt_file)  # includes .txt

			# choose '_epa' versions (manually updated by Emily)
			if file_basename.startswith('pnr') and not file_basename.endswith('_epa.txt'):
				continue

			if 'sokriti' in elan_txt_file:
				speaker = 'sokriti'
			else:
				speaker = file_basename.split('_')[2].split('-')[0]

			with open(elan_txt_file, 'r') as f:
				lines = [line.strip() for line in f.readlines() if line.startswith('A_Transcription')]

			print(f'\n*** {file_basename} ***')
			tg = textgrid.Textgrid()
			# tg = textgrids.TextGrid()
			write_tg_file = os.path.join(args.input_dir, file_basename.replace('.txt', '.TextGrid'))
			tg_list = []
			duration = 0
			for elan_line in lines:
				tab_splits = elan_line.split('\t')
				start = float(tab_splits[3])
				end = float(tab_splits[5])
				duration = end
				elan_txt = tab_splits[8]

				# basic clean-up
				elan_txt = elan_txt.lower()
				elan_txt = elan_txt.replace('/', '')
				elan_txt = elan_txt.replace('?', '')
				elan_txt = elan_txt.replace('!', '')
				elan_txt = elan_txt.replace('"', '')
				elan_txt = elan_txt.replace('.', '')  # but keep commas for now

				# remove all content within ()
				elan_txt = re.sub("\(.*?\)", "", elan_txt)

				for umlaut_char, nasal_char in orth_dict.items():
					elan_txt = elan_txt.replace(umlaut_char, nasal_char)

				# entire words in brackets: treat as Portuguese
				# partial words in brackets (direclty attached to a Panara word): treat as Panara
				elan_space_sep = elan_txt.split()
				accumulated_panara = ''
				accumulated_total_prons = []
				for elan_word in elan_space_sep:
					# full portuguese words
					if elan_word.startswith('[') and elan_word.endswith(']'):
						if accumulated_panara:
							accumulated_total_prons += eval_g2p(accumulated_panara)
						portuguese_phone_list = epi.trans_list(elan_word[1:-1])
						if '́' in portuguese_phone_list:
							portuguese_phone_list.remove('́')
						print(portuguese_phone_list)
						accumulated_total_prons += portuguese_phone_list
						accumulated_panara = ''  # reset
						continue

					# remove remaining brackets
					if '[' in elan_word:
						elan_word = elan_word.replace('[', '').replace(']', '')

					accumulated_panara += elan_word

				if accumulated_panara:
					accumulated_total_prons += eval_g2p(accumulated_panara)

				if args.dictfile:
					phone_set.update(accumulated_total_prons)

				pron_str = ' '.join(accumulated_total_prons)
				tg_list.append((start, end, pron_str))
				# print(f'{elan_txt}\n{pron_str}')

			continue
			# tier = tgio.IntervalTier(speaker, tg_list, 0, duration)  # TierName, List of intervals, tier start time, tier end time
			tier = textgrid.IntervalTier(speaker, tg_list, 0, duration)  # TierName, List of intervals, tier start time, tier end time
			tg.addTier(tier)
			tg.save(write_tg_file, "long_textgrid", includeBlankSpaces=True)

	if args.dictfile:
		with open(args.dictfile, 'w') as w:
			remove_phones = [',']
			for uniq_phone in sorted(phone_set):
				if uniq_phone in remove_phones:
					continue

				w.write(f'{uniq_phone}\t{uniq_phone}\n')

	if args.wordlist:
		wordlist_file = args.wordlist
		with open(wordlist_file, 'r') as f:
			gold_dict = {line.split('\t')[0] : line.split('\t')[1].strip().replace(':', 'ː') for line in f.readlines()}

		count_mismatch = 0

		for orth, phonetic in gold_dict.items():
			orth2 = orth
			for umlaut_char, nasal_char in orth_dict.items():
				orth2 = orth2.replace(umlaut_char, nasal_char)

			orth2 = orth2.replace(" ", "")
			g2p_input = f'//[]<{orth2}>(){{}}||'
			g2p_output = tempfile.PHONFILL(g2p_input)
			out_phoneme = g2p_output.split('/')[1]
			out_phones = g2p_output.split('[')[1].split(']')[0]
			out_phones = post_process(out_phones).replace(' ', '')

			if phonetic != out_phones:
				if '~' in phonetic:
					if phonetic.split(' ~ ')[1] == out_phones:
						continue

				print(f'{orth}\t{phonetic}')
				print(f'{out_phoneme}\t{out_phones}')
				count_mismatch +=1
			# print(f'{orth2}\t{phonetic}')
			# print(f'{out_phoneme}\t{out_phones}')

		print(count_mismatch)

	# JS file generally works like this
	# out = tempfile.PHONFILL("//[]<pê nê+rõwã kô ho>(){}||")
	# print(out)
	# phonemic_seq = out.split('/')[1]
	# print(phonemic_seq)
	# phonetic_seq = out.split('[')[1].split(']')[0]
	# phonetic_seq = post_process(phonetic_seq)
	# print(phonetic_seq)

	'''

	print(epi.transliterate(u'ou'))
	print(epi.transliterate(u'ou'))
	print(epi.transliterate(u'índio'))
	'''
