import csv
import datetime
import argparse

def clean_date(item):
    date = item.get('dernier_jour_du_trimestre', None)
    if date:
        try:
            date_formatted = datetime.datetime.strptime(date, '%d/%m/%Y')
        except ValueError:
            date_formatted = datetime.datetime.strptime(date, '%Y/%m/%d')
        item['dernier_jour_du_trimestre'] = datetime.datetime.strftime(date_formatted, '%d/%m/%Y')
    return item

def clean_sexe(item):
    sexe = item.get('sexe_majoritaire', None)
    if sexe:
        sexe = sexe.lower()
        if sexe == 'masculin' or sexe == 'm' or sexe == 'homme':
            item['sexe_majoritaire'] = 'M'
        elif sexe == 'feminin' or sexe == 'f' or sexe == 'femme':
            item['sexe_majoritaire'] = 'F'
        else:
            item['sexe_majoritaire'] = 'NaN'
    return item

def clean_yes_or_no(item):
    response = item.get('a_jour', None)
    if response:
        response = response.lower()
        if response == 'oui' or response == 'o':
            item['a_jour'] = 'O'
        elif response == 'non' or response == 'n':
            item['a_jour'] = 'N'
        else:
            item['a_jour'] = 'NaN'
    return item

def dollar_to_euro(item):
    EURO_TO_DOLLAR = 0.73
    value = item.get('total_salaire_brut', None)
    if value:
        if '€' not in value:
            dollars = float(value)
            item['total_salaire_brut'] = f'{dollars * EURO_TO_DOLLAR} €'
    return item

def format_encodage(item):
    to_encode = item.get('grand_secteur_d_activite')
    to_encode = to_encode.encode('latin-1').decode('utf-8')
    item['grand_secteur_d_activite'] = to_encode
    return item

def open_clean_file(filepath):
    cleaned_data = []
    with open(filepath, mode='r') as infile:
        reader = csv.DictReader(infile, delimiter=';')
        for line in reader:
            line = clean_date(line)
            line = clean_sexe(line)
            line = dollar_to_euro(line)
            line = format_encodage(line)
            cleaned_data.append(line)
    return cleaned_data

def write_clean_file(data, filename):
    with open(f'clean_{filename}', 'w+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys())
        writer.writeheader()
        for d in data:
            writer.writerow(d) 

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="nom du fichier que vous souhaitez clean")
    args = parser.parse_args()
    if args.filename:
        data = open_clean_file(args.filename)
        write_clean_file(data, args.filename)
    else:
        print('Veuillez spécifier un nom de fichier')
