
principle = 5000
interestRate = 1.0028
totalDays = 279
years = 4
biWeeklyDep = 50

# Calculating final balance
balance = principle*(interestRate**totalDays)
for i in range(52*years, 0, -2):
    balance += biWeeklyDep*(interestRate**(totalDays*i/(52*years)))

print(balance)
print(balance - principle - biWeeklyDep * 26*years)

# Calculating necessary weekly deposit
'''balance = 1000000 - principle*(interestRate**totalDays)
# weeklyDep = 0
for i in range(52*4, 0, -1):
    weeklyDep += interestRate**(totalDays*i/(52*4))
weeklyDep = balance/weeklyDep
print(weeklyDep)'''

'''balance = principle*(interestRate**totalDays)
print(balance)
for i in range(52*4, 0, -2):
    balance += weeklyDep*(interestRate**(totalDays*i/52))
    print(i/(52*4))

print(balance)'''
