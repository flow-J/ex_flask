def decorator_factory(enter_message, exit_message):
    def simple_decorator(f):
        def wrapper():
            print enter_message
            f()
            print exit_message

        return wrapper
    return simple_decorator

@decorator_factory("Start", "End")
def hello():
    print "Hello World"

hello()


