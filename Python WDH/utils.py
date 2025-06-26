def eingabe_validieren(betrag):
    try:
        betrag = float(betrag)
        if betrag <= 0:
            return False
        return True
    except ValueError:
        return False

def berechne_gesamt(einnahmen, ausgaben):
    gesamt_einnahmen = sum(betrag for betrag, _ in einnahmen)
    gesamt_ausgaben = sum(betrag for betrag, _ in ausgaben)
    return gesamt_einnahmen, gesamt_ausgaben