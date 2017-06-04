from sys import exit
from random import randint

class Player(object):
    def __init__(self,id,name):

        self.id = id
        self.name = name
        # begin at beginning point
        self.position = 0

    def where_am_I(self):
        """
        return the string showing player's position
        """
        return "%s is at Node %r" % (self.name, self.position)

class Engine(object):

    def __init__(self, map, players):
        """
        :param Map map: a Map object
        :param list players: list of Player objects
        """
        self.map = map
        self.players = players

    def roll_dice(self):
        """
        roll the dice, return 1~6
        """
        return randint(1, 6)

    def play(self):
        """
        init the game and start
        :return:
        """
        # every game, it will be reset
        self.steps = 0
        # recognize the current player
        self.index = 0
        # init current player
        self.current_player = self.players[self.index]

    def next_turn(self):
        """
        :return: True means not end yet, False means that has a winner
        """
        if not self.index:
            # the first player's id=0, so we count his steps for recording the num of turns
            self.steps += 1

        # result of this roll
        num = self.roll_dice()

        # send to service
        self.messages = ["Player %s rolled %d" % (self.current_player.name,num)]
        flag = True

        # the expected position, when it's greater than endpoint(len of nodes), it will be back "some steps"
        p = self.current_player.position = self.possible_position(self.current_player.position + num)

        # using while to continue the magic! Responsibility Chains
        while flag:

            flag,message = self.map.nodes[p].magic(self.current_player)
            self.messages.append(message)

            # this may cause bug, such as dead-while
            p = self.current_player.position = self.possible_position(self.current_player.position)

        # we recognize the last node as the end
        return self.current_player.position != self.map.size -1

    def possible_position(self, position):
        """
        We can't break through the world of THE MAP!
        Make position always in the index of nodes list
        :param int position: dirty position
        :return clean position
        """
        if position < 0:
            return 0
        return position if position < self.map.size else 2*(self.map.size - 1)-position

    def next_ready(self):
        """
        next player ready
        :return: None
        """
        self.index = (self.index + 1) % len(self.players)
        self.current_player = self.players[self.index]

class Map(object):
    """
    Nest the map(which includes nodes) of the game
    """
    def __init__(self,nodes=None):
        self.nodes = nodes
        if nodes:
            self.size = len(nodes)

    def describe(self):
        return "This map has %d nodes. Node %d is the endpoint. Good luck, guys!" % (self.size, self.size-1)

    def make_up(self):
        """
        Init the map nodes
        Very important method, you should call this or you got nothing!
        :return:
        """
        if not self.nodes:
            nodes = [Node(x) for x in range(0, 2)]
            nodes.append(MoveNode(2, 2))
            nodes.append(Node(3))
            nodes.append(MoveNode(4, -3))
            nodes.extend([Node(x) for x in range(5, 10)])
        self.nodes = nodes
        self.size = len(nodes)

class Node(object):

    def __init__(self,id):
        self.id = id

    def magic(self,player):

        message = "Node %d, oops, nothing good, nothing bad!" % self.id
        # no chance to continue magic
        return (False, message)

class MoveNode(Node):

    def __init__(self, id, buff):
        super(MoveNode,self).__init__(id)
        self.buff = buff

    def magic(self,player):
        if self.buff > 0:
            message = "Yeah, Node %d is a lucky node, you could probably move for another %d stpes." % (self.id,self.buff)
        elif self.buff < 0:
            message = "Oh, Node %d is a bad node, you should backoff for %d steps." % (self.id, abs(self.buff))
        else:
            return super(MoveNode,self).magic(player)

        player.position += self.buff
        # because it changes the position, the magic may last for a while
        return (True, message)

