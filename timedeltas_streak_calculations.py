import datetime


comp_date = datetime.datetime.today()
print(comp_date)

last_comp_date = datetime.datetime(2023, 4, 22, 10, 11, 2)
print(last_comp_date)

day_delta = (comp_date.day - last_comp_date.day)
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
    print("You can't complete the habit! Come back next week...")
else:
    print("complete streak")


comp_date = datetime.datetime.today()
print(comp_date)

last_comp_date = datetime.datetime(2023, 5, 1, 10, 11, 2)
print(last_comp_date)

month_delta = (comp_date.month - last_comp_date.month)
print(month_delta)

print(type(month_delta))

if month_delta > 1:
    print("break streak")
elif month_delta < 1:
    print("You can't complete the habit! Come back next month...")
else:
    print("complete streak")
