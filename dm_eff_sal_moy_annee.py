import csv
import argparse

def get_date(item):
    value = item.get('annee', None)
    if value:
        return value

def get_trimestre(item):
    value = item.get('trimestre', None)
    if value:
        return value

def get_effectifs_salaries(item):
    value = item.get('effectifs_salaries', None)
    if value:
        return value

def open_clean_file(filepath):
    cleaned_data = []
    with open(filepath, mode='r', encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter=',')
        table = {}
        for line in reader:
            date = get_date(line)
            if not date in table:
              table[date] = {}
            trimestre = get_trimestre(line)
            if not trimestre in table[date]:                
               table[date][trimestre] = {0}
            effectifs_salaries = get_effectifs_salaries(line)
            table[date][trimestre] += effectifs_salaries        

        
    print(table)
    return cleaned_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="nom du fichier que vous souhaitez clean")
    args = parser.parse_args()
    if args.filename:
        data = open_clean_file(args.filename)
    else:
        print('Veuillez spécifier un nom de fichier')