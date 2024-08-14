# all commands that involve MFA

####
# Lang-only train/test
####

# Panara (train/test)
mfa train --clean data/panara/sok_out/train data/dict/dict_panara_phone_medium.txt out/models/pnr-sok_out-sca.zip
mfa train --clean data/panara/sok_out/train data/dict/dict_panara_phone_narrow.txt out/models/pnr-sok_out-exp.zip
mfa train --clean data/panara/tur_out/train data/dict/dict_panara_phone_medium.txt out/models/pnr-tur_out-sca.zip
mfa train --clean data/panara/tur_out/train data/dict/dict_panara_phone_narrow.txt out/models/pnr-tur_out-exp.zip

mfa align data/panara/tur_out/test/ data/dict/dict_panara_phone_medium.txt out/models/pnr-tur_out-sca.zip out/aligned/pnr-tur-sca
mfa align data/panara/tur_out/test/ data/dict/dict_panara_phone_narrow.txt out/models/pnr-tur_out-exp.zip out/aligned/pnr-tur-exp
mfa align data/panara/sok_out/test/ data/dict/dict_panara_phone_medium.txt out/models/pnr-sok_out-sca.zip out/aligned/pnr-sok-sca
mfa align data/panara/sok_out/test/ data/dict/dict_panara_phone_narrow.txt out/models/pnr-sok_out-exp.zip out/aligned/pnr-sok-exp

## no diacritics version
mfa train --clean data/panara/sok_out/train data/dict/dict_panara_no-diacritics.txt out/models/pnr-sok_out-no_diacritics.zip
mfa train --clean data/panara/tur_out/train data/dict/dict_panara_no-diacritics.txt out/models/pnr-tur_out-no_diacritics.zip
mfa align data/panara/tur_out/test/ data/dict/dict_panara_no-diacritics.txt out/models/pnr-tur_out-no_diacritics.zip out/aligned/pnr-tur-no-diacritics
mfa align data/panara/sok_out/test/ data/dict/dict_panara_no-diacritics.txt out/models/pnr-sok_out-no_diacritics.zip out/aligned/pnr-sok-no-diacritics


# TIMIT (train/test)
mfa train --clean data/timit_mod/full_train data/dict/timit-explicit-lex.txt out/models/timit-full-exp.zip
mfa train --clean data/timit_mod/full_train data/dict/timit-medium-sca.txt out/models/timit-full-sca.zip
mfa train --clean data/timit_mod/small_test_26min data/dict/timit-explicit-lex.txt out/models/timit-small-exp.zip
mfa train --clean data/timit_mod/small_test_26min data/dict/timit-medium-sca.txt out/models/timit-small-sca.zip

mfa align data/timit_mod/eval_core data/dict/timit-explicit-lex.txt out/models/timit-full-exp.zip out/aligned/timit-full-exp
mfa align data/timit_mod/eval_core data/dict/timit-medium-sca.txt out/models/timit-full-sca.zip out/aligned/timit-full-sca
mfa align data/timit_mod/eval_core data/dict/timit-explicit-lex.txt out/models/timit-small-exp.zip out/aligned/timit-small-exp
mfa align data/timit_mod/eval_core data/dict/timit-medium-sca.txt out/models/timit-small-sca.zip out/aligned/timit-small-sca


####
# X-lang (Eng train / Panara test) [not used in analysis]
####

mfa align data/panara/sok_and_tur data/dict/pan-to-timit-explicit.txt out/models/timit-full-exp.zip out/aligned/xlang-timit-full-pnr-exp
mfa align data/panara/sok_and_tur data/dict/dict_panara_phone_medium.txt out/models/timit-full-sca.zip out/aligned/xlang-timit-full-pnr-sca
mfa align data/panara/sok_and_tur data/dict/pan-to-timit-explicit.txt out/models/timit-small-exp.zip out/aligned/xlang-timit-small-pnr-exp
mfa align data/panara/sok_and_tur data/dict/dict_panara_phone_medium.txt out/models/timit-small-sca.zip out/aligned/xlang-timit-small-pnr-sca

####
# Adapted (Eng train / Panara adapt / Panara test)
####

# TIMIT full, explicit
mfa adapt --clean data/panara/sok_out/train data/dict/pan-to-timit-explicit.txt out/models/timit-full-exp.zip out/models/adapt-tim-full-pnr-sok_out-exp.zip
mfa align data/panara/sok_out/test/ data/dict/pan-to-timit-explicit.txt out/models/adapt-tim-full-pnr-sok_out-exp.zip out/aligned/adapt-tim-full-pnr-sok-exp
mfa adapt --clean data/panara/tur_out/train data/dict/pan-to-timit-explicit.txt out/models/timit-full-exp.zip out/models/adapt-tim-full-pnr-tur_out-exp.zip
mfa align data/panara/tur_out/test/ data/dict/pan-to-timit-explicit.txt out/models/adapt-tim-full-pnr-tur_out-exp.zip out/aligned/adapt-tim-full-pnr-tur-exp

