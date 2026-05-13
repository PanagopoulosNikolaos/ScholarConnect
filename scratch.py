from nicegui import ui

def test():
    t = ui.textarea(value=None)
    try:
        print(t.value.strip())
    except Exception as e:
        print(type(e))

test()
