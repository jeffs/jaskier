import random

from rhythm import Space_Values
from rhythm_track import generate_rhythmic_beat, generate_rhythmic_motion
from stems import choose_leading_tone, shift_octave


def min_chord_size(chords):
    return min([len(i[0]) for i in chords])
# TODO: add/complete hand motions

def octave_doubling(chords, meter, rhythm):
    min_chord_length = min_chord_size(chords)
    degree = generate_rhythmic_motion(min_chord_length, min_chord_length, True)[0]
    measure_length = meter[0]/(meter[1]/4)
    notes = []
    time_length = 0
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(len(rhythm)*((chords[i][1][1]-chords[i][1][0])/measure_length))
        current_rhythm = rhythm[0:len(rhythm)]
        # potential warning: is funky with small fractions, like .23 of a measure
        while measure_size > len(current_rhythm):
            if len(current_rhythm) + len(rhythm) <= measure_size: 
                current_rhythm += rhythm
            else:
                current_rhythm += current_rhythm[:int(len(rhythm)/2)+1]
        for j in range(measure_size):
            notes.append([chords[i][0][degree], current_rhythm[j], time_length])
            notes.append([chords[i][0][degree]-12, current_rhythm[j], time_length])
            time_length += Space_Values[current_rhythm[j]]
    return notes

def seesaw(chords, meter, rhythm):
    min_chord_length = min_chord_size(chords)
    degrees = generate_rhythmic_motion(min_chord_length, min_chord_length, False)
    for i in range(min_chord_length-1):
        if degrees[i] > degrees[i+1]:
            degrees[i+1] += 12
    # whether num_pitches per beat is 2 1 2 1 2 or 1 2 1 2 1
    heavier_side = random.randint(0,1)
    # whether the first beat is lower than the second 
    lower_side = random.choice([0,min_chord_length-1])
    if lower_side == 0:
        upper_side = min_chord_length-1
    else:
        upper_side = 0
    measure_length = meter[0]/(meter[1]/4)
    notes = []
    time_length = 0
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(len(rhythm)*((chords[i][1][1]-chords[i][1][0])/measure_length))
        current_rhythm = rhythm[0:len(rhythm)]
        # potential warning: is funky with small fractions, like .23 of a measure
        while measure_size > len(current_rhythm):
            if len(current_rhythm) + len(rhythm) <= measure_size: 
                current_rhythm += rhythm
            else:
                current_rhythm += current_rhythm[:int(len(rhythm)/2)+1]
        for j in range(measure_size):
            if j % 2 == 0:
                notes.append([chords[i][0][lower_side], current_rhythm[j], time_length])
            if j % 2 == heavier_side:
                notes.append([chords[i][0][1], current_rhythm[j], time_length])
            if j % 2 == 1:
                notes.append([chords[i][0][upper_side], current_rhythm[j], time_length])
            time_length += Space_Values[current_rhythm[j]]
    return notes

def arpeggios(chords, meter, rhythm):
    min_chord_length = min_chord_size(chords)
    # whether the first beat is lower than the second 
    direction = random.choice([list(range(0, min_chord_length)),
                               list(range(min_chord_length, 0, -1))])
    measure_length = meter[0]/(meter[1]/4)
    notes = []
    time_length = 0
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(len(rhythm)*((chords[i][1][1]-chords[i][1][0])/measure_length))
        current_rhythm = rhythm[0:len(rhythm)]
        # potential warning: is funky with small fractions, like .23 of a measure
        while measure_size > len(current_rhythm):
            if len(current_rhythm) + len(rhythm) <= measure_size: 
                current_rhythm += rhythm
            else:
                current_rhythm += current_rhythm[:int(len(rhythm)/2)+1]
        for j in range(measure_size):
            for k in range(len(direction)):
                if j % len(direction) == k:
                    notes.append([chords[i][0][k], current_rhythm[j], time_length])
            time_length += Space_Values[current_rhythm[j]]
    return notes

def full_chord(chords, meter, rhythm, *guitar_strum):
    measure_length = meter[0]/(meter[1]/4)
    notes = []
    time_length = 0
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(len(rhythm)*((chords[i][1][1]-chords[i][1][0])/measure_length))
        current_rhythm = rhythm[0:len(rhythm)]
        # potential warning: is funky with small fractions, like .23 of a measure
        while measure_size > len(current_rhythm):
            if len(current_rhythm) + len(rhythm) <= measure_size: 
                current_rhythm += rhythm
            else:
                current_rhythm += current_rhythm[:int(len(rhythm)/2)+1]
        for j in range(measure_size):
            strum_offset = 0
            for pitch in chords[i][0]:
                if guitar_strum:
                    notes.append([pitch, current_rhythm[j], time_length+strum_offset])
                else:
                    notes.append([pitch, current_rhythm[j], time_length])
                strum_offset += .05
            time_length += Space_Values[current_rhythm[j]]
    return notes

