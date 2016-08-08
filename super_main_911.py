import multiprocessing
import time, os
import subprocess, signal

id = '-weijiejason911'
config = 'configs/config' + id + '.json'

# bar
def catch_pokemons_or_get_balls():
    os.system("python2 pokecli" + id +  ".py -cf " + config);

def run_robot(f, t):
    # Start bar as a process
    p = multiprocessing.Process(target=f)
    p.start()

    time.sleep(t) # sec
    p2 = subprocess.Popen(['ps', '-h'], stdout=subprocess.PIPE)
    out, err = p2.communicate()
    for line in out.splitlines():
        if id in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

def poke(t):
    #print " ---- Do some poke in " + config
    #os.system("rm " + config  + "config.json")
    #os.system("cp " + config + "config_poke.json " + config + "config.json")
    #print "cp config_poke to config"
    run_robot(catch_pokemons_or_get_balls, t)
    time.sleep(3) # wait for clean up

def farm(t):
    #print " ---- Do some farm in " + config
    #os.system("rm " + config  + "config.json")
    #os.system("cp " + config + "config_farm.json " + config + "config.json")
    #print "cp config_farm to config"
    run_robot(catch_pokemons_or_get_balls, t)
    time.sleep(3) # wait for clean up

if __name__ == '__main__':
    while True:
        print "\n\n--------- Restart the bot for transferring evolved pokemons "
        poke(1800)
        farm(1800)
        #poke(600)
