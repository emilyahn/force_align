# Phonetic Granularity in Forced Alignment

Emily P. Ahn, UW Linguistics

## Data

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

## Run alignment with Montreal Forced Aligner (MFA)
* Download MFA with `conda create -n aligner -c conda-forge montreal-forced-aligner`
* Initialize MFA env with `conda activate aligner` (current MFA version 2.2.10)
* pilot (small batch) under English explicit setting of TIMIT (DR7: ~38min speech)
	* validate: `mfa validate /Users/eahn/work/force_align/data/LDC93S1/TIMIT/TRAIN/DR7 /Users/eahn/work/force_align/data/notes/timit-explicit-lex.txt`
	* train model, save model, and generate alignments on train set: `mfa train --clean --output_directory /Users/eahn/work/force_align/data/out/ldc_pilot /Users/eahn/work/force_align/data/LDC93S1/TIMIT/TRAIN/DR7 /Users/eahn/work/force_align/data/notes/timit-explicit-lex.txt /Users/eahn/work/force_align/data/out/models/ldc_pilot.zip`
	* to just align with acoustic model: `mfa align [IN_DIR] [DICTIONARY] [MODEL.zip] [OUT_DIR]`

## Evaluate alignments
* `src/eval_align.py`
