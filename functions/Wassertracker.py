from datetime import date

def get_today():
    return str(date.today())


def init_day(history, num_glasses=8):
    today = get_today()
    if today not in history:
        history[today] = [False] * num_glasses
    return history


def toggle_glass(water_list, index):
    new_list = water_list.copy()
    new_list[index] = not new_list[index]
    return new_list


def calculate_water(water_list):
    return sum(water_list) * 0.25
