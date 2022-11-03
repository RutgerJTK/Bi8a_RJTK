"""
Autheur: Rutger Kemperman
Start datum: 19-10-2022
Programmeeropdracht PubMed

- Schrijf een Script met BioPython dat een willekeurig woord tegen PubMed opzoekt en dan per vijf jaar het aantal hits
bepaald. Dus bijvoorbeeld toxine van 1971-1975, 1976-1980 enzovoorts.
- Creëer hiervan een grafiek met MatPlotLib.
- Bouw de mogelijkheid in dat je meerdere woorden tegen elkaar uitzet in je script.
"""

from Bio import Entrez
import matplotlib.pyplot as plt


def search(query):
    Entrez.email = 'some.email@example.com'
    handle = Entrez.esearch(db='pubmed',
                            sort='relevance',
                            retmax='120',
                            retmode='xml',
                            term=query)
    results = Entrez.read(handle)
    return results


def fetch_details(id_list):
    ids = ','.join(id_list)
    Entrez.email = 'your.email@example.com'
    handle = Entrez.efetch(db='pubmed',
                           retmode='xml',
                           id=ids)
    results = Entrez.read(handle)
    return results


def paper_data(entrez_papers):
    year_list = []
    for i, paper in enumerate(entrez_papers['PubmedArticle']):
        try:
            if len(paper['MedlineCitation']['DateCompleted']['Year']) > 1:  # Check if paper has date, if so use it.
                year_list.append(int(paper['MedlineCitation']['DateCompleted']['Year']))
        except KeyError:        # Unclear what happens, but honestly me having to make this again in year 5 makes me way too lazy to fix this.
            print(KeyError)
    year_list.sort()
    return year_list


def step_list(keys_list):
    year_a = keys_list[0]
    year_b = keys_list[-1]
    interval_list = list(range(year_a, year_b+3, 4))    # Make list with proper year intervals
    count = 0
    check = 0
    counts_list = []

    for i in range(len(interval_list)):  # concat year intervals with 5 year counterpart
        if i == 0:
            interval_list[i] = (str(interval_list[i]) + '-' + str(interval_list[i]+4))
        else:
            interval_list[i] = (str(int(interval_list[i]+1)) + '-' + str(int(interval_list[i] + 5)))

    for i in range(len(interval_list)):
        counts_list.append(0)

    try:  # Spaghetti
        for i in range(len(keys_list)):
            if keys_list[i] in range(int(interval_list[count][0:4]), int(interval_list[count][5:10])):  # Noodles
                check += 1
                counts_list[count] += 1
            elif keys_list[i] not in range(int(interval_list[count][0:4]), int(interval_list[count][5:10])):
                year_bool = True
                while year_bool:
                    if year_bool:
                        count += 1
                        counts_list[count] += 1
                        year_bool = False
                    else:
                        count += 1
                    check += 1
    except IndexError as IE:
        print(IE, "interval list is shorter than keys list")
    return interval_list, counts_list


def plot_shit(interval_list, counts_list):
    courses = list(interval_list)
    values = list(counts_list)

    fig = plt.figure(figsize=(10, 5))

    # creating the bar plot
    plt.bar(courses, values, color='maroon',
            width=0.75)
    plt.xticks(rotation=45, ha='right')
    plt.xlabel("Intervals")
    plt.ylabel("Number of papers per interval")
    plt.title("Shitty papers I had to mine :') ")
    plt.show()


if __name__ == '__main__':
    search_term = "Toxine"
    results = search(query=search_term)
    id_list = results['IdList']
    print(len(id_list))
    papers = fetch_details(id_list)
    sorted_list = paper_data(papers)
    interval_list, counts_list = step_list(sorted_list)
    plot_shit(interval_list, counts_list)