# The Use of Phone Categories and Cross-Language Modeling for Phone Alignment of Panãra

Emily P. Ahn, UW Linguistics (eahn@uw.edu)

Paper accepted to INTERSPEECH 2024.
With Gina-Anne Levow, Myriam Lapierre, & Eleanor Chodroff.

## Paper / Poster / Citation 
Download the Camera-ready PDF: `ahn2024_interspeech_granularity_camera.pdf`

Download the Interspeech Poster PDF: `ahn2024_interspeech_granularity_poster.pdf`

Citation forthcoming...

## Requirements
* conda (4.12.0)
* Montreal Forced Aligner version (2.2.17)
	* `conda create -n aligner2.2.17 -c conda-forge montreal-forced-aligner=2.2.17`

## Data Processing

Processed data included in this repository are dictionary files.
TIMIT English data is licensed through LDC, and the Panãra data is private.
Please contact Dr. Myriam Lapierre for access of any Panãra data.

### TIMIT English
* download corpus and convert .WAV to .wav format
```sh
# copy LDC folder from patas (UW Ling cluster)
scp -r patas:/corpora/LDC/LDC93S1/ .

# convert .WAV files to .wav
# (hack around sox issue: `sox file.WAV file.wav` somehow deletes info and leaves file.WAV)
for file in `find . -name '*.WAV'`; do new_file="${file%%.WAV}_new.wav"; sox $file $new_file; rm $file; mv $new_file ${file%%.WAV}.wav; done
```

* collapse some categories for the explicit/full English version
	* map file: `data/notes/timit-map-phones-explicit.txt`

* create lexicon, .lab files, and updated gold .PHN files (format `*.exp.phn`)
	* `python src/get_timit_dict_lab.py --timit_dir data/LDC93S1/TIMIT --phone_map_file data/notes/timit-map-phones-explicit.txt --outf data/notes/timit-explicit-lex.txt`

* convert phone set to IPA
	* map file: `data/notes/timit-ipa-map.txt`

* convert phone set to medium-broad classes with package lingpy
	* script: `src/q_lingpy_sca.py`

* calculate length of files (.wav) recursively in a directory
	* `find . -type f -name *.wav | xargs -L 1 ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 | awk '{s+=$1} END {print s}'`
	* TIMIT total: 19379.75 sec (05:22:59). 630 speakers.
		* TRAIN dir: 14193.1 sec (03:56:33)
			* problem dirs (56:28): DR3 (2293 sec = 38:13. 76 spkrs), DR6 (1095 sec = 18:15, 35 spkrs)
		* TEST dir: 5186.65 sec (01:26:26). 168 speakers.
		* core test set: 730sec (0:12:10). 24 speakers.
			* `for line in `cat timit_core_test_set_dirs.txt`; do find TEST/$line -type f -name *.wav | xargs -L 1 ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 | awk '{s+=$1} END {print s}'; done`

* my new splits under `data/timit_mod/`:
	* full train (3:44:23) = TRAIN (no DR3/6) + TEST - CORETEST. 495 speakers. `full_train/`
	* small train (0:26:24) = TEST subset (no core). 51 speakers. `small_test_26min/`
	* eval (0:12:10) = CORETEST. 24 speakers. `eval_core/`

* separate out core test set: `cd data/timit_mod; for line in `cat timit_core_test_set_dirs.txt`; do mv TEST/$line; done`

* created Dictionary files (MFA input):
	* Full phone set: `data/dict/timit_explicit_lex.txt`
	* Medium phone set (SCA classes): `data/dict/timit_medium_sca.txt`

### Panãra
Unfortunately, this data is not public. I have included, however, commands and scripts to process the data.

* Quantity of transcribed (sum over utterance durations): 2130 sec (35.5 minutes)
	* `grep A_Transcription data/panara/intvw_input/{file}.txt | cut -f8 | awk '{s+=$1} END {print s}'`
	* Note: discarded `pnr_hist_snake` file
		* gold files: 770 sec (0:12:50)
			* sokriti: 485 sec (0:08:05)
			* turen: 285 sec (0:04:45)
		* other: 1360 sec (0:22:40)
			* sykja: 498 sec (0:08:18)
			* karansa: 862 sec (0:14:22)
	* trimmed several wav files to reduce storage space: sokriti(575sec), turen(330sec), karansa(985sec)
