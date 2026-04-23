from datetime import date
 
def get_today():
    return str(date.today())
 
def init_day(history):
    today = get_today()
    if today not in history:
        history[today] = [False] * 8
    return history
 
def toggle_glass(water_list, index):
    water_list[index] = not water_list[index]
    return water_list
 
def calculate_water(water_list):
    return sum(water_list) * 0.25