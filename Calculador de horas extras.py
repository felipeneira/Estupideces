# =============================================================================
# Sin def
# =============================================================================
hrs = "45"
rph = "10.50"
h = float(hrs)
r = float(rph)
if h<=40:
    pay = h*r
    print(pay)
else:
    pay1 = 40*r
    h = h-40
    r = r*1.5
    pay2 = h*r
    pay = pay1+pay2
    print(pay)
    
# =============================================================================
# Con def    
# =============================================================================
    
def computepay(h, r):
    h=float(h)
    r=float(r)
    if h<=40:
        pay = h*r
        print(pay)
    else:
        pay1 = 40*r
        h = h-40
        r = r*1.5
        pay2 = h*r
        pay = pay1+pay2
    return pay

hrs = input("Enter Hours:")
rph = input("Enter rate per hour:")
p = computepay(hrs, rph)
print("Pay", p)