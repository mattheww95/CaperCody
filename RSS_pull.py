import feedparser
import re
from datetime import date
import time
import sys

# TODO: add this functionality at a later date
# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive

NewsFeed_1 = feedparser.parse("http://connect.biorxiv.org/biorxiv_xml.php?subject=all")
NewsFeed_2 = feedparser.parse("http://connect.medrxiv.org/medrxiv_xml.php?subject=all")

covid_searches = ["SARS", "Covid", "Covid-19", "COVID-19", "SARS-CoV-2", "Coronavirus", "coronavirus",
                  "WasteWater", "Wastewater", "wastewater", "waste", "SARS2"]

while True:
    f = open(f"log_{date.today()}.txt", "w")
    sys.stdout = f

    
    def get_paper_to_keep(newsfeed):
        papers_keep = {}
        for i2 in newsfeed.entries:
            for ii in covid_searches:
                pattern = "(" + ii + ")"
                pat = re.compile(pattern)
                # print(str(i))
                searched = re.search(pat, str(i2))
                if searched is None:
                    continue
                else:
                    papers_keep[i2['id']] = i2.items()
        return papers_keep


    biorxive = get_paper_to_keep(newsfeed=NewsFeed_1)
    medrxive = get_paper_to_keep(newsfeed=NewsFeed_2)

    # print(papers_to_keep)


    def main(papers_to_keep, bio_or_med):
        cols = []
        if bool(papers_to_keep):  # empty dictionaries evaluate to false in python
            get_cols = list(papers_to_keep.keys())[0]
            print(get_cols)
            for i in papers_to_keep[get_cols]:
                print(i[1])
                cols.append(i[0])
        else:
            with open(f"K:/RSS_scraper/{bio_or_med}_{date.today()}.txt", 'w', encoding='utf8') as date_check:
                date_check.write("No new papers!\n")

        if bio_or_med == "biorxive":
            name = str(bio_or_med) + "_" + str(date.today()) + ".txt"
            with open(f"{name}", 'w', encoding="utf8") as current_files:  # change to a when done
                current_files.write(f"RSS Information for {date.today()}, "
                                    f"a total of {len(papers_to_keep.keys())} papers were found\n\n\n")
                for i in papers_to_keep.keys():
                    paper = papers_to_keep[i]
                    # print(paper)
                    to_write = [i[1] for i in paper]
                    # print(type(to_write))
                    to_write2 = [str(i) for i in to_write]
                    current_files.write(f"*******{to_write2[1]}*******\n\n")
                    current_files.write(f"Title: {to_write2[1]} \n\nLink: {to_write2[4]},\n\n Summary: {to_write2[5]} \n\n"
                                        f"Authors: {to_write2[7]}\n\n -----Full RSS Information-----\n\n")
                    writing_out = ', '.join(to_write2)
                    writing_out2 = writing_out + '\n\n\n'
                    current_files.write(writing_out2)
                    current_files.write("\nNEXT ENTRY\n\n")

        elif bio_or_med == "medrxive":
            name = str(bio_or_med) + "_" + str(date.today()) + ".txt"
            with open(f"{name}", 'w', encoding="utf8") as current_files:  # change to a when done
                current_files.write(f"RSS Information for {date.today()}, "
                                    f"a total of {len(papers_to_keep.keys())} papers were found\n\n\n")
                for i in papers_to_keep.keys():
                    paper = papers_to_keep[i]
                    # print(paper)
                    to_write = [i[1] for i in paper]
                    # print(type(to_write))
                    to_write2 = [str(i) for i in to_write]
                    current_files.write(f"*******{to_write2[1]}*******\n\n")
                    current_files.write(f"Title: {to_write2[1]} \n\nLink: {to_write2[4]}\n\n Summary: {to_write2[5]} \n\n"
                                        f"Authors: {to_write2[7]}\n\n -----Full RSS Information-----\n\n")
                    writing_out = ', '.join(to_write2)
                    writing_out2 = writing_out + '\n\n\n'
                    current_files.write(writing_out2)
                    current_files.write("\nNEXT ENTRY\n\n")


    main(biorxive, bio_or_med="biorxive")
    main(medrxive, bio_or_med="medrxive")
    f.close()
    time.sleep(24.0 * 60.0 * 60.0)
