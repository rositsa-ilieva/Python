class Tone:
    """A class that represents a musical tone."""
    TONES = ("C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B")

    def __init__(self, tone):
        if tone not in Tone.TONES or not tone:
            raise ValueError("Invalid input for tone")
        self.tone = tone

    def __str__(self):
        return self.tone

    def __eq__(self, other):
        if isinstance(other, Tone):
            return self.tone == other.tone
        return False

    def __add__(self, other):
        if isinstance(other, Interval):
            return self.add_interval(other)
        if isinstance(other, Tone):
            return Chord(self, other)
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Interval):
            return self.sub_interval(other)
        if isinstance(self, Tone) and isinstance(other, Tone):
            return Interval(abs(self.TONES.index(self.tone) - other.TONES.index(other.tone)))
        raise TypeError("Invalid operation")

    def add_interval(self, other):
        """A method that adds an interval to a tone and returns new tone."""
        if isinstance(other, Tone):
            raise TypeError("Invalid operation")
        elif isinstance(self, Tone) and isinstance(other, Interval):
            cur_tone_index = self.TONES.index(self.tone)
            new_index = (cur_tone_index + other.number_of_semitones) % len(self.TONES)
            return Tone(self.TONES[new_index])
        raise TypeError("Invalid operation")

    def sub_interval(self, other):
        """A method that subtracts an interval to a tone and returns new tone."""
        if isinstance(self, Tone) and isinstance(other, Interval):
            cur_tone_index = self.TONES.index(self.tone)
            new_index = abs((cur_tone_index - other.number_of_semitones) % len(self.TONES))
            return Tone(self.TONES[new_index])
        if isinstance(other, Tone):
            raise TypeError("Invalid operation")
        raise TypeError("Invalid operation")


class Interval:
    """A class that represents a musical interval."""
    INTERVALS = ("unison", "minor 2nd", "major 2nd", "minor 3rd", "major 3rd", "perfect 4th",
                 "diminished 5th", "perfect 5th", "minor 6th", "major 6th", "minor 7th", "major 7th")
    INTERVALS_LENGTH = len(INTERVALS)

    def __init__(self, number_of_semitones):
        if not isinstance(number_of_semitones, int):
            raise TypeError("Invalid input for number of semitones")
        self.number_of_semitones = number_of_semitones % Interval.INTERVALS_LENGTH

    def __str__(self):
        return self.INTERVALS[self.number_of_semitones % Interval.INTERVALS_LENGTH]

    def __add__(self, other):
        if isinstance(self, Interval) and isinstance(other, Interval):
            return Interval(self.number_of_semitones + other.number_of_semitones)
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        raise TypeError("Invalid operation")

    def __neg__(self):
        return Interval(-self.number_of_semitones)


class Chord:
    """A class that represents a musical chord."""

    def __init__(self, *args):
        if len(args) == 0:
            raise TypeError("Empty chord")
        self.root = args[0].tone
        self.all_tones = []
        for cur_tone in args:
            if cur_tone not in self.all_tones:
                self.all_tones.append(cur_tone)

        if len(self.all_tones) == 1:
            raise TypeError("Cannot have a chord made of only 1 unique tone")
        
        root_index = Tone.TONES.index(self.root)
        sorted_all_tones = []
        sorted_all_tones.append(Tone.TONES[root_index])

        for i in range(1, len(Tone.TONES)):
            current_index = (root_index + i) % len(Tone.TONES)
            current_tone = Tone.TONES[current_index]
            if Tone(current_tone) in self.all_tones:
                sorted_all_tones.append(current_tone)
        self.all_tones = sorted_all_tones

    def __str__(self):
        return "-".join(str(cur_tone) for cur_tone in self.all_tones)

    def is_minor(self):
        """A method that checks if there is a tone in the chord that together
           with the root tone form minor 3rd interval. Returns a boolean."""
        root_index = Tone.TONES.index(self.root)
        for tone in self.all_tones:
            tone_index = Tone.TONES.index(tone)
            if tone == self.root:
                continue
            elif tone_index - root_index == 3:
                return True
            elif (root_index - tone_index) % 12 == 9:
                return True
        return False

    def is_major(self):
        """A method that checks if there is a tone in the chord that together
           with the root tone form major 3rd interval. Returns a boolean."""
        root_index = Tone.TONES.index(self.root)
        for tone in self.all_tones:
            tone_index = Tone.TONES.index(tone)
            if tone == self.root:
                continue
            elif tone_index - root_index == 4:
                return True
            elif (root_index - tone_index) % 12 == 9:
                return True
        return False

    def is_power_chord(self):
        """A method that checks if a chord does not contain a tone that, together 
           with the root, forms a minor 3rd or a major 3rd. Returns a boolean."""
        if not self.is_major() and not self.is_minor():
            return True
        return False

    def __add__(self, other):
        if isinstance(other, Tone):
            return Chord(*map(Tone, self.all_tones + [other.tone]))
        if isinstance(other, Chord):
            result = []
            for tone in self.all_tones:
                result.append(Tone(tone))
            for tone in other.all_tones:
                result.append(Tone(tone))
            return Chord(*result)
        raise TypeError("Invalid operation")

    def __sub__(self, other):
        if isinstance(other, Tone):
            result = []
            additional_tone = Tone(other.tone)
            result.append(Tone(other.tone))
            for tone in self.all_tones:
                if Tone(tone) == additional_tone:
                    result.remove(additional_tone)
                else:
                    result.append(Tone(tone))
            if additional_tone in result:
                raise TypeError(f"Cannot remove tone {Tone(other.tone)} from chord {str(self)}")
            return Chord(*result)
        raise TypeError("Invalid operation")

    def transposed(self, interval):
        """A method that shifts each of its tones by the same interval."""
        transposed_tones = [Tone(tone) + interval for tone in self.all_tones]
        return Chord(*transposed_tones)
