# Phonetic Granularity in Forced Alignment

## Data

### TIMIT English
* download corpus and convert .WAV to .wav format
```sh
# copy LDC folder from patas
scp -r patas:/corpora/LDC/LDC93S1/ .

# convert .WAV files to .wav
# (hack around sox issue: `sox file.WAV file.wav` somehow deletes info and leaves file.WAV)
for file in `find . -name '*.WAV'`; do new_file="${file%%.WAV}_new.wav"; sox $file $new_file; rm $file; mv $new_file ${file%%.WAV}.wav; done
```

* collapse some categories for the explicit/full English version
	* map file: `data/notes/timit-map-phones-explicit.txt`

* create lexicon, .lab files, and updated gold .PHN files (format `*.exp.phn`)
	* `python src/get_timit_dict_lab.py --timit_dir data/LDC93S1/TIMIT --phone_map_file data/notes/timit-map-phones-explicit.txt --outf data/notes/timit-explicit-lex.txt`