# TODO: Needs good polish
def walking_bass(chords, meter):
    measure_length = meter[0]/(meter[1]/4)
    notes = []
    time_length = 0
    if meter[0] % 3 == 0:
        if meter[1] == 4:
            rhythm = ['qn', 'qn', 'qn']
        else:
            rhythm = ['en', 'en', 'en']
    else:
        if meter[1] == 4:
            rhythm = ['qn', 'qn', 'qn', 'qn']
        else:
            rhythm = ['en', 'en', 'en', 'en']
    for i in range(len(chords)):
        # \/ size of measure for the chord
        measure_size = int(len(rhythm)*((chords[i][1][1]-chords[i][1][0])/measure_length))
        current_rhythm = rhythm[0:len(rhythm)]
        # potential warning: is funky with small fractions, like .23 of a measure
        while measure_size > len(current_rhythm):
            if len(current_rhythm) + len(rhythm) <= measure_size: 
                current_rhythm += rhythm
            else:
                current_rhythm += current_rhythm[:int(len(rhythm)/2)+1]
        measure = []
        for j in range(measure_size):
            if j == 0:
                measure.append([chords[i][0][0], current_rhythm[j], time_length])
            elif meter[0] > 2 and j == 1:
                measure.append([random.choice(chords[i][0][1:]), current_rhythm[j],
                                                                       time_length])
            elif i < len(chords)-1 and j == measure_size-1:
                measure.append([choose_leading_tone(measure[-1][0], chords[i+1][0][0]),
                                                   current_rhythm[j], time_length])
            elif meter[0] % 4 == 0 and j > 1:
                possibility = random.choice([i for i in chords[i][0]
                                              if i not in measure])
                measure.append([random.choice([i for i in chords[i][0]
                                              if i not in measure]),
                                        current_rhythm[j], time_length])
            else:
                measure.append([chords[i][0][0], current_rhythm[j], time_length])
            time_length += Space_Values[current_rhythm[j]]
        notes += measure
    return notes


def running_scale(pitches):
    return

def pick_hand_motion(chords, meter, rhythm):
    motion = random.randint(0,4) 
    # return full_chord(chords, me ter, rhythm)
    # return walking_bass(chords, meter)
    # return arpeggios(chords, meter, rhythm)
    # return seesaw(chords, meter, rhythm)
    # return octave_doubling(chords, meter, rhythm)
    if motion == 0:
        return seesaw(chords, meter, rhythm)
    elif motion == 1:
        return full_chord(chords, meter, rhythm)
    elif motion == 2:
        return arpeggios(chords, meter, rhythm)
    elif motion == 3:
        return walking_bass(chords, meter)
    else:
        return octave_doubling(chords, meter, rhythm)

def generate_rhythm_from_meter(meter, **kargs):
    if "intensity" in kargs:
        intensity = kargs["intensity"]
    else:
        intensity = random.choice(list(range(0, 4)))
    # TODO: make different rhythm-measure lengths work fine with chord-measure-durations
    if "rhythm_len" in kargs:
        rhythm_length = kargs["rhythm_len"]
    else:
        rhythm_length = 1 # random.choice(1,2)
    # TODO: Adjust intensity of rhythm accordingly, but maybe in a better place?
    return generate_rhythmic_beat(meter, intensity, rhythm_length, False)

def generate_hand_motion(chords, meter, **args):
    if "rhythm" in args:
        beats = args["rhythm"]
    else:
        if "rhythm_len" in args:
            l = args["rhythm_len"]
        else:
            l = False
        if "intensity" in args:
            inten = args["intensity"]
        else:
            inten = False
        if inten and l:
            beats = generate_rhythm_from_meter(meter, rhythm_len=l, intensity=inten)
        elif inten:
            beats = generate_rhythm_from_meter(meter, intensity=inten)
        elif l:
            beats = generate_rhythm_from_meter(meter, rhythm_len=l)
        else:
            beats = generate_rhythm_from_meter(meter)

    # determine how much shift_octave to do
    if "hand" in args:
        hand = args["hand"]
    else:
        hand = "left"

    if hand.lower() == "left":
        return shift_octave(pick_hand_motion(chords, meter, beats), -2)
    else:
        return shift_octave(pick_hand_motion(chords, meter, beats), 1)

def generate_hand_motions(parts, meter, **args):
    motions = {}
    if "rhythm" in args:
        beats = args["rhythm"]
        for part in parts:
            motions[part] = generate_hand_motion(parts[part], meter, rhythm=beats)
    else:
        if "rhythm_len" in args:
            l = args["rhythm_len"]
        else:
            l = False
        if "intensity" in args:
            inten = args["intensity"]
        else:
            inten = False
        if inten and l:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter, 
                                                     rhythm_len=l,
                                                     intensity=inten)
        elif inten:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter, 
                                                         intensity=inten)
        elif l:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter,
                                                            rhythm_len=l)
        else:
            for part in parts:
                motions[part] = generate_hand_motion(parts[part], meter)
    return motions
