from web3 import Web3
import json

# Connecting to Ganache (HTTP connection to the local blockchain)
ganache_url = "http://127.0.0.1:7545"
web3 = Web3(Web3.HTTPProvider(ganache_url))

# Check connection
if not web3.isConnected():
    raise Exception("Could not connect to Ganache")

# Set the default account (this is an account from Ganache)
web3.eth.defaultAccount = web3.eth.accounts[0]

# Load ABI and contract addresses
GRULL_TOKEN_ABI = json.loads('''''')  # Replace with GRULL Token ABI (JSON)
GRULL_TOKEN_ADDRESS = "0xYourGRULLTokenContractAddress"  # Replace with actual contract address

ARBITRATION_SYSTEM_ABI = json.loads('[...]')  # Replace with ArbitrationSystem ABI (JSON)
ARBITRATION_SYSTEM_ADDRESS = "0xYourArbitrationSystemContractAddress"  # Replace with actual contract address

# Load GRULL Token contract
grull_token = web3.eth.contract(address=GRULL_TOKEN_ADDRESS, abi=GRULL_TOKEN_ABI)

# Load ArbitrationSystem contract
arbitration_system = web3.eth.contract(address=ARBITRATION_SYSTEM_ADDRESS, abi=ARBITRATION_SYSTEM_ABI)

# Helper function to check account balances (in GRULL tokens)
def check_grull_balance(account):
    balance = grull_token.functions.balanceOf(account).call()
    print(f"GRULL balance of {account}: {web3.fromWei(balance, 'ether')} GRULL")
    return balance

# Function to stake GRULL tokens
def stake_tokens(account, amount):
    # Convert the amount to Wei (assuming GRULL token has 18 decimals)
    wei_amount = web3.toWei(amount, 'ether')
    
    # Approve the arbitration system to spend user's GRULL tokens
    approval_tx = grull_token.functions.approve(ARBITRATION_SYSTEM_ADDRESS, wei_amount).transact({'from': account})
    web3.eth.waitForTransactionReceipt(approval_tx)
    
    print(f"Approved {amount} GRULL for staking by {account}")

    # Stake tokens in the Arbitration System
    stake_tx = arbitration_system.functions.stakeTokens(wei_amount).transact({'from': account})
    web3.eth.waitForTransactionReceipt(stake_tx)
    
    print(f"Staked {amount} GRULL by {account}")

# Function to cast a vote on a dispute
def cast_vote(account, dispute_id, vote_for_plaintiff):
    # Cast the vote (True = vote for plaintiff, False = vote for defendant)
    vote_tx = arbitration_system.functions.castVote(dispute_id, vote_for_plaintiff).transact({'from': account})
    web3.eth.waitForTransactionReceipt(vote_tx)
    
    print(f"Vote cast by {account} for dispute {dispute_id}: {'Plaintiff' if vote_for_plaintiff else 'Defendant'}")

# Function to resolve the dispute and distribute rewards/penalties
def resolve_dispute(dispute_id):
    # Resolve the dispute and finalize the voting
    resolve_tx = arbitration_system.functions.resolveDispute(dispute_id).transact()
    web3.eth.waitForTransactionReceipt(resolve_tx)
    
    print(f"Dispute {dispute_id} resolved")

# Sample execution flow
if __name__ == "__main__":
    # Example accounts from Ganache (replace with your addresses)
    account1 = web3.eth.accounts[0]
    account2 = web3.eth.accounts[1]

    # 1. Check GRULL balance
    check_grull_balance(account1)
    
    # 2. Stake tokens (Example: Stake 50 GRULL tokens)
    stake_tokens(account1, 50)

    # 3. Cast a vote (For example, vote for the plaintiff in dispute ID 1)
    dispute_id = 1  # Assume this dispute ID exists in the Arbitration System
    cast_vote(account1, dispute_id, vote_for_plaintiff=True)

    # 4. Resolve the dispute and distribute rewards/penalties
    resolve_dispute(dispute_id)
