
def debug(debug_mode, anything) -> None:
    if debug_mode:
        if anything is str:
            print("DEBUG: " + anything)
        else:
            print("DEBUG: " + str(anything))

