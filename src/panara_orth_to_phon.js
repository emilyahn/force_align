// Writen by Teela Huff (thuff@berkeley.edu) for LRAP in Fall 2018
// Must be in JavaScript in order to be implemented as a script in Google Sheets

// Returns a dict of Panãra consonant phonetic forms that change for phonemic forms
function GETPHONCHANGED(INPUT1) {
    var cons;
    cons = {}; // all cons that change
    cons["mp"] = "m"; // post-oralized nasal
    cons["nt"] = "n";
    cons["ns"] = "ɲ";
    cons["ŋk"] = "ŋ";
    return cons;
}

// Returns a list of nt and gemintates for checking if word initial i is epenthetic
function GETINITIALEPEN(INPUT1) {
    var ntgems;
    ntgems = [];
    ntgems.push("nt"); // short oral
    ntgems.push("pp");
    ntgems.push("tt");
    ntgems.push("ss");
    ntgems.push("kk");
    ntgems.push("mm");
    ntgems.push("nn");
    return ntgems;
}

// Returns a dict of Panãra consonants orthography conventions
function GETC(INPUT1) {
    var cons;
    cons = {}; // all consonants except ɲ (done after syllabification)
    cons["p"] = "p"; // singleton obstruent
    cons["t"] = "t";
    cons["s"] = "s";
    cons["k"] = "k";
    cons["pp"] = "pp"; // geminate obstruent
    cons["tt"] = "tt";
    cons["ss"] = "ss";
    cons["kk"] = "kk";
    cons["m"] = "m"; // singleton nasal
    cons["n"] = "n";
    cons["j"] = "ŋ"; // ŋ<j> == ["j"] = "ŋ"
    cons["mm"] = "mm"; // geminate nasal
    cons["nn"] = "nn";
    cons["np"] = "mp"; // post-oralized nasal
    cons["nt"] = "nt";
    cons["ns"] = "ns";
    cons["nk"] = "ŋk";
    cons["w"] = "w"; // approximant
    cons["r"] = "ɾ";
    cons["j"] = "j";
    return cons;
}

// Returns a dict of Panãra vowels orthography conventions
function GETV(INPUT1) {
    var vowels;
    vowels = {};
    vowels["í"] = "í"; // not epenthetic i
    vowels["i"] = "i"; // short oral
    vowels["y"] = "ɯ";
    vowels["u"] = "u";
    vowels["ê"] = "e";
    vowels["â"] = "ɤ";
    vowels["ô"] = "o";
    vowels["e"] = "ɛ";
    vowels["a"] = "a";
    vowels["o"] = "ɔ";
    vowels["ii"] = "i:"; // long oral
    vowels["yy"] = "ɯ:";
    vowels["uu"] = "u:";
    vowels["êê"] = "e:";
    vowels["ââ"] = "ɤ:";
    vowels["ôô"] = "o:";
    vowels["ee"] = "ɛ:";
    vowels["aa"] = "a:";
    vowels["oo"] = "ɔ:";
    vowels["ĩ"] = "ĩ"; // short nasal
    vowels["ỹ"] = "ɯ̃";
    vowels["ũ"] = "ũ";
    vowels["ẽ"] = "ẽ";
    vowels["ã"] = "ã";
    vowels["õ"] = "õ";
    vowels["ĩĩ"] = "ĩ:"; // long nasal
    vowels["ỹỹ"] = "ɯ̃:";
    vowels["ũũ"] = "ũ:";
    vowels["ẽẽ"] = "ẽ:";
    vowels["ãã"] = "ã:";
    vowels["õõ"] = "õ:";
    return vowels;
}

// Returns a dict of POA for C for syllabification
function GETCPOA(INPUT1) {
    var cons;
    cons = {};
    cons["p"] = "bilabial"; // singleton obstruents
    cons["t"] = "alveolarandpalatal";
    cons["s"] = "alveolarandpalatal";
    cons["k"] = "velar";
    cons["m"] = "bilabial"; // singleton nasals
    cons["n"] = "alveolarandpalatal";
    cons["ɲ"] = "alveolarandpalatal";
    cons["ŋ"] = "velar";
    cons["w"] = "bilabial"; // approximants
    cons["ɾ"] = "alveolarandpalatal";
    cons["j"] = "alveolarandpalatal";
    return cons;
}

