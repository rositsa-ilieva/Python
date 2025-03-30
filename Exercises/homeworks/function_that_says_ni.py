def function_that_says_ni(*args, **kwargs):
    total_price = 0
    valid_bushes = False
    for arg in args:
        if isinstance(arg, dict) and is_bush(arg):
            valid_bushes = True
            total_price += cost_of_bush(arg)

    for kwarg_value in kwargs.values():
        if isinstance(kwarg_value, dict) and is_bush(kwarg_value):
            valid_bushes = True
            total_price += cost_of_bush(kwarg_value)

    output = generate_output(kwargs, total_price, valid_bushes)
    return output

def generate_output(kwargs, total_price, valid_bushes):
    output_text = 'Ni!'
    if valid_bushes == False:
        return output_text
    elif not one_that_looks_nice(kwargs, total_price) or is_too_expensive(total_price):
        return output_text
    else:
        return f'{total_price:.2f}лв'

def is_bush(arg):
    key = 'name'
    return key in arg.keys() and str(arg[key]).lower() in ('храст', 'shrub', 'bush')

def cost_of_bush(arg):
    value = 'cost'
    if value in arg.keys() and isinstance(arg[value], (int, float)):
        price = arg[value]
        return price
    return 0

def one_that_looks_nice(kwargs, price):
    whole_part_price = int(price)
    if whole_part_price == 0:
        return False
    if len(kwargs) == 0:
        return True
    elif kwargs:
        unique_chars = set()
        for kwarg_key, kwarg_value in kwargs.items():
            if isinstance(kwarg_value, dict) and is_bush(kwarg_value):
                unique_chars.update(kwarg_key)
        unique_chars_count = len(unique_chars)
        looks_nice = unique_chars_count % whole_part_price == 0
        return looks_nice
    else:
        return False

def is_too_expensive(price):
    return price > 42.00
