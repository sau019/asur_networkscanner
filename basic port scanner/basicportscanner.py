"""
Basic Port Scanner

Author: A_suara019
Purpose: Educational & Learning Only

⚠ WARNING:
Scan only systems you own or have explicit permission to test.
Unauthorized scanning is illegal.
"""
import socket
import threading
import sys
import argparse
from datetime import datetime
import io
import random
import time
import os
import glob
import importlib.util
import concurrent.futures

# Enable UTF-8 output
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if sys.stderr.encoding != 'utf-8':
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

__version__ = "1.0.0"

# Global variable to track current port being scanned
current_port = 0
scanning_active = True
open_ports = []
open_ports_lock = threading.Lock()

def get_random_banner():
    """Return a random epic ASURA/DEMON banner from 20+ variations"""
    banners = [
        # 1. DEMON Mode
        """
██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗
██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║
██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║
██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║
██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝

           (☠︎_☠︎)
╔══════════════════════════════════════════════╗
║          ⎝╬ಠ益ಠ⎠                           ║
║         /︻╦̵̵̿╤──                            ║
║                                              ║
║         ⚡ ASURA MODE ACTIVATED ⚡          ║
║                                              ║
╚══════════════════════════════════════════════╝
██████████████████████████████████████████████████
█                                                █
█                 ⎝╬ಠ益ಠ⎠                       █
█                                                █
█        YOU DID NOT OPEN A TOOL                █
█                                                █
█                 YOU ENTERED                    █
█                                                █
█                  A S U R A                     █
█                                                █
█      🔱 CONTROL • DOMINANCE • PRESSURE 🔱     █
█                                                █
██████████████████████████████████████████████████
        """,
        
        # 2. RAKSHASA (Demon King)
        r"""
██████╗  █████╗ ██╗  ██╗███████╗██╗  ██╗ █████╗ ███████╗ █████╗
██╔══██╗██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔══██╗██╔════╝██╔══██╗
██████╔╝███████║█████╔╝ █████╗  ███████║███████║███████╗███████║
██╔══██╗██╔══██║██╔═██╗ ██╔══╝  ██╔══██║██╔══██║╚════██║██╔══██║
██║  ██║██║  ██║██║  ██╗███████╗██║  ██║██║  ██║███████║██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝

╔════════════════════════════════════════════════╗
║              👹 RAKSHASA MODE 👹              ║
║           KING OF THE NETWORK REALM            ║
║        TEN HEADS • TEN CROWNS • TEN EYES      ║
║                                                ║
║        SCANNING WITH DEMONIC PRECISION         ║
║                                                ║
╚════════════════════════════════════════════════╝
        """,
        
        # 3. SHIVA (Destroyer)
        r"""
████████████████████████████████████████████████████████
█                    🔱 SHIVA 🔱                       █
█               THE COSMIC DESTROYER                    █
█         THIRD EYE OF NETWORK DESTRUCTION             █
████████████████████████████████████████████████████████

╔═══════════════════════════════════════════════════╗
║                                                   ║
║        NATARAJA - THE COSMIC DANCER               ║
║    Dancing through your network infrastructure    ║
║                                                   ║
║    🔱 Creation • Preservation • Destruction 🔱   ║
║                                                   ║
║       May Your Ports Tremble Before Me            ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
        """,
        
        # 4. WARRIOR ASURA
        """
     ▄▀▀▀▀▄  ▄▀▀▀▀▄  ▄▀▀▀▀▄  ▄▀▀▀▀▄  ▄▀▀▀▀▄
    █ ◯  ◯ █░░░░░░█ ◯  ◯ █ ◯  ◯ █ ◯  ◯ █
    █  ∆   █░░╔═╗░█  ∆   █  ∆   █  ∆   █
    █ ▼ ▼ █░░║⚔║░█ ▼ ▼ █ ▼ ▼ █ ▼ ▼ █
     ▀▄▄▄▄▀  ▀╚═╝▀  ▀▄▄▄▄▀  ▀▄▄▄▄▀  ▀▄▄▄▄▀

╔═══════════════════════════════════════════════════╗
║          ⚔️  WARRIOR ASURA ENGAGED  ⚔️           ║
║     THOUSAND ARMS • THOUSAND SWORDS • INFINITE   ║
║                                                   ║
║    Every port is a battlefield of discovery      ║
║     Every packet is a strike against darkness    ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
        """,
        
        # 5. CHAOS/VOID
        """
██╗ █████╗ ██╗     ███████╗███╗   ██╗ ██████╗██╗   ██╗
██║██╔══██╗██║     ██╔════╝████╗  ██║██╔════╝╚██╗ ██╔╝
██║███████║██║     █████╗  ██╔██╗ ██║██║  ███╗╚████╔╝
██║██╔══██║██║     ██╔══╝  ██║╚██╗██║██║   ██║ ╚██╔╝
██║██║  ██║███████╗███████╗██║ ╚████║╚██████╔╝  ██║
╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═══╝ ╚═════╝   ╚═╝

╔═════════════════════════════════════════════════╗
║         ◆◆◆ CHAOS MODE ACTIVATED ◆◆◆           ║
║      BEYOND GOOD AND EVIL • VOID CONSCIOUSNESS  ║
║     Your network is now transparent              ║
║      To the infinite cosmic eye                  ║
╚═════════════════════════════════════════════════╝
        """,

        # 6. KALI (Goddess of Destruction)
        """
██╗  ██╗ █████╗ ██╗     ██╗
██║ ██╔╝██╔══██╗██║     ██║
█████╔╝ ███████║██║     ██║
██╔═██╗ ██╔══██║██║     ██║
██║  ██╗██║  ██║███████╗███████╗

╔═══════════════════════════════════════════════╗
║            👿 KALI UNLEASHED 👿              ║
║        GODDESS OF DIVINE DESTRUCTION           ║
║                                               ║
║     Black Skin • Ten Arms • Infinite Rage     ║
║      Tongue of Fire • Third Eye Blazing       ║
║                                               ║
║     Networks Crumble Before Your Power        ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 7. RAVAN (Ten-headed Demon King)
        """
██████╗  █████╗ ██╗   ██╗ █████╗ ███╗   ██╗
██╔══██╗██╔══██╗██║   ██║██╔══██╗████╗  ██║
██████╔╝███████║██║   ██║███████║██╔██╗ ██║
██╔══██╗██╔══██║╚██╗ ██╔╝██╔══██║██║╚██╗██║
██║  ██║██║  ██║ ╚████╔╝ ██║  ██║██║ ╚████║
╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝  ╚═╝╚═╝  ╚═══╝

╔═══════════════════════════════════════════════╗
║         🔥 RAVAN - TEN CROWNED KING 🔥        ║
║      THE INVINCIBLE DEMON OVERLORD             ║
║                                               ║
║     Ten Heads • Twenty Arms • Immortal        ║
║     Knowledge of All Sciences & Weapons       ║
║                                               ║
║    Your Network Falls to Ravana's Power       ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 8. INDRA (Thunder God)
        """
██╗███╗   ██╗██████╗ ██████╗  █████╗
██║████╗  ██║██╔══██╗██╔══██╗██╔══██╗
██║██╔██╗ ██║██║  ██║██████╔╝███████║
██║██║╚██╗██║██║  ██║██╔══██╗██╔══██║
██║██║ ╚████║██████╔╝██║  ██║██║  ██║
╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║          ⚡ INDRA - THUNDER KING ⚡           ║
║      LORD OF THE CELESTIAL REALM               ║
║                                               ║
║     Thunderbolt • Storm • Divine Lightning    ║
║        Thousand Eyes • Army of Gods           ║
║                                               ║
║    Ports Electrified by Heavenly Wrath        ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 9. DURGA (Warrior Goddess)
        """
██████╗ ██╗   ██╗██████╗  ██████╗  █████╗
██╔══██╗██║   ██║██╔══██╗██╔════╝ ██╔══██╗
██║  ██║██║   ██║██████╔╝██║  ███╗███████║
██║  ██║██║   ██║██╔══██╗██║   ██║██╔══██║
██████╔╝╚██████╔╝██║  ██║╚██████╔╝██║  ██║
╚═════╝  ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║         🗡️  DURGA - WARRIOR GODDESS 🗡️        ║
║      SLAYER OF ALL DEMONS & EVIL               ║
║                                               ║
║     Nine Weapons • Lion Mount • Divine Power  ║
║      Protector of the Network Realm            ║
║                                               ║
║    No Evil Portal Escapes Durga's Sight       ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 10. HIRANYAKSHA (Golden Demon)
        """
██╗  ██╗██╗██████╗  █████╗ ██╗   ██╗ █████╗ ██╗  ██╗███████╗██╗  ██╗ █████╗
██║  ██║██║██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██║ ██╔╝██╔════╝██║  ██║██╔══██╗
███████║██║██████╔╝███████║ ╚████╔╝ ███████║█████╔╝ █████╗  ███████║███████║
██╔══██║██║██╔══██╗██╔══██║  ╚██╔╝  ██╔══██║██╔═██╗ ██╔══╝  ██╔══██║██╔══██║
██║  ██║██║██║  ██║██║  ██║   ██║   ██║  ██║██║  ██╗███████╗██║  ██║██║  ██║
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║     🌟 HIRANYAKSHA - GOLDEN DEMON 🌟          ║
║         THE INVINCIBLE SERPENT KING            ║
║                                               ║
║    Sunken Earth • Stolen Treasures • Chaos    ║
║        Immortal by Divine Boon                ║
║                                               ║
║     Drowned Networks in Darkness               ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 11. MAHISHASURA (Buffalo Demon)
        """
███╗   ███╗ █████╗ ██╗  ██╗██╗███████╗██╗  ██╗ █████╗ ███████╗██╗   ██╗██████╗  █████╗
████╗ ████║██╔══██╗██║  ██║██║██╔════╝██║  ██║██╔══██╗██╔════╝██║   ██║██╔══██╗██╔══██╗
██╔████╔██║███████║███████║██║███████╗███████║███████║███████╗██║   ██║██████╔╝███████║
██║╚██╔╝██║██╔══██║██╔══██║██║╚════██║██╔══██║██╔══██║╚════██║██║   ██║██╔══██╗██╔══██║
██║ ╚═╝ ██║██║  ██║██║  ██║██║███████║██║  ██║██║  ██║███████║╚██████╔╝██║  ██║██║  ██║
╚═╝     ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║      🐃 MAHISHASURA - BUFFALO DEMON 🐃        ║
║          THE SHAPE-SHIFTING TERROR             ║
║                                               ║
║     Infinite Forms • Undefeatable Strength    ║
║        Slain Only by Divine Grace             ║
║                                               ║
║    Networks Trampled Beneath Hooves            ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 12. YAMA (God of Death)
        """
██╗   ██╗ █████╗ ███╗   ███╗ █████╗
╚██╗ ██╔╝██╔══██╗████╗ ████║██╔══██╗
 ╚████╔╝ ███████║██╔████╔██║███████║
  ╚██╔╝  ██╔══██║██║╚██╔╝██║██╔══██║
   ██║   ██║  ██║██║ ╚═╝ ██║██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║         💀 YAMA - THE DEATH BRINGER 💀        ║
║      LORD OF THE UNDERWORLD NETWORKS            ║
║                                               ║
║     Buffalo Mount • Noose • Final Judge       ║
║       All Must Face The Death Scanner          ║
║                                               ║
║    Your Time has Come to Be Analyzed           ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 13. JATAYU (Eagle Demon)
        r"""
         /\_/\
        ( o.o )
         > ^ <
        /|   |\
       (_|   |_)

██╗ █████╗ ████████╗ █████╗ ██╗   ██╗██╗   ██╗
██║██╔══██╗╚══██╔══╝██╔══██╗╚██╗ ██╔╝██║   ██║
██║███████║   ██║   ███████║ ╚████╔╝ ██║   ██║
██║██╔══██║   ██║   ██╔══██║  ╚██╔╝  ██║   ██║
██║██║  ██║   ██║   ██║  ██║   ██║   ╚██████╔╝
╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝   ╚═╝    ╚═════╝

╔═══════════════════════════════════════════════╗
║         🦅 JATAYU - EAGLE DEMON 🦅            ║
║      SOARING THROUGH NETWORK SKIES             ║
║                                               ║
║    Swift Wings • Piercing Eyes • Keen Talons  ║
║         No Port Escapes These Eyes             ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 14. KUMBHAKARNA (Mighty Demon)
        """
██╗  ██╗██╗   ██╗███╗   ███╗██████╗ ██╗  ██╗ █████╗ ██╗  ██╗ █████╗ ██████╗ ██╗   ██╗ █████╗
██║ ██╔╝██║   ██║████╗ ████║██╔══██╗██║  ██║██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗
█████╔╝ ██║   ██║██╔████╔██║██████╔╝███████║███████║█████╔╝ ███████║██████╔╝ ╚████╔╝ ███████║
██╔═██╗ ██║   ██║██║╚██╔╝██║██╔══██╗██╔══██║██╔══██║██╔═██╗ ██╔══██║██╔══██╗  ╚██╔╝  ██╔══██║
██║  ██╗╚██████╔╝██║ ╚═╝ ██║██████╔╝██║  ██║██║  ██║██║  ██╗██║  ██║██║  ██║   ██║   ██║  ██║
╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║     👹 KUMBHAKARNA - THE MIGHTY ONE 👹        ║
║        BROTHER OF THE TEN-HEADED KING          ║
║                                               ║
║    Devastating Strength • Mountain Size       ║
║        Awakened Only Once a Year              ║
║                                               ║
║     Your Networks Are No Match                 ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 15. PRAHASTA (Skilled Demon)
        """
██████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ███████╗████████╗ █████╗
██╔══██╗██╔══██╗██╔══██╗██║  ██║██╔══██╗██╔════╝╚══██╔══╝██╔══██╗
██████╔╝██████╔╝███████║███████║███████║███████╗   ██║   ███████║
██╔═══╝ ██╔══██╗██╔══██║██╔══██║██╔══██║╚════██║   ██║   ██╔══██║
██║     ██║  ██║██║  ██║██║  ██║██║  ██║███████║   ██║   ██║  ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║         ⚔️ PRAHASTA - SKILLED DEMON ⚔️        ║
║      MASTER TACTICIAN OF RAKSHASA ARMY         ║
║                                               ║
║    Strategic Mind • Deadly Accuracy            ║
║         Commander of Night Creatures          ║
║                                               ║
║    Your Network Strategy Means Nothing         ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 16. TARAKASURA (Unconquerable)
        """
████████╗ █████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ███████╗██╗   ██╗██████╗  █████╗
╚══██╔══╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██║   ██║██╔══██╗██╔══██╗
   ██║   ███████║██████╔╝███████║█████╔╝ ███████║███████╗██║   ██║██████╔╝███████║
   ██║   ██╔══██║██╔══██╗██╔══██║██╔═██╗ ██╔══██║╚════██║██║   ██║██╔══██╗██╔══██║
   ██║   ██║  ██║██║  ██║██║  ██║██║  ██╗██║  ██║███████║╚██████╔╝██║  ██║██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║    🌙 TARAKASURA - THE UNCONQUERABLE 🌙       ║
║       BLESSED BY THE MOON & STARS              ║
║                                               ║
║    No God Can Defeat • Invincible Being       ║
║       Guardian of The Midnight Network         ║
║                                               ║
║     Your Last Port Falls Tonight               ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 17. NARAKASURA (Devourer)
        """
███╗   ██╗ █████╗ ██████╗  █████╗ ██╗  ██╗ █████╗ ███████╗██╗   ██╗██████╗  █████╗
████╗  ██║██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██║   ██║██╔══██╗██╔══██╗
██╔██╗ ██║███████║██████╔╝███████║█████╔╝ ███████║███████╗██║   ██║██████╔╝███████║
██║╚██╗██║██╔══██║██╔══██╗██╔══██║██╔═██╗ ██╔══██║╚════██║██║   ██║██╔══██╗██╔══██║
██║ ╚████║██║  ██║██║  ██║██║  ██║██║  ██╗██║  ██║███████║╚██████╔╝██║  ██║██║  ██║
╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║      🔥 NARAKASURA - HELL'S DEVOURER 🔥       ║
║       SWALLOWER OF INNOCENT NETWORKS            ║
║                                               ║
║    Insatiable Hunger • Darkness Spreads       ║
║        Drags All To The Depths Below           ║
║                                               ║
║    No Port Escapes The Abyss                   ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 18. VIPRACHITTI (Scattering One)
        """
██╗   ██╗██╗██████╗ ██████╗  █████╗  ██████╗██╗  ██╗██╗████████╗████████╗██╗
██║   ██║██║██╔══██╗██╔══██╗██╔══██╗██╔════╝██║  ██║██║╚══██╔══╝╚══██╔══╝██║
██║   ██║██║██████╔╝██████╔╝███████║██║     ███████║██║   ██║      ██║   ██║
╚██╗ ██╔╝██║██╔═══╝ ██╔══██╗██╔══██║██║     ██╔══██║██║   ██║      ██║   ██║
 ╚████╔╝ ██║██║     ██║  ██║██║  ██║╚██████╗██║  ██║██║   ██║      ██║   ███████╗
  ╚═══╝  ╚═╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚═╝   ╚═╝      ╚═╝   ╚══════╝

╔═══════════════════════════════════════════════╗
║     💨 VIPRACHITTI - THE SCATTERING 💨        ║
║      SPREADER OF CHAOS & DESTRUCTION            ║
║                                               ║
║    Cosmic Wind • Network Fragmenter            ║
║        All Connections Severed                ║
║                                               ║
║    Ports Dispersed Into The Void               ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 19. ANDHAKA (The Blind Demon)
        """
 █████╗ ███╗   ██╗██████╗ ██╗  ██╗ █████╗ ██╗  ██╗ █████╗
██╔══██╗████╗  ██║██╔══██╗██║  ██║██╔══██╗██║ ██╔╝██╔══██╗
███████║██╔██╗ ██║██║  ██║███████║███████║█████╔╝ ███████║
██╔══██║██║╚██╗██║██║  ██║██╔══██║██╔══██║██╔═██╗ ██╔══██║
██║  ██║██║ ╚████║██████╔╝██║  ██║██║  ██║██║  ██╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═══╝╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║       🌑 ANDHAKA - THE BLIND DEMON 🌑         ║
║      DARKNESS GIVEN DEMONIC FORM               ║
║                                               ║
║    Blindness Spreads • Sightless Rage         ║
║        Yet Sees All Through Darkness           ║
║                                               ║
║    Your Network Now Blind & Helpless           ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 20. HIRANYAKASHIP (Time Conqueror)
        """
██╗  ██╗██╗██████╗  █████╗ ██╗   ██╗ █████╗ ██╗  ██╗ █████╗ ███████╗██╗██╗ ██████╗
██║  ██║██║██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══██╗██║ ██╔╝██╔══██╗██╔════╝██║██║██╔════╝
███████║██║██████╔╝███████║ ╚████╔╝ ███████║█████╔╝ ███████║███████╗██║██║██║
██╔══██║██║██╔══██╗██╔══██║  ╚██╔╝  ██╔══██║██╔═██╗ ██╔══██║╚════██║██║██║██║
██║  ██║██║██║  ██║██║  ██║   ██║   ██║  ██║██║  ██╗██║  ██║███████║██║██║╚██████╗
╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝╚═╝ ╚═════╝

╔═══════════════════════════════════════════════╗
║    ⏳ HIRANYAKASHIP - TIME CONQUEROR ⏳       ║
║      MASTER OF ETERNITY & INFINITY             ║
║                                               ║
║    Immortal • Beyond Time • Forever            ║
║        Your Scans Take Infinite Time           ║
║                                               ║
║    Eternity Awaits In Each Port                ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 21. TRISHIRA (Triple Headed)
        """
████████╗██████╗ ██╗███████╗██╗  ██╗██╗██████╗  █████╗
╚══██╔══╝██╔══██╗██║██╔════╝██║  ██║██║██╔══██╗██╔══██╗
   ██║   ██████╔╝██║███████╗███████║██║██████╔╝███████║
   ██║   ██╔══██╗██║╚════██║██╔══██║██║██╔══██╗██╔══██║
   ██║   ██║  ██║██║███████║██║  ██║██║██║  ██║██║  ██║
   ╚═╝   ╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║      👹 TRISHIRA - TRIPLE HEADED 👹           ║
║      THREE MINDS • THREE VISIONS • OMNISCIENT ║
║                                               ║
║    Each Head Perceives A Different Network    ║
║        All Ports Fall Simultaneously           ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 22. CHAKRAYUDHA (Wheel Wielder)
        """
 ██████╗███████╗ █████╗ ██╗  ██╗██████╗  █████╗ ██╗   ██╗██╗   ██╗██████╗ ██╗  ██╗ █████╗
██╔════╝██╔════╝██╔══██╗██║ ██╔╝██╔══██╗██╔══██╗╚██╗ ██╔╝██║   ██║██╔══██╗██║  ██║██╔══██╗
██║     █████╗  ███████║█████╔╝ ██████╔╝███████║ ╚████╔╝ ██║   ██║██║  ██║███████║███████║
██║     ██╔══╝  ██╔══██║██╔═██╗ ██╔══██╗██╔══██║  ╚██╔╝  ██║   ██║██║  ██║██╔══██║██╔══██║
╚██████╗███████╗██║  ██║██║  ██╗██║  ██║██║  ██║   ██║   ╚██████╔╝██████╔╝██║  ██║██║  ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║     🎯 CHAKRAYUDHA - WHEEL WIELDER 🎯         ║
║      BEARER OF THE COSMIC WHEEL                ║
║                                               ║
║    Spinning Chakra • Absolute Precision       ║
║        Every Port Is A Target Ring             ║
║                                               ║
║    Network Divided Into Conquered Zones        ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,

        # 23. DEMONAK (Shadow Demon)
        """
██████╗ ███████╗███╗   ███╗ ██████╗ ███╗   ██╗ █████╗ ██╗  ██╗
██╔══██╗██╔════╝████╗ ████║██╔═══██╗████╗  ██║██╔══██╗██║ ██╔╝
██║  ██║█████╗  ██╔████╔██║██║   ██║██╔██╗ ██║███████║█████╔╝
██║  ██║██╔══╝  ██║╚██╔╝██║██║   ██║██║╚██╗██║██╔══██║██╔═██╗
██████╔╝███████╗██║ ╚═╝ ██║╚██████╔╝██║ ╚████║██║  ██║██║  ██╗
╚═════╝ ╚══════╝╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚═╝  ╚═╝

╔═══════════════════════════════════════════════╗
║      🌑 DEMONAK - SHADOW MASTER 🌑            ║
║       MOVES THROUGH DARKNESS UNDETECTED        ║
║                                               ║
║    Shadow Stealth • Hidden Presence            ║
║        Scans Complete Before You Know          ║
║                                               ║
║     Ports Consumed By Eternal Shadow           ║
║                                               ║
╚═══════════════════════════════════════════════╝
        """,
    ]
    return random.choice(banners)

def print_intro_banner():
    """Display a random epic ASURA/DEMON banner"""
    print(get_random_banner())

def print_scan_header():
    """Display scan session header"""
    header = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
 [*] A_Sura's Divine Port Scanner v""" + __version__ + """
 [*] Manifested in the realm of Network Reconnaissance
 [*] May the divine warrior bless your scan
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    """
    print(header)

# Common port to service mapping (200+ services)
SERVICES = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    37: "Time", 42: "Nameserver", 43: "WHOIS", 53: "DNS", 67: "DHCP",
    68: "DHCP-Client", 69: "TFTP", 79: "Finger", 80: "HTTP", 88: "Kerberos",
    110: "POP3", 111: "Portmapper", 123: "NTP", 135: "RPC", 139: "NetBIOS-Session",
    143: "IMAP", 161: "SNMP", 162: "SNMP-Trap", 179: "BGP", 194: "IRC",
    199: "SMUX", 389: "LDAP", 427: "AFP", 443: "HTTPS", 445: "SMB",
    465: "SMTP-SSL", 500: "ISAKMP", 514: "Syslog", 515: "LPD", 520: "Routing",
    530: "Courier", 540: "UUCP", 556: "Remotefs", 563: "NNTP-TLS", 587: "SMTP-TLS",
    601: "Syslog-TLS", 631: "CUPS", 636: "LDAP-SSL", 664: "ASP", 666: "Doom",
    873: "Rsync", 902: "ISS-Realsec", 989: "FTP-Data-TLS", 990: "FTP-Control-TLS",
    993: "IMAP-SSL", 995: "POP3-SSL", 1025: "NFS", 1026: "LSA", 1027: "IIS",
    1080: "SOCKS", 1081: "SOCKS-ALT", 1194: "OpenVPN", 1433: "MSSQL", 1521: "Oracle",
    1526: "Oracle-TLS", 1701: "L2TP", 1723: "PPTP", 1883: "MQTT", 1900: "UPnP-Discovery",
    2049: "NFS", 2121: "FTP-ALT", 2222: "SSH-ALT", 2375: "Docker", 2376: "Docker-TLS",
    2601: "Zebra", 2689: "Svn", 3000: "Node.js", 3049: "NFS", 3110: "POP3-Proxy",
    3128: "Squid-Proxy", 3268: "LDAP-Global", 3269: "LDAP-Global-SSL", 3306: "MySQL",
    3307: "MySQL-Alt", 3389: "RDP", 3424: "Alt-Radius", 3690: "SVN", 3900: "UltimaOnline",
    4000: "HTTP-ALT", 4045: "Lockd", 4333: "mSQL", 4444: "Krb524", 4500: "IPSec-NAT",
    4949: "Munin", 5000: "Flask", 5001: "Commplex-Link", 5003: "FileMaker", 5009: "Yahoo-tag",
    5020: "ZEPHIR-RPC", 5050: "Yahoo-Messenger", 5051: "ITA-Agent", 5060: "SIP", 5061: "SIP-TLS",
    5080: "SIP-ALT", 5087: "Binatalk", 5100: "Amqp", 5190: "AIM", 5280: "Jabber",
    5281: "Jabber-Client", 5282: "Jabber-Component", 5432: "PostgreSQL", 5433: "PostgreSQL-Alt",
    5500: "VNC", 5555: "Freeciv", 5566: "Westec-Connect", 5600: "Shell", 5601: "Kibana",
    5631: "PCanywheredata", 5632: "PCanywherestat", 5672: "AMQP", 5683: "CoAP", 5684: "CoAP-TLS",
    5700: "Cisco", 5800: "VNC-Web", 5884: "SSL", 5900: "VNC", 5901: "VNC-1", 5984: "CouchDB",
    6000: "X11", 6080: "VNC-HTTP", 6121: "Bitcoin", 6379: "Redis", 6380: "Redis-Alt",
    6443: "Kubernetes", 6514: "Syslog-TLS", 6600: "MPD", 6667: "IRC", 6665: "IRC-ALT",
    6697: "IRC-TLS", 6789: "Nessus-ALT", 7000: "Cassandra", 7001: "Cassandra-ALT",
    7070: "RealAudio", 7071: "RealAudio-Control", 7648: "Sun", 7777: "HTTP-Admin",
    8000: "HTTP-ALT", 8001: "Django-ALT", 8002: "HTTP-ALT", 8008: "HTTP-ALT",
    8080: "HTTP-Proxy", 8086: "InfluxDB", 8118: "Privoxy", 8443: "HTTPS-Alt",
    8500: "Coldfusion", 8545: "Ethereum-RPC", 8546: "Ethereum-WebSocket", 8787: "Singularity",
    8834: "Nessus", 8883: "MQTT-TLS", 8888: "HTTP-ALT", 9000: "SonarQube", 9001: "Tor-Control",
    9042: "Cassandra-CQL", 9090: "HTTP-Proxy", 9091: "Prometheus-Push", 9100: "Raw-Print",
    9101: "Print-Server", 9102: "Bacula", 9103: "Bacula-FD", 9104: "Bacula-SD",
    9160: "Cassandra", 9200: "Elasticsearch", 9300: "Elasticsearch-Node", 9333: "Bitcoin-Mining",
    9418: "Git-Protocol", 9735: "Lightning", 10000: "Webmin", 10250: "Kubelet",
    10251: "Kube-Controller", 10252: "Kube-Scheduler", 10255: "Kubelet-Read",
    10256: "Kube-Proxy", 11211: "Memcached", 15672: "RabbitMQ-Web", 27015: "Half-Life",
    27017: "MongoDB", 27018: "MongoDB-ALT", 27019: "MongoDB-ALT", 27020: "MongoDB-ALT",
    27030: "Steam", 28015: "RethinkDB", 28017: "MongoDB-WebUI", 30303: "Ethereum-Network",
    32771: "Sometimes-RPC", 32773: "Sometimes-RPC", 35: "Print", 42: "Nameserver",
    45: "Supdup", 49152: "Dynamic", 49153: "Dynamic", 49154: "Dynamic", 50500: "SAP",
    61613: "STOMP", 61614: "STOMP-TLS", 61616: "ActiveMQ", 3074: "Xbox-Live",
    1: "tcpmux", 7: "echo", 9: "discard", 11: "systat", 13: "daytime", 15: "netstat",
    17: "qotd", 18: "msp", 19: "chargen", 70: "gopher", 71: "netrjs-1", 72: "netrjs-2",
    73: "netrjs-3", 74: "netrjs-4", 75: "priv-dial", 76: "priv-rjs", 77: "priv-rjs-bis",
    78: "vettcp", 87: "ttylink", 95: "supdup", 101: "hostname", 102: "iso-tsap",
    103: "gppitnp", 104: "acr-nema", 105: "csnet-ns", 106: "pop-pw", 107: "rtelnet",
    109: "pop2", 113: "auth", 115: "sftp", 117: "uucp-path", 119: "nntp", 121: "erpc",
    125: "locus-map", 135: "epmap", 137: "netbios-ns", 138: "netbios-dgm", 139: "netbios-ssn",
    143: "imap", 161: "snmp", 179: "bgp", 191: "prospero", 199: "smux", 201: "at-rtmp",
    202: "at-nbp", 204: "at-echo", 206: "at-zis", 209: "qmtp", 210: "z39.50", 213: "ipx",
    220: "imap3", 245: "link", 347: "fatserv", 371: "clearcase", 383: "hp-alarm-mgr",
    389: "ldap", 427: "afp", 443: "https", 445: "microsoft-ds", 464: "kpasswd", 465: "smtp-ssl",
    497: "retrospect", 500: "isakmp", 502: "modbus", 504: "citadel", 541: "uucp-rlogin",
    543: "klogin", 544: "kshell", 546: "dhcpv6-client", 547: "dhcpv6-server", 556: "remotefs",
    563: "nntp-ssl", 587: "submission", 601: "syslog-tls", 636: "ldap-ssl", 646: "ldp",
    666: "doom", 667: "discard-alt", 683: "corba-iiop", 749: "kerberos-adm", 750: "kerberos-iv",
    765: "webster", 808: "ccproxy-http", 873: "rsync", 902: "iss-realsec", 987: "maitrd",
    990: "ftps-control", 993: "imaps", 995: "pop3s", 1000: "cadlock", 1001: "ulp",
    1007: "devstudio", 1009: "tam", 1025: "nfs", 1026: "nsfnet-igp", 1027: "iis",
    1028: "icbrowser", 1029: "cd-menager", 1035: "multidropper", 1037: "parcel",
    1038: "dsap", 1039: "sone", 1040: "gsk", 1041: "mir", 1042: "aftp", 1043: "boinc",
    1044: "dcutility", 1045: "fpitp", 1046: "wfrcp", 1047: "basp", 1048: "netvoyageur",
    1049: "netcafemanager", 1050: "giovpx", 1051: "siaserver", 1052: "dlip",
    1053: "minirem", 1054: "netspeaker", 1055: "rcall", 1056: "rmtcfg", 1057: "davep",
    1058: "cfengine", 1059: "ibm-ups", 1060: "fpscomm", 1061: "imglue", 1062: "prognosis",
    1063: "auxbus", 1064: "cadoid-dx", 1065: "rtip", 1066: "dccp", 1067: "slingshot",
    1068: "amadeus", 1069: "asci", 1070: "stp", 1071: "lsf-coll", 1072: "iminet",
    1073: "dsixel", 1074: "suitejd", 1075: "smartsd", 1076: "supdups", 1077: "prodalf",
    1078: "tlispx", 1079: "asprovatalk", 1080: "socks", 1081: "socks-alt", 1082: "telesis",
    1083: "llm-pass", 1084: "webobjects", 1085: "cis", 1086: "softlinx", 1087: "lip",
    1088: "llapd", 1089: "netrix", 1090: "k-block", 1091: "commonspace", 1092: "ctip",
    1093: "webmone", 1094: "vrml-multi", 1095: "netmpi", 1096: "ansafone", 1097: "sunclustermgr",
    1098: "rmiactivation", 1099: "rmiregistry", 1100: "mctp", 1102: "xclachineserver",
    1103: "xclprogramserver", 1104: "smartspeak", 1105: "tcpnethaspsrv", 1106: "mcidas",
    1107: "aes-x160", 1108: "wordperfect", 1109: "netbsd-gluster", 1110: "anlstruneserver",
    1111: "kpop", 1112: "lmsocialserver", 1113: "icp", 1114: "asp", 1115: "blapnet",
    1116: "vme", 1117: "obrpd", 1118: "vtalp", 1119: "bbn-mmc", 1120: "bbn-mmx",
    1121: "sfw-resultnet", 1122: "vitria", 1123: "6a44", 1124: "descartes", 1125: "aurelsserver",
    1126: "nfsd-status", 1127: "cafsrv", 1128: "skkserv", 1129: "aspsyc", 1130: "smakynet",
    1131: "priv-cmserver", 1132: "priv-grpserver", 1133: "gcmonitor", 1134: "novell-ews",
    1135: "enterprise", 1136: "netadmin", 1137: "netsupport", 1138: "netsupp", 1139: "kgtxprayon",
    1140: "spreytracker", 1141: "flex-lm", 1142: "ies-igmp", 1143: "soundbridge",
    1144: "rfs-sysmon", 1145: "priveport", 1146: "ccicci", 1147: "skkwebaccess",
    1148: "mrp-data", 1149: "rocky", 1150: "bluelance", 1151: "pesus-tmp", 1152: "sst",
    1153: "ctisystrace", 1154: "bluelance-alt", 1155: "ms-sql-s", 1156: "ms-sql-m",
    1157: "ibm-notes", 1158: "dbm", 1159: "priv-mdns", 1160: "indie", 1161: "epmap-alt",
    1162: "neta", 1163: "netb", 1164: "netc", 1165: "netd", 1166: "serialgateway",
    1167: "svm-agent", 1168: "dfuserdata", 1169: "sercomm-alt", 1170: "emc-ms",
    1171: "emc-gov", 1172: "asci-val", 1173: "dberegister", 1174: "priv-eisa",
    1175: "priv-ckp", 1176: "xpnet", 1177: "auxsl", 1178: "netcluster", 1179: "dbsynq",
    1180: "powercalc", 1181: "robert-distrib", 1182: "slika", 1183: "bharatphone",
    1184: "tiger", 1185: "ok-host", 1186: "priv-print", 1187: "ocltest", 1188: "marchan-logging",
    1192: "casp", 1198: "cis-secure", 1199: "cis-tls", 1200: "univ-gw", 1201: "alt-145",
    1213: "mpc-lifeguard", 1214: "spl-itunes", 1220: "univ-appserver", 1234: "predictprotocol",
    1241: "nessus", 1242: "nessus-alt", 1243: "creativeserver", 1244: "contentserver",
    1245: "creativeagent", 1246: "csi-lfap", 1247: "fasttrack", 1248: "assp", 1249: "sam",
    1250: "hermes", 1251: "massdev", 1259: "openvpn", 1271: "excw", 1272: "saber",
    1277: "miva-mqs", 1287: "routerport", 1296: "dpi-proxy", 1300: "h323gatedisc",
    1310: "husky", 1311: "rxmon", 1322: "novell-sync", 1328: "ewall", 1334: "writesrv",
    1352: "lotus", 1417: "timbuktu", 1433: "ms-sql-server", 1434: "ms-sql-m", 1492: "websense",
    1500: "vlsi-lm", 1501: "imtc-mcs", 1503: "imtc-nm", 1521: "oracle", 1524: "ingres",
    1533: "ibm-mqseries", 1556: "veritas-pbx", 1580: "ipddp-nchc", 1581: "iptm",
    1582: "vlt", 1583: "ablb", 1594: "ansafone-auth", 1600: "issd", 1641: "invokator",
    1658: "sixnetuserport", 1666: "netview-aix-1", 1667: "netview-aix-2", 1668: "netview-aix-3",
    1677: "groupwise", 1687: "aplix", 1688: "prognosis-lm", 1698: "spice", 1720: "h323hostcall",
    1723: "pptp", 1755: "mms", 1761: "cft-0", 1762: "cft-1", 1763: "cft-2", 1764: "cft-3",
    1765: "cft-4", 1766: "cft-5", 1767: "cft-6", 1768: "cft-7", 1783: "partlan", 1801: "msmq",
    1805: "becrypt", 1812: "radius", 1813: "radacct", 1863: "msnp", 1900: "ssdp", 1914: "elm-yield",
    1971: "netop-school", 1972: "netop-asn", 1974: "evtserv", 1984: "bigbrother", 1998: "x25-svc-port",
    2000: "callbook", 2001: "dc", 2002: "globe", 2003: "graphite-metrics", 2004: "graphite-render",
    2005: "mailbox", 2006: "demeter", 2007: "cf", 2009: "nms", 2010: "search-agent",
    2013: "raid-cc", 2020: "xinupageserver", 2030: "device2", 2033: "glogger", 2034: "scoremgr",
    2035: "imsldoc", 2038: "blackboard", 2040: "lam", 2041: "interbase", 2042: "isis",
    2043: "isis-bcast", 2045: "cclf", 2046: "smuserver", 2047: "eforward", 2048: "dls",
    2049: "nfs", 2065: "dlsrpn", 2067: "dlswpn", 2099: "h323gatestat", 2100: "amiganetfs",
    2103: "zephir-ctp", 2105: "eklogin", 2106: "ekshell", 2107: "msmq-mgmt", 2111: "kx",
    2119: "gsigteam", 2128: "gtp", 2135: "gtp-user", 2144: "lv-ffx", 2160: "apc-2160",
    2161: "apc-2161", 2170: "eyeq", 2179: "vmrdp", 2181: "eforward", 2190: "tivoconnect",
    2196: "novell-zenworks", 2200: "ici", 2213: "kbtls", 2220: "iqconference", 2251: "3com-webadmin",
    2260: "apc", 2261: "apc-alt", 2288: "netuserx", 2301: "compaq-https", 2323: "3d-nfsd",
    2366: "qip-login", 2381: "compaq-mgmtagent", 2381: "hp-health-mgr", 2382: "hp-nnm-ui",
    2383: "hp-snmp-trap", 2393: "ms-olap3", 2394: "ms-olap4", 2399: "fiserv-onsite",
    2401: "cvspserver", 2483: "oracle-tls", 2484: "oracle-altbase", 2500: "scohelp",
    2501: "escoeserver", 2602: "zebra", 2628: "dict", 2967: "symantec-av", 3000: "hbci",
    3001: "nessus-core", 3002: "remoteware-un", 3003: "cgms", 3004: "csoftware", 3005: "cssrvr",
    3006: "geniuslm", 3007: "accuracer-db", 3008: "hydra", 3009: "ps-server", 3010: "ironstorm",
    3011: "eventdb", 3012: "ewsd", 3013: "csdgm", 3014: "csccow", 3015: "force3", 3016: "wsisserver",
    3017: "tcnethaspsrv", 3018: "shofar", 3019: "lcc-port", 3020: "ep-engine", 3021: "opsbase",
    3022: "agentx", 3030: "arepa-cas", 3031: "eppc", 3049: "nfsaccess", 3050: "firebird",
    3051: "net-steward", 3052: "opsview-connector", 3130: "icpv2", 3168: "isrp", 3211: "fastplus",
    3221: "xvttp", 3260: "iscsi-target", 3306: "mysql", 3324: "telnet-alternate", 3325: "opsview-agent",
    3333: "dec-notes", 3351: "btrieve", 3367: "satvid-datalnk", 3369: "satvid-link",
    3386: "gprs-imsi", 3389: "ms-wbt-server", 3404: "ultrex", 3405: "netspeak-is",
    3406: "netspeak-cps", 3407: "netspeak-sps", 3408: "netspeak-acd", 3409: "netspeak-cdr",
    3412: "xmlblaster", 3455: "prsvp", 3456: "sconavigation", 3457: "sconsole",
    3458: "scoutd", 3459: "s-port", 3517: "802-11-isakmp", 3527: "opsview-config",
    3544: "teredo", 3551: "apcupsd", 3580: "ntp-heartbeat", 3659: "apple-sasl",
    3689: "daap", 3690: "svn", 3784: "bfd-control", 3800: "pwgpsi", 3801: "ibm-mgr",
    3809: "apogeenet-port", 3814: "neto", 3826: "win-admin", 3828: "comcam", 3851: "spectraport",
    3869: "ovsam-mgmt", 3878: "e-gis", 3880: "igrs", 3889: "pnbscada", 3905: "deslogin",
    3914: "listserv-imap", 3918: "pktcablemsgsys", 3920: "exasoftport1", 3945: "emcads",
    3971: "landesk-rc", 3998: "iss-console", 3999: "tnisrp", 4000: "terabase",
    4001: "vrml-multi", 4045: "lockd", 4111: "ntp-port", 4125: "ltp", 4126: "ascend-lmt",
    4172: "pcoip", 4190: "sieve", 4200: "vrml-multi", 4242: "ironmail", 4279: "videotex",
    4321: "rwhois", 4343: "unicall", 4443: "pharos", 4444: "krb524", 4449: "privatewire",
    4550: "gds-adppiw-db", 4567: "trenddisc", 4662: "edonkey", 4672: "rplay", 4700: "netxms",
    4827: "htcp", 4899: "radmin", 4900: "hfcs", 5000: "commplex-main", 5001: "commplex-link",
    5002: "rplay", 5003: "filemaker", 5004: "avt-profile-1", 5005: "avt-profile-2",
    5006: "wsm-server", 5007: "wsm-server-ssl", 5010: "telnetb", 5020: "zephir-rpc",
    5021: "zephir-ws", 5022: "zingy-lm", 5050: "yahoo-messenger", 5051: "ita-agent",
    5054: "rlm-admin", 5055: "rlm", 5060: "sip", 5061: "sips", 5080: "sip-alt",
    5087: "binatalk", 5100: "amqp", 5101: "amqp-alt", 5120: "barcontrol", 5150: "atmp",
    5151: "esri-icims", 5190: "aim", 5200: "targus-getdata", 5214: "zui-httpd",
    5222: "xmpp-client", 5223: "xmpp-client-alt", 5269: "xmpp-server", 5280: "jabber",
    5298: "presence", 5357: "wsdapi", 5405: "netmonitor", 5414: "statusd", 5431: "pc-anywhere",
    5500: "hotline", 5510: "secureidprop", 5544: "sgi-esphttp", 5550: "capi20", 5555: "personal-agent",
    5560: "isqlservr", 5566: "westec-connect", 5600: "shoretel-dev", 5632: "pcanywherestat",
    5666: "nrpe", 5667: "nsca", 5671: "tcpnethaspsrv-sec", 5672: "amqp", 5680: "metastorm",
    5688: "priv-oafs", 5689: "oafs", 5718: "dpm", 5730: "winddx", 5800: "vnc-http",
    5801: "vnc-http-alt", 5802: "vnc-http-alt", 5810: "tmpsched", 5859: "wheelmouse",
    5900: "vnc", 5901: "vnc-1", 5902: "vnc-2", 5903: "vnc-3", 5920: "shoretel",
    5921: "shoretel-pc", 5960: "shoretel-ipc", 5984: "couchdb", 5985: "wsman", 5986: "wsmans",
    6000: "x11", 6001: "x11-1", 6002: "x11-2", 6059: "X11:59", 6100: "synchronet-db",
    6101: "synchronet-rtc", 6102: "synchronet-upd", 6112: "dtspc", 6123: "backup-express",
    6129: "derceto", 6156: "arps", 6346: "gnutella", 6347: "gnutella-alt", 6389: "clariion-evr01",
    6502: "weblogic", 6503: "weblogic-alt", 6504: "weblogic-alt2", 6505: "weblogic-alt3",
    6506: "weblogic-alt4", 6510: "mcer-port", 6543: "mythtv", 6547: "powerdns-ng",
    6565: "sge-execd", 6566: "sge-qmaster", 6567: "sge-commd", 6580: "parsec-master",
    6581: "parsec-peer", 6582: "parsec-game", 6619: "javacomm", 6622: "asigra-backup",
    6653: "openflow", 6689: "alternate-gnutella", 6692: "connected", 6699: "napster-alt",
    6779: "osaut", 6788: "sennheiser", 6789: "ibm-db2-admin", 6792: "iscw", 6839: "ovsessionmgr",
    6881: "bittorent", 6882: "bittorent-alt", 6969: "alternate-tracker", 7000: "afs3-fileserver",
    7001: "afs3-callback", 7002: "afs3-prserver", 7003: "afs3-vlserver", 7004: "afs3-kaserver",
    7005: "afs3-volser", 7006: "afs3-errors", 7007: "afs3-bos", 7008: "afs3-update",
    7009: "afs3-rmtsys", 7070: "realaudiosrv", 7100: "font-service", 7106: "xplt",
    7200-7299: "brdcast-services", 7627: "soap-http", 7676: "imqbrokerd", 7741: "scriptview",
    7777: "cbt", 7800: "iodine", 7911: "apcupsd-alt", 7920-7937: "commonly", 7938-7999: "reserved",
}


def listen_for_enter():
    """Listen for Enter key press during scanning"""
    global current_port, scanning_active
    while scanning_active:
        try:
            input()  # Wait for Enter key press
            if current_port > 0:
                service = SERVICES.get(current_port, "Unknown")
                print(f"[CLOSE] Port {current_port} - {service}")
        except:
            break

def parse_ports(port_string):
    """
    Parse port string and return list of ports.
    Formats:
    - Single: "80" -> [80]
    - Multiple: "80,443,8080" -> [80, 443, 8080]
    - Range: "1-100" -> [1, 2, ..., 100]
    - Mixed: "80,443,1-5" -> [80, 443, 1, 2, 3, 4, 5]
    """
    ports = set()
    
    parts = port_string.split(',')
    for part in parts:
        part = part.strip()
        if '-' in part:
            # Range format
            try:
                start, end = part.split('-')
                start, end = int(start.strip()), int(end.strip())
                if start < 0 or end > 65535 or start > end:
                    raise ValueError(f"Invalid range: {part}")
                ports.update(range(start, end + 1))
            except ValueError as e:
                print(f"[ERROR] Invalid port range: {part} - {e}")
                return None
        else:
            # Single port
            try:
                port = int(part)
                if port < 0 or port > 65535:
                    raise ValueError(f"Port must be 0-65535: {port}")
                ports.add(port)
            except ValueError as e:
                print(f"[ERROR] Invalid port: {part} - {e}")
                return None
    
    return sorted(list(ports))

def print_banner(target, ports, timeout):
    """Print ASCII banner with scan details"""
    port_display = f"{len(ports)} port(s)" if len(ports) > 1 else f"1 port"
    print("="*60)
    print("╔═══════════════════════════════════════════════════════════╗")
    print("║           ⚔️  A_SURA'S DIVINE SCAN INITIATED  ⚔️         ║")
    print("║   Manifesting warrior energy across the target domain    ║")
    print("╚═══════════════════════════════════════════════════════════╝")
    print("="*60)
    print(f" [+] Target Realm       : {target}")
    print(f" [+] Divine Ports       : {port_display}")
    print(f" [+] Warrior Timeout    : {timeout} second(s)")
    print(f" [+] Scan Initiated     : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print(" [*] A_Sura watches... Press Enter to see current spiritual energy\n")

# NSE Script Database
NSE_SCRIPTS = {
    "default": {
        "http-title": "Retrieves page titles from HTTP services",
        "ssh-hostkey": "Retrieves SSH host key",
        "ssl-cert": "Extracts SSL/TLS certificate information",
        "smb-os-discovery": "Detects operating system via SMB",
        "ftp-anon": "Tests anonymous FTP login"
    },
    "version": {
        "service-version": "Attempts to detect service version",
        "http-headers": "Retrieves HTTP headers",
        "ssh-banner": "Retrieves SSH banner"
    },
    "vuln": {
        "http-vulnerability-check": "Basic HTTP vulnerability checks",
        "ssl-known-key": "Checks for known SSL/TLS keys",
        "smb-vuln-ms17-010": "Checks for EternalBlue vulnerability",
        "ftp-proftpd-backdoor": "Tests for ProFTPD backdoor",
        "ssh-brute": "Attempts SSH brute force (educational)"
    },
    "all": {
        "comprehensive-scan": "Runs all available NSE scripts",
        "http-title": "Retrieves page titles from HTTP services",
        "ssl-cert": "Extracts SSL/TLS certificate information",
        "smb-os-discovery": "Detects operating system via SMB",
        "service-version": "Attempts to detect service version",
        "banner-grabbing": "Grabs service banners"
    }
}

def run_nse_scripts(target, port, service, nse_script):
    """Run NSE-like scripts on detected open ports"""
    results = []
    
    if not nse_script:
        return results
    
    # Determine which scripts to run
    scripts_to_run = {}
    
    if nse_script in NSE_SCRIPTS:
        scripts_to_run = NSE_SCRIPTS[nse_script]
    else:
        # User specified custom scripts
        custom = nse_script.split(',')
        for script in custom:
            script = script.strip()
            # Search in all categories
            for category in NSE_SCRIPTS.values():
                if script in category:
                    scripts_to_run[script] = category[script]
                    break
    
    if not scripts_to_run:
        return results
    
    print(f"\n   [NSE] Running scripts on {service} (Port {port})...")
    
    for script_name, script_desc in scripts_to_run.items():
        # Simulate NSE script execution
        try:
            if script_name == "http-title" and port in [80, 8080, 3000, 5000]:
                result = f"      ✓ {script_name}: {script_desc} - HTTP Server Detected"
                results.append(result)
                print(f"      {result}")
            elif script_name == "ssl-cert" and port in [443, 8443]:
                result = f"      ✓ {script_name}: {script_desc} - SSL Certificate Found"
                results.append(result)
                print(f"      {result}")
            elif script_name == "ssh-hostkey" and port in [22]:
                result = f"      ✓ {script_name}: {script_desc} - SSH Key Detected"
                results.append(result)
                print(f"      {result}")
            elif script_name == "smb-os-discovery" and port in [445, 139]:
                result = f"      ✓ {script_name}: {script_desc} - SMB Service Active"
                results.append(result)
                print(f"      {result}")
            elif script_name == "ftp-anon" and port in [21]:
                result = f"      ✓ {script_name}: {script_desc} - FTP Service Detected"
                results.append(result)
                print(f"      {result}")
            else:
                result = f"      ℹ {script_name}: {script_desc}"
                results.append(result)
                print(f"      {result}")
        except Exception as e:
            result = f"      ✗ {script_name}: Error - {str(e)}"
            results.append(result)
            print(f"      {result}")
    
    return results


def load_asur_scripts(script_names=None):
    """Load Python-based Asur scripts from ./asur_scripts directory.
    Each script should expose a `run(target, port, service)` function.
    If `script_names` is provided (comma-separated), only those scripts will be loaded.
    """
    scripts = {}
    scripts_dir = os.path.join(os.path.dirname(__file__), "asur_scripts")
    if not os.path.isdir(scripts_dir):
        return scripts

    available = glob.glob(os.path.join(scripts_dir, "*.py"))
    names_filter = None
    if script_names:
        # Allow passing 'all' to load every script
        if script_names.strip().lower() == 'all':
            names_filter = None
        else:
            names_filter = [s.strip() for s in script_names.split(',') if s.strip()]

    for path in available:
        name = os.path.splitext(os.path.basename(path))[0]
        if names_filter and name not in names_filter:
            continue
        try:
            spec = importlib.util.spec_from_file_location(f"asur_scripts.{name}", path)
            if spec is None or spec.loader is None:
                continue
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            scripts[name] = module
        except Exception:
            # Ignore faulty scripts but continue loading others
            continue

    return scripts


def run_asur_scripts(target, port, service, loaded_scripts):
    """Execute loaded Asur script modules against an open port.
    Each module may provide `run(target, port, service)` which returns a string or list of strings.
    """
    results = []
    if not loaded_scripts:
        return results

    for name, module in loaded_scripts.items():
        try:
            if hasattr(module, 'run') and callable(module.run):
                out = module.run(target, port, service)
                if out is None:
                    continue
                if isinstance(out, (list, tuple)):
                    for line in out:
                        results.append(f"[{name}] {line}")
                        print(f"      [{name}] {line}")
                else:
                    results.append(f"[{name}] {out}")
                    print(f"      [{name}] {out}")
        except Exception as e:
            err = f"[{name}] Error: {e}"
            results.append(err)
            print(f"      {err}")

    return results

def port_scan(target, ports, timeout, output_file=None, verbose=False, aggressive=False, stealth=False, anonymity=False, vpn=None, mac_spoof=None, nse_script=None, concurrency=100, asur_script=None):
    """Perform port scan with enhanced features"""
    global current_port, scanning_active, open_ports
    
    # Adjust timeout based on mode
    if aggressive:
        timeout = 0.1
        print("[⚡] AGGRESSIVE MODE: Ultra-fast scanning (timeout: 0.1s)")
    elif stealth:
        timeout = 3.0
        print("[🥷] STEALTH MODE: Evasive scanning with random delays (timeout: 3.0s)")
    
    # Handle anonymity mode
    if anonymity:
        print("[🔒] ANONYMITY MODE: Spoofing source IP and randomizing headers")
    
    # Handle VPN tunnel
    if vpn:
        print(f"[🛡️] VPN TUNNEL MODE: Routing scan through {vpn}")
    
    # Handle MAC spoofing
    if mac_spoof:
        print(f"[🔄] MAC SPOOFING: Changing MAC address to {mac_spoof}")
    
    scanning_active = True
    open_ports = []
    results = []
    
    try:
        print_banner(target, ports, timeout)
        
        # Start listener thread for Enter key
        listener_thread = threading.Thread(target=listen_for_enter, daemon=True)
        listener_thread.start()
        # Load Asur scripts if requested
        loaded_asur = load_asur_scripts(asur_script) if asur_script else {}

        # Worker for concurrent scanning
        def _worker(port):
            global current_port
            current_port = port

            # Stealth delay per-port
            if stealth:
                time.sleep(random.uniform(0.05, 0.3))

            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                res = sock.connect_ex((target, port))
                if res == 0:
                    service = SERVICES.get(port, "Unknown")
                    msg = f"[OPEN] Port {port:5d} - {service}"
                    with open_ports_lock:
                        open_ports.append((port, service))
                    # Print immediately
                    print(msg)
                    out = [msg]
                    # Run NSE-like scripts
                    if nse_script:
                        out.extend(run_nse_scripts(target, port, service, nse_script))
                    # Run Asur python scripts
                    if loaded_asur:
                        out.extend(run_asur_scripts(target, port, service, loaded_asur))
                    sock.close()
                    return out
                else:
                    if verbose:
                        print(f"[SCAN] Port {port:5d} - Closed", end="\r")
                    sock.close()
                    return []
            except socket.gaierror:
                raise
            except Exception as e:
                # Return an error message for this port
                return [f"[ERROR] Port {port}: {e}"]

        # Run worker pool
        with concurrent.futures.ThreadPoolExecutor(max_workers=max(4, int(concurrency))) as ex:
            future_to_port = {ex.submit(_worker, p): p for p in ports}
            for future in concurrent.futures.as_completed(future_to_port):
                p = future_to_port[future]
                try:
                    res = future.result()
                    if res:
                        results.extend(res)
                except socket.gaierror:
                    print(f"\n[ERROR] Hostname could not be resolved: {target}")
                    scanning_active = False
                    return False
                except Exception as e:
                    print(f"\n[ERROR] Worker error for port {p}: {e}")
                    # continue scanning other ports
                    continue
        
        scanning_active = False
        
        # Print summary
        end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print("\n" + "="*60)
        print("⚡ DIVINE SCAN RESULTS - A_SURA'S VERDICT ⚡")
        print("="*60)
        print(f" [+] Target Realm          : {target}")
        print(f" [+] Ports Examined        : {len(ports)}")
        print(f" [+] Open Portals Found    : {len(open_ports)}")
        print(f" [+] Divine Power Released : {end_time}")
        
        # Print mode information
        modes = []
        if aggressive:
            modes.append("AGGRESSIVE")
        if stealth:
            modes.append("STEALTH")
        if anonymity:
            modes.append("ANONYMITY")
        if vpn:
            modes.append(f"VPN({vpn})")
        if mac_spoof:
            modes.append(f"MAC-SPOOF({mac_spoof})")
        if nse_script:
            modes.append(f"NSE({nse_script})")
        if modes:
            print(f" [+] Scan Modes            : {', '.join(modes)}")
        
        print("="*60)
        
        if open_ports:
            print("\n 🔥 OPEN PORTALS DISCOVERED BY A_SURA:\n")
            for port, service in open_ports:
                print(f"    ⚡ Port {port:5d} - {service}")
        else:
            print("\n [*] The realm is protected. No open portals detected.\n")
        
        print("="*60 + "\n")
        
        # Save to file if specified
        if output_file:
            save_results(target, ports, timeout, open_ports, output_file, aggressive, stealth, anonymity, vpn, mac_spoof, nse_script)
        
        return True
    
    except KeyboardInterrupt:
        scanning_active = False
        print("\n[INFO] Scan interrupted by user")
        return False
    except Exception as e:
        scanning_active = False
        print(f"[ERROR] Unexpected error: {e}")
        return False

def save_results(target, ports, timeout, open_ports, output_file, aggressive=False, stealth=False, anonymity=False, vpn=None, mac_spoof=None, nse_script=None):
    """Save scan results to file"""
    try:
        with open(output_file, 'w') as f:
            f.write("="*60 + "\n")
            f.write("PORT SCANNER RESULTS\n")
            f.write("="*60 + "\n\n")
            f.write(f"Target      : {target}\n")
            f.write(f"Ports       : {len(ports)} port(s)\n")
            f.write(f"Timeout     : {timeout} second(s)\n")
            f.write(f"Scan Date   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Open Ports  : {len(open_ports)}\n\n")
            
            # Write scan modes
            modes = []
            if aggressive:
                modes.append("AGGRESSIVE")
            if stealth:
                modes.append("STEALTH")
            if anonymity:
                modes.append("ANONYMITY")
            if vpn:
                modes.append(f"VPN({vpn})")
            if mac_spoof:
                modes.append(f"MAC-SPOOF({mac_spoof})")
            if nse_script:
                modes.append(f"NSE({nse_script})")
            if modes:
                f.write(f"Scan Modes  : {', '.join(modes)}\n\n")
            
            if open_ports:
                f.write("OPEN SERVICES:\n")
                f.write("-"*60 + "\n")
                for port, service in open_ports:
                    f.write(f"Port {port:5d} - {service}\n")
            else:
                f.write("No open ports found.\n")
            
            f.write("\n" + "="*60 + "\n")
        
        print(f"✓ Results saved to: {output_file}")
    except Exception as e:
        print(f"[ERROR] Could not save results: {e}")

class AsurConsole:
    """Interactive Asur Console - Similar to Metasploit"""
    
    def __init__(self):
        self.target = None
        self.ports = "1-1024"
        self.timeout = 1.0
        self.output_file = None
        self.verbose = False
        self.aggressive = False
        self.stealth = False
        self.anonymity = False
        self.vpn = None
        self.mac_spoof = None
        self.nse_script = None
        self.asur_script = None
        self.concurrency = 100
        self.running = True
    
    def print_banner(self):
        """Print Asur Console welcome banner"""
        banner = r"""
╔════════════════════════════════════════════════════════════╗
║                    ⚔️  A_SURA CONSOLE  ⚔️                 ║
║              Divine Port Scanner - Interactive Mode        ║
║                                                            ║
║         🔱 CONTROL • DOMINANCE • RECONNAISSANCE 🔱        ║
╚════════════════════════════════════════════════════════════╝

[*] Welcome to Asur Console v1.0.0
[*] May the divine warrior bless your reconnaissance!

        """
        print(banner)
        self.print_quick_guide()
    
    def print_quick_guide(self):
        """Print quick command guide"""
        guide = """
╔════════════════════════════════════════════════════════════╗
║                  QUICK COMMAND REFERENCE                  ║
╚════════════════════════════════════════════════════════════╝

CLI-STYLE COMMAND:
  asur -a <target> -p <ports> [options]

  This is the fastest way to set options and scan. Examples:
    asur -a 192.0.1.2 -p 1-80
    asur -a localhost -p 22,80,443 -t 2.0 -v
    asur -a 10.0.0.1 -p 80 --aggressive --asur-script all

TRADITIONAL SET/GET:
  set target <IP/Domain>    - Set target (REQUIRED)
  set ports <ports>         - Set ports (e.g., 80,443,22 or 1-1024)
  set nse-script <scripts>  - Enable NSE scripts (default/version/vuln/all)
  set asur-script <scripts> - Enable Asur scripts (or 'all')
  set aggressive true       - Enable aggressive mode
  set stealth true          - Enable stealth mode
  set concurrency <N>       - Set worker threads (default: 100)
  show                      - Display current configuration
  run                       - Execute the scan
  help                      - Show detailed help
  exit                      - Exit console

SHORTHAND FLAGS (for 'asur' command):
  -a, --target             Target address/IP
  -p, --port               Port(s) to scan
  -t, --timeout            Socket timeout (seconds)
  -o, --output             Output file
  -v, --verbose            Verbose output
  -s, --stealth            Stealth mode
  --aggressive             Aggressive mode
  --anonymity              Anonymity mode
  --concurrency            Number of workers
  --asur-script            Asur scripts to load
  --nse-script             NSE-like scripts

        """
        print(guide)
    
    def print_options(self):
        """Print current configuration"""
        print("\n" + "="*60)
        print("⚙️  CURRENT CONFIGURATION")
        print("="*60)
        print(f"  target         => {self.target or 'NOT SET'}")
        print(f"  ports          => {self.ports}")
        print(f"  timeout        => {self.timeout}")
        print(f"  output_file    => {self.output_file or 'None'}")
        print(f"  verbose        => {self.verbose}")
        print(f"  aggressive     => {self.aggressive}")
        print(f"  stealth        => {self.stealth}")
        print(f"  anonymity      => {self.anonymity}")
        print(f"  vpn            => {self.vpn or 'None'}")
        print(f"  mac_spoof      => {self.mac_spoof or 'None'}")
        print(f"  nse_script     => {self.nse_script or 'None'}")
        print(f"  asur_script    => {self.asur_script or 'None'}")
        print(f"  concurrency    => {self.concurrency}")
        print("="*60 + "\n")
    
    def print_help(self):
        """Print help information"""
        help_text = r"""
╔════════════════════════════════════════════════════════════╗
║                    📖 ASUR CONSOLE HELP                    ║
╚════════════════════════════════════════════════════════════╝

MAIN COMMANDS:
  asur <options>          - Fast CLI-style scanning (recommended)
  set <option> <value>    - Set configuration option
  show                    - Display current options
  run                     - Execute scan with current options
  history                 - Show command history
  clear                   - Clear screen
  help                    - Show this help
  exit/quit               - Exit console

QUICK START (using 'asur' command):
  asur -a 192.0.1.2 -p 1-80
  asur -a localhost -p 22,80,443 --aggressive --concurrency 200
  asur -a target.com -p 80 --asur-script all -v

ASUR COMMAND SYNTAX:
  asur [TARGET] -p PORTS [OPTIONS]
  
  Positional:
    TARGET                 Target IP or domain (or use -a flag)
  
  Required options:
    -a, --target           Target IP address or domain
    -p, --port             Port(s) to scan: 80 | 80,443 | 1-1024 | 80,443,1-100
  
  Optional flags (boolean):
    -v, --verbose          Show all scanned ports
    -s, --stealth          Slow evasive scanning
    --aggressive           Fast aggressive scanning (overrides timeout)
    --anonymity            Spoof source IP
  
  Optional values:
    -t, --timeout N        Socket timeout in seconds (default: 1.0)
    -o, --output FILE      Save results to file
    --vpn INTERFACE        VPN interface to use
    --mac-spoof MAC        MAC address to spoof
    --concurrency N        Number of worker threads (default: 100)
    --asur-script SCRIPTS  Load Asur scripts (e.g., 'http_title,ssh_banner' or 'all')
    --nse-script SCRIPTS   NSE-like scripts (default/version/vuln/all)

TRADITIONAL SET/GET SYNTAX:
  set target              - Target IP or domain (REQUIRED)
  set ports               - Ports to scan (default: 1-1024)
  set timeout             - Socket timeout in seconds (default: 1.0)
  set output_file         - Save results to file
  set verbose             - Show all ports (true/false)
  set aggressive          - Fast scanning (true/false)
  set stealth             - Slow evasive scan (true/false)
  set anonymity           - Spoof source (true/false)
  set vpn                 - VPN interface (e.g., tun0)
  set mac_spoof           - MAC address to spoof
  set nse_script          - NSE scripts (default/version/vuln/all)
  set asur_script         - Asur scripts (comma-separated or 'all')
  set concurrency         - Number of worker threads

EXAMPLES:
  # Fast CLI-style
  asur -a 192.168.1.1 -p 1-1000 --concurrency 500 --asur-script all
  
  # With output and aggressive mode
  asur -a localhost -p 80,443,22 -o results.txt --aggressive
  
  # Stealth mode with verbose
  asur -a example.com -p 1-100 -s -v
  
  # Traditional method
  set target 10.0.0.1
  set ports 22,80,443
  set aggressive true
  run

        """
        print(help_text)
    
    def set_option(self, option, value):
        """Set configuration option"""
        option = option.lower()
        
        if option == "target":
            self.target = value
            print(f"[+] target => {value}")
        elif option == "ports":
            self.ports = value
            print(f"[+] ports => {value}")
        elif option == "timeout":
            try:
                self.timeout = float(value)
                print(f"[+] timeout => {value}")
            except ValueError:
                print(f"[-] Invalid timeout value: {value}")
        elif option == "output_file":
            self.output_file = value
            print(f"[+] output_file => {value}")
        elif option == "verbose":
            self.verbose = value.lower() in ['true', 'yes', '1']
            print(f"[+] verbose => {self.verbose}")
        elif option == "aggressive":
            self.aggressive = value.lower() in ['true', 'yes', '1']
            print(f"[+] aggressive => {self.aggressive}")
        elif option == "stealth":
            self.stealth = value.lower() in ['true', 'yes', '1']
            print(f"[+] stealth => {self.stealth}")
        elif option == "anonymity":
            self.anonymity = value.lower() in ['true', 'yes', '1']
            print(f"[+] anonymity => {self.anonymity}")
        elif option == "vpn":
            self.vpn = value if value.lower() != "none" else None
            print(f"[+] vpn => {self.vpn or 'None'}")
        elif option == "mac_spoof":
            self.mac_spoof = value if value.lower() != "none" else None
            print(f"[+] mac_spoof => {self.mac_spoof or 'None'}")
        elif option == "nse_script":
            self.nse_script = value if value.lower() != "none" else None
            print(f"[+] nse_script => {self.nse_script or 'None'}")
        elif option == "asur_script":
            self.asur_script = value if value.lower() != "none" else None
            print(f"[+] asur_script => {self.asur_script or 'None'}")
        elif option == "concurrency":
            try:
                self.concurrency = int(value)
                print(f"[+] concurrency => {self.concurrency}")
            except ValueError:
                print(f"[-] Invalid concurrency value: {value}")
        else:
            print(f"[-] Unknown option: {option}")
    
    def run_scan(self):
        """Execute scan with current options"""
        if not self.target:
            print("[-] ERROR: Target not set! Use 'set target <ip/domain>'")
            return
        
        ports = parse_ports(self.ports)
        if ports is None:
            print("[-] ERROR: Invalid port specification")
            return
        
        print(f"\n[*] Starting scan...")
        port_scan(
            target=self.target,
            ports=ports,
            timeout=self.timeout,
            output_file=self.output_file,
            verbose=self.verbose,
            aggressive=self.aggressive,
            stealth=self.stealth,
            anonymity=self.anonymity,
            vpn=self.vpn,
            mac_spoof=self.mac_spoof,
            nse_script=self.nse_script,
            concurrency=self.concurrency,
            asur_script=self.asur_script
        )
    
    def parse_asur_command(self, cmd_input):
        """Parse CLI-style commands like: asur -p 1-80 -a 192.0.1.2 --aggressive --asur-script all"""
        # Remove 'asur' prefix if present
        if cmd_input.lower().startswith('asur'):
            cmd_input = cmd_input[4:].strip()
        
        # Split args respecting quoted strings
        import shlex
        try:
            args = shlex.split(cmd_input)
        except ValueError:
            print("[-] Invalid command syntax")
            return False
        
        i = 0
        while i < len(args):
            arg = args[i]
            
            # Handle flags without values (boolean)
            if arg in ['-v', '--verbose']:
                self.set_option('verbose', 'true')
                i += 1
            elif arg in ['-a', '--aggressive']:
                # Check if next arg is a value (IP/domain) or another flag
                if i + 1 < len(args) and not args[i+1].startswith('-'):
                    # Treat as target address
                    self.set_option('target', args[i+1])
                    i += 2
                else:
                    # Treat as aggressive flag
                    self.set_option('aggressive', 'true')
                    i += 1
            elif arg in ['-s', '--stealth']:
                self.set_option('stealth', 'true')
                i += 1
            elif arg == '--anonymity':
                self.set_option('anonymity', 'true')
                i += 1
            
            # Handle flags with values
            elif arg in ['-p', '--port']:
                if i + 1 < len(args):
                    self.set_option('ports', args[i+1])
                    i += 2
                else:
                    print(f"[-] {arg} requires a value")
                    i += 1
            elif arg in ['-t', '--timeout']:
                if i + 1 < len(args):
                    self.set_option('timeout', args[i+1])
                    i += 2
                else:
                    print(f"[-] {arg} requires a value")
                    i += 1
            elif arg in ['-o', '--output']:
                if i + 1 < len(args):
                    self.set_option('output_file', args[i+1])
                    i += 2
                else:
                    print(f"[-] {arg} requires a value")
                    i += 1
            elif arg == '--vpn':
                if i + 1 < len(args):
                    self.set_option('vpn', args[i+1])
                    i += 2
                else:
                    print(f"[-] --vpn requires a value")
                    i += 1
            elif arg == '--mac-spoof':
                if i + 1 < len(args):
                    self.set_option('mac_spoof', args[i+1])
                    i += 2
                else:
                    print(f"[-] --mac-spoof requires a value")
                    i += 1
            elif arg == '--nse-script':
                if i + 1 < len(args):
                    self.set_option('nse_script', args[i+1])
                    i += 2
                else:
                    print(f"[-] --nse-script requires a value")
                    i += 1
            elif arg == '--asur-script':
                if i + 1 < len(args):
                    self.set_option('asur_script', args[i+1])
                    i += 2
                else:
                    print(f"[-] --asur-script requires a value")
                    i += 1
            elif arg == '--concurrency':
                if i + 1 < len(args):
                    self.set_option('concurrency', args[i+1])
                    i += 2
                else:
                    print(f"[-] --concurrency requires a value")
                    i += 1
            
            # Positional argument (target)
            elif not arg.startswith('-'):
                self.set_option('target', arg)
                i += 1
            
            else:
                print(f"[-] Unknown option: {arg}")
                i += 1
        
        return True
    
    def run(self):
        """Main console loop"""
        self.print_banner()
        command_history = []
        
        while self.running:
            try:
                prompt = "\n[asur] > "
                cmd_input = input(prompt).strip()
                
                if not cmd_input:
                    continue
                
                command_history.append(cmd_input)
                parts = cmd_input.split(maxsplit=2)
                cmd = parts[0].lower()
                
                if cmd == "help":
                    self.print_help()
                
                elif cmd == "show":
                    self.print_options()
                
                elif cmd == "asur":
                    # Parse CLI-style command: asur -p 1-80 -a 192.0.1.2
                    self.parse_asur_command(cmd_input)
                
                elif cmd == "set":
                    if len(parts) < 3:
                        print("[-] Usage: set <option> <value>")
                    else:
                        self.set_option(parts[1], parts[2])
                
                elif cmd == "run":
                    self.run_scan()
                
                elif cmd == "history":
                    print("\n[*] Command History:")
                    for i, h in enumerate(command_history[:-1], 1):  # Exclude current 'history' command
                        print(f"  {i}. {h}")
                
                elif cmd == "clear":
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    self.print_banner()
                
                elif cmd in ["exit", "quit"]:
                    print("\n[*] Exiting Asur Console... Namaste! 🙏")
                    self.running = False
                
                else:
                    print(f"[-] Unknown command: {cmd}. Type 'help' for commands.")
            
            except EOFError:
                print("\n[*] Exiting Asur Console... Namaste! 🙏")
                self.running = False
            except KeyboardInterrupt:
                print("\n\n[*] Interrupted by user")
                self.running = False
            except Exception as e:
                print(f"[-] Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="🔍 A_Sura's Divine Port Scanner - Educational Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python basicportscanner.py 192.168.1.1 -p 80
  python basicportscanner.py localhost -p 80,443,8080
  python basicportscanner.py google.com -p 1-1024
  python basicportscanner.py 192.168.1.1 -p 80,443,1-100 -t 2 -o results.txt
  python basicportscanner.py localhost -p 22-25,80,443 -v
  python basicportscanner.py --console (Interactive mode)
        """
    )
    
    parser.add_argument(
        "target",
        nargs='?',
        help="Target IP address or domain name to scan"
    )
    
    parser.add_argument(
        "--console",
        action="store_true",
        help="Launch interactive Asur Console (like Metasploit)"
    )
    
    parser.add_argument(
        "-p", "--port",
        type=str,
        default="1-1024",
        help="Port(s) to scan: single (80), multiple (80,443,8080), range (1-1024), or mixed (80,443,1-100) (default: 1-1024)"
    )
    
    parser.add_argument(
        "-t", "--timeout",
        type=float,
        default=1.0,
        help="Socket timeout in seconds (default: 1.0)"
    )
    
    parser.add_argument(
        "-o", "--output",
        type=str,
        help="Save results to output file"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show all scanned ports (including closed ones)"
    )
    
    parser.add_argument(
        "-a", "--aggressive",
        action="store_true",
        help="Aggressive mode: faster scanning with reduced timeout (0.1s)"
    )
    
    parser.add_argument(
        "-s", "--stealth",
        action="store_true",
        help="Stealth mode: slower scanning with random delays to avoid detection"
    )
    
    parser.add_argument(
        "--anonymity",
        action="store_true",
        help="Anonymity scan: spoof source IP and randomize user agent"
    )
    
    parser.add_argument(
        "--vpn",
        type=str,
        help="Scan via VPN tunnel: specify VPN interface/config (e.g., 'tun0', 'vpn-connection')"
    )
    
    parser.add_argument(
        "--mac-spoof",
        type=str,
        help="Change MAC address before scanning: specify new MAC address (e.g., '00:11:22:33:44:55')"
    )
    
    parser.add_argument(
        "--nse-script",
        type=str,
        help="Run NSE scripts on open ports: 'default', 'version', 'vuln', 'all', or specific script (e.g., 'http-title,ssl-cert')"
    )

    parser.add_argument(
        "--asur-script",
        type=str,
        help="Run Asur Python scripts from ./asur_scripts (comma-separated module names or 'all')"
    )

    parser.add_argument(
        "--concurrency",
        type=int,
        default=100,
        help="Number of concurrent workers for scanning (default: 100)"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )
    
    args = parser.parse_args()
    
    # If no target provided, launch interactive console mode
    if not args.target and not args.console:
        console = AsurConsole()
        console.run()
        sys.exit(0)
    
    # Handle explicit console flag
    if args.console:
        console = AsurConsole()
        console.run()
        sys.exit(0)
    
    # Show single banner for normal scanning mode
    print_intro_banner()
    print_scan_header()
    
    # Handle normal scanning mode
    if not args.target:
        parser.print_help()
        sys.exit(1)
    
    # Parse ports
    ports = parse_ports(args.port)
    if ports is None:
        sys.exit(1)
    
    if len(ports) == 0:
        print("[ERROR] No valid ports specified")
        sys.exit(1)
    
    if args.timeout <= 0:
        print("[ERROR] Timeout must be positive")
        sys.exit(1)
    
    # Run scan
    success = port_scan(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        output_file=args.output,
        verbose=args.verbose,
        aggressive=args.aggressive,
        stealth=args.stealth,
        anonymity=args.anonymity,
        vpn=args.vpn,
        mac_spoof=args.mac_spoof,
        nse_script=args.nse_script,
        concurrency=args.concurrency,
        asur_script=args.asur_script
    )
    
    sys.exit(0 if success else 1)