# TIMIT small, explicit
mfa adapt --clean data/panara/sok_out/train data/dict/pan-to-timit-explicit.txt out/models/timit-small-exp.zip out/models/adapt-tim-small-pnr-sok_out-exp.zip
mfa align data/panara/sok_out/test/ data/dict/pan-to-timit-explicit.txt out/models/adapt-tim-small-pnr-sok_out-exp.zip out/aligned/adapt-tim-small-pnr-sok-exp
mfa adapt --clean data/panara/tur_out/train data/dict/pan-to-timit-explicit.txt out/models/timit-small-exp.zip out/models/adapt-tim-small-pnr-tur_out-exp.zip
mfa align data/panara/tur_out/test/ data/dict/pan-to-timit-explicit.txt out/models/adapt-tim-small-pnr-tur_out-exp.zip out/aligned/adapt-tim-small-pnr-tur-exp

# TIMIT full, SCA
mfa adapt --clean data/panara/sok_out/train data/dict/dict_panara_phone_medium.txt out/models/timit-full-sca.zip out/models/adapt-tim-full-pnr-sok_out-sca.zip
mfa align data/panara/sok_out/test/ data/dict/dict_panara_phone_medium.txt out/models/adapt-tim-full-pnr-sok_out-sca.zip out/aligned/adapt-tim-full-pnr-sok-sca
mfa adapt --clean data/panara/tur_out/train data/dict/dict_panara_phone_medium.txt out/models/timit-full-sca.zip out/models/adapt-tim-full-pnr-tur_out-sca.zip
mfa align data/panara/tur_out/test/ data/dict/dict_panara_phone_medium.txt out/models/adapt-tim-full-pnr-tur_out-sca.zip out/aligned/adapt-tim-full-pnr-tur-sca

# TIMIT small, SCA
mfa adapt --clean data/panara/sok_out/train data/dict/dict_panara_phone_medium.txt out/models/timit-small-sca.zip out/models/adapt-tim-small-pnr-sok_out-sca.zip
mfa align data/panara/sok_out/test/ data/dict/dict_panara_phone_medium.txt out/models/adapt-tim-small-pnr-sok_out-sca.zip out/aligned/adapt-tim-small-pnr-sok-sca
mfa adapt --clean data/panara/tur_out/train data/dict/dict_panara_phone_medium.txt out/models/timit-small-sca.zip out/models/adapt-tim-small-pnr-tur_out-sca.zip
mfa align data/panara/tur_out/test/ data/dict/dict_panara_phone_medium.txt out/models/adapt-tim-small-pnr-tur_out-sca.zip out/aligned/adapt-tim-small-pnr-tur-sca

####
# Pretrained Global English model eval (X-lang and adapt) on TIMIT / Panara
####

mfa model download acoustic english_mfa

# X-lang [not used in analysis]
mfa align data/panara/sok_and_tur data/dict/pan-to-globaleng.txt english_mfa out/aligned/xlang-global-pnr
mfa align data/timit_mod/eval_core data/dict/timit-to-globaleng.txt english_mfa out/aligned/xlang-global-tim

# Adapt
mfa adapt --clean data/panara/sok_out/train data/dict/pan-to-globaleng.txt english_mfa out/models/adapt-global-pnr-sok_out.zip
mfa align data/panara/sok_out/test/ data/dict/pan-to-globaleng.txt out/models/adapt-global-pnr-sok_out.zip out/aligned/adapt-global-pnr-sok
mfa adapt --clean data/panara/tur_out/train data/dict/pan-to-globaleng.txt english_mfa out/models/adapt-global-pnr-tur_out.zip
mfa align data/panara/tur_out/test/ data/dict/pan-to-globaleng.txt out/models/adapt-global-pnr-tur_out.zip out/aligned/adapt-global-pnr-tur

mfa adapt --clean data/timit_mod/full_train data/dict/timit-to-globaleng.txt english_mfa out/models/adapt-global-tim-full.zip
mfa align data/timit_mod/eval_core data/dict/timit-to-globaleng.txt out/models/adapt-global-tim-full.zip out/aligned/adapt-global-tim-full
mfa adapt --clean data/timit_mod/small_test_26min data/dict/timit-to-globaleng.txt english_mfa out/models/adapt-global-tim-small.zip
mfa align data/timit_mod/eval_core data/dict/timit-to-globaleng.txt out/models/adapt-global-tim-small.zip out/aligned/adapt-global-tim-small