// Returns a list of V
function GETSYLLV(INPUT1) {
    var vowels;
    vowels = [];
    vowels.push("í")
    vowels.push("i"); // short oral
    vowels.push("ɯ");
    vowels.push("u");
    vowels.push("e");
    vowels.push("ɤ");
    vowels.push("o");
    vowels.push("ɛ");
    vowels.push("a");
    vowels.push("ɔ");
    vowels.push("i:"); // long oral
    vowels.push("ɯ:");
    vowels.push("u:");
    vowels.push("e:");
    vowels.push("ɤ:");
    vowels.push("o:");
    vowels.push("ɛ:");
    vowels.push("a:");
    vowels.push("ɔ:");
    vowels.push("ĩ"); // short nasal
    vowels.push("ɯ̃");
    vowels.push("ũ");
    vowels.push("ẽ");
    vowels.push("ã");
    vowels.push("õ");
    vowels.push("ĩ:"); // long nasal
    vowels.push("ɯ̃:");
    vowels.push("ũ:");
    vowels.push("ẽ:");
    vowels.push("ã:");
    vowels.push("õ:");
    return vowels;
}

// Returns a list of nasal V
function GETNASALV(INPUT1) {
    var vowels;
    vowels = [];
    vowels.push("ĩ"); // short nasal
    vowels.push("ɯ̃");
    vowels.push("ũ");
    vowels.push("ẽ");
    vowels.push("ã");
    vowels.push("õ");
    vowels.push("ĩ:"); // long nasal
    vowels.push("ũ:");
    vowels.push("ẽ:");
    vowels.push("ã:");
    vowels.push("õ:");
    return vowels;
}

// Returns a list of preceding V for n in coda that becomes ŋ {u, u:, ũ, ũ:, o, o:, õ, õ:, ɔ, ɔ:}
function GETENGMAV(INPUT1) {
    var vowels;
    vowels = [];
    vowels.push("u"); // short oral
    vowels.push("o");
    vowels.push("ɔ");
    vowels.push("u:"); // long oral
    vowels.push("o:");
    vowels.push("ɔ:");
    vowels.push("ũ"); // short nasal
    vowels.push("õ");
    vowels.push("ũ:"); // long nasal
    vowels.push("õ:");
    return vowels;
}

// Takes in a phonetic form without syllabification and returns one with syllabification
function SYLLABIFYPHONETIC(INPUT1) {
    var phon, syll, cPOA, syllV, afterV;
    phon = INPUT1;
    syll = "";
    cPOA = GETCPOA(1);
    syllV = GETSYLLV(1);
    afterV = 0;
    // Consider current two, if not in cons or vowels, then assign first
    // and move one forward, repeat
    for (i = 0; i < phon.length; i++) {
        var first = phon.charAt(i);
        if (first == ":") {
            syll += first;
            continue;
        }
        if (syllV.indexOf(first) >= 0) { // if is a V
            if (afterV == 1) {
                syll += "." + first;
            } else {
                afterV = 1;
                syll += first;
            }
        }
        else if (afterV == 1) { // if in syllable coda, at potential C3
            if (i < phon.length - 1) { // if two or more C left
                var next = phon.charAt(i + 1);
                if (cPOA[first] == cPOA[next]) { // if POA matches, then VC3.
                    syll += first + ".";
                    afterV = 0;
                } else { // if POA does not match, then V.C1
                    syll += "." + first;
                    afterV = 0;
                }

            } else { // if only one C left
                syll += first;
                afterV = 0;
            }
        } else {
            syll += first;
        }
    }
    return syll;
}

// Takes in an unfilled string panãra /phonemic/[phonetic]<orthography>(author,year,page){POR,ENG}|note|
// and a filler string to be placed between the left input3 and right input4 (ex. "<" and ">")
function FILLAT(INPUT1, INPUT2, INPUT3, INPUT4) {
    var unfilled, filler, leftLim, rightLim, prevBracket, postBracket;
    unfilled = INPUT1;
    filler = INPUT2;
    leftLim = INPUT3;
    rightLim = INPUT4;
    prevBracket = -1;
    postBracket = -1;
    if (filler == "") {
      return unfilled;
    }
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == leftLim && prevBracket == -1) {
            prevBracket = i;
        }
        else if (unfilled.charAt(i) == rightLim) {
            postBracket = i;
        }
    }
    return unfilled.slice(0, prevBracket + 1) + filler + unfilled.slice(postBracket, unfilled.length);
}

