import datetime


comp_date = datetime.date.today()
print(comp_date)

last_comp_date = datetime.date(2023, 4, 22)
print(last_comp_date)

day_delta = (comp_date - last_comp_date).days
print(day_delta)

print(type(day_delta))

if day_delta > 1:
    print("break streak")
elif day_delta < 1:
    print("You can't complete the habit! Come back tomorrow...")
else:
    print("complete streak")
    

comp_date = datetime.date.today()
print(comp_date.isocalendar())
print(comp_date.isocalendar()[1])

last_comp_date = datetime.date(2023, 4, 9)
print(last_comp_date.isocalendar())
print(last_comp_date.isocalendar()[1])

week_delta = (comp_date.isocalendar()[1] - last_comp_date.isocalendar()[1])
print(week_delta)

if week_delta > 1:
    print("break streak")
elif week_delta < 1:
    print("You can't complete the habit! Come back tomorrow...")
else:
    print("complete streak")
