import multiprocessing
import time, os
import subprocess, signal

# bar
def catch_pokemons_or_get_balls():
    os.system("python2 pokecli.py");

def run_robot(f, t):
    # Start bar as a process
    p = multiprocessing.Process(target=f)
    p.start()

    time.sleep(t) # sec
    p2 = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, err = p2.communicate()
    for line in out.splitlines():
        if 'python2' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)

def poke(t):
    print " ---- Do some poke"
    os.system("rm ./config.json")
    os.system("cp ./config_poke.json ./config.json")
    print "cp config_poke to config"
    run_robot(catch_pokemons_or_get_balls, t)
    time.sleep(3) # wait for clean up

def farm(t):
    print " ---- Do some farm"
    os.system("rm ./config.json")
    os.system("cp ./config_farm.json ./config.json")
    print "cp config_farm to config"
    run_robot(catch_pokemons_or_get_balls, t)
    time.sleep(3) # wait for clean up

if __name__ == '__main__':
    while True:
        print "\n\n--------- Restart the bot for transferring evolved pokemons "
        poke(600)
        farm(600)
