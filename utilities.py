"""
Utilities aggregates some simple generic functions that
are useful for in multiple sections of Matnpy.

Author: Eduardo Farinati Leite
Date: 22/03/2021
"""

TAB = "  "


def to_type(element, type_):
    """Transforms element to type it isn't yet of this type."""
    if isinstance(element, type_):
        return element
    else:
        # Assumes type_ is callable as a constructor
        return type_(element)


def to_list(element):
    """If element is not a list, returns a list containing element."""
    if isinstance(element, list):
        return element
    elif element is None:
        return []
    else:
        return [element]


def unique(list_):
    """Returns a list containing the unique elements from list_."""
    return list(set(list_))


def flatten_dict(dict_):
    """Flattens a dictionary with sub dictionaries to one that aggregates all keys."""
    # Items is converted to a list to prevent dictionary changed during iteration error
    for key, item in list(dict_.items()):
        if isinstance(item, dict):
            flatten_dict(item)
            for sub_key, sub_item in item.items():
                dict_[sub_key] = sub_item
            del dict_[key]


def to_slices(starts, ends):
    """Receives two lists (starts, ends) and returns a list with slices from start to end."""
    slices = [slice(start, end) for start, end in zip(starts, ends)]
    return slices


def boolean_to_indices(array_):
    """Turns an np.array into an array indices where the it is True."""
    return array_.values.nonzero()[0]


def is_tuple_of_tuples(tuple_):
    """Verifies if the provided tuple only contains tuples."""
    if not isinstance(tuple_, tuple):
        # Not a tuple
        return False
    else:
        for element in tuple_:
            if not isinstance(element, tuple):
                # Not a tuple of tuples
                return False
        # Tuple of tuples
        return True


def progress_bar(items, prefix="", width=25, indentation=0):
    """Displays a progress bar as a loop iterates through items."""
    # Timer
    import datetime

    time = datetime.datetime.now
    starting = time()

    def elapsed_time():
        # -4 to remove some of the decimals
        return str(time() - starting)[:-4]

    # Number of indexes
    total = len(items)

    # Phases
    phases = get_bar_phases()
    number_of_phases = len(phases)
    complete_symbol = phases[-1]
    incomplete_symbol = phases[0]

    # Digits in total
    digits = len(str(total))

    # Show bar with progress at current index
    def get_bar(index):
        progress = (width * number_of_phases * index) // total
        complete = progress // number_of_phases
        
        if complete != width:
            phase = phases[progress % number_of_phases]
        else:
            phase = ''
        incomplete = width - (complete + len(phase))
        
        bar_ = (
            f"{TAB * indentation}{prefix}: "
            f"|{complete_symbol * complete}{phase}"
            f"{incomplete_symbol * incomplete}|"
            f"{index: {digits + 1}d}/{total}"
            f" {elapsed_time()}"
        )
        return bar_

    # Erase previous bar
    def erase(bar_):
        length = len(bar_)
        print(f"\r{' ' * length}", end="\r")

    # Initial bar setup
    bar = get_bar(0)
    print(bar, end="")

    # Iterates over indexes and elements, showing progress
    for i, item in enumerate(items, start=1):
        yield item
        erase(bar)
        bar = get_bar(i)
        print(bar, end="")

    # Progress end
    print(f"\n{TAB * (indentation - 1)}Done!\n")


def get_bar_phases():
    import sys

    if sys.platform.startswith('win'):
        phases = (u' ', u'▌', u'█')
    else:
        phases = (' ', '▏', '▎', '▍', '▌', '▋', '▊', '▉', '█')
    
    return phases
