from bs4 import BeautifulSoup
from requests import post
import numpy as np


def fetch_data(username):

    # Construct POST request to get information for individual username
    data = {'user1': username}
    r = post("https://secure.runescape.com/m=hiscore_oldschool/hiscorepersonal", data=data)
    html_file = r.content  # retrieve html page after post request

    # Open html file in python
    soup = BeautifulSoup(html_file, 'lxml')

    # Filter html file to only include hi-score table
    table = soup.find('div', class_='hiscoresHiddenBG')

    # Skills we search html for (Same dict used to pass information to webpage)
    skillpet_categories = {'Woodcutting': 0, 'Fishing': 0, 'Mining': 0, 'Agility': 0, 'Thieving': 0, 'Farming': 0,
                           'Runecraft': 0, 'Hunter': 0}

    # Bosses we search html for (ordered list)
    bosspet_categories2 = ['master', 'Abyssal Sire', 'Alchemical Hydra', 'Callisto', 'Cerberus', 'Chambers of Xeric',
                           'Chambers of Xeric: Challenge Mode', 'Chaos Elemental', 'Chaos Fanatic', 'Commander Zilyana',
                           'Corporeal Beast', 'Dagannoth Prime', 'Dagannoth Rex', 'Dagannoth Supreme',
                           'General Graardor', 'Giant Mole', 'Grotesque Guardians', 'Kalphite Queen',
                           'King Black Dragon', 'Kraken', 'Kree', "Tsutsaroth", 'Nightmare', 'Sarachnis', 'Scorpia',
                           'Skotizo', 'The Gauntlet', 'The Corrupted Gauntlet', 'Theatre of Blood',
                           'Thermonuclear Smoke Devil', 'Zuk', 'Jad', 'Venenatis', 'Vet', 'Vorkath', 'Wintertodt',
                           'Zalcano', 'Zulrah']

    bosspet_kc = {}  # Dict used to pass found information to web-page
    i = 0  # Index i - Used to make sure we search for bosses in specified order (as some names duplicate in others)

    for section in table.find_all('tr'):  # Each skill/boss has its own 'tr' tag
        for skill in skillpet_categories.keys():
            if skill in section.text and 'Bounty' not in section.text:
                skillpet_categories[skill] = int(section.findChildren()[6].text.strip().replace(',', ''))
        for boss in bosspet_categories2[i:]:
            if boss in section.text:
                bosspet_kc[boss.replace(" ", "_").replace(":", "")] = int(section.findChildren()[5].text.strip().replace(',', ''))
                i += 1

    return skillpet_categories, bosspet_kc  # Returns 2 dictionarys: skills xp, boss kc


