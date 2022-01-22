import pefile
import requests
import bs4
import argparse
import sys
from utils.colors import *
from datetime import datetime

parser = argparse.ArgumentParser(description="Read information from MalAPI.io for WinAPI information.")
parser.add_argument("--pe", "-p",
                    help="Specify a PE to read. The WinAPI will be checked against MalAPI and information will be "
                         "printed about the API if the information is present.")
parser.add_argument("--look", "-l", help="Look up an API by name and print all information.")
parser.add_argument("--verbose", "-v", help="Increase verbosity of output", action="store_true")
parser.add_argument("--report", "-r", help="Write report to the reports directory", action="store_true")

args = parser.parse_args()
if len(sys.argv) == 1:
    parser.print_help()
    parser.exit()

# Globals
current_time = datetime.now()

if args.report:
    class Logger(object):
        def __init__(self):
            self.terminal = sys.stdout
            self.log = open("reports/" + str(datetime.now().strftime("%Y-%m-%d-%H-%M")) + "_report.log", "a")

        def write(self, message):
            self.terminal.write(message)
            self.log.write(message)

        def flush(self):
            pass


    sys.stdout = Logger()


def check_api(api):
    sus_api = {}
    APItoCheck = api
    if args.verbose:
        print(info + APItoCheck)
    APICheck = requests.get("https://malapi.io/winapi/" + APItoCheck)
    APICheck.raise_for_status()
    APISoup = bs4.BeautifulSoup(APICheck.text, 'html.parser')
    details = APISoup.select('.detail-container .content')
    ApiInfo = details[1].getText().lstrip().rstrip()
    if ApiInfo != "":
        if args.verbose:
            print(important + "Hit: " + api)
        else:
            print("Hit: " + api)
        sus_api[api] = ApiInfo
        return sus_api
    else:
        return


def api_lookup():
    mal_apis = {}
    # Lookup an individual API by name
    if args.look:
        try:
            lookup = check_api(args.look)
            mal_apis.update(lookup)
        except Exception as e:
            print(printError + "No result")
            print(printError + "Full error: {}".format(str(e)))
            quit()
    # Read read import table from PE and print information when it is found.
    elif args.pe:
        try:
            pe = pefile.PE(args.pe, fast_load=True)
        except Exception as e:
            print(printError + "Unable to parse file. May not be a PE.")
            print(printError + "Full error: {}".format(str(e)))
            quit()
        pe.parse_data_directories()
        try:
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                if args.verbose:
                    print("----", entry.dll.decode("utf-8"), "----")
                for imp in entry.imports:
                    try:
                        imp_name = imp.name.decode("utf-8").strip()

                        # There's, like, probably a better way to do this but ¯\_(ツ)_/¯
                        if imp_name.endswith("W"):
                            if args.verbose:
                                print("[*] Unicode API detected: " + imp_name)
                            ansi_imp = (imp_name[:-1] + "A")
                            if args.verbose:
                                print("[*] Checking ANSI variant: {}".format(ansi_imp))
                            ansi_mal = check_api(ansi_imp)
                            mal_apis.update(ansi_mal)
                        if imp_name.endswith("A"):
                            if args.verbose:
                                print("[*] ANSI API detected: " + imp_name)
                            unicode_imp = (imp_name[:-1] + "W")
                            if args.verbose:
                                print("[*] Checking Unicode variant: {}".format(unicode_imp))
                            unicode_mal = check_api(unicode_imp)
                            mal_apis.update(unicode_mal)
                        malicious = check_api(imp_name)
                        mal_apis.update(malicious)
                    except:
                        continue
        except KeyboardInterrupt:
            pass
    return mal_apis


def print_results(mal_results):
    if args.verbose:
        print("")
        print("-" * 15 + "RESULTS" + "-" * 15)
        print("")

        print("Time: " + str(current_time))
    if args.pe:
        print("Sample: " + args.pe + "\n")

    for x in mal_results.keys():
        print(str(x) + "\n    \\\\---> " + str(mal_results[x]))

    print("\n\nIf a WINAPI listed here was used maliciously, but no description was given, consider contributing "
          "information to https://malapi.io.\n Thank you for using MalAPIReader!\n Squiblydoo | HuskyHacks")


def main():
    print("-" * 15 + "MalAPIReader.py" + "-" * 15)
    if args.verbose:
        print(info + "Current time: {}".format(current_time))
        print(info + "Sample name: {}".format(args.pe))
    mal_api_results = api_lookup()
    print_results(mal_api_results)


if __name__ == "__main__":
    main()
