"""
╔═══════════════════════════════════════════════════════════╗
║           DHURANDHAR (2025)  —  Kivy Mobile App           ║
║    Text-Based Stealth Game  |  Bollywood Spy Universe     ║
║    Agent  : Hamza Ali Mazari  |  Codename : PHANTOM       ║
╚═══════════════════════════════════════════════════════════╝

Architecture
────────────
  ScreenManager
    WelcomeScreen  → title card + START button
    Level1Screen   → Entry       (2 choice buttons)
    Level2Screen   → Spying      (2 choice buttons)
    Level3Screen   → Escape      (2 choice buttons)
    DebriefScreen  → final score + replay

  GameState        → shared suspicion meter + choice log
  GameScreen       → base class with shared layout helpers

Kivy layout per game screen
────────────────────────────
  BoxLayout (vertical, root)
  ├── lbl_header   Label  — level title         (fixed h)
  ├── lbl_meter    Label  — suspicion % + tag   (fixed h)
  ├── bar          ProgressBar                  (fixed h)
  ├── ScrollView                                (expand)
  │   └── lbl_story  Label (markup, auto-wrap)
  └── btn_box      BoxLayout (vertical)         (fixed h)
      └── Button × 1-2
"""

# ── disable Kivy's default key-handler so ESC doesn't quit ──
import os
os.environ.setdefault("KIVY_NO_ENV_CONFIG", "1")

from kivy.config import Config
Config.set("kivy", "exit_on_escape", "0")          # safe on Android too

from kivy.app import App
from kivy.uix.screenmanager import (
    ScreenManager, Screen, SlideTransition, FadeTransition,
)
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar
from kivy.core.window import Window
from kivy.metrics import dp, sp

# Dark navy — matches the Android status bar on most launchers
Window.clearcolor = (0.04, 0.04, 0.09, 1)

# ─────────────────────────────────────────────────────────────
#  COLOR PALETTE  (Spy Noir × Bollywood Gold)
# ─────────────────────────────────────────────────────────────
C = {
    # Signature accent
    "gold"     : (0.976, 0.773, 0.118, 1),   # #F9C51E
    "gold_dk"  : (0.68,  0.52,  0.07,  1),   # darker gold
    # Feedback
    "green"    : (0.08,  0.74,  0.40,  1),   # stealth success
    "orange"   : (0.88,  0.42,  0.06,  1),   # risky choice
    "red"      : (0.84,  0.14,  0.14,  1),   # alert / critical
    # Buttons
    "btn_blue" : (0.09,  0.27,  0.54,  1),   # primary CTA
    "btn_teal" : (0.05,  0.40,  0.26,  1),   # stealth option
    "btn_rust" : (0.44,  0.16,  0.05,  1),   # risky option
    # Text
    "white"    : (0.95,  0.95,  0.95,  1),
    "dim"      : (0.58,  0.62,  0.70,  1),
}

