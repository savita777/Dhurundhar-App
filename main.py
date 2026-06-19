"""
=============================================================
  DHURANDHAR (2025)
  A Text-Based Stealth-Action Game
  Bollywood Spy Universe | Powered by Python
  Protagonist: Hamza Ali Mazari | RAW Agent, Cover ID: PHANTOM
=============================================================
"""

import time
import sys


# ─────────────────────────────────────────────
#  GLOBAL STATE
# ─────────────────────────────────────────────
suspicion_meter = 0   # 0 = invisible ghost | 100 = blown cover
player_name     = "Hamza Ali Mazari"
codename        = "PHANTOM"


# ─────────────────────────────────────────────
#  UTILITY HELPERS
# ─────────────────────────────────────────────
def slow_print(text: str, delay: float = 0.03) -> None:
    """Print text character-by-character for a cinematic effect."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()


def divider(char: str = "═", width: int = 60) -> None:
    print(char * width)


def show_suspicion(meter: int) -> None:
    """Display a visual suspicion bar."""
    filled = int(meter / 5)          # 20 blocks = 100 %
    bar    = "█" * filled + "░" * (20 - filled)
    status = "SAFE" if meter < 40 else ("RISKY" if meter < 70 else "CRITICAL")
    print(f"\n  🕵️  SUSPICION  [{bar}]  {meter}%  —  {status}\n")


def get_choice(prompt: str, options: list) -> str:
    """
    Display numbered options and return the validated choice string.
    Loops until the player enters a valid option number.
    """
    print(prompt)
    for idx, option in enumerate(options, start=1):
        print(f"  [{idx}] {option}")
    while True:
        raw = input("\n  ► Enter your choice (number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(options):
            chosen = options[int(raw) - 1]
            print()
            return chosen
        print("  ⚠  Invalid choice. Try again.")


def pause(seconds: float = 1.2) -> None:
    time.sleep(seconds)


# ─────────────────────────────────────────────
#  WELCOME SCREEN
# ─────────────────────────────────────────────
def welcome_screen() -> None:
    """Render the ASCII title card and lore intro."""
    print("\n")
    divider("═")
    slow_print("   ██████╗ ██╗  ██╗██╗   ██╗██████╗  █████╗ ███╗   ██╗██████╗ ██╗  ██╗ █████╗ ██████╗ ")
    slow_print("   ██╔══██╗██║  ██║██║   ██║██╔══██╗██╔══██╗████╗  ██║██╔══██╗██║  ██║██╔══██╗██╔══██╗")
    slow_print("   ██║  ██║███████║██║   ██║██████╔╝███████║██╔██╗ ██║██║  ██║███████║███████║██████╔╝")
    slow_print("   ██║  ██║██╔══██║██║   ██║██╔══██╗██╔══██║██║╚██╗██║██║  ██║██╔══██║██╔══██║██╔══██╗")
    slow_print("   ██████╔╝██║  ██║╚██████╔╝██║  ██║██║  ██║██║ ╚████║██████╔╝██║  ██║██║  ██║██║  ██║")
    slow_print("   ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝")
    divider("═")
    slow_print("                    ✦  धुरंधर  ✦  —  THE PHANTOM PROTOCOL  ✦  2025  ✦", delay=0.04)
    divider("═")

    pause(0.5)
    print("""
  SETTING :  Mumbai — a luxury hotel hosting foreign delegates.
  MISSION :  Infiltrate the Crescent Summit.
             Obtain intel on Operation Zulfiqar.
             Escape before dawn — without firing a single shot.

  AGENCY  :  Research & Analysis Wing  (R.A.W.)
  AGENT   :  Hamza Ali Mazari  |  Codename: PHANTOM
  STATUS  :  DEEP COVER  —  Alias: "Rahul Khanna", journalist
""")
    divider("─")
    slow_print("  Your choices shape the mission. Every second counts.", delay=0.04)
    slow_print("  Trust no one. Leave no trace.", delay=0.04)
    divider("─")
    input("\n  [ Press ENTER to begin the mission... ] ")
    print()


# ─────────────────────────────────────────────
#  LEVEL 1 — ENTRY
# ─────────────────────────────────────────────
def level_1_entry() -> int:
    """
    Level 1 — Hotel Entry
    Player chooses how to enter the secured hotel premises.
    Returns: suspicion delta (int)
    """
    global suspicion_meter

    divider()
    slow_print("  LEVEL 1  ▸  ENTRY :  THE CRESCENT SUMMIT HOTEL", delay=0.05)
    divider()
    print("""
  TIME     :  22:14 HRS
  LOCATION :  Service entrance alley, south wing.

  The hotel is on lockdown — a VIP corridor summit is underway
  on the 14th floor. Two armed guards flank the main entrance.
  Your press credentials won't hold under a biometric scan.

  R.A.W. handler whispers in your earpiece:
  "Phantom, we have a 4-minute window. Choose wisely."
