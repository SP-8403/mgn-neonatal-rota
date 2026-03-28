from datetime import datetime, timedelta
from collections import defaultdict
import calendar


# ---------------------------
# CONFIG
# ---------------------------

YEAR = 2026
MONTH = 4

mos = [
    {"name": "Shannon Harries",
     "leave": [(datetime(2026, 4, 23), datetime(2026, 5, 10))]},
    {"name": "Sanam Moothiram",
     "leave": []},
    {"name": "Juhi Maharaj",
     "leave": []}
]

interns = [
    {"name": "Jade Phillips",
     "leave": []},
    {"name": "Razeena Bhol",
     "leave": [(datetime(2026, 4, 13), datetime(2026, 4, 17))]},
    {"name": "Kelly Cleone Bettesworth",
     "leave": []},
    {"name": "Patisa Bunu",
     "leave": []},
    {"name": "Sarah Lapersonne",
     "leave": [(datetime(2026, 4, 1), datetime(2026, 4, 7))]}
]


# ---------------------------
# BUILD DATES
# ---------------------------

def build_dates(year, month):
    first = datetime(year, month, 1)
    last = datetime(year, month,
                    calendar.monthrange(year, month)[1])
    dates = []
    d = first
    while d <= last:
        dates.append(d)
        d += timedelta(days=1)
    return dates


dates = build_dates(YEAR, MONTH)

fridays = [d for d in dates if d.weekday() == 4]
saturdays = [d for d in dates if d.weekday() == 5]
sundays = [d for d in dates if d.weekday() == 6]

roster = {}


# ---------------------------
# HELPER
# ---------------------------

def available(person, date):
    for start, end in person["leave"]:
        if start <= date <= end:
            return False
    if (date - timedelta(days=1)) in roster and \
       roster[date - timedelta(days=1)] == person["name"]:
        return False
    return True


# ---------------------------
# 1️⃣ Assign Saturdays to MOs evenly
# ---------------------------

mo_counts = defaultdict(int)

for date in saturdays:
    sorted_mos = sorted(mos, key=lambda x: mo_counts[x["name"]])
    for mo in sorted_mos:
        if available(mo, date):
            roster[date] = mo["name"]
            mo_counts[mo["name"]] += 1
            break


# ---------------------------
# 2️⃣ Assign weekend intern exposures evenly
# ---------------------------

weekend_slots = fridays + sundays
weekend_slots.sort()

intern_counts = defaultdict(int)
target = len(weekend_slots) // len(interns)

for date in weekend_slots:
    sorted_interns = sorted(interns,
                            key=lambda x: intern_counts[x["name"]])
    for intern in sorted_interns:
        if intern_counts[intern["name"]] < target and \
           available(intern, date):
            roster[date] = intern["name"]
            intern_counts[intern["name"]] += 1
            break


# ---------------------------
# 3️⃣ Fill weekdays
# ---------------------------

weekday_dates = [d for d in dates
                 if d.weekday() not in [4, 5, 6]]

for date in weekday_dates:

    if date in roster:
        continue

    # Try interns first
    sorted_interns = sorted(interns,
                            key=lambda x: intern_counts[x["name"]])
    assigned = False

    for intern in sorted_interns:
        if intern_counts[intern["name"]] < target + 2 and \
           available(intern, date):
            roster[date] = intern["name"]
            intern_counts[intern["name"]] += 1
            assigned = True
            break

    if not assigned:
        for mo in mos:
            if available(mo, date):
                roster[date] = mo["name"]
                break


# ---------------------------
# PRINT
# ---------------------------

import json

# After roster is generated
output = {}

for date in sorted(roster.keys()):
    output[date.strftime("%Y-%m-%d")] = roster[date]

with open("roster.json", "w") as f:
    json.dump(output, f, indent=2)

print("Roster written to roster.json")
