principle = 5000 # Initial amount invested
interestRate = 1.0028 # Daily ROI
totalDays = 279 # Stock market trading days per year
years = 4 # How many years the simulation takes into account
biWeeklyDep = 50 # Amount deposited biweekly

# Calculating final balance
balance = principle*(interestRate**(totalDays*years))
for i in range(52*years, 0, -2):
    balance += biWeeklyDep*(interestRate**(totalDays*i/52))

print(balance) # Final account balance
print(balance - principle - biWeeklyDep * 26 * years) # Actual investment profit (Subtracting the amount invested)
