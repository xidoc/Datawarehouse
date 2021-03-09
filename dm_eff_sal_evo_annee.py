import csv
import datetime
import argparse

def get_eff_per_year(line, data):
    effectif = line.get('effectif_moyen')
    year = line.get('annee')
    if data.get(year) is None:
        data[year] = {
            "year_prev": int(year) - 1,
            "effectif_moyen": effectif,
        }
    return data

def get_evo_effectif(data):
    final_data = []
    for year in data.keys():
        previous_year = str(int(year) - 1)
        if data.get(previous_year, None) is not None:
            data[year]["effectif_moyen_prev"] = data[previous_year].get("effectif_moyen")
            data[year]["evo_effectif"] = ((float(data[year]["effectif_moyen"]) - float(data[year]["effectif_moyen_prev"])) / float(data[year]["effectif_moyen_prev"])) * 100
        else:
            data[year]["effectif_moyen_prev"] = ""
        del data[year]["year_prev"]
        final_data.append({"annee": year, **data[year]})
    return final_data


###########################


def get_sal_per_year(line, data):
    salaire = line.get('salaire_moyen')
    year = line.get('annee')
    if data.get(year) is None:
        data[year] = {
            "year_prev": int(year) - 1,
            "salaire_moyen": salaire,
        }
    return data

def get_evo_salaire(data, final_data):
    for year in data.keys():
        for item in final_data:
            if year == item.get("annee"):
                previous_year = str(int(year) - 1)                
                if data.get(previous_year, None) is not None:
                    item["salaire_moyen_prev"] = data[previous_year].get("salaire_moyen")
                    item["evo_salaire"] = ((float(data[year]["salaire_moyen"]) - float(item["salaire_moyen_prev"])) / float(item["salaire_moyen_prev"])) * 100
                else:
                    item["salaire_moyen_prev"] = ""
    return final_data

########################

def write_final_file(data):
    with open(f'dm_eff_sal_evo.csv', 'w+', encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=data[0].keys(), delimiter=";")
        writer.writeheader()
        for d in data:
            writer.writerow(d) 


def main():
    data_eff = {}
    data_sal = {}
    with open('dm_eff_sal_moy_annee.csv', mode="r", encoding="utf-8") as infile:
        reader = csv.DictReader(infile, delimiter=";")
        for line in reader:
            data_eff = get_eff_per_year(line, data_eff)
            data_sal = get_sal_per_year(line, data_sal)     
    final_data = get_evo_effectif(data_eff)
    final_data = get_evo_salaire(data_sal, final_data)
    write_final_file(final_data)


if __name__ == '__main__':
    main()