// Takes in a string of panãra orthography and returns the wide phonetic form without syllables.
// ex. takes in "nãnsy" and returns "nãnsɯ"
function ORTHTOPHONETIC(INPUT1) {
    var orth, phon, cons, vowels;
    orth = INPUT1;
    phon = "";
    cons = GETC(1);
    vowels = GETV(1);
    if (orth == "joopy") { // hard code <joopy>
        orth = "jopy"
    }
    // Consider current two, if not in cons or vowels, then assign first
    // and move one forward, repeat
    for (i = 0; i < orth.length; i++) {
        if (i < orth.length - 1) { // if two or more letters left
            var first = orth.charAt(i);
            var pair = first + orth.charAt(i + 1);
            if (pair in cons) {
                phon += cons[pair];
                i += 1;
            } else if (pair in vowels) {
                phon += vowels[pair];
                i += 1;
            } else if (first in cons) {
                phon += cons[first];
            } else if (first in vowels) {
                phon += vowels[first];
            } else {
                phon += first;
            }
        } else { // if only one letter left
            var first = orth.charAt(i);
            if (first in cons) {
                phon += cons[first];
            } else if (first in vowels) {
                phon += vowels[first];
            } else {
                phon += first;
            }
        }
    }
    return phon;
}

// Takes in a string of panãra /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note|
// and returns the string with the [phonetic] portion (and /phonemic/ portion todo) filled based off of the orthography
function ONEPHONFILL(INPUT1){
    var filled;
    filled = INPUT1;
    filled = PHONETICFILL(filled);
    filled = NFILL(filled);
    filled = PHONEMICFILL(filled);
    filled = STRESSFILL(filled);
    return String(filled);
}

// Takes in a string of panãra /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note|
// and returns the string with the [phonetic] portion (and /phonemic/ portion todo) filled based off of the orthography
function PHONFILL(INPUT1){
    var filled, unfilled, filler, isOrtho, words;
    // Checking for multiple words, if so treating them as separate words
    // and merging phonetic and phonemic with commas at the end
    unfilled = INPUT1;
    if (unfilled == "") { // for blank cells
        return "";
    }
    filler = ""; // will contain orthography
    isOrtho = 0;
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == "<") {
            isOrtho = 1;
        }
        else if (unfilled.charAt(i) == ">") {
            break;
        }
        else if (isOrtho == 1) {
            filler += unfilled.charAt(i);
        }
    }
    words = filler.replace(/\s/g, ''); // will contain all words, removing spaces
    words = words.split(","); // splitting on comma for list of multiple words
    if (words.length == 1) {
        return ONEPHONFILL(unfilled);
    }
    var orthSkeleton;
    orthSkeleton = unfilled.split("<");
    orthSkeleton[1] = orthSkeleton[1].split(">")[1];
    var curr;
    var finalWords = []; // list of /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note| for each word
    for (j = 0; j < words.length; j++) {
        curr = orthSkeleton[0] + "<" + words[j] + ">" + orthSkeleton[1];
        curr = ONEPHONFILL(curr);
        finalWords.push(curr);
    }
    // combining each string into a single comma delineated entry for orthography, phonetic, and phonemic word(s)
    filled = "";
    var finalOrtho, finalPhonetic, finalPhonemic, currWord, currMatch;
    finalOrtho = "";
    finalPhonetic = "";
    finalPhonemic = "";
    for (i = 0; i < finalWords.length; i++) {
        currWord = finalWords[i];
        if (i > 0) {
            finalOrtho += ", ";
            finalPhonetic += ", ";
            finalPhonemic += ", ";
        }
        currMatch = currWord.match(/\<(.*?)\>/);
        if (currMatch) {
            finalOrtho += currMatch[1];
        }
        currMatch = currWord.match(/\[(.*?)\]/);
        if (currMatch) {
            finalPhonetic += currMatch[1];
        }
        currMatch = currWord.match(/\/(.*?)\//);
        if (currMatch) {
            finalPhonemic += currMatch[1];
        }
    }
    filled = FILLAT(unfilled, finalOrtho, "<", ">");
    filled = FILLAT(filled, finalPhonetic, "[", "]");
    filled = FILLAT(filled, finalPhonemic, "/", "/");
    return filled;
}

