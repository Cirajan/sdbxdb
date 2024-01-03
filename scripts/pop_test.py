#Script to do initial testing to learn how to populate the storeroom db with values from Dad's excel file

import csv
from catalogue.models import Item, Box, Category
from dateutil import parser
from datetime import date

def mk_int(s):
    s = s.strip()
    if any(substring in s for substring in ['?', '??', 'nd', 's', 'or']):
        s = None
    return int(s) if s else None

def mk_date(d):
    if d:
        r = d.split('/')
        return date(int(r[2]), int(r[1]), int(r[0]))
    else:
        return None

def run():
    raw_csv =open('sdb_full_data2.csv')
    # raw_csv =open('sdb_full_data.csv')
    reader = csv.reader(raw_csv)

    print('Script running')

    Item.objects.all().delete()
    Box.objects.all().delete()
    Category.objects.all().delete()
    # ItemCat.objects.all().delete()

    for row in reader:


        b, created = Box.objects.get_or_create(name = row[1])

        i = Item(last_moved=mk_date(row[0]),
                 box=b,
                 folder=row[2],
                 start_year=mk_int(row[3]),
                 end_year=mk_int(row[4]),
                 contents=row[6])
        i.save()



        cats = row[5].replace(', ','; ')
        cats = cats.split('; ')
        for c in cats:
            cat, created = Category.objects.get_or_create(name = c)
            i.category.add(cat)


        # ic = ItemCat(item = i, category = c)
        # ic.save()
