import math

from chord_progression import generate_full_chord_sequence, Special_Chords
from forms import Forms, pick_random_form, match_parts_to_form
from modes_and_keys import apply_key
from motif_generator import generate_pitches
from rhythm import generate_rhythm, merge_pitches_with_rhythm, rhythm_pdf_presets, replace_some_quarters_with_eights
from stems import full_walking_bass_over_form, shift_octave


Presets = {
    "meter"      : (3,4),
    "key"        : "Ionian",
    "mode"       : "B",
    "base"       : 62,
    "rhythm_pdf" : rhythm_pdf_presets["default"],
    "chords"     : "major",
    "form"       : Forms["Ballad"],
    "rhythm_length" : 2,
    "rhythm_repetition_in_mel" : 3,
}

def repeat_section(section, times):
    return sum([section for i in range(times)], [])


def generate_song(presets):
    
    parts = {}
    applied_key = apply_key(presets["key"], presets["mode"])[1]

    for part in presets["form"]:
        if part not in parts:
            option = generate_full_chord_sequence(presets["chords"], applied_key,
                                                  presets["base"])
            while option in list(parts.values()):
                option = generate_full_chord_sequence(presets["chords"],
                                                      applied_key,
                                                      presets["base"])
            parts[part] = option
    
    pieces = {}
    for part in parts:
        chords = parts[part]
        rhythmic_backbone = generate_rhythm(presets["meter"], 
                                            presets["rhythm_length"],
                                            True, presets["rhythm_pdf"])
        rhythmic_backbone = [replace_some_quarters_with_eights(rhythmic_backbone[i], 3)\
                             for i in range(len(rhythmic_backbone))]
        rhythmic_backbone = replace_some_quarters_with_eights(rhythmic_backbone, 3)
        rhythm = repeat_section(rhythmic_backbone,
                                math.ceil(len(chords)/len(rhythmic_backbone)))
                                # presets["rhythm_repetition_in_mel"])
    # TODO: Better selection of # of repetitions for rhythm per melody
    # TODO: FIX problem \/
    #  Warning!: does 1 chord per measure
 
        melody_length = len(sum(rhythm, []))
        melody = generate_pitches(melody_length, applied_key, 18,
                                    presets["base"], chords, rhythm)
    
        while len(melody) > len(sum(rhythm,[])):
            melody.pop()
    
        pieces[part] = merge_pitches_with_rhythm(melody, sum(rhythm,[]))
    
    bass = full_walking_bass_over_form(presets["form"], parts, presets["meter"])
    print("Walking Bass", shift_octave(bass, -1))
    song = match_parts_to_form(presets["form"], pieces)        

    song += ":+: note wn " + str(presets["base"]) 

    print("Main song", song)
    return song



# TODO: Proper type-checking
def handle_set(command):
    try:
        Presets[command[1]]
        if command[1] == "meter":
            Presets[command[1]] = tuple([int(command[2]), int(command[3])])
        elif command[1] == "base":
            Presets[command[1]] = int(command[2])
        elif command[1] == "rhythm_length":
            Presets[command[1]] = int(command[2])
        elif command[1] == "rhythm_repetition_in_mel":
            Presets[command[1]] = int(command[2])
        else: 
            Presets[command[1]] = command[2]
    except:
        print("Failed:", command[1], "is not in Presets.")


def handle_input(command):
    if command.split()[0] == "set":
        handle_set(command.split())

generate_song(Presets)
# generate_rhythm(meter, measure_count, show_seperate_measures, rhythm_pdf)