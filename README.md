# CrunchDAO CLI Skill

## Profile Configuration

1. **Copy the example profiles file:**
   ```bash
   cp profiles.json.example profiles.json
   ```

2. **Edit `profiles.json` with your specific configuration:**
   - Replace placeholder values with your actual Helius API key / RPC URL
   - Replace `path/to/your/keypair.json` with actual paths to your Solana keypairs
   - Adjust coordinator wallets and multisig addresses as needed

3. **Test your setup:**
   ```bash
   crunch-cli --version
   ```

## Security Note

- **Never commit `profiles.json`** — it contains sensitive API keys and wallet paths
- The file is automatically ignored by git via `.gitignore`
- Each environment should have its own customized `profiles.json`

## Usage

Profiles are resolved automatically from `profiles.json` when you reference them by name. See `SKILL.md` for the full profile format and command mapping rules.
