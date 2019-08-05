#Selecting sensitivity

def main():
    entered_sensitivity = int(input("\n>> Please enter sensitivy level from [1-10] where 10 is most sensitive : "))
    #Is sensitivit between 1-10 ?
    if (entered_sensitivity >= 1 and entered_sensitivity <= 10):
        return entered_sensitivity
    else:
        raise ValueError('Invalid value. Please select a valid value between [1-10]')