// Takes in a string of panãra /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note|
// and returns the string with the [phonetic] portion filled based off of the orthography
function PHONETICFILL(INPUT1) {
    var unfilled, filler, isOrtho;
    unfilled = INPUT1;
    filler = "";
    isOrtho = 0;
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == "<") {
            isOrtho = 1;
        }
        else if (unfilled.charAt(i) == ">") {
            break;
        }
        else if (isOrtho == 1) {
            filler += unfilled.charAt(i);
        }
    }
    filler = ORTHTOPHONETIC(filler);
    filler = SYLLABIFYPHONETIC(filler);
    // Utilities.sleep(1000);
    return FILLAT(unfilled, filler, "[", "]");
}

// Takes in a string of panãra /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note|
// and returns the string with the [phonetic] portion with ɲ in place of j in onset
// and ɲ or ŋ in place of n in coda (given correct environments).
function NFILL(INPUT1) {
    var unfilled, filler, isPhon;
    unfilled = INPUT1;
    filler = "";
    isPhon = 0;
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == "[") {
            isPhon = 1;
        }
        else if (unfilled.charAt(i) == "]") {
            break;
        }
        else if (isPhon == 1) {
            filler += unfilled.charAt(i);
        }
    }
    filler = PHONETICN(filler);
    // Utilities.sleep(1000);
    return FILLAT(unfilled, filler, "[", "]");
}

// Takes in a string of panãra syllabified panãra phonetic form and returns it with ɲ
// in place of j in onset and ɲ or ŋ in place of n in coda (given correct environments).
function PHONETICN(INPUT1) {
    var oldphon, nphon, vowels, nasalvowels, engmavowels, incoda;
    oldphon = INPUT1;
    nphon = "";
    vowels = GETSYLLV(1);
    nasalvowels = GETNASALV(1);
    engmavowels = GETENGMAV(1);
    incoda = 0;
    for (i = 0; i < oldphon.length - 1; i++) { // includes penultimate final sound
        var curr = oldphon.charAt(i);
        if (curr == "j" && incoda == 0) { // if j and in onset
            // if j is first, or if j is preceded by a syllable break (making it C1V)
            if (i == 0 || (i != 0 && oldphon.charAt(i - 1) == ".")) {
                // if following V is nasal
                if (i < oldphon.length - 1 && nasalvowels.indexOf(oldphon.charAt(i + 1)) >= 0) {
                    nphon += "ɲ";
                } else {
                    nphon += curr;
                }
            } else {
                nphon += curr;
            }
        } else if (vowels.indexOf(curr) >= 0) { // if V, set in coda to 1
            incoda = 1;
            nphon += curr;
        } else if (curr == ".") { // if at syllable break, set in coda to 0
            incoda = 0;
            nphon += curr;
        } else {
            nphon += curr;
        }
    }
    if (oldphon.charAt(oldphon.length - 1) == "n") { // checking ultimate sound, if n word final
        if (engmavowels.indexOf(oldphon.charAt(oldphon.length - 2)) >= 0) { // n is [ŋ] due to preceding V
            nphon += "ŋ";
        } else { // n is [ɲ] due to preceding V
            nphon += "ɲ";
        }
    } else {
        nphon += oldphon.charAt(oldphon.length - 1); // if not n, add ultimate sound
    }
    return nphon;
}

// Takes in a string of panãra /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note|
// and returns the string with the /phonemic/ portion filled based off of the phonetic portion
function PHONEMICFILL(INPUT1) {
    var unfilled, isPhon, filler;
    unfilled = INPUT1;
    isPhon = 0;
    filler = "";
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == "[") {
            isPhon = 1;
        }
        else if (unfilled.charAt(i) == "]") {
            break;
        }
        else if (isPhon == 1) {
            filler += unfilled.charAt(i);
        }
    }
    filler = PHONETICTOPHONEMIC(filler);
    // Utilities.sleep(1000);
    return FILLAT(unfilled, filler, "/", "/");
}

// Takes in a string of panãra phonetic form and returns the phonemic form
function PHONETICTOPHONEMIC(INPUT1) {
    var phonetic, phonemic, postOrals, ntgems, vowels, nasalV;
    phonetic = INPUT1.split(".").join(""); // without syllable breaks "."
    phonemic = "";
    postOrals = GETPHONCHANGED(1);
    ntgems = GETINITIALEPEN(1);
    vowels = GETSYLLV(1);
    nasalV = GETNASALV(1);
    // consider current two, and add to phonemic form, then move forward one
    for (i = 0; i < phonetic.length; i++) {
        var first = phonetic.charAt(i);
        // console.log(first);
        // i epenthesis
        if (first == "i") {
            if (i == 0 && phonetic.length > 2) { // checking for #_nt and #_geminates
                var nextTwo = phonetic.charAt(i + 1) + phonetic.charAt(i + 2);
                if (ntgems.indexOf(nextTwo) >= 0) { // if i is epenthetic
                    continue;
                } else {
                    phonemic += first;
                }
            }  else if (i > 0 && i < phonetic.length - 1) { // ɾ_C
                var prev = phonetic.charAt(i - 1);
                var next = phonetic.charAt(i + 1);
                if (prev == "ɾ" && !(vowels.indexOf(next) >= 0)) {
                    continue;
                } else {
                    phonemic += first;
                }
            } else if (i > 1 && i == phonetic.length - 1) { // word final
                var prev1 = phonetic.charAt(i - 2);
                var prev2 = phonetic.charAt(i - 1);
                if (prev1 == ":" || vowels.indexOf(prev1) >= 0) { // must be VCi, not CCi
                    if (prev2 == "ɾ") { // ɾ_#
                        continue;
                    } else if (prev2 == "p" || prev2 == "t" || prev2 == "s" || prev2 == "k") { //{p,t,s,k} -> C_#
                        continue;
                    } else {
                        phonemic += first;
                    }
                } else {
                    phonemic += first;
                }
            } else {
                phonemic += first;
            }
        } else if (first == "ĩ") {
            if (i > 1) { // nasal Vɾ_ (epenthesis as a nasal i)
                var prev1 = phonetic.charAt(i - 2);
                var prev2 = phonetic.charAt(i - 1);
                if (prev2 == "ɾ" && (prev1 == ":" || nasalV.indexOf(prev1) >= 0)) {
                    continue;
                } else {
                    phonemic += first;
                }
            } else {
                phonemic += first;
            }
        } else if (first == "ɯ") { // ɯ epenthesis
            if (i > 1 && i == phonetic.length - 1) { // word final only ɔp_# and op_#
                var prev1 = phonetic.charAt(i - 2);
                var prev2 = phonetic.charAt(i - 1);
                if (prev2 == "p" ) {
                    if (prev1 == ":") { // long ɔ and o
                        prev0 = phonetic.charAt(i - 3);
                        if (prev0 == "ɔ" || prev0 == "o") {
                            continue;
                        } else {
                            phonemic += first;
                        }
                    } else if (prev1 == "ɔ" || prev1 == "o") { // short ɔ and o
                        continue;
                    } else {
                        phonemic += first;
                    }
                } else {
                    phonemic += first;
                }
            } else {
                phonemic += first;
            }
        } else if (i < phonetic.length - 1) { // post oralized nasals
            var double = first + phonetic.charAt(i + 1);
            if (double in postOrals) {
                phonemic += postOrals[double];
                i += 1;
                continue;
            } else {
                phonemic += first;
            }
        } else {
            phonemic += first;
        }
    }
    return phonemic;
}

// Takes in a string of panãra /phonemic/[phonetic]<orthography>(author,year,page) {POR,ENG}|note|
// and returns the string with stress and resulting V length added to the [phonetic] portion
function STRESSFILL(INPUT1) {
    var unfilled, isPhon, filler, phonemic, phonetic;
    unfilled = INPUT1;
    isPhon = 0;
    filler = "";
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == "[") {
            isPhon = 1;
        }
        else if (unfilled.charAt(i) == "]") {
            break;
        }
        else if (isPhon == 1) {
            filler += unfilled.charAt(i);
        }
    }
    phonetic = filler;
    isPhon = 0;
    filler = "";
    for (i = 0; i < unfilled.length; i++) {
        if (unfilled.charAt(i) == "/" && isPhon == 0) {
            isPhon = 1;
        }
        else if (unfilled.charAt(i) == "/" && isPhon == 1) {
            break;
        }
        else if (isPhon == 1) {
            filler += unfilled.charAt(i);
        }
    }
    phonemic = filler;
    filler = PHONEMICTOSTRESS(phonemic, phonetic);
    // Utilities.sleep(1000);
    return FILLAT(unfilled, filler, "[", "]");
}

