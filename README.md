# CrunchDAO Skill Setup

## Profile Configuration

1. **Copy the example profiles file:**
   ```bash
   cp profiles.json.example profiles.json
   ```

2. **Edit `profiles.json` with your specific configuration:**
   - Replace `YOUR_API_KEY` with your actual Helius API key
   - Replace `path/to/your/keypair.json` with actual paths to your Solana keypairs
   - Adjust coordinator wallets and multisig addresses as needed

3. **Test your profiles:**
   ```bash
   python3 scripts/identity_manager.py list
   python3 scripts/crunch_role_switcher.py m-jeremy
   ```

## Security Note

- **Never commit `profiles.json`** - it contains sensitive API keys and wallet paths
- The file is automatically ignored by git via `.gitignore`
- Each environment should have its own customized `profiles.json`

## Usage

```bash
# List all profiles
python3 scripts/identity_manager.py list

# Quick switch to a profile
python3 scripts/crunch_role_switcher.py m-jeremy

# Show coordinator overview
python3 scripts/crunch_role_switcher.py overview
```