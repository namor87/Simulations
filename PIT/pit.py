import math


tier1_rate_2019 = 0.1775
tier1_rate_2020 = 0.17

tier2_threshold = 85_528
tier2_rate = 0.32



def tax_of_tier(income, low_bound, rate, high_bound):
    return max(0, min(income, high_bound) - low_bound) * rate


def writeoff_2019(income):
    if income <= 8_000 :
        return 1_420
    elif income <= 13_000 :
        return 1_420 - round((income - 8_000) * 871.7/5_000.0, 2)
    elif income < 85_528 :
        return 548.30
    elif income < 127_000 :
        return 548.30 - round((income - 85_528) * 548.3/41_472.0, 2)
    else :
        return 0


def writeoff_2020(income):
    if income <= 8_000 :
        return 1_360
    elif income <= 13_000 :
        return 1_360 - (income - 8_000) * 834.88/5_000.0
    elif income < 85_528 :
        return 525.12
    elif income < 127_000 :
        return 525.12 - (income - 85_528) * 525.12/41_472.0
    else :
        return 0


def pit(income, tier1_rate, writeoff):
    t1_tax = tax_of_tier(income, 0, tier1_rate, tier2_threshold)
    t2_tax = tax_of_tier(income, tier2_threshold, tier2_rate, math.inf)
    writeoff_ammount = writeoff(income)
    total_tax = t1_tax + t2_tax - writeoff_ammount
    # print (t1_tax, t2_tax, writeoff_ammount, total_tax)
    return round(total_tax, 2)


def pit2019(income) :
    return pit(income, tier1_rate_2019, writeoff_2019)

def pit2020(income) :
    return pit(income, tier1_rate_2020, writeoff_2020)


my_income = 92_517


print('2019:', pit2019(my_income))

print('2020:', pit2020(my_income))

# 16_961.80

