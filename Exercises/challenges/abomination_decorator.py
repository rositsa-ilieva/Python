def type_check(input_output_mode):
    """Performs mode checking."""
    def var_types(*input_types):
        """Performs variables types checking."""
        def decorator(func):
            """Decorates the function."""
            def wrapper(*args, **kwargs):
                """Wraps the functioin."""
                if input_output_mode == "in":
                    for arg in args:
                        if not isinstance(arg, input_types):
                            print(f"Invalid input arguments, expected {', '.join(str(curent_type) for curent_type in input_types)}!")
                            break
                    for kwarg_value in kwargs.values():
                        if not isinstance(kwarg_value, input_types):
                            print(f"Invalid input arguments, expected {', '.join(str(curent_type) for curent_type in input_types)}!")
                            break

                decorated = func(*args, **kwargs)

                if input_output_mode == "out":
                    if not isinstance(decorated, input_types):
                        print(f"Invalid output value, expected {', '.join(str(curent_type) for curent_type in input_types)}!")
                return decorated
            return wrapper
        return decorator
    return var_types
