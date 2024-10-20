import sqlite3
import random

# Connect to SQLite database (create if doesn't exist)
conn = sqlite3.connect('jurors.db')
cursor = conn.cursor()

# Create a juror table if it doesn't exist
cursor.execute('''CREATE TABLE IF NOT EXISTS jurors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    tokens INTEGER NOT NULL
                )''')
conn.commit()

# Function to add jurors to the database
def add_juror(name, tokens):
    cursor.execute("INSERT INTO jurors (name, tokens) VALUES (?, ?)", (name, tokens))
    conn.commit()

# Function to fetch all jurors from the database
def fetch_jurors():
    cursor.execute("SELECT * FROM jurors")
    return cursor.fetchall()

# Function to update a juror's tokens in the database
def update_juror_tokens(juror_id, tokens):
    cursor.execute("UPDATE jurors SET tokens = ? WHERE id = ?", (tokens, juror_id))
    conn.commit()

# Function to dynamically price tokens
def dynamic_token_pricing(base_price, demand):
    return base_price * (1 + demand / 100)

# Weighted random selection function for jurors
def select_jurors(num_jurors):
    jurors = fetch_jurors()
    weights = [juror[2] for juror in jurors]  # Tokens are in the third column
    selected_jurors = random.choices(jurors, weights=weights, k=num_jurors)
    return selected_jurors

# Function to distribute rewards and penalties after dispute resolution
def resolve_dispute(selected_jurors, votes):
    majority_vote = max(set(votes), key=votes.count)  # Find majority vote
    winners = [juror for juror, vote in zip(selected_jurors, votes) if vote == majority_vote]
    losers = [juror for juror in selected_jurors if juror not in winners]
    
    # Reward winners, penalize losers
    for loser in losers:
        new_tokens = loser[2] - 100  # Loser loses 100 tokens
        update_juror_tokens(loser[0], new_tokens)
    
    for winner in winners:
        new_tokens = winner[2] + 100 / len(winners)  # Winner gains part of 100 tokens
        update_juror_tokens(winner[0], new_tokens)
    
    return winners, losers

# Add sample jurors to the database (only run this once)
# add_juror("A", 2000)
# add_juror("B", 1500)
# add_juror("C", 2500)
# add_juror("D", 3000)
# add_juror("E", 1000)
# add_juror("F", 2000)

# Example of dynamic pricing based on demand
demand = 50
new_price = dynamic_token_pricing(1, demand)
print(f"New token price based on demand: {new_price}")

# Select 5 jurors for a dispute
selected_jurors = select_jurors(5)
print("\nSelected Jurors:")
for juror in selected_jurors:
    print(f"Juror {juror[1]} with {juror[2]} tokens")  # Name and tokens

# Simulate voting process (example votes)
votes = ["X", "X", "Y", "X", "X"]  # Random voting outcome
winners, losers = resolve_dispute(selected_jurors, votes)

print("\nWinners and Losers after dispute resolution:")
for winner in winners:
    print(f"Winner: Juror {winner[1]}, Tokens: {winner[2]}")
for loser in losers:
    print(f"Loser: Juror {loser[1]}, Tokens: {loser[2]}")
