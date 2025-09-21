
def register(pm):
    def hello(name='world'):
        return f'hello {name}'
    pm.register_action('hello.sample', hello)
