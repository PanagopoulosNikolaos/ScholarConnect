from nicegui import ui, app

# mock data
professors = [{"AM": "P1", "FirstName": "A", "LastName": "B"}]
students = [{"AM": "S1", "FirstName": "C", "LastName": "D"}]
courses = [{"C_Code": "C1", "Title": "Course 1"}]

def test():
    try:
        data = {}
        instr_choices = [{"label": "x", "value": "x"}]
        instr_select = (
            ui.select(
                options=instr_choices,
                label="Instructor",
                value=data.get("AM_Instructor", ""), # This causes "Invalid value"
            )
        )
        print("Success!")
    except Exception as e:
        print(f"Error 1: {e}")
        
    try:
        data = {}
        instr_choices = [{"label": "x", "value": "x"}]
        instr_select = (
            ui.select(
                options=instr_choices,
                label="Instructor",
                value=data.get("AM_Instructor"), # returns None
            )
        )
        print("Success 2!")
    except Exception as e:
        print(f"Error 2: {e}")

test()
