#!/usr/bin/env python3
"""
CrunchDAO Identity Manager - Profile Management Script
Manage multiple coordinator/cruncher profiles for different networks and roles.
"""

import json
import os
import sys
import argparse
from pathlib import Path

PROFILES_FILE = Path(__file__).parent.parent / "profiles.json"

def load_profiles():
    """Load profiles from profiles.json"""
    if not PROFILES_FILE.exists():
        return {"profiles": {}}
    
    with open(PROFILES_FILE, 'r') as f:
        return json.load(f)

def save_profiles(data):
    """Save profiles to profiles.json"""
    with open(PROFILES_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def list_profiles():
    """List all available profiles"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if not profiles:
        print("No profiles configured")
        return
    
    print("\n🔧 Available Crunch Profiles:")
    print("=" * 50)
    
    for name, config in profiles.items():
        network = "mainnet" if "mainnet" in config.get("url", "") else "devnet"
        coord_wallet = config.get("coordinatorWallet", "")
        multisig = config.get("multisigAddress", "")
        
        status = "🟢" if coord_wallet else "⚫"
        
        print(f"{status} {name:<15} ({network})")
        if coord_wallet:
            print(f"   Coordinator: {coord_wallet[:8]}...{coord_wallet[-8:]}")
        if multisig:
            print(f"   Multisig:    {multisig[:8]}...{multisig[-8:]}")
        print()

def show_profile(profile_name=None):
    """Show details of a specific profile or current active profile"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if profile_name:
        if profile_name not in profiles:
            print(f"❌ Profile '{profile_name}' not found")
            return
        
        config = profiles[profile_name]
        print(f"\n📋 Profile: {profile_name}")
        print("=" * 30)
        print(f"Network:     {'mainnet' if 'mainnet' in config.get('url', '') else 'devnet'}")
        print(f"URL:         {config.get('url', '')}")
        print(f"Wallet:      {config.get('wallet', '')}")
        if config.get('coordinatorWallet'):
            print(f"Coordinator: {config.get('coordinatorWallet')}")
        if config.get('multisigAddress'):
            print(f"Multisig:    {config.get('multisigAddress')}")
    else:
        print("Active profile functionality not implemented yet")

def generate_cli_command(profile_name):
    """Generate CLI command for a profile"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if profile_name not in profiles:
        print(f"❌ Profile '{profile_name}' not found")
        return
    
    config = profiles[profile_name]
    
    # Base command
    cmd_parts = ["npm", "run", "coordinator-cli", "--"]
    
    # Add URL
    if config.get("url"):
        cmd_parts.extend(["-u", config["url"]])
    
    # Add wallet
    if config.get("wallet") and config["wallet"] != "your keypair":
        cmd_parts.extend(["-w", config["wallet"]])
    
    # Add multisig
    if config.get("multisigAddress"):
        cmd_parts.extend(["-m", config["multisigAddress"]])
    
    # Add coordinator-specific command if available
    if config.get("coordinatorWallet"):
        cmd_parts.extend(["get", config["coordinatorWallet"]])
    else:
        cmd_parts.append("get")
    
    print(f"\n🚀 CLI Command for '{profile_name}':")
    print(" ".join(cmd_parts))
    return " ".join(cmd_parts)

def setup_coordinator():
    """Interactive setup for coordinator profile"""
    print("🔧 Coordinator Profile Setup")
    print("This would interactively create a coordinator profile")
    print("Implementation pending...")

def setup_cruncher():
    """Interactive setup for cruncher profile"""
    print("🔧 Cruncher Profile Setup") 
    print("This would interactively create a cruncher profile")
    print("Implementation pending...")

def switch_profile():
    """Interactive profile switching"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if not profiles:
        print("No profiles available to switch to")
        return
    
    print("\n🔄 Available profiles:")
    for i, name in enumerate(profiles.keys(), 1):
        print(f"{i}. {name}")
    
    try:
        choice = input("\nSelect profile (number or name): ").strip()
        
        # Try to parse as number
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(profiles):
                profile_name = list(profiles.keys())[choice_num - 1]
            else:
                print("Invalid selection")
                return
        except ValueError:
            # Treat as profile name
            if choice in profiles:
                profile_name = choice
            else:
                print(f"Profile '{choice}' not found")
                return
        
        print(f"\n✅ Switched to profile: {profile_name}")
        generate_cli_command(profile_name)
        
    except KeyboardInterrupt:
        print("\n❌ Cancelled")

def main():
    parser = argparse.ArgumentParser(description="CrunchDAO Identity Manager")
    parser.add_argument("command", nargs="?", choices=[
        "list", "show", "switch", "setup-coordinator", "setup-cruncher", "cmd"
    ], default="list", help="Command to execute")
    parser.add_argument("profile", nargs="?", help="Profile name (for show/cmd commands)")
    
    args = parser.parse_args()
    
    if args.command == "list":
        list_profiles()
    elif args.command == "show":
        show_profile(args.profile)
    elif args.command == "switch":
        switch_profile()
    elif args.command == "setup-coordinator":
        setup_coordinator()
    elif args.command == "setup-cruncher":
        setup_cruncher()
    elif args.command == "cmd":
        if args.profile:
            generate_cli_command(args.profile)
        else:
            print("Profile name required for cmd command")

if __name__ == "__main__":
    main()