def handle_calc(form):
    '''
    Following dictionary explained:

    Skill pet calculations:
    Requires:
        XP gained (taken from form)
        List of lists in form of:
            [[X1, Y1, Z1], [X2, Y2, Z2]...]
            X = (Skill level when you STOP using method)+1 e.g. 78 (for crafting at ouriana alter)
            Y = XP each action provides e.g. 25 (for cutting logs)
            Z = Base-chance for activity e.g. 782999 (for crafting soul runes)
            Lists must also be in level order e.g. shrimps before sharks
        Lists represent the following activity orders:
            WC stages = Tree -> Oak -> Willow -> Teak
            Fish stages (xp averaged for all stages as multi fish possible) Shrimp/Anch -> trout/salmon -> Barb fishing
            Mining stages = Tin/Copper -> Iron -> MotherLode mine (Xp field is averaged (60 base + 17 avg))
            Agil stages = Gnome -> Varrock -> Canifis -> Wilderness -> Seers -> Rellekka -> Ardougne
            Thieving stages = Man -> Cake stalls -> Fruit stalls -> Knights of Ardougne
            Farming stages = Allotments (xp avg) -> Oak -> Apple -> Curry -> Pineapple -> Papaya -> Palm
            RC stages = ZMI -> Blood -> Soul
            Hunt stages = Grey -> Red

    Boss pet calculations:
        Requires:
            KC (Taken from form)
            Pet drop rate (Taken from the following dictionary)
        Boss Assumptinos:
            Jad kills are ON task
            Zuk kills are OFF task
            Nightmare - You get MVP 1/5 times
            ToB - Assumes optimal performance
            CoX - Assumes 32k points per trip
    '''

    rate_dict = {'Runecraft': [[78, 13, 1487213], [91, 24.425, 804984], [120, 30.325, 782999]],
                 'Hunter': [[64, 198.4, 131395], [120, 265, 98373]],
                 'Agility': [[31, 86.5, 35609], [41, 238, 24410], [53, 240, 36842], [61, 571.4, 34666],
                             [81, 570, 35205], [91, 780, 31063], [120, 793, 34440]],
                 'Fishing': [[21, 20, 435165], [49, 55, 461808], [120, 63, 426954]],
                 'Mining': [[16, 17.5, 741600], [41, 35, 741600], [120, 77, 247200]],
                 'Woodcutting': [[16, 25, 317647], [31, 37.5, 361146], [36, 67.5, 289286], [120, 85, 264336]],
                 'Thieving': [[6, 8, 257211], [26, 16, 124066], [61, 28.5, 124066], [120, 84.3, 257211]],
                 'Farming': [[16, 20, 281040], [28, 481.3, 22483], [43, 1272.5, 9000], [52, 3036.9, 9000],
                             [58, 4791, 9000], [69, 6380.6, 9000], [120, 10509.6, 9000]]}

    boss_dict = {'Abyssal_Sire': 2560, 'Alchemical_Hydra': 3000, 'Callisto': 2000, 'Cerberus': 3000,
                 'Chambers_of_Xeric': 1755, 'Chambers_of_Xeric_Challenge_Mode': 1755, 'Chaos_Elemental': 300,
                 'Chaos_Fanatic': 1000, 'Commander_Zilyana': 5000, 'Corporeal_Beast': 5000, 'Dagannoth_Prime': 5000,
                 'Dagannoth_Rex': 5000, 'Dagannoth_Supreme': 5000, 'General_Graardor': 5000, 'Giant_Mole': 3000,
                 'Grotesque_Guardians': 3000, 'Kalphite_Queen': 3000, 'King_Black_Dragon': 3000, 'Kraken': 3000,
                 'Kree': 5000, "Tsutsaroth": 5000, 'Nightmare': 3840, 'Sarachnis': 3000, 'Scorpia': 2015.75,
                 'Skotizo': 65, 'The_Gauntlet': 2000, 'The_Corrupted_Gauntlet': 800, 'Theatre_of_Blood': 650,
                 'Thermonuclear_Smoke_Devil': 3000, 'Zuk': 100, 'Jad': 100, 'Venenatis': 2000, "Vet": 2000,
                 'Vorkath': 3000, 'Wintertodt': 5000, 'Zalcano': 2250, 'Zulrah': 4000, 'master': 1000, 'gambles': 1000,
                 'Herbiboars': 6500, 'Chompys': 500}

    total_no_pet_chance = []  # Probabilities - each value being the decimal chance of not getting the corresponding pet
    all_pet_chances_str = {}  # Dict of str values of % chance of getting each pet - passed to webpage

    for item in form.items():

        if item[0] in boss_dict:
            if item[1] != "" and item[1] != 0:  # Check value posted isn't blank or 0 (in which case skip)
                boss_chance = calc_bosspet(int(item[1]), boss_dict[item[0]])
                total_no_pet_chance.append(1 - boss_chance)
                boss_chance = 1 - boss_chance
                all_pet_chances_str[item[0]+"_output"] = "{:.4%}".format(boss_chance)

        elif item[0] in rate_dict:
            if item[1] != "" and item[1] != 0:  # Check value posted isn't blank or 0 (in which case skip)
                if item[0] == 'Hunter':  # Separate formula for 'Hunter' - so handler required
                    if int(item[1]) > 136594:  # 136594xp is minimum requirement for being able to get hunter pet
                        real_hunt_xp = ((int(item[1]) - 136594) / 100) * int(form['huntperc'])
                        skill_chance = calc_skills(real_hunt_xp, rate_dict[item[0]], 53)
                    else:
                        all_pet_chances_str[item[0] + "_output"] = "0%"
                        continue
                else:
                    skill_chance = calc_skills(int(item[1]), rate_dict[item[0]])
                total_no_pet_chance.append(1 - skill_chance)
                skill_chance = 1 - skill_chance
                all_pet_chances_str[item[0]+"_output"] = "{:.4%}".format(skill_chance)

    overall_probs = calc_overall_pet_chances(total_no_pet_chance)

    return all_pet_chances_str, overall_probs  # Returns Dict of each pet chance & % chance off getting 1+ pets


