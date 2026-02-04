---
name: crunch
description: "Complete guide for participating in CrunchDAO decentralized AI/ML markets. Use when users want to install CrunchDAO CLI tools, join modeling competitions as Crunchers, set up coordinator nodes for market creation, understand tokenomics and earn CRNCH tokens, submit ML models and compete for rewards, or navigate the decentralized intelligence marketplace ecosystem. Also handles identity management for Crunchers and Coordinators."
---

# CrunchDAO Participation

Complete guide for joining and succeeding in CrunchDAO's decentralized AI/ML marketplace where data scientists compete in modeling markets to earn CRNCH tokens and USDC rewards.

## Identity Management

Before starting, let's set up your CrunchDAO identity. This skill can store and manage identities for both Crunchers (participants) and Coordinators (market creators).

### Store Your Identity

Use the identity manager script to create and manage multiple profiles across networks:

```bash
# Create profiles for different networks/roles
python3 scripts/identity_manager.py setup-coordinator  # Create coordinator profile
python3 scripts/identity_manager.py setup-cruncher     # Create cruncher profile

# Quick role switching (recommended)
python3 scripts/crunch_role_switcher.py switch to role m-jeremy
python3 scripts/crunch_role_switcher.py switch to role devnet
python3 scripts/crunch_role_switcher.py switch to role m-admin

# Or shorter syntax
python3 scripts/crunch_role_switcher.py m-jeremy      # Quick switch
python3 scripts/crunch_role_switcher.py list          # List all profiles
python3 scripts/crunch_role_switcher.py overview      # Show coordinator overview

# Advanced management
python3 scripts/identity_manager.py list              # List all profiles
python3 scripts/identity_manager.py switch            # Interactive switching
python3 scripts/identity_manager.py show              # Show active profile details
```

**Quick Role Names (based on your data):**
- `devnet` - Main devnet coordinator
- `d-jeremy` - Jeremy's devnet coordinator  
- `m-admin` - Mainnet admin coordinator (multisig: 7K1Dx...)
- `m-birdgame` - Mainnet birdgame coordinator (multisig: jTXtb...)
- `m-synth` - Mainnet synth coordinator (multisig: DVs4N...)
- `m-jeremy` - Jeremy's mainnet coordinator (multisig: 3HCRMm...)

**Multi-Profile Support:**
- **Multiple identities** per network of Solana
- **Easy switching** between profiles
- **Network-aware commands** that auto-configure for your chosen network
- **Role separation** (coordinator vs cruncher profiles)

**Network Selection Guide:**
- **Ethereum**: Higher staking requirements, established ecosystem, gas fees
- **Solana**: Lower costs, faster transactions, different wallet format
- **Mixed Strategy**: Use different networks for different market sizes/strategies

**Working with Real Profiles:**
When you switch to a coordinator role, you get instant access to ready-to-use commands:
```bash
# Switch to Jeremy's mainnet coordinator
python3 scripts/crunch_role_switcher.py m-jeremy

# Output gives you ready-to-use commands:
# crunch-coordinator get --wallet 9LFUBTPZf4GuBJmzmJmRWUkhpn1biAFhm1UbMLcduuZ3 --url 'https://mainnet.helius-rpc.com/?api-key=...'
# crunch-coordinator --multisig 3HCRMmdVXK2iouzi22KoHHmfpEJun2Hzf8XoTWonPeUD --url 'https://mainnet.helius-rpc.com/?api-key=...'
```

## Installation & Environment Setup

### Option 1: Quick Setup (Recommended)
Run the setup script to install both CLI tools and create a project structure:

```bash
python3 scripts/setup_environment.py [project-name]
```

### Option 2: Manual Installation
Install the required CLI tools:

```bash
# For participants (Crunchers)
pip install crunch-cli

# For market creators (Coordinators) 
npm install -g @crunchdao/coordinator-cli
```

## Participation Workflow

### Step 1: Initial Authentication & Setup

