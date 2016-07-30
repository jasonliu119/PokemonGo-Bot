import json
import time
from pokemongo_bot.human_behaviour import sleep
from pokemongo_bot import logger

iv_map = {"Eevee":0.8, "Dratini": 0.8, "Magikarp": 0.8, "Poliwag": 0.8, "Growlithe": 0.8, "Exeggcute": 0.8, "Squirtle":0.8,"Bulbasaur":0.8,"Charmander":0.8}

should_transfer = ['Rattata','Pidgey','Zubat','Weedle','Spearow','Drowzee']


class InitialTransferWorker(object):
    def __init__(self, bot):
        self.config = bot.config
        self.pokemon_list = bot.pokemon_list
        self.api = bot.api

    def work(self):
        logger.log('[x] Initial Transfer.')

        logger.log(
        '[x] Preparing to transfer all duplicate Pokemon, keeping the highest CP of each type.')

        logger.log('[x] Will NOT transfer anything above CP {}'.format(
            self.config.initial_transfer))
        
        keep_map = {"Eevee" : 600, "Dratini": 570, "Growlithe": 570}
       

        pokemon_groups = self._initial_transfer_get_groups()

        for id in pokemon_groups:

            group_cp = pokemon_groups[id].keys()

            if len(group_cp) > 1:
                group_cp.sort()
                group_cp.reverse()


                for x in range(1, len(group_cp)):
                    poke_data = pokemon_groups[id][group_cp[x]]
                    poke_id = poke_data['id']
                    poke_name = self.pokemon_list[id - 1]['Name']

                    iv_stats = ['individual_attack', 'individual_defense', 'individual_stamina']
                    total_IV = 0
                    for individual_stat in iv_stats:
                        try:
                            total_IV += poke_data[individual_stat]
                        except:
                            poke_data[individual_stat] = 0
                            continue

                    pokemon_potential = round((total_IV / 45.0), 2)

                    if pokemon_potential > 0.85 and poke_name not in should_transfer:
                        print('[!] Keep ' + poke_name + ' with IV ' + str(pokemon_potential))
                        continue

                    if self.config.initial_transfer and group_cp[x] > self.config.initial_transfer:
                        continue

                    print('[x] Transferring {} with CP {}'.format(
                        self.pokemon_list[id - 1]['Name'], group_cp[x]))
                    self.api.release_pokemon(
                        pokemon_id=pokemon_groups[id][group_cp[x]]['id'])
                    response_dict = self.api.call()
                    sleep(2)

        logger.log('[x] Transferring Done.')

    def _initial_transfer_get_groups(self):
        pokemon_groups = {}
        #self.api.get_player().get_inventory()
        inventory_req = {}
        inventory_dict = {}
   
        while True: 
            try:
                self.api.get_player().get_inventory()
                inventory_req = self.api.call()
                inventory_dict = inventory_req['responses']['GET_INVENTORY'][
                    'inventory_delta']['inventory_items']
                break
            except Exception as e:
                print '[!] Failed to get pokemon group for initial_transfer'
                time.sleep(2)

        user_web_inventory = 'web/inventory-%s.json' % (self.config.username)
        with open(user_web_inventory, 'w') as outfile:
            json.dump(inventory_dict, outfile)

        for pokemon in inventory_dict:
            try:
                reduce(dict.__getitem__, [
                    "inventory_item_data", "pokemon_data", "pokemon_id"
                ], pokemon)
            except KeyError:
                continue

            group_id = pokemon['inventory_item_data'][
                'pokemon_data']['pokemon_id']
            group_pokemon = pokemon['inventory_item_data'][
                'pokemon_data'] #rm ['id'] 
            group_pokemon_cp = pokemon[
                'inventory_item_data']['pokemon_data']['cp'] 

            if group_id not in pokemon_groups:
                pokemon_groups[group_id] = {}

            pokemon_groups[group_id].update({group_pokemon_cp: group_pokemon})
        return pokemon_groups
