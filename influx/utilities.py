def check_callsign(callsign):
    if not callsign:
        callsign = "None"      # If callsign is empty
    elif callsign[0] == "0":   # Sometime empty callsign is registered as "00000000"
        callsign = "None"

    return callsign