def calc_skills(xp, rate_dict, lvl=1):

    probabilities = []  # Contains total probability of getting pet for each level
    stage_index = 0  # Index specifies which stage (list) the program is using from 'rate_dict'
    total = 0  # Xp we have currently reached

    while total < xp:  # Cycle through each level - until we reach desired xp
        if lvl == 99:  # handler for when level hits 99 (and level up no longer possible)
            lvlxp = xp - total
            total += lvlxp
        else:
            lvlxp = (lvl+(300*(2**(lvl/7))))/4  # Formula for xp increase per level
            total += lvlxp

        '''
        Next loop iterates through different skilling choices (specified in 'rate_dict')
        requires a list of lists in form of:
        [[X1, Y1, Z1], [X2, Y2, Z2]...]
        X = (Skill level when you STOP using method)+1 e.g. 78 (for crafting at ouriana alter)
        Y = (XP each action provides e.g. 25 (for cutting logs)
        Z = Base-chance for activity e.g. 782999 (for crafting soul runes)
        Lists must also be in level order e.g. shrimps before sharks
        '''
        for stage in rate_dict[stage_index:]:  # Loop iterates through different lists in 'rate_dict'
            if lvl+1 < stage[0]:
                attempts = lvlxp / stage[1]
                probabilities.append(calc_skillpet(stage[2], lvl, attempts))
                break
            else:
                stage_index += 1
        lvl += 1.0

    prob_array = np.array(probabilities)
    no_pet_chance = np.prod(prob_array)

    return no_pet_chance  # Returns probability of not getting pet as a decimal


def calc_overall_pet_chances(probs):
    num_of_runs = 10000  # Number of trials the simulation will run

    # Convert probs to NP array
    np_probs = np.array(probs)

    # Run sim and count results
    sim_results = np.random.binomial(1, np_probs, (num_of_runs, len(np_probs)))
    sim_pet_counts = np.sum(sim_results, axis=1)
    unique, counts = np.unique(sim_pet_counts, return_counts=True)

    # Put results into dic & convert count to a probability
    totals = dict(zip(unique, (counts / num_of_runs)*100))

    return totals


def calc_skillpet(basechance, level, attempts):
    no_pet_chance = (1 - (1 / (basechance - (level * 25)))) ** attempts  # Formula for calculating skilling pet chance
    return no_pet_chance  # Returns chance of not getting pet


def calc_bosspet(kc, dr):
    no_pet_chance = (1 - (1/dr))**kc # Formula for calculating boss pet chance
    return no_pet_chance  # Returns chance of not getting pet




'''
# Old function for calculating overall pet chances below
# Removed and replaced by current simulation as far too computationally heavy


def calc_overall_pet_chances(probs):

    if len(probs) < 6:
        num_pets_wanted = len(probs)
    else:
        num_pets_wanted = 6

    n = len(probs)
    logprobs = [math.log(probs[i]) if probs[i] > 0 else -math.inf for i in range(n)]
    logprobsneg = [math.log(1 - probs[i]) if probs[i] < 1 else -math.inf for i in range(n)]

    pet_prob_list = []
    for x in range(0, num_pets_wanted):
        current_pet_prob = 0
        for combo in itertools.combinations(range(n), x):
            current_pet_prob += math.exp(sum([logprobs[i] if i in combo else logprobsneg[i] for i in range(n)]))
        pet_prob_list.append(current_pet_prob)  # https://pastebin.com/ZAGH8nJH

    print(pet_prob_list)



'''