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

    #read gold files
    file_id_gold = 'kre_sokriti_20180902_mjl_1_narrative'
    utt_list = []
    grid = textgrids.TextGrid('/mnt/c/Users/bridg/documents/uw/project/gold_star/kre_sokriti_20180902_mjl_1_narrative_gold_star.TextGrid')
    for item in grid['phones']:
        phone = item.text
        phone = phone.strip()
        if not phone: # ''
            continue
        if phone == "unk":
            continue
        if phone == "\s":
            continue
        if phone.isspace():
            continue
        if phone == "  ":
            continue
        start = round(item.xmin * 1000)
        end = round(item.xmax * 1000)
        utt_list.append((phone, start, end))
    gold_dict[file_id_gold] = utt_list
    
    file_id_gold = 'pnr_txt_turen-hist-a_24072019'
    utt_list = []
    grid = textgrids.TextGrid('/mnt/c/Users/bridg/documents/uw/project/gold_star/pnr_txt_turen-hist-a_24072019_gold_star.TextGrid')
    for item in grid['phones']:
        phone = item.text
        phone = phone.strip()
        if not phone: # ''
            continue
        if phone == "unk":
            continue
        if phone == "\s":
            continue
        if phone.isspace():
            continue
        if phone == "  ":
            continue
        start = round(item.xmin * 1000)
        end = round(item.xmax * 1000)
        utt_list.append((phone, start, end))
    gold_dict[file_id_gold] = utt_list

    # read system predicted textgrids
    file_id_pred = 'kre_sokriti_20180902_mjl_1_narrative'
    utt_list = []
    grid = textgrids.TextGrid('/mnt/c/Users/bridg/documents/uw/project/panara_only/kre_sokriti_20180902_mjl_1_narrative_g2p.TextGrid')
    for item in grid['phones']:
        phone = item.text
        if not phone: # ''
            continue
        start = round(item.xmin * 1000)
        end = round(item.xmax * 1000)
        utt_list.append((phone, start, end))
    pred_dict[file_id_pred] = utt_list
    
    file_id_pred = 'pnr_txt_turen-hist-a_24072019'
    utt_list = []
    grid = textgrids.TextGrid('/mnt/c/Users/bridg/documents/uw/project/panara_only/pnr_txt_turen-hist-a_24072019_g2p.TextGrid')
    for item in grid['phones']:
        phone = item.text
        if not phone: # ''
            continue
        start = round(item.xmin * 1000)
        end = round(item.xmax * 1000)
        utt_list.append((phone, start, end))
    pred_dict[file_id_pred] = utt_list
    diffs = []
    vowel_list = ["aː", "ɯ", "ɤ", "u", "oː", "ũ", "ẽ", "e", "uː", "õ", "ĩ", "ɛ", "ɔ", "i", "ãː", "ɐ", "õː", "ɯː", "ɔː", "ɤː", "eː", "á", "ÿ", "ɛː", "ẽː", "ɔ̃", "ã", "â", "ɛ̂", "ɛ̃", "ɔ̂", "ĩ", "ũ", "í", "ó", "a", "o"]
    voweldiffs = []
    long_vowel_list = ["aː", "oː", "uː", "ɯː", "ɔː", "ɤː", "eː", "ɛː",]
    longvoweldiffs = []
    long_nasal_vowel_list = ["ũ", "ẽ", "ãː", "õː", "ẽː"]
    longnasalvoweldiffs = []
    plain_vowel_list = ["ɯ", "ɤ", "u", "e", "ɛ", "ɔ", "i", "ɐ", "á", "ÿ", "â", "ɛ̂", "ɔ̂", "í", "ó", "a", "o"]
    plainvoweldiffs = []
    nasal_vowel_list = ["ũ", "ẽ", "õ", "ĩ", "ɔ̃", "ã", "ɛ̃", "ĩ", "ũ"]
    nasalvoweldiffs = []
    fricative_list = ["h", "s", "ʃ", "ʁ", "ʒ"]
    fricativediffs = []
    nasal_list = ["m", "ŋ", "ɲ", "n"]
    nasaldiffs = []
    approximant_list = ["j", "w", "l", "j́"]
    approximantdiffs = []
    tap_list = ["ɾ", "ɾː", "ɾ̃"]
    tapdiffs = []
    stop_list = ["p", "k", "t", "b", "d", "g", "c"]
    stopdiffs = []
    onsetpaireval = []
    prev_phon = ""
    for file_id, gold_list in gold_dict.items():
        pred_list = pred_dict[file_id]
        print(str(len(gold_list))+" "+str(len(pred_list)))
        #if len(gold_list) != len(pred_list):
            #print(file_id)  # all good!
        for i_tup, gold_tup in enumerate(gold_list):
            pred_tup = pred_list[i_tup]
            # absolute diff of each phone's ONSET only
            # if want OFFSET, use tup[2]
            diff = abs(gold_tup[1] - pred_tup[1])
            diffs.append(diff)
            if gold_tup[0] in vowel_list:
                voweldiffs.append(diff)
                if gold_tup[0] in long_vowel_list:
                    longvoweldiffs.append(diff)
                if gold_tup[0] in long_nasal_vowel_list:
                    longnasalvoweldiffs.append(diff)
                if gold_tup[0] in plain_vowel_list:
                    plainvoweldiffs.append(diff)
                if gold_tup[0] in nasal_vowel_list:
                    nasalvoweldiffs.append(diff)
            if gold_tup[0] in fricative_list:
                fricativediffs.append(diff)
            if gold_tup[0] in nasal_list:
                nasaldiffs.append(diff)
            if gold_tup[0] in approximant_list:
                approximantdiffs.append(diff)
            if gold_tup[0] in tap_list:
                tapdiffs.append(diff)
            if gold_tup[0] in stop_list:
                stopdiffs.append(diff) 
            onsetpaireval.append(tuple[prev_phon, gold_tup[0], diff])
            prev_phon = gold_tup[0]
    offdiffs = []
    ovd = []
    ofd = []
    ond = []
    oad = []
    otd = []
    osd = []
    prev_phon = ""
    offsetpaireval = []
    for file_id, gold_list in gold_dict.items():
        pred_list = pred_dict[file_id]
        print(str(len(gold_list))+" "+str(len(pred_list)))
        #if len(gold_list) != len(pred_list):
            #print(file_id)  # all good!
        for i_tup, gold_tup in enumerate(gold_list):
            pred_tup = pred_list[i_tup]
            # absolute diff of each phone's OFFSET
            diff = abs(gold_tup[2] - pred_tup[2])
            offdiffs.append(diff)
            if gold_tup[0] in vowel_list:
                ovd.append(diff)
            if gold_tup[0] in fricative_list:
                ofd.append(diff)
            if gold_tup[0] in nasal_list:
                ond.append(diff)
            if gold_tup[0] in approximant_list:
                oad.append(diff)
            if gold_tup[0] in tap_list:
                otd.append(diff)
            if gold_tup[0] in stop_list:
                osd.append(diff)
            offsetpaireval.append(tuple[gold_tup[0], prev_phon, diff])
            prev_phon = gold_tup[0]
    # evaluate
    if not args.command or args.command == 'boundary_diff':

        print("Full evaluation:")
        print(f'MEAN: {statistics.mean(diffs):0.2f}')
        print(f'MEDIAN: {statistics.median(diffs)}')
        print(f'MIN: {min(diffs)}')
        print(f'MAX: {max(diffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in diffs:
                if diff_item < window_msec:
                    within_window += 1
            

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(diffs)):0.2f}')
            
    # evaluate vowels
    if not args.command or args.command == 'boundary_diff':

        print("\nVowel evaluation:")
        print(f'MEAN: {statistics.mean(voweldiffs):0.2f}')
        print(f'MEDIAN: {statistics.median(voweldiffs)}')
        print(f'MIN: {min(voweldiffs)}')
        print(f'MAX: {max(voweldiffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in voweldiffs:
                if diff_item < window_msec:
                    within_window += 1
            

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(voweldiffs)):0.2f}')
    
    # evaluate fricatives
    if not args.command or args.command == 'boundary_diff':

        print("\nFricative evaluation:")
        print(f'MEAN: {statistics.mean(fricativediffs):0.2f}')
        print(f'MEDIAN: {statistics.median(fricativediffs)}')
        print(f'MIN: {min(fricativediffs)}')
        print(f'MAX: {max(fricativediffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in fricativediffs:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(fricativediffs)):0.2f}')
    
    # evaluate nasals
    if not args.command or args.command == 'boundary_diff':

        print("\nNasal evaluation:")
        print(f'MEAN: {statistics.mean(nasaldiffs):0.2f}')
        print(f'MEDIAN: {statistics.median(nasaldiffs)}')
        print(f'MIN: {min(nasaldiffs)}')
        print(f'MAX: {max(nasaldiffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in nasaldiffs:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(nasaldiffs)):0.2f}')

    # evaluate approximants
    if not args.command or args.command == 'boundary_diff':

        print("\nApproximant evaluation:")
        print(f'MEAN: {statistics.mean(approximantdiffs):0.2f}')
        print(f'MEDIAN: {statistics.median(approximantdiffs)}')
        print(f'MIN: {min(approximantdiffs)}')
        print(f'MAX: {max(approximantdiffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in approximantdiffs:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(approximantdiffs)):0.2f}')

    # evaluate taps
    if not args.command or args.command == 'boundary_diff':

        print("\nTap evaluation:")
        print(f'MEAN: {statistics.mean(tapdiffs):0.2f}')
        print(f'MEDIAN: {statistics.median(tapdiffs)}')
        print(f'MIN: {min(tapdiffs)}')
        print(f'MAX: {max(tapdiffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in tapdiffs:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(tapdiffs)):0.2f}')

    # evaluate stops
    if not args.command or args.command == 'boundary_diff':

        print("\nStop evaluation:")
        print(f'MEAN: {statistics.mean(stopdiffs):0.2f}')
        print(f'MEDIAN: {statistics.median(stopdiffs)}')
        print(f'MIN: {min(stopdiffs)}')
        print(f'MAX: {max(stopdiffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in stopdiffs:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(stopdiffs)):0.2f}')
            
            
    # evaluate offset
    if not args.command or args.command == 'boundary_diff':

        print("Full offset evaluation:")
        print(f'MEAN: {statistics.mean(offdiffs):0.2f}')
        print(f'MEDIAN: {statistics.median(offdiffs)}')
        print(f'MIN: {min(offdiffs)}')
        print(f'MAX: {max(offdiffs)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in offdiffs:
                if diff_item < window_msec:
                    within_window += 1
            

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(diffs)):0.2f}')
            
    # evaluate vowels
    if not args.command or args.command == 'boundary_diff':

        print("\nVowel offset evaluation:")
        print(f'MEAN: {statistics.mean(ovd):0.2f}')
        print(f'MEDIAN: {statistics.median(ovd)}')
        print(f'MIN: {min(ovd)}')
        print(f'MAX: {max(ovd)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in ovd:
                if diff_item < window_msec:
                    within_window += 1
            

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(voweldiffs)):0.2f}')
    
    # evaluate fricatives
    if not args.command or args.command == 'boundary_diff':

        print("\nFricative offset evaluation:")
        print(f'MEAN: {statistics.mean(ofd):0.2f}')
        print(f'MEDIAN: {statistics.median(ofd)}')
        print(f'MIN: {min(ofd)}')
        print(f'MAX: {max(ofd)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in ofd:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(fricativediffs)):0.2f}')
    
    # evaluate nasals
    if not args.command or args.command == 'boundary_diff':

        print("\nNasal offset evaluation:")
        print(f'MEAN: {statistics.mean(ond):0.2f}')
        print(f'MEDIAN: {statistics.median(ond)}')
        print(f'MIN: {min(ond)}')
        print(f'MAX: {max(ond)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in ond:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(nasaldiffs)):0.2f}')

    # evaluate approximants
    if not args.command or args.command == 'boundary_diff':

        print("\nApproximant offset evaluation:")
        print(f'MEAN: {statistics.mean(oad):0.2f}')
        print(f'MEDIAN: {statistics.median(oad)}')
        print(f'MIN: {min(oad)}')
        print(f'MAX: {max(oad)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in oad:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(approximantdiffs)):0.2f}')

    # evaluate taps
    if not args.command or args.command == 'boundary_diff':

        print("\nTap offset evaluation:")
        print(f'MEAN: {statistics.mean(otd):0.2f}')
        print(f'MEDIAN: {statistics.median(otd)}')
        print(f'MIN: {min(otd)}')
        print(f'MAX: {max(otd)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in otd:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(tapdiffs)):0.2f}')

    # evaluate stops
    if not args.command or args.command == 'boundary_diff':

        print("\nStop offset evaluation:")
        print(f'MEAN: {statistics.mean(osd):0.2f}')
        print(f'MEDIAN: {statistics.median(osd)}')
        print(f'MIN: {min(osd)}')
        print(f'MAX: {max(osd)}')

    if not args.command or args.command == 'accuracy_window':
        if not args.window_msec:
            windows = [1, 5, 10, 15, 20]

        else:
            windows = [args.window_msec]

        for window_msec in windows:
            within_window = 0
            for diff_item in osd:
                if diff_item < window_msec:
                    within_window += 1

            print(f'WINDOW ({window_msec}ms): {float(within_window/len(stopdiffs)):0.2f}')
    
    totalnum = 0
    allmiddle = 0
    vowelmiddle = 0
    fricativemiddle = 0
    nasalmiddle = 0
    approximantmiddle = 0
    tapmiddle = 0
    stopmiddle = 0

    #is the middle of the gold standard phon within the predicted phon
    for file_id, gold_list in gold_dict.items():
        pred_list = pred_dict[file_id]
        for i_tup, gold_tup in enumerate(gold_list):
            totalnum += 1
            pred_tup = pred_list[i_tup]
            middle = gold_tup[1]+((gold_tup[2]-gold_tup[1])/2)
            if middle >= pred_tup[1] and middle <= pred_tup[2]:
                allmiddle += 1
                if pred_tup[0] in vowel_list:
                    vowelmiddle += 1
                if pred_tup[0] in fricative_list:
                    fricativemiddle += 1
                if pred_tup[0] in nasal_list:
                    nasalmiddle += 1
                if pred_tup[0] in approximant_list:
                    approximantmiddle += 1
                if pred_tup[0] in tap_list:
                    tapmiddle += 1
                if pred_tup[0] in stop_list:
                    stopmiddle += 1
    print("Total: " + str(totalnum))
    print("All Middle: " + str(allmiddle))
    print("Total Vowels: " + str(len(ovd)))
    print("Vowel Middle: " + str(vowelmiddle))
    print("Total Fricatives: " + str(len(ofd)))
    print("Fricative Middle: " + str(fricativemiddle))
    print("Total Nasals: " + str(len(ond)))
    print("Nasal Middle: " + str(nasalmiddle))
    print("Total Approximants: " + str(len(oad)))
    print("Approximant Middle: " + str(approximantmiddle))
    print("Total Taps: " + str(len(otd)))
    print("Tap Middle: " + str(tapmiddle))
    print("Total Stops: " + str(len(osd)))
    print("Stop Middle: " + str(stopmiddle))




    #print(diffs)
    #print(voweldiffs)
    #print(fricativediffs)
    #print(nasaldiffs)
    #print(approximantdiffs)
    #print(tapdiffs)
    #print(stopdiffs)
    
    #print(offdiffs)
    #print(ovd)
    #print(ofd)
    #print(ond)
    #print(oad)
    #print(otd)
    #print(osd)
            
