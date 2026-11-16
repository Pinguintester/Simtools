"""
Mensch ärgere Dich nicht - Simulation

Positionen sind relativ zum eigenen Startfeld.
Das Standardfeld hat folgende Eigenschaften:
Haus = -1
Bahn = 0, ..., 39
Ziel = 40, ..., 43
"""
from dataclasses import dataclass


HAUS = -1
SPIELER = 4
FIGUREN_ANZAHL = 4
BAHN_LAENGE = 40
ZIEL_START = BAHN_LAENGE
ZIEL_ENDE = BAHN_LAENGE + FIGUREN_ANZAHL - 1
ABSTAND_STARTFELDER = 10
RAUSKOMMEN = 6


@dataclass(frozen=True)
class Zug:
    """Eine Zugaktion im Spiel."""
    figur: int
    von: int
    nach: int
    geschlagen: tuple[int, int] | None = None


def startzustand(n_spieler: int = SPIELER) -> list[list[int]]:
    """Offizielle Aufstellung: 1 Figur auf dem Startfeld, 3 im Haus."""
    return [[0] + [HAUS] * (FIGUREN_ANZAHL - 1) for _ in range(n_spieler)]


def auf_bahn(position: int) -> bool:
    """True, wenn die Figur auf der Bahn steht (nicht Haus, nicht Ziel)."""
    return 0 <= position < BAHN_LAENGE


def absolut(spieler: int, position: int) -> int:
    """Relative Bahnposition -> Feld auf dem gemeinsamen Ring (0..39)."""
    return (position + spieler * ABSTAND_STARTFELDER) % BAHN_LAENGE


def fertig(pos: list[list[int]], spieler: int) -> bool:
    """True, wenn alle Figuren des Spielers im Ziel stehen."""
    return all(ZIEL_START <= figur <= ZIEL_ENDE for figur in pos[spieler])


def neue_position(position: int, wurf: int) -> int | None:
    """Wohin käme die Figur? None, wenn der Zug unmöglich ist."""
    if position == HAUS:
        if wurf == RAUSKOMMEN:
            return 0
        return None

    nach = position + wurf
    if nach > ZIEL_ENDE:
        return None
    return nach


def figur_auf_feld(pos: list[list[int]], feld: int) -> tuple[int, int] | None:
    """Welche Figur steht auf diesem absoluten Bahnfeld? (spieler, figur) oder None."""
    for spieler, figuren in enumerate(pos):
        for figur, position in enumerate(figuren):
            if auf_bahn(position) and absolut(spieler, position) == feld:
                return (spieler, figur)
    return None


def legale_zuege(pos: list[list[int]], spieler: int, wurf: int) -> list[Zug]:
    """Alle erlaubten Züge eines Spielers bei diesem Wurf, nach den Pflichtregeln."""
    eigene = pos[spieler]
    zuege = []

    # Alle theoretischen Züge
    for figur, von in enumerate(eigene):
        nach = neue_position(von, wurf)
        if nach is None or nach in eigene:
            continue
        geschlagen = None
        if auf_bahn(nach):
            geschlagen = figur_auf_feld(pos, absolut(spieler, nach))
        zuege.append(Zug(figur, von, nach, geschlagen))

    # Alle Pflichtzüge (Rauskommen und Startfeld räumen)
    if HAUS in eigene:
        rauskommen = [zug for zug in zuege if zug.von == HAUS]
        if rauskommen:
            return rauskommen
        startfeld = [zug for zug in zuege if zug.von == 0]
        if startfeld:
            return startfeld
    return zuege


def moegliche_zuege(pos: list[list[int]], spieler: int, wurf: int) -> list[Zug]:
    """Alle Züge nach den Grundregeln, ohne Pflichtregeln."""
    eigene = pos[spieler]
    zuege = []
    haus_schon_gezogen = False
    for figur, von in enumerate(eigene):
        if von == HAUS:
            # Alle Hausfiguren sind gleichwertig: nur einen Rauskomm-Zug anbieten
            if haus_schon_gezogen:
                continue
            haus_schon_gezogen = True

        nach = neue_position(von, wurf)
        if nach is None or nach in eigene:
            continue  # unmöglich oder eigene Figur blockiert

        geschlagen = None
        if auf_bahn(nach):
            geschlagen = figur_auf_feld(pos, absolut(spieler, nach))
        zuege.append(Zug(figur=figur, von=von, nach=nach, geschlagen=geschlagen))
    return zuege