# ─────────────────────────────────────────────────────────────
#  SHARED GAME STATE
# ─────────────────────────────────────────────────────────────
class GameState:
    """
    Singleton-style object that persists between screens.
    Call reset() at the start of each new game.
    """

    def reset(self):
        self.suspicion: int       = 0
        self.choices  : list[str] = []
        self.deltas   : list[int] = []

    def add_suspicion(self, delta: int) -> None:
        self.suspicion = min(100, self.suspicion + delta)
        self.deltas.append(delta)

    # ── derived properties ──────────────────────────────────
    @property
    def meter_tag(self) -> str:
        s = self.suspicion
        if s < 40:
            return "[color=#22CC77]SAFE[/color]"
        if s < 70:
            return "[color=#F9C51E]RISKY[/color]"
        return "[color=#EE3333][b]CRITICAL[/b][/color]"

    @property
    def rating(self) -> tuple[str, str, tuple]:
        """Returns (title_str, outcome_str, kivy_color_tuple)."""
        s = self.suspicion
        if s <= 30:
            return ("👁  GHOST OPERATIVE",
                    "MISSION SUCCESS — PERFECT RUN", C["green"])
        if s <= 60:
            return ("🕵  SHADOW OPERATIVE",
                    "MISSION SUCCESS — EXPOSURE RISK", C["gold"])
        return ("🔴  COMPROMISED",
                "MISSION PARTIAL — COVER BURNED", C["red"])

    @property
    def stars(self) -> int:
        return max(1, 5 - self.suspicion // 20)


GAME = GameState()
GAME.reset()


# ─────────────────────────────────────────────────────────────
#  BASE GAME SCREEN  (shared layout + helpers)
# ─────────────────────────────────────────────────────────────
class GameScreen(Screen):
    """
    Shared skeleton used by Level1 / Level2 / Level3.

    ┌───────────────────────────────────┐
    │  lbl_header  (level title)        │  dp(28)
    │  lbl_meter   (suspicion text)     │  dp(22)
    │  bar         (progress bar)       │  dp(12)
    ├───────────────────────────────────┤
    │  ScrollView → lbl_story           │  weight=1
    ├───────────────────────────────────┤
    │  btn_box (2 choices or 1 next)    │  dp(148)|dp(72)
    └───────────────────────────────────┘
    """

    def __init__(self, **kw):
        super().__init__(**kw)

        root = BoxLayout(
            orientation="vertical",
            padding=(dp(14), dp(12), dp(14), dp(10)),
            spacing=dp(8),
        )

        # ── header ──────────────────────────────────────────
        self.lbl_header = Label(
            text="",
            font_size=sp(12),
            bold=True,
            color=C["gold"],
            markup=True,
            size_hint=(1, None),
            height=dp(28),
            halign="center",
            valign="middle",
        )
        self.lbl_header.bind(size=self.lbl_header.setter("text_size"))

        # ── suspicion label ──────────────────────────────────
        self.lbl_meter = Label(
            text="",
            font_size=sp(11),
            color=C["dim"],
            markup=True,
            size_hint=(1, None),
            height=dp(22),
            halign="center",
            valign="middle",
        )
        self.lbl_meter.bind(size=self.lbl_meter.setter("text_size"))

        # ── progress bar ─────────────────────────────────────
        self.bar = ProgressBar(
            max=100,
            value=0,
            size_hint=(1, None),
            height=dp(12),
        )

        # ── scrollable story area ────────────────────────────
        sv = ScrollView(size_hint=(1, 1), do_scroll_x=False)
        self.lbl_story = Label(
            text="",
            font_size=sp(15),
            color=C["white"],
            markup=True,
            halign="left",
            valign="top",
            size_hint=(1, None),
            padding=(dp(4), dp(8)),
        )
        # auto-resize height to fit text; auto-wrap to widget width
        self.lbl_story.bind(
            texture_size=lambda inst, val: setattr(inst, "height", val[1]),
            width=lambda inst, val: setattr(inst, "text_size", (val, None)),
        )
        sv.add_widget(self.lbl_story)

        # ── button container ─────────────────────────────────
        self.btn_box = BoxLayout(
            orientation="vertical",
            size_hint=(1, None),
            height=dp(148),          # 2× dp(64) + spacing + padding
            spacing=dp(8),
            padding=(0, dp(6)),
        )

        root.add_widget(self.lbl_header)
        root.add_widget(self.lbl_meter)
        root.add_widget(self.bar)
        root.add_widget(sv)
        root.add_widget(self.btn_box)
        self.add_widget(root)

    # ── helpers ──────────────────────────────────────────────

    def _sync_meter(self) -> None:
        """Refresh the progress bar and suspicion label from GAME state."""
        self.bar.value = GAME.suspicion
        self.lbl_meter.text = (
            f"[b]SUSPICION:[/b]  {GAME.suspicion}%  —  {GAME.meter_tag}"
        )

    def _make_choice_btn(self, text: str, color: tuple, cb) -> Button:
        """Create a tall, mobile-friendly choice button."""
        btn = Button(
            text=text,
            markup=True,
            font_size=sp(14),
            size_hint=(1, None),
            height=dp(64),
            background_normal="",
            background_color=color,
            color=C["white"],
            halign="center",
            valign="middle",
        )
        btn.bind(
            size=lambda inst, val: setattr(inst, "text_size", val),
            on_release=cb,
        )
        return btn

    def _make_next_btn(self, label: str, target_screen: str) -> Button:
        """Create the 'Proceed to next level' button after a choice is made."""
        btn = Button(
            text=f"[b]▶  {label}[/b]",
            markup=True,
            font_size=sp(15),
            size_hint=(1, None),
            height=dp(60),
            background_normal="",
            background_color=C["btn_blue"],
            color=C["white"],
        )

        def _go(_btn):
            if target_screen == "debrief":
                self.manager.get_screen("debrief").rebuild()
                self.manager.transition = FadeTransition(duration=0.45)
            else:
                self.manager.transition = SlideTransition(
                    direction="left", duration=0.30
                )
            self.manager.current = target_screen

        btn.bind(on_release=_go)
        return btn

    def _resolve_choice(
        self,
        outcome_markup: str,
        delta: int,
        next_screen: str,
        next_label: str,
    ) -> None:
        """
        Called when the player taps a choice button:
          1. Record suspicion delta.
          2. Replace story text with the outcome.
          3. Swap 2-choice buttons for 1 'next level' button.
        """
        GAME.add_suspicion(delta)
        self.lbl_story.text = (
            outcome_markup
            + f"\n\n[b][color=#F9C51E]⬆  SUSPICION  +{delta}%[/color][/b]"
        )
        self.btn_box.clear_widgets()
        self.btn_box.height = dp(72)
        self.btn_box.add_widget(self._make_next_btn(next_label, next_screen))
        self._sync_meter()


# ─────────────────────────────────────────────────────────────
#  WELCOME SCREEN
# ─────────────────────────────────────────────────────────────
class WelcomeScreen(Screen):

    def on_enter(self, *_args):
        """Reset game state every time this screen is shown (covers replay)."""
        GAME.reset()

    def __init__(self, **kw):
        super().__init__(**kw)

        root = BoxLayout(
            orientation="vertical",
            padding=(dp(24), dp(28), dp(24), dp(20)),
            spacing=dp(14),
        )

        # ── Title block ──────────────────────────────────────
        root.add_widget(Label(
            text=(
                "[b][color=#F9C51E]✦  DHURANDHAR  ✦[/color][/b]\n"
                "[size=16sp][color=#999999]THE PHANTOM PROTOCOL[/color][/size]\n"
                "[size=11sp][color=#44445A]2 0 2 5[/color][/size]"
            ),
            markup=True,
            font_size=sp(33),
            halign="center",
            valign="middle",
            size_hint=(1, 0.26),
        ))

        # ── Divider ──────────────────────────────────────────
        root.add_widget(Label(
            text="[color=#1E2030]" + "═" * 52 + "[/color]",
            markup=True,
            size_hint=(1, None),
            height=dp(16),
            halign="center",
        ))

        # ── Mission lore ─────────────────────────────────────
        lore = Label(
            text=(
                "[b][color=#F9C51E]  MISSION BRIEFING[/color][/b]\n\n"
                "[color=#C2C6CE]"
                "  SETTING :  Mumbai\n"
                "             Crescent Summit Hotel\n\n"
                "  MISSION :  Infiltrate the VIP summit.\n"
                "             Obtain intel on\n"
                "             [b]Operation Zulfiqar[/b].\n"
                "             Escape before dawn.\n\n"
                "  AGENCY  :  Research & Analysis Wing\n\n"
                "  AGENT   :  [b]Hamza Ali Mazari[/b]\n"
                "  COVER   :  Journalist, Rajasthan Press\n"
                "  CODE    :  [b][color=#F9C51E]PHANTOM[/color][/b]"
                "[/color]"
            ),
            markup=True,
            font_size=sp(15),
            halign="left",
            valign="top",
            size_hint=(1, 1),
        )
        lore.bind(size=lore.setter("text_size"))
        root.add_widget(lore)

        # ── Start button ─────────────────────────────────────
        start = Button(
            text="[b]▶  BEGIN MISSION[/b]",
            markup=True,
            font_size=sp(17),
            size_hint=(1, None),
            height=dp(68),
            background_normal="",
            background_color=C["btn_blue"],
            color=C["white"],
        )
        start.bind(on_release=self._start)
        root.add_widget(start)

        self.add_widget(root)

    def _start(self, _btn):
        self.manager.transition = FadeTransition(duration=0.40)
        self.manager.current = "level1"


# ─────────────────────────────────────────────────────────────
#  LEVEL 1  —  ENTRY
# ─────────────────────────────────────────────────────────────
class Level1Screen(GameScreen):
    """
    The player chooses how to enter the hotel.
    on_pre_enter rebuilds the screen so 'Play Again' works correctly.
    """

    def on_pre_enter(self, *_args):
        self.lbl_header.text = "LEVEL 1  ▸  ENTRY :  CRESCENT SUMMIT HOTEL"
        self.lbl_story.text = (
            "[b][color=#F9C51E]⏱  22:14 HRS[/color][/b]  "
            "[color=#888888]|  Service entrance alley, south wing[/color]\n\n"
            "[color=#C2C6CE]"
            "The hotel is on lockdown — a VIP summit is underway\n"
            "on the 14th floor. Two armed guards flank the main\n"
            "entrance. Your press credentials won't hold under a\n"
            "biometric scan.\n\n"
            "Handler in your earpiece:\n"
            "[/color]"
            "[b][color=#F9C51E]\"Phantom — 4-minute window. Choose wisely.\"[/color][/b]"
        )
        self.btn_box.clear_widgets()
        self.btn_box.height = dp(148)
        self.btn_box.add_widget(self._make_choice_btn(
            "🚪  [b]Backdoor Stealth Entry[/b]\n"
            "[size=12sp]Slip through the kitchen service door[/size]",
            C["btn_teal"],
            self._choice_stealth,
        ))
        self.btn_box.add_widget(self._make_choice_btn(
            "💰  [b]Guard Bribery[/b]\n"
            "[size=12sp]Flash a forged VIP pass and a bribe[/size]",
            C["btn_rust"],
            self._choice_bribe,
        ))
        self._sync_meter()

    def _choice_stealth(self, _btn):
        GAME.choices.append("Backdoor Stealth Entry")
        self._resolve_choice(
            outcome_markup=(
                "[color=#22CC77]✔  You ghost past the CCTV blind spot and slide\n"
                "through the kitchen service door behind a catering\n"
                "trolley. Not a single pixel on any screen moved.[/color]\n\n"
                "[color=#C2C6CE]You reach the staff stairwell completely undetected.\n"
                "Guards are unaware. Clean entry.[/color]"
            ),
            delta=5,
            next_screen="level2",
            next_label="Proceed to Level 2",
        )

    def _choice_bribe(self, _btn):
        GAME.choices.append("Guard Bribery")
        self._resolve_choice(
            outcome_markup=(
                "[color=#EE8833]⚠  You slip ₹50,000 in an envelope and flash\n"
                "the forged Rajasthan Press Council badge.[/color]\n\n"
                "[color=#C2C6CE]Guard pockets the cash — but radios a colleague\n"
                "first. You're in, but a pair of eyes just clocked\n"
                "your face.[/color]"
            ),
            delta=25,
            next_screen="level2",
            next_label="Proceed to Level 2",
        )


# ─────────────────────────────────────────────────────────────
#  LEVEL 2  —  SPYING
# ─────────────────────────────────────────────────────────────
class Level2Screen(GameScreen):

    def on_pre_enter(self, *_args):
        self.lbl_header.text = "LEVEL 2  ▸  SPYING :  ZULFIQAR BRIEFING ROOM"
        self.lbl_story.text = (
            "[b][color=#F9C51E]⏱  22:31 HRS[/color][/b]  "
            "[color=#888888]|  Suite 1407, 14th Floor[/color]\n\n"
            "[color=#C2C6CE]"
            "Through a ventilation grille you can see\n"
            "[b]General Khalid[/b] briefing three ISI operatives.\n"
            "The dossier on [b]Operation Zulfiqar[/b] is visible\n"
            "on the encrypted projector.\n\n"
            "You have exactly one shot to capture it.\n"
            "[/color]"
            "[b][color=#F9C51E]\"Phantom — 8 minutes before shift change.\"[/color][/b]"
        )
        self.btn_box.clear_widgets()
        self.btn_box.height = dp(148)
        self.btn_box.add_widget(self._make_choice_btn(
            "📹  [b]Record Meeting[/b]\n"
            "[size=12sp]Plant micro-bug + activate wrist-cam[/size]",
            C["btn_teal"],
            self._choice_record,
        ))
        self.btn_box.add_widget(self._make_choice_btn(
            "👂  [b]Listen Through Door[/b]\n"
            "[size=12sp]Press contact-mic to the mahogany door[/size]",
            C["btn_rust"],
            self._choice_listen,
        ))
        self._sync_meter()

    def _choice_record(self, _btn):
        GAME.choices.append("Record Meeting")
        self._resolve_choice(
            outcome_markup=(
                "[color=#22CC77]✔  Grille eased open 2 cm. The micro-bug drops\n"
                "silently onto the chandelier chain above the table.\n"
                "Wrist-cam rolling. Crystal clear feed.[/color]\n\n"
                "[color=#C2C6CE]Full video + audio captured. Dossier pages\n"
                "visible on stream. Intel quality: [b]GOLD[/b].[/color]"
            ),
            delta=10,
            next_screen="level3",
            next_label="Proceed to Level 3",
        )

    def _choice_listen(self, _btn):
        GAME.choices.append("Listen Through Door")
        self._resolve_choice(
            outcome_markup=(
                "[color=#EE8833]⚠  A bellboy rounds the corner mid-operation.\n"
                "You pocket the mic and pretend to check your watch.\n"
                "He slows... then moves on.[/color]\n\n"
                "[color=#C2C6CE]Partial audio captured. Key phrases recorded —\n"
                "enough to build a picture.\n"
                "Intel quality: [b]SILVER[/b].[/color]"
            ),
            delta=20,
            next_screen="level3",
            next_label="Proceed to Level 3",
        )


# ─────────────────────────────────────────────────────────────
#  LEVEL 3  —  ESCAPE
# ─────────────────────────────────────────────────────────────
class Level3Screen(GameScreen):

    def on_pre_enter(self, *_args):
        self.lbl_header.text = "LEVEL 3  ▸  ESCAPE :  PHANTOM EXTRACTION"
        self.lbl_story.text = (
            "[b][color=#F9C51E]⏱  22:58 HRS[/color][/b]  "
            "[color=#888888]|  12th Floor fire-exit stairwell[/color]\n\n"
            "[color=#EE4444][b]⚠  ALERT:[/b][/color]  "
            "[color=#C2C6CE]Bribed guard has been replaced.\n"
            "New shift commander is running biometric sweeps.\n"
            "Elevators locking floor by floor — going UP.\n\n"
            "Extraction van is waiting in the alley. 90 seconds.\n"
            "[/color]"
            "[b][color=#F9C51E]\"Phantom — DO NOT get caught.\"[/color][/b]"
        )
        self.btn_box.clear_widgets()
        self.btn_box.height = dp(148)
        self.btn_box.add_widget(self._make_choice_btn(
            "💨  [b]Smoke Bomb Escape[/b]\n"
            "[size=12sp]Deploy tactical smoke in stairwell and run[/size]",
            C["btn_teal"],
            self._choice_smoke,
        ))
        self.btn_box.add_widget(self._make_choice_btn(
            "🔔  [b]Fire Alarm Distraction[/b]\n"
            "[size=12sp]Pull the emergency alarm to flood the floor[/size]",
            C["btn_teal"],
            self._choice_smoke,
        ))
        self.btn_box.add_widget(self._make_choice_btn(
            "🔔  [b]Fire Alarm Distraction[/b]\n"
            "[size=12sp]Pull the emergency alarm to flood the floor[/size]",
            C["btn_rust"],
            self._choice_alarm,
        ))
        self._sync_meter()

    def _choice_smoke(self, _btn):
        GAME.choices.append("Smoke Bomb Escape")
        self._resolve_choice(
            outcome_markup=(
                "[color=#22CC77]✔  Smoke canister cracked against the railing.\n"
                "Grey haze floods Floors 11-13 in 4 seconds.\n"
                "Thermal masking cape activated.[/color]\n\n"
                "[color=#C2C6CE]You hit the service alley at 22:59:47.\n"
                "Van door slides open. Textbook extraction.[/color]"
            ),
            delta=15,
            next_screen="debrief",
            next_label="Mission Debrief",
        )

    def _choice_alarm(self, _btn):
        GAME.choices.append("Fire Alarm Distraction")
        self._resolve_choice(
            outcome_markup=(
                "[color=#EE8833]⚠  Emergency klaxons BLARE across all 18 floors.\n"
                "300 guests flood the corridors in seconds.[/color]\n\n"
                "[color=#C2C6CE]You blend in wearing a fire warden's vest grabbed\n"
                "from the emergency cabinet.\n\n"
                "General Khalid makes eye contact — 0.8 seconds.\n"
                "He can't place the face. You make the van.[/color]"
            ),
            delta=30,
            next_screen="debrief",
            next_label="Mission Debrief",
        )


# ─────────────────────────────────────────────────────────────
#  DEBRIEF SCREEN
# ─────────────────────────────────────────────────────────────
class DebriefScreen(Screen):
    """
    Dynamically built when rebuild() is called from Level3Screen.
    Shows: rating title, outcome, star rating, choice log, replay button.
    """

    def __init__(self, **kw):
        super().__init__(**kw)
        self._root = BoxLayout(
            orientation="vertical",
            padding=(dp(22), dp(20), dp(22), dp(16)),
            spacing=dp(10),
        )
        self.add_widget(self._root)

    def rebuild(self) -> None:
        """Populate or repopulate the debrief layout from current GAME state."""
        self._root.clear_widgets()

        title_str, outcome_str, color = GAME.rating
        r, g, b, _ = color
        hex_c = "%02x%02x%02x" % (int(r * 255), int(g * 255), int(b * 255))
        stars_filled = "★" * GAME.stars
        stars_empty  = "☆" * (5 - GAME.stars)

        # ── debrief title ─────────────────────────────────
        self._root.add_widget(Label(
            text="[b][color=#F9C51E]✦  MISSION DEBRIEF  ✦[/color][/b]",
            markup=True,
            font_size=sp(21),
            halign="center",
            size_hint=(1, None),
            height=dp(46),
        ))

        # ── operative rating ──────────────────────────────
        rating_lbl = Label(
            text=(
                f"[b][color=#{hex_c}]{title_str}[/color][/b]\n"
                f"[size=12sp][color=#AAAAAA]{outcome_str}[/color][/size]"
            ),
            markup=True,
            font_size=sp(19),
            halign="center",
            size_hint=(1, None),
            height=dp(64),
        )
        rating_lbl.bind(size=rating_lbl.setter("text_size"))
        self._root.add_widget(rating_lbl)

        # ── star rating ───────────────────────────────────
        self._root.add_widget(Label(
            text=(
                f"[size=30sp]{stars_filled}[color=#333355]{stars_empty}[/color][/size]\n"
                f"[size=11sp][color=#888888]{GAME.stars} / 5  STARS[/color][/size]"
            ),
            markup=True,
            halign="center",
            size_hint=(1, None),
            height=dp(68),
        ))

        # ── choice log ────────────────────────────────────
        log_lines = "\n".join(
            f"  L{i + 1}:  [b]{choice}[/b]  "
            f"[color=#F9C51E]+{delta}%[/color]"
            for i, (choice, delta)
            in enumerate(zip(GAME.choices, GAME.deltas))
        )
        score_lbl = Label(
            text=(
                "[b][color=#F9C51E]CHOICE LOG[/color][/b]\n\n"
                f"[color=#C2C6CE][size=13sp]{log_lines}[/size][/color]\n\n"
                f"[b]FINAL SUSPICION :  "
                f"[color=#F9C51E]{GAME.suspicion}%[/color][/b]"
            ),
            markup=True,
            font_size=sp(14),
            halign="left",
            valign="top",
            size_hint=(1, 1),
        )
        score_lbl.bind(size=score_lbl.setter("text_size"))
        self._root.add_widget(score_lbl)

        # ── flavour quote ─────────────────────────────────
        self._root.add_widget(Label(
            text='[i][color=#44445A]"The shadow war never ends."[/color][/i]',
            markup=True,
            font_size=sp(12),
            halign="center",
            size_hint=(1, None),
            height=dp(26),
        ))

        # ── replay button ─────────────────────────────────
        replay = Button(
            text="[b]↺  PLAY AGAIN[/b]",
            markup=True,
            font_size=sp(16),
            size_hint=(1, None),
            height=dp(62),
            background_normal="",
            background_color=C["btn_blue"],
            color=C["white"],
        )
        replay.bind(on_release=self._replay)
        self._root.add_widget(replay)

    def _replay(self, _btn) -> None:
        """Reset game and return to welcome screen; level screens auto-refresh via on_pre_enter."""
        GAME.reset()
        self.manager.transition = FadeTransition(duration=0.40)
        self.manager.current = "welcome"


# ─────────────────────────────────────────────────────────────
#  APP ENTRY POINT
# ─────────────────────────────────────────────────────────────
class DhurandharApp(App):

    def build(self):
        self.title = "DHURANDHAR (2025)"
        sm = ScreenManager()
        for name, cls in [
            ("welcome", WelcomeScreen),
            ("level1",  Level1Screen),
            ("level2",  Level2Screen),
            ("level3",  Level3Screen),
            ("debrief", DebriefScreen),
        ]:
            sm.add_widget(cls(name=name))
        return sm


if __name__ == "__main__":
    DhurandharApp().run()