* some manual corrections of ELAN txt files (diacritics, brackets), renamed to `data/panara/intvw_input/{}_epa.txt`
* adapt Teela Huff's G2P (written in JavaScript), modify within python script
	* follow `src/g2p_panara.py`
		* creates TextGrids, MFA dictionary
	* to run JS directly from terminal: comment in lines at the end and run `node src/panara_orth_to_phon.js "//[]<päpaa>(){}||"`
* created Dictionary files (MFA input):
	* Full phone set: `data/dict/dict_panara_phone_narrow.txt`
	* No-Diacritics: `data/dict/dict_panara_no-diacritics.txt`
	* Medium phone set (SCA classes): `data/dict/dict_panara_phone_medium.txt`
		* convert phone set to medium-broad classes with package lingpy
		* script: `src/q_lingpy_sca.py`


## Run alignment with Montreal Forced Aligner (MFA)
* Download MFA
* Initialize MFA env with `conda activate aligner`
* see all MFA commands in file: `mfa_commands_all.sh`

Examples of some MFA commands in use:
* pilot (small batch) under English explicit setting of TIMIT (DR7: ~38min speech)
	* validate: `mfa validate /Users/eahn/work/force_align/data/LDC93S1/TIMIT/TRAIN/DR7 /Users/eahn/work/force_align/data/notes/timit-explicit-lex.txt`
	* train model, save model, and generate alignments on train set: `mfa train --clean --output_directory /Users/eahn/work/force_align/data/out/ldc_pilot /Users/eahn/work/force_align/data/LDC93S1/TIMIT/TRAIN/DR7 /Users/eahn/work/force_align/data/notes/timit-explicit-lex.txt /Users/eahn/work/force_align/data/out/models/ldc_pilot.zip`
* train acoustic models
	* e.g. TIMIT TEST set: `mfa train --clean --output_directory /Users/eahn/work/force_align/data/out/timit_test_medium /Users/eahn/work/force_align/data/LDC93S1/TIMIT/TEST/ /Users/eahn/work/force_align/data/notes/timit-medium-sca.txt /Users/eahn/work/force_align/data/out/models/timit_test_medium.zip`
	* e.g. Panara interviews: `mfa train --clean --output_directory /Users/eahn/work/force_align/data/out/panara_explicit /Users/eahn/work/force_align/data/panara/clean_pnr_input /Users/eahn/work/force_align/data/panara/dict_panara_phone_narrow.txt /Users/eahn/work/force_align/data/out/models/panara_explicit.zip`
* X-lang alignment
	* to just align with acoustic model: `mfa align [IN_DIR] [DICTIONARY] [MODEL.zip] [OUT_DIR]`
	* ex. run Eng-Medium-Full on Panara-Medium: `mfa align data/panara/clean_pnr_input/ data/panara/dict_panara_phone_medium.txt data/out/models/timit_full_medium.zip data/out/train-timit-full-med_test-pan-med`

* adapt acoustic models
	* general command: `mfa adapt [OPTIONS] CORPUS_DIRECTORY DICTIONARY_PATH ACOUSTIC_MODEL_PATH OUTPUT_MODEL_PATH`
	* ex. adapt TIMIT FULL to PANARA `mfa adapt --clean --output_directory /Users/eahn/work/force_align/data/out/adapt-tim-full-pnr-exp /Users/eahn/work/force_align/data/panara/clean_pnr_input /Users/eahn/work/force_align/data/notes/pan-to-timit-explicit.txt /Users/eahn/work/force_align/data/out/models/timit_full_explicit.zip /Users/eahn/work/force_align/data/out/models/adapt-tim-full-pnr-exp.zip`

* Download pretrained Global English model from MFA
	* download command: `mfa model download acoustic english_mfa`
	* 3771.35 hours, summing across description on the MFA acoustic model [page](https://mfa-models.readthedocs.io/en/latest/acoustic/English/English%20MFA%20acoustic%20model%20v2_2_1.html)
	* acoustic model version: 2.2.6.dev1+g6874b58.d20230320
	* conduct X-lang alignment and model adaptation over TIMIT
		* create mapping file of TIMIT phones to Global-Eng phones: `data/dict/timit-to-globaleng.txt`
	* conduct X-lang alignment and model adaptation over Panara
		* create mapping file of Panara phones to Global-Eng phones: `data/dict/pan-to-globaleng.txt`

## Evaluate alignments
* `src/eval_align.py`
	* ex. TIMIT TEST data: `py src/eval_align.py --gold_dir data/timit_mod/TEST/ --pred_dir data/out/timit_full_explicit/TEST/ --gold_extension exp.phn`
	* for natural class analysis, use TSV file: `data/notes/pnr_natural_classes.tsv`
