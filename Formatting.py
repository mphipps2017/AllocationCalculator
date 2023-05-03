def stringify_dollar(value):
    return "$" + str(round(value,2))

def stringify_percentage(value):
    return str(round(value*100,2)) + '%'

# %-4.4f float print string