""")

    choice = get_choice(
        "  How do you enter the hotel?",
        [
            "Backdoor stealth entry (slip through the kitchen service door)",
            "Guard bribery (flash a forged VIP pass and a bribe)"
        ]
    )

    if "Backdoor" in choice:
        slow_print("  ► You ghost past the CCTV blind spot and slide through the\n"
                   "    kitchen service door behind a catering trolley. Flawless.", delay=0.03)
        pause()
        slow_print("  ✔  You reach the staff stairwell undetected.", delay=0.03)
        delta = 5
        print(f"\n  📊  Suspicion +{delta}% — Guards unaware. Clean entry.")
    else:
        slow_print("  ► You approach the guard, slip ₹50,000 in a folded envelope,\n"
                   "    and flash the forged Rajasthan Press Council badge.", delay=0.03)
        pause()
        slow_print("  ⚠  The guard pockets the cash — but radios a colleague first.", delay=0.03)
        slow_print("  ✔  You're in, but a pair of eyes just clocked your face.", delay=0.03)
        delta = 25
        print(f"\n  📊  Suspicion +{delta}% — Money talks, but so do guards.")

    suspicion_meter += delta
    show_suspicion(suspicion_meter)
    input("  [ Press ENTER to proceed to Level 2... ] ")
    return delta


# ─────────────────────────────────────────────
#  LEVEL 2 — SPYING
# ─────────────────────────────────────────────
def level_2_spying() -> int:
    """
    Level 2 — Intelligence Gathering
    Player chooses how to capture the classified meeting.
    Returns: suspicion delta (int)
    """
    global suspicion_meter

    divider()
    slow_print("  LEVEL 2  ▸  SPYING :  THE ZULFIQAR BRIEFING ROOM", delay=0.05)
    divider()
    print("""
  TIME     :  22:31 HRS
  LOCATION :  14th Floor — Suite 1407, Presidential Corridor.

  Through a ventilation grille you can see GENERAL KHALID
  briefing three ISI operatives using an encrypted projector.
  The dossier on 'Operation Zulfiqar' is visible on screen.

  You have one shot to capture the intelligence.
  Your earpiece crackles: "Phantom — 8 minutes before shift change."
""")

    choice = get_choice(
        "  How do you gather the intel?",
        [
            "Record meeting (plant a micro-bug and activate your wrist-cam)",
            "Listen through door (press a contact-mic to the mahogany door)"
        ]
    )

    if "Record" in choice:
        slow_print("  ► You ease the grille open by 2 cm — just enough for the\n"
                   "    micro-bug to drop silently onto the chandelier chain above\n"
                   "    the conference table. Wrist-cam rolling. Crystal clear.", delay=0.03)
        pause()
        slow_print("  ✔  Full video + audio captured. Dossier pages visible on feed.", delay=0.03)
        delta = 10
        print(f"\n  📊  Suspicion +{delta}% — Minimal risk. Intel quality: GOLD.")
    else:
        slow_print("  ► You press the contact-mic against the door and activate\n"
                   "    the amplifier in your cufflink.", delay=0.03)
        pause()
        slow_print("  ⚠  A bellboy rounds the corner — you pocket the mic and\n"
                   "    pretend to check your watch. He slows down... then moves on.", delay=0.03)
        slow_print("  ✔  Partial audio captured. Key phrases recorded — enough to act on.", delay=0.03)
        delta = 20
        print(f"\n  📊  Suspicion +{delta}% — Near miss. Intel quality: SILVER.")

    suspicion_meter += delta
    show_suspicion(suspicion_meter)
    input("  [ Press ENTER to proceed to Level 3... ] ")
    return delta


# ─────────────────────────────────────────────
#  LEVEL 3 — ESCAPE
# ─────────────────────────────────────────────
def level_3_escape() -> int:
    """
    Level 3 — Extraction
    Player chooses how to escape the hotel before dawn.
    Returns: suspicion delta (int)
    """
    global suspicion_meter

    divider()
    slow_print("  LEVEL 3  ▸  ESCAPE :  PHANTOM EXTRACTION PROTOCOL", delay=0.05)
    divider()
    print("""
  TIME     :  22:58 HRS
  LOCATION :  12th Floor fire exit stairwell — south wing.

  ALERT! The guard who took your bribe has been replaced.
  The new shift commander is running biometric sweeps.
  Hotel elevators are being locked floor by floor — going UP.

  Extraction van is waiting in the alley. You have 90 seconds.
  Your handler: "Phantom, whatever you do — DO NOT get caught."
""")

    choice = get_choice(
        "  How do you get out?",
        [
            "Smoke bomb escape (deploy tactical smoke in the stairwell and run)",
            "Fire alarm distraction (pull the emergency alarm to evacuate the floor)"
        ]
    )

    if "Smoke" in choice:
        slow_print("  ► You crack the smoke canister against the stairwell railing.\n"
                   "    Grey haze floods Floors 11-13 in under 4 seconds.", delay=0.03)
        pause()
        slow_print("  ► Guards shout. Radio static. You're already two floors down,\n"
                   "    thermal masking cape activated.", delay=0.03)
        pause()
        slow_print("  ✔  You hit the service alley at 22:59:47. Van door slides open.", delay=0.03)
        delta = 15
        print(f"\n  📊  Suspicion +{delta}% — Chaos created, identity preserved. Textbook.")
    else:
        slow_print("  ► You yank the red lever in the corridor. Emergency klaxons\n"
                   "    BLARE across all 18 floors. Sprinklers rain down.", delay=0.03)
        pause()
        slow_print("  ► Guests pour into corridors — 300 bodies create perfect cover.\n"
                   "    You blend into the evacuation stream in a fire warden's vest\n"
                   "    grabbed from the emergency cabinet.", delay=0.03)
        pause()
        slow_print("  ⚠  General Khalid is being rushed out by his team — he\n"
                   "    makes eye contact with you for exactly 0.8 seconds.", delay=0.03)
        slow_print("  ✔  You make the van. He can't place the face. You're out.", delay=0.03)
        delta = 30
        print(f"\n  📊  Suspicion +{delta}% — Mass distraction works, but it was close.")

    suspicion_meter += delta
    show_suspicion(suspicion_meter)
    return delta


# ─────────────────────────────────────────────
#  MISSION DEBRIEF  (Ending Screen)
# ─────────────────────────────────────────────
def mission_debrief() -> None:
    """Calculate and display the final mission result."""
    global suspicion_meter

    divider("═")
    slow_print("  MISSION DEBRIEF  ▸  OPERATION ZULFIQAR", delay=0.05)
    divider("═")
    show_suspicion(suspicion_meter)

    # ── Determine ending tier ──────────────────────────────────────
    if suspicion_meter <= 30:
        title   = "👁️   GHOST OPERATIVE"
        outcome = "MISSION SUCCESS — PERFECT RUN"
        lines   = [
            "Zero trace. Zero witnesses. Zero noise.",
            "The intel on Operation Zulfiqar is already on the\n"
            "    Director's encrypted terminal in New Delhi.",
            "You were never there.",
            "\n  R.A.W. HQ transmission (eyes only):",
            "  'Phantom — DHURANDHAR protocol complete.\n"
            "   You are the finest blade in the dark.\n"
            "   India sleeps safely tonight.'"
        ]
    elif suspicion_meter <= 60:
        title   = "🕵️   SHADOW OPERATIVE"
        outcome = "MISSION SUCCESS — WITH EXPOSURE RISK"
        lines   = [
            "Intel retrieved. Extraction clean.",
            "However, two loose threads remain — a bribed guard\n"
            "    and a partial audio gap in the recording.",
            "Counter-intelligence is already handling the cover-up.",
            "\n  R.A.W. HQ transmission:",
            "  'Phantom — good work. Expect a debrief in 48 hours.\n"
            "   Keep your alias active for 72 more hours.'"
        ]
    else:
        title   = "🔴   COMPROMISED OPERATIVE"
        outcome = "MISSION PARTIAL — COVER AT RISK"
        lines   = [
            "The intel is valuable — but your cover is burning.",
            "General Khalid's team has initiated a photo\n"
            "    comparison sweep across hotel CCTV feeds.",
            "R.A.W. is extracting alias 'Rahul Khanna' from all\n"
            "    databases. You'll need a new identity by morning.",
            "\n  R.A.W. HQ transmission:",
            "  'Phantom — stand by for identity burn protocol.\n"
            "   Check into the safe house. NOW.'"
        ]

    # ── Print the debrief ─────────────────────────────────────────
    print(f"\n  {'─'*56}")
    slow_print(f"  FIELD RATING  :  {title}", delay=0.04)
    slow_print(f"  STATUS        :  {outcome}", delay=0.04)
    print(f"  {'─'*56}\n")
    for line in lines:
        slow_print(f"  {line}", delay=0.03)
        pause(0.4)

    # ── Score breakdown ───────────────────────────────────────────
    print(f"\n  {'─'*56}")
    print(f"  FINAL SUSPICION SCORE  :  {suspicion_meter} / 100")
    stars = max(1, 5 - suspicion_meter // 20)
    print(f"  MISSION RATING         :  {'★' * stars}{'☆' * (5 - stars)}  ({stars}/5)")
    print(f"  {'─'*56}\n")

    divider("═")
    slow_print("              Thank you for playing  DHURANDHAR (2025)", delay=0.04)
    slow_print("                  — The shadow war never ends —", delay=0.04)
    divider("═")
    print()


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────
def main() -> None:
    """Orchestrate the full game flow."""
    welcome_screen()
    level_1_entry()
    level_2_spying()
    level_3_escape()
    mission_debrief()


if __name__ == "__main__":
    main()
