import sys
import json
import numpy as np
import multiprocessing as multi
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import unicodedata
import string


def perform_extraction(page_ranges):
    """Extracts data, does preprocessing, writes the data"""
    # do requests and BeautifulSoup
    for url in page_ranges:
        uClient = urlopen(url)
        page = uClient.read()
        page_soup = soup(page, "html.parser")
        uClient.close()

        modpack_containers = page_soup.findAll('li', {"class": "project-list-item"})
        for modpack in modpack_containers:
            catagories = []
            avatarurl = modpack.div.a.img['src']
            packurl = modpack.div.a['href']
            packname = modpack.find('div', {"class": "name-wrapper"}).a.text
            author = modpack.find('span', {"class": "byline"}).a.text
            authorurl = modpack.find('span', {"class": "byline"}).a['href']
            downloads = modpack.find('p', {"class": "e-download-count"}).text
            creation_date = modpack.find('p', {"class": "e-update-date"}).abbr.text
            description = modpack.find('div', {"class": "description"}).p.text
            catagories_raw = modpack.findAll('div', {"class": "category-icons"})  # .a['title']
            versions = getversioninfo(packurl)  # "projects/sevtech-ages"

            for catagory in catagories_raw:
                catagories.append(catagory.a['title'])
            # preprocess the data
            file_name = "json/" + clean_filename(packname) + '.json'
            # write into current process file

            data = {
                "Packname": packname,
                "Avatar URL": avatarurl,
                "Author": author,
                "Author URL": authorurl,
                "Total Downloads": downloads,
                "First Creation Date": creation_date,
                "Description": description,
                "Catagories": catagories,
                "Versions": versions
            }
            with open(file_name, 'w') as outfile:
                json.dump(data, outfile)


def getversioninfo(pack):
    version_info = {}
    uClient = urlopen("https://minecraft.curseforge.com/" + pack + "/files")
    page = uClient.read()
    page_soup = soup(page, "html.parser")
    uClient.close()
    version_containers = page_soup.findAll('tr', {"class": "project-file-list-item"})

    for version in version_containers:
        versionname = version.find('td', {"class": "project-file-name"}).div.div.a.text
        version_link = version.find('td', {"class": "project-file-name"}).div.div.a["href"]
        versionsize = version.find('td', {"class": "project-file-size"}).text.strip()
        uploaded_date = version.find('td', {"class": "project-file-date-uploaded"}).abbr.text
        game_version = version.find('td', {"class": "project-file-game-version"}).span.text
        dowloads = version.find('td', {"class": "project-file-downloads"}).text.strip()
        download_links = getdownloadlinks(version_link)

        version_info[versionname] = {
            "Version": versionname,
            "Size": versionsize,
            "Upload Date": uploaded_date,
            "Minecraft Version": game_version,
            "DownloadCount": dowloads,
            "Download Links": download_links
        }

    return version_info


def getdownloadlinks(version):
    uClient = urlopen("https://minecraft.curseforge.com/" + version)
    page = uClient.read()
    page_soup = soup(page, "html.parser")
    uClient.close()

    changelog = page_soup.find('section', {"class": {"details-changelog"}}).div.text

    additonal_files = page_soup.findAll('tr', {"class": "project-file-list-item"})

    if additonal_files:
        for additional_file in additonal_files:
            additional_downloads = additional_file.findAll('div', {"class": "project-file-name-container"})
            additional_download_links = {}
            for additional_download in additional_downloads:
                dllink = additional_download.a['href']
                title = additional_download.a.text

                additional_download_links = {
                    "name": title,
                    "Download Link": dllink
                }

            download_links = {
                "client_download": "https://minecraft.curseforge.com" + version + "/download",
                "additional_files": additional_download_links,
                "Changelog": changelog.strip()
            }
    else:
        download_links = {
            "client_download": "https://minecraft.curseforge.com/" + version + "/download",
            "Changelog": changelog.strip()
        }
    return download_links


valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)


def clean_filename(filename, whitelist=valid_filename_chars, replace=' '):
    # replace spaces
    for r in replace:
        filename = filename.replace(r, '_')

    # keep only valid ascii chars
    cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()

    # keep only whitelisted chars
    return ''.join(c for c in cleaned_filename if c in whitelist)


def main():
    def chunks(n, page_list):
        """Splits the list into n chunks"""
        return np.array_split(page_list, n)

    cpus = multi.cpu_count()
    workers = []
    # 31 pages should be more then enough to get most popular packs
    page_list = ['https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=1',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=2',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=3',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=4',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=5',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=6',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=7',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=8',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=9',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=10',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=11',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=12',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=13',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=14',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=15',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=16',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=17',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=18',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=19',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=20',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=21',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=22',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=23',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=24',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=25',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=26',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=27',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=28',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=29',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=30',
                 'https://www.curseforge.com/minecraft/modpacks?filter-sort=4&page=31']

    page_bins = chunks(cpus, page_list)

    for cpu in range(cpus):
        sys.stdout.write("CPU " + str(cpu) + "\n")
        # Process that will send corresponding list of pages
        # to the function perform_extraction
        worker = multi.Process(name=str(cpu),
                               target=perform_extraction,
                               args=(page_bins[cpu],))
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()


if __name__ == "__main__":
    main()