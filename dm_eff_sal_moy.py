import csv
import datetime
import argparse

###########################
#        ETAPE 1
#   EFFECTIF MOYEN
###########################

def get_eff(line, data):
    effectif = line.get('effectifs_salaries_brut')
    secteur = line.get('grand_secteur_d_activite')
    region = line.get('region')
    date = line.get('dernier_jour_du_trimestre')
    year = date.split('/')[2]
    concat_identifier = f"{year};{region};{secteur}"
    if data.get(concat_identifier) is None:
        data[concat_identifier] = {
            "effectif": 0,
            "nb_trimestre": 0
        }
    if effectif is not None:
        data[concat_identifier]["effectif"] += int(effectif)
        data[concat_identifier]["nb_trimestre"] += 1
    return data

def calcul_moy_eff(data):
    final_data = []
    for identifier, eff in data.items():
        annee, region, secteur = identifier.split(";")
        final_data.append({
            "annee": annee,
            "region": region,
            "secteur": secteur,
            "effectif_moyen": eff["effectif"] / eff["nb_trimestre"]
        })
    return final_data

def calcul_eff_sal_evo_annee(data):
    final_data = []
    print(next(iter(data.values())))
    for identifier, eff in data.items():
        annee, region, secteur = identifier.split(";")

        effectif_moyen = eff["effectif"] / eff["nb_trimestre"]
        final_data.append({
            "annee": annee,
            "effectif_moyen": effectif_moyen,
            "region": region,
            "secteur": secteur
        })
    return final_data

def get_eff_by_year(line, data):
    effectif = line.get('effectifs_salaries_brut')
    date = line.get('dernier_jour_du_trimestre')
    year = date.split('/')[2]
    if data.get(year) is None:
        data[year] = {
            "effectif": 0,
            "nb_trimestre": 0
        }
    if effectif is not None:
        data[year]["effectif"] += int(effectif)
        data[year]["nb_trimestre"] += 1
    return data


############################################################################

###########################
#        ETAPE 2
#   SALAIRE MOYEN
###########################

def get_sal_by_year(line, data):
    salaire = line.get('total_salaire_brut')
    date = line.get('dernier_jour_du_trimestre')
    year = date.split('/')[2]
    if data.get(year) is None:
        data[year] = {
            "salaire": 0,
            "nb_trimestre": 0
        }
    if salaire is not None:
        data[year]["salaire"] += float(salaire.split("€")[0].replace(',', '.').replace(' ', ''))
        data[year]["nb_trimestre"] += 1
    return data

def calcul_moy_sal(data, final_data):
    for year, sal in data.items():
        for item in final_data:
            if item.get('annee') == year:
                item["salaire_moyen"] = sal["salaire"] / sal["nb_trimestre"]
    return final_data
###########################

def write_final_file(data):
    with open(f'dm_eff_sal_moy_annee.csv', 'w+', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys(), delimiter=";")
        writer.writeheader()
        for d in data:
            writer.writerow(d) 



def main():
    data = {}
    with open('clean_occitanie_nb_salarie.csv', mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for line in reader:
            data = get_eff(line, data)
    with open('clean_loire_nb_salarie.csv', mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for line in reader:
            data = get_eff(line, data)
    final_data = calcul_moy_eff(data)
    ###### ETAPE 1 FIN
    data = {}
    with open('clean_occitanie_salaire.csv', mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for line in reader:
            data = get_sal_by_year(line, data)
    with open('clean_loire_salaire.csv', mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for line in reader:
            data = get_sal_by_year(line, data)
    final_data = calcul_moy_sal(data, final_data)
    ##### ETAPE 2 FIN
    write_final_file(final_data)

if __name__ == '__main__':
    main()