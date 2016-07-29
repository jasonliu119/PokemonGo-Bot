import multiprocessing
import time, os
import subprocess, signal

# bar
def catch_pokemons_or_get_balls():
    os.system("python2 pokecli.py -cf ./configs/config.json");

def do_catch(f, t):
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

def poke():
    print " ---- do some poke"
    os.system("rm configs/config.json")
    os.system("cp configs/config_poke.json configs/config.json")
    print "cp config_poke to config"
    do_catch(catch_pokemons_or_get_balls, 600)
    time.sleep(3) # wait for clean up

def farm():
    print " ---- do some farm"
    os.system("rm configs/config.json")
    os.system("cp configs/config_farm.json configs/config.json")
    print "cp config_farm to config"
    do_catch(catch_pokemons_or_get_balls, 600)
    time.sleep(3) # wait for clean up

if __name__ == '__main__':
    while True:
        print "\n\n--------- restart the bot for transferring evolved pokemons "
        poke()
        farm()
        
        
        
	
        

        

        
        
        
    
