from json import JSONEncoder

from monopoly import *


class PlayerEncoder(JSONEncoder):
    """
    JSONEncoder for class:Player
    """
    def default(self, obj):
        if isinstance(obj, Player):
            return {'id':obj.id,
                    'name':obj.name,
                    'position':obj.position}
        return JSONEncoder.default(self, obj)


class ServicesManager:
    """
    Game services manager, expose api to app.py
    """

    def __init__(self):
        self.services = dict()

    def register_service(self,key):
        self.services[key] = Service()

    def get_service_by_key(self,key):
        if self.services.has_key(key):
            return self.services[key]
        raise KeyError

    def close_service_by_key(self,key):
        del self.services[key]


class Service(object):
    """
    Apply service for playing game
    """

    def __init__(self):
        pass

    def map_describe(self):
        """
        Get map describe
        :return: string: describe how's the map like
        """
        return self.engine.map.describe()

    def init_game(self,player_names):
        """
        init the parm of the game
        :param list player_names: pass from the view page
        :return: None
        """

        players = []
        index = 0

        #create players distinct
        for name in set(player_names):
            players.append(Player(index,name))
            index += 1

        # temporary
        map = Map()
        map.make_up()

        self.engine = Engine(map,players)
        self.current_player = players[0]
        self.engine.play()
        print "Linking Start!"


    def next_turn(self):
        """
        :return: the result of this turn
        """
        if self.engine.next_turn():

            # ready for next turn
            self.engine.next_ready()

            # send to view
            self.current_player = self.engine.current_player

            # send to view
            self.messages = self.engine.messages

        else:

            self.sum_turns = self.engine.steps
            return True
        # no one has won yet
        return False

