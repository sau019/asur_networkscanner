#!/usr/bin/env python3
"""
Test script for Asur Console CLI-style commands
"""
import sys
sys.path.insert(0, '.')

from basicportscanner import AsurConsole

# Test the parse_asur_command method
console = AsurConsole()

print("=" * 70)
print("TESTING ASUR CLI-STYLE COMMANDS")
print("=" * 70)

# Test 1: Basic command
print("\n[TEST 1] asur -a 192.0.1.2 -p 1-80")
console.parse_asur_command("asur -a 192.0.1.2 -p 1-80")
console.print_options()

# Test 2: With aggressive and concurrency
print("\n[TEST 2] asur -a localhost -p 80,443 --aggressive --concurrency 200")
console.target = None  # Reset
console.ports = "1-1024"
console.aggressive = False
console.concurrency = 100
console.parse_asur_command("asur -a localhost -p 80,443 --aggressive --concurrency 200")
console.print_options()

# Test 3: Positional target with options
print("\n[TEST 3] asur 10.0.0.1 -p 22,23,25,80 -s -v --asur-script all")
console.target = None
console.ports = "1-1024"
console.stealth = False
console.verbose = False
console.asur_script = None
console.parse_asur_command("asur 10.0.0.1 -p 22,23,25,80 -s -v --asur-script all")
console.print_options()

print("\n" + "=" * 70)
print("TESTS COMPLETED")
print("=" * 70)
