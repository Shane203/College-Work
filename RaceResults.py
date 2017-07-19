def ReadDictionary (filename) :
    try:
        filehandle = open(filename, "r")
    except IOError :
        print ("Error: File cannot be read")
        return {}
    d = {}
    for line in filehandle :
        value = []
        linewords = line.split()
        key = linewords[0]
        value += [linewords[1]]
        value += [linewords[2]]
        d[key] = value
    return d

def RaceResults2 (entries) :
    try :
        filehandle = open(entries, "r")
    except IOError :
        return ("Error: File cannot be read")
    racerdict = ReadDictionary(entries)
    position = 0
    teamscore = {}
    finished = []
    scoringnum = 3
    teamdictname = {}
    finishednums = []
    teamsdone = []
    print ("Enter the racers' numbers as they arrive at the finish line")
    print ("Enter 0 to end the program")
    while True :
        racernum = input("Racer's number = ")
        if racernum == "0" :
            if len(teamsdone) > 0 :
                print ("PLACE  SCORE  TEAM  SCORING MEMBERS")
                place = 0
                for team in teamsdone :
                    place += 1
                    print("%3s %6s %8s %s"
             % (place, teamscore[team], team, ", ".join(teamdictname[team])))
            return
        elif racernum not in racerdict :
            print ("Error: This racer number has not been regsitered")
        elif racernum not in finishednums :
            finishednums += [racernum]
            position += 1
            value = racerdict[racernum]
            name = value[0]
            team = value[1]
            finished += [(position, racernum, name, team)]
            if team in teamdictname :
                if len(teamdictname[team]) < scoringnum :
                    if team in teamscore :
                        teamscore[team] += position
                        teamdictname[team] += [name]
            else :
                teamscore[team] = position
                teamdictname[team] = [name]
        elif racernum in finishednums :
            print ("Error: This racer has already finished")
        for team in teamdictname :
            if len(teamdictname[team]) == scoringnum and team not in teamsdone :
                print ("SCORE = %s TEAM = %s: %s"
                       % (teamscore[team], team, ", ".join(teamdictname[team])))
                teamsdone += [team]
                
    

            
        
            