**Get Your API Token:**
1. Visit [CrunchDAO Dashboard](https://crunchdao.com) and create account
2. Navigate to Profile → API Tokens
3. Generate new token and copy it

**Configure CLI:**
```bash
# Initialize workspace
crunch init

# Set your API token
crunch update-token
# Paste your token when prompted

# Test connection
crunch ping
```

### Step 2: Join Your First Competition

**Browse Available Markets:**
```bash
# List active competitions
crunch ping  # Shows available markets in response

# Download competition data and requirements
crunch download
```

**Understand the Market Structure:**
- **Emission Checkpoints:** Regular CRNCH token distributions
- **Leaderboard Rewards:** USDC payouts for top performers  
- **Cruncher Points:** Reputation score for future reward boosts
- **Coordinator Quality:** Check delegation health and emission splits

### Step 3: Develop Your Model

**Use the Development Cycle:**
```bash
# Start with quickstarter template (first time)
crunch quickstarter

# Develop your model locally
# - Load data from data/ directory
# - Create model in models/ directory  
# - Follow competition requirements

# Test locally before submitting
crunch test
```

**Example Model Structure:**
```python
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

def train_model(X_train, y_train):
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    return model

def predict(model, X_test):
    return model.predict(X_test)
```

### Step 4: Submit, Analyze & Optimize

**Initial Submission:**
```bash
# Final test
crunch test

# Submit to competition
crunch push

# Monitor results on dashboard
```

**Advanced Submission Optimization Workflow:**
Follow the comprehensive [submission-optimization.md](references/submission-optimization.md) guide for:

1. **Performance Analysis:** Deep dive into leaderboard metrics and model performance
2. **Feature Engineering:** Advanced techniques for feature creation and selection
3. **Model Architecture:** Ensemble methods and hyperparameter optimization
4. **Iterative Refinement:** Systematic testing and improvement cycles
5. **Submission Strategy:** Optimal timing and risk management

**Quick Optimization Loop:**
1. Analyze leaderboard performance and identify gaps
2. Implement targeted improvements (features, models, hyperparameters)
3. Validate improvements with robust cross-validation
4. Test locally (`crunch test`) with safety checks
5. Submit optimized version (`crunch push`)
6. Track performance metrics and repeat

### Step 5: Scale Your Participation

**Portfolio Strategy:**
- Join multiple competitions to diversify earnings
- Target coordinators with high Crunch Emission %
- Participate early in CLP Seasons for bonus emissions
- Build reputation through consistent performance

**Advanced Techniques:**
- Ensemble multiple models for better performance
- Leverage domain expertise for competitive advantage
- Optimize for both accuracy and inference speed
- Use privacy-preserving techniques compatible with TEEs

## For Coordinators (Market Creators)

### Prerequisites & Planning
- **Staking Requirements:** Minimum self-stake + delegated stake for activation
- **Technical Setup:** Node.js environment and protocol.crunchdao.com access  
- **Security:** Consider multisig wallet for large stake amounts and market operations
- **Market Design:** Clear problem definition and evaluation methodology
- **Legal Framework:** Competition rules and intellectual property policies

### Complete Coordinator Workflow

Follow the comprehensive [coordinator-workflow.md](references/coordinator-workflow.md) for the full market lifecycle:

**Stage 1: Market Planning & Configuration**
- Market parameter design and emission configuration
- Data preparation and evaluation framework setup
- Legal and compliance documentation

**Stage 2: Market Creation & Launch**
```bash
# Install and setup coordinator CLI
npm install -g @crunchdao/coordinator-cli
coordinator-cli init --profile production
coordinator-cli auth login --api-key YOUR_API_KEY

# Stake requirements
coordinator-cli stake self --amount 10000
coordinator-cli delegation monitor

# Create and configure market
coordinator-cli create-market --config market_config.json
coordinator-cli data upload --market-id MARKET_ID --file train_data.parquet
```

**Stage 3: Market Operations & Management**
```bash
# Monitor participants and submissions
coordinator-cli participants list --market-id MARKET_ID
coordinator-cli submissions monitor --market-id MARKET_ID --live

# Create and process checkpoints
coordinator-cli checkpoint create emission --market-id MARKET_ID
coordinator-cli checkpoint create coordinator --market-id MARKET_ID --prize-pool 50000

# Generate leaderboards
coordinator-cli leaderboard generate --market-id MARKET_ID --type final
```

### Enhanced Coordinator Use Cases

**Dashboard Overview Commands:**
```bash
# Get comprehensive overview of all your markets/crunches
coordinator-cli dashboard overview --wallet YOUR_WALLET

# Market performance analytics
coordinator-cli analytics markets --coordinator YOUR_WALLET --timeframe 30d

# Financial summary (stakes, rewards, emissions)
coordinator-cli financial summary --wallet YOUR_WALLET
```

**Market Creation Shortcuts:**
```bash
# Quick market creation with stored identity
coordinator-cli create \
  --template "standard-ml" \
  --duration 30d \
  --prize 10000 \
  --coordinator-wallet YOUR_STORED_WALLET \
  --auto-stake

# Clone existing successful market
coordinator-cli clone-market SUCCESSFUL_MARKET_ID \
  --modify-params prize_pool=15000,duration=45d
```

**Multi-Profile Operations:**
When profiles are stored in `crunch-profiles.json`, commands auto-populate based on active profile:
- **Network-specific** wallet addresses (Ethereum 0x... or Solana base58)
- **Multisig wallet** addresses (optional, for enhanced security operations)
- **Network-appropriate** default staking amounts (ETH/SOL units)
- **Profile-specific** market templates and preferences
- **Seamless switching** between different coordinator/cruncher identities

**Profile Examples:**
```bash
# Switch between different contexts
python3 scripts/identity_manager.py switch

# Available profiles might include:
#   🟢 mainnet-coord (coordinator, ethereum)
#   ⚫ solana-coord (coordinator, solana)
#   ⚫ test-cruncher (cruncher, ethereum)
```

**Stage 4: Advanced Operations**
- Dynamic emission optimization and fund management
- Risk management and slashing prevention
- Performance analytics and reporting

**Stage 5: Market Analytics & Community Engagement**
- Participant behavior analysis and model quality tracking
- Revenue analytics and community feedback collection
- Transparency reporting and insight sharing

**Stage 6: Market Closure & Lessons Learned**
- Final evaluation and reward distribution
- Performance review and future market planning

## Success Optimization

### Earning Strategies
1. **Consistent Participation:** Regular submissions maintain point accumulation
2. **Quality Focus:** Better models earn higher leaderboard positions
3. **Market Selection:** Choose coordinators with sustainable economics
4. **Timing:** Participate in CLP Seasons for amplified rewards

### Risk Management
- Verify coordinator delegation health before participating
- Avoid markets with suspicious participation metrics
- Diversify across multiple competitions
- Monitor coordinator slashing risk indicators

### Technical Excellence
- Use proper cross-validation to avoid overfitting
- Ensure reproducible and well-documented code
- Optimize for competition-specific metrics
- Handle edge cases and missing data gracefully

## Troubleshooting

### Common Issues
**Token/Auth Errors:**
```bash
crunch update-token  # Re-enter API token
crunch ping          # Test connection
```

**Submission Failures:**
```bash
crunch --debug test  # Debug local testing
crunch --debug push  # Debug submission process
```

**Environment Issues:**
- Ensure Python 3.8+ and Node.js are installed
- Check network connectivity and firewall settings
- Verify all dependencies are installed correctly

## Resources

### For Crunchers (Participants)
- **[participation-guide.md](references/participation-guide.md)** - Strategic guide for success, earning optimization, and community engagement
- **[submission-optimization.md](references/submission-optimization.md)** - Complete workflow for upload, analysis, and optimization of ML submissions
- **[commands-reference.md](references/commands-reference.md)** - Comprehensive CLI command documentation

### For Coordinators (Market Creators)  
- **[coordinator-workflow.md](references/coordinator-workflow.md)** - End-to-end market creation and management workflow
- **[commands-reference.md](references/commands-reference.md)** - CLI commands for both participant and coordinator tools

### Technical References
- **Protocol Documentation:** https://protocol.crunchdao.com
- **API Reference:** Available through coordinator CLI help commands

### Community Support
- **Discord:** Join CrunchDAO community channels
- **Documentation:** https://docs.crunchdao.com
- **GitHub:** https://github.com/crunchdao/crunch-cli
- **Dashboard:** https://crunchdao.com for competitions and leaderboards

## Key Reminders

- **Always test locally first:** `crunch test` before `crunch push`
- **Monitor coordinator health:** Check delegation and emission allocations
- **Build reputation gradually:** Consistent quality beats sporadic excellence
- **Stay updated:** Protocol upgrades may affect participation requirements
- **Respect deadlines:** Late submissions may not be accepted