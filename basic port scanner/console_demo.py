#!/usr/bin/env python3
"""
Demo script to show Asur Console functionality
"""

from basicportscanner import AsurConsole

if __name__ == "__main__":
    console = AsurConsole()
    
    # Display banner
    console.print_banner()
    
    # Display help
    console.print_help()
    
    # Show current options
    console.print_options()
    
    # Simulate some commands
    print("\n" + "="*60)
    print("DEMO: Setting options")
    print("="*60)
    
    console.set_option("target", "192.168.1.1")
    console.set_option("ports", "80,443,22")
    console.set_option("nse_script", "default")
    console.set_option("aggressive", "true")
    
    # Show updated options
    console.print_options()
    
    print("\n[*] Console is ready! Type 'python basicportscanner.py --console' to use it interactively")