// Takes in two strings of (1) panãra phonemic form and (2) panãra phonetic form
// and returns a string of panãra phonetic form with stress and resulting V length
function PHONEMICTOSTRESS(INPUT1, INPUT2) {
    var phonemic, phonetic, stressPhonetic, vowels, phonemicV, phoneticV;
    phonemic = INPUT1;
    phonetic = INPUT2;
    stressPhonetic = "";
    vowels = GETSYLLV(1);
    phonemicV = "";
    phoneticV = ""
    for (i = phonemic.length - 1; i >= 0; i--) { // iterate backwards, find final V in phonemic
        phonemicV = phonemic.charAt(i);
        if (vowels.indexOf(phonemicV) >= 0) { // if current sound is a vowel
            break; // break and phonemicV = first V encountered
        }
    }
    for (i = phonetic.length - 1; i >= 0; i--) { // iterate backwards, find final V in phonemic
        phoneticV = phonetic.charAt(i);
        if (vowels.indexOf(phoneticV) >= 0) { // if current sound is a vowel
            break; // break and phoneticV = first V encountered
        }
    }
    var syllables = phonetic.split(".");
    if (syllables.length == 1) {
        return phonetic;
    }
    if (phonemicV == "a" && syllables[syllables.length - 1] == "a") { // check for epenthetic a
        var penultSyll = syllables[syllables.length - 2];
        var lastInPenult = penultSyll.charAt(penultSyll.length - 1);
        if (lastInPenult == ":") {
            lastInPenult = penultSyll.charAt(penultSyll.length - 2);
        }
        if (vowels.indexOf(lastInPenult) >= 0 && lastInPenult != "a") { // a is epenthetic, stress is penultimate
            for (i = 0; i < syllables.length; i++) {
                if (i == syllables.length - 2) { // at penultimate syllable
                    stressPhonetic += "ˈ";
                    var currSyll = syllables[i];
                    for (n = 0; n < currSyll.length; n++) {
                        stressPhonetic += currSyll.charAt(n);
                        if (vowels.indexOf(currSyll.charAt(n)) >= 0) { // if V, make it long
                            stressPhonetic += ":";
                        }
                    }
                    stressPhonetic += ".";
                } else {
                    if (i < syllables.length - 1) {
                        stressPhonetic += syllables[i] + ".";
                    } else {
                        stressPhonetic += syllables[i];
                    }
                }
            }
        } else {
            if (i == syllables.length - 1) { // stress is ultimate
                stressPhonetic += "ˈ";
            }
            if (i < syllables.length - 1) {
                stressPhonetic += syllables[i] + ".";
            } else {
                stressPhonetic += syllables[i];
            }
        }
    }
    else if (phonemicV == phoneticV) { // final phonemic V in ultimate syll, ultimate stress
        for (i = 0; i < syllables.length; i++) {
            if (i == syllables.length - 1) {
                stressPhonetic += "ˈ";
            }
            if (i < syllables.length - 1) {
                stressPhonetic += syllables[i] + ".";
            } else {
                stressPhonetic += syllables[i];
            }
        }
    } else { // otherwise stress is penultimate
        for (i = 0; i < syllables.length; i++) {
            if (i == syllables.length - 2) { // at penultimate syllable
                stressPhonetic += "ˈ";
                var currSyll = syllables[i];
                for (n = 0; n < currSyll.length; n++) {
                    stressPhonetic += currSyll.charAt(n);
                    if (vowels.indexOf(currSyll.charAt(n)) >= 0) { // if V, make it long
                        stressPhonetic += ":";
                    }
                }
                stressPhonetic += ".";
            } else {
                if (i < syllables.length - 1) {
                    stressPhonetic += syllables[i] + ".";
                } else {
                    stressPhonetic += syllables[i];
                }
            }
        }
    }
    return stressPhonetic;
}


// Emily adding
// var arguments = process.argv;
// var str_out = PHONFILL(arguments[2]);
// console.log(str_out);
