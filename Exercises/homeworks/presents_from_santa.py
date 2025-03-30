import re

class SingletonType(type):
    def __new__(mcs, name, bases, attrs):
        def singleton_new(cls):
            if not hasattr(cls, 'instance'):
                cls.instance = object.__new__(cls)
            return cls.instance
        attrs['__new__'] = singleton_new
        return type.__new__(mcs, name, bases, attrs)


class Santa(metaclass = SingletonType):
    """A class for greedy kids."""
    all_kids = set()
    kids_objects = {}
    kids_ages = {}
    gifts = {}
    naughty_kids = set()

    def extract_gift(self, letter: str):
        """Extracts a gift from a letter or call."""
        pattern_gift = r'(?:\")([A-Za-z0-9]+[A-Za-z0-9 ]*)(?:\")|(?:\')([A-Za-z0-9]+[A-Za-z0-9 ]*)(?:\')'
        pattern = re.compile(pattern_gift, re.MULTILINE)
        gifts = pattern.findall(letter)

        for gift_tuple in reversed(gifts):
            for gift in gift_tuple:
                if gift:
                    return gift
        return None

    def extract_signature_from_letter(self, letter: str):
        """Extracts a signiture from a letter."""
        pattern_signature = r'\s*(\d+)\s*'
        pattern = re.compile(pattern_signature, re.MULTILINE)
        signature = pattern.findall(letter)
        if signature:
            return signature[-1]
        return None

    def __matmul__(self, letter: str):
        """Predefined operator @ when a kid writes a letter to Santa."""
        gift = self.extract_gift(letter)
        signature = self.extract_signature_from_letter(letter)

        index = int(signature)
        self.gifts[index] = gift
        self.all_kids.add(index)
        self.kids_ages[index] = 0
        if id(signature) in self.kids_objects:
            self.kids_objects[signature] = signature

    def __call__(self, child, wish: str):
        """Predefined operator () when a kid calls Santa."""
        index = id(child)
        self.gifts[index] = self.extract_gift(wish)

    def __iter__(self):
        return iter(self.gifts.values())

    def get_most_wanted_gift_this_year(self):
        """Calculates what is the most wanted gift this year."""
        this_years_gifts = [gift for gift in self.gifts.values() if gift is not None]

        if set(this_years_gifts):
            most_wanted_gift_this_year = max(set(this_years_gifts) , key = this_years_gifts.count)
        else:
            most_wanted_gift_this_year = None
        return most_wanted_gift_this_year

    def remove_kid(self, keys_to_delete):
        """Deletes kid because it is too old for presents."""
        for key in keys_to_delete:
            del self.gifts[key]
            del self.kids_ages[key]
            del self.kids_objects[key]
            self.all_kids.remove(key)

    def mark_as_naughty(self, kid):
        """Marks a kid as naughty."""
        if id(kid) in self.all_kids:
            self.naughty_kids.add(id(kid))

    def xmas(self):
        """Time for presents."""
        for key in self.kids_ages:
            self.kids_ages[key] += 1

        most_wanted_gift = self.get_most_wanted_gift_this_year()
        keys_to_delete = []

        for kid, age in self.kids_ages.items():
            cur_gift = self.gifts[kid]
            if age > 5:
                keys_to_delete.append(kid)
                continue
            elif age <= 5:
                kid_obj = self.kids_objects.get(kid)
                if all(value == None for value in self.gifts.values()):
                    break
                elif kid in self.naughty_kids:
                    kid_obj("coal")
                elif cur_gift is None:
                    kid_obj(most_wanted_gift)
                else:
                    kid_obj(cur_gift)

        for cur_gift in self.gifts:
            self.gifts[cur_gift] = None

        self.remove_kid(keys_to_delete)
        self.naughty_kids.clear()


def detect_naughty_kid(func):
    """Checks if the kid is naughty."""
    def wrapper(self, *args, **kwargs):
        try:
            return func(self, *args, **kwargs)
        except Exception:
            Santa().mark_as_naughty(self)
            raise
    return wrapper


class Kid(type):
    """A class that defines a kid."""
    def __new__(mcs, name, bases, attrs):
        if '__call__' not in attrs:
            raise NotImplementedError("Sorry, you should implement the __call__ method of the kid :).")
        for key, value in attrs.items():
            if callable(value) and not key.startswith("_"):
                attrs[key] = detect_naughty_kid(value)
        return super().__new__(mcs, name, bases, attrs)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if id(instance) not in Santa().all_kids:
            Santa().all_kids.add(id(instance))
            Santa().gifts[id(instance)] = None
            Santa().kids_ages[id(instance)] = 0
            Santa().kids_objects[id(instance)] = instance
        return instance
