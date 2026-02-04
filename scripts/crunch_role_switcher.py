#!/usr/bin/env python3
"""
CrunchDAO Role Switcher - Quick Profile Switching
Quick switching between different coordinator/cruncher identities with ready-to-use CLI commands.
"""

import json
import sys
import os
from pathlib import Path

PROFILES_FILE = Path(__file__).parent.parent / "profiles.json"

def load_profiles():
    """Load profiles from profiles.json"""
    if not PROFILES_FILE.exists():
        return {"profiles": {}}
    
    with open(PROFILES_FILE, 'r') as f:
        return json.load(f)

def generate_cli_command(profile_name, command="get"):
    """Generate ready-to-use CLI command for a profile"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if profile_name not in profiles:
        return None
    
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
    
    # Add the command
    cmd_parts.append(command)
    
    # Add coordinator wallet for get commands
    if command == "get" and config.get("coordinatorWallet"):
        cmd_parts.append(config["coordinatorWallet"])
    
    return " ".join(cmd_parts)

def switch_to_role(profile_name):
    """Switch to a specific role and show ready commands"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if profile_name not in profiles:
        print(f"❌ Profile '{profile_name}' not found")
        available = ", ".join(profiles.keys())
        print(f"Available profiles: {available}")
        return
    
    config = profiles[profile_name]
    network = "mainnet" if "mainnet" in config.get("url", "") else "devnet"
    
    print(f"\n🔄 Switched to: {profile_name} ({network})")
    print("=" * 50)
    
    # Show profile details
    if config.get("coordinatorWallet"):
        print(f"📋 Coordinator: {config['coordinatorWallet']}")
    if config.get("multisigAddress"):
        print(f"🔐 Multisig: {config['multisigAddress']}")
    
    print(f"\n🚀 Ready-to-use commands:")
    
    # Generate common commands
    commands = [
        ("get", "Get coordinator details"),
        ("crunches list", "List all crunches"), 
        ("list", "List all coordinators"),
        ("get-config", "Get coordinator config")
    ]
    
    for cmd, desc in commands:
        cli_cmd = generate_cli_command(profile_name, cmd)
        if cli_cmd:
            print(f"\n# {desc}")
            print(cli_cmd)

def list_profiles():
    """List all available profiles with quick info"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    if not profiles:
        print("No profiles configured")
        return
    
    print("\n🎭 Quick Role Profiles:")
    print("=" * 40)
    
    for name, config in profiles.items():
        network = "mainnet" if "mainnet" in config.get("url", "") else "devnet"
        coord_wallet = config.get("coordinatorWallet", "")
        multisig = config.get("multisigAddress", "")
        
        # Status indicator
        if coord_wallet and multisig:
            status = "🟢🔐"  # Coordinator with multisig
        elif coord_wallet:
            status = "🟢"    # Coordinator only
        else:
            status = "⚫"     # Basic profile
        
        print(f"{status} {name:<15} ({network})")
        
        # Quick switch command
        print(f"   python3 scripts/crunch_role_switcher.py {name}")

def show_overview():
    """Show coordinator overview for current profiles"""
    data = load_profiles()
    profiles = data.get("profiles", {})
    
    print("\n📊 Coordinator Overview:")
    print("=" * 40)
    
    mainnet_coords = []
    devnet_coords = []
    
    for name, config in profiles.items():
        if config.get("coordinatorWallet"):
            network = "mainnet" if "mainnet" in config.get("url", "") else "devnet"
            if network == "mainnet":
                mainnet_coords.append((name, config))
            else:
                devnet_coords.append((name, config))
    
    if mainnet_coords:
        print("\n🌍 Mainnet Coordinators:")
        for name, config in mainnet_coords:
            wallet = config["coordinatorWallet"]
            multisig = config.get("multisigAddress", "")
            print(f"  • {name}: {wallet[:8]}...{wallet[-8:]}")
            if multisig:
                print(f"    Multisig: {multisig[:8]}...{multisig[-8:]}")
    
    if devnet_coords:
        print("\n🧪 Devnet Coordinators:")
        for name, config in devnet_coords:
            wallet = config["coordinatorWallet"]
            print(f"  • {name}: {wallet[:8]}...{wallet[-8:]}")

def main():
    if len(sys.argv) < 2:
        list_profiles()
        return
    
    command = sys.argv[1].lower()
    
    # Handle "switch to role" syntax
    if command == "switch" and len(sys.argv) >= 4 and sys.argv[2].lower() == "to" and sys.argv[3].lower() == "role":
        if len(sys.argv) >= 5:
            profile_name = sys.argv[4]
            switch_to_role(profile_name)
        else:
            print("Usage: python3 crunch_role_switcher.py switch to role <profile-name>")
        return
    
    # Handle direct commands
    if command == "list":
        list_profiles()
    elif command == "overview":
        show_overview()
    elif command in ["help", "--help", "-h"]:
        print("\n🎭 CrunchDAO Role Switcher")
        print("Quick switching between coordinator profiles")
        print("\nUsage:")
        print("  python3 crunch_role_switcher.py <profile-name>     # Quick switch")
        print("  python3 crunch_role_switcher.py list              # List profiles")
        print("  python3 crunch_role_switcher.py overview          # Show coordinator overview")
        print("  python3 crunch_role_switcher.py switch to role <name>  # Full syntax")
        print("\nAvailable profiles:")
        data = load_profiles()
        profiles = data.get("profiles", {})
        for name in profiles.keys():
            print(f"  - {name}")
    else:
        # Treat as profile name for quick switch
        switch_to_role(command)

if __name__ == "__main__":
    main()