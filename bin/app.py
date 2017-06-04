from time import strftime, localtime, time

import web
import json

from monopoly import Player
from services import PlayerEncoder, ServicesManager
from stuff import DBHelper, RecordEncoder

# APIs exposed to front end
urls = (
    '/nextTurn','Game',
    '/getRecord','Record',
    "/(.*)", "Index"
)

app = web.application(urls,globals())

class Index:

    def GET(self,url):
        """
        :param url: needs, or will throw exception
        :return:
        """
        raise web.redirect('/static/web-angular/app/index.html')

class Record:
    """
    Charge the record
    """

    def POST(self):
        records = DBHelper.get_by_mapcode_from_records_ranked(1)

        # bower will recognize the data as json
        web.header('Content-Type', 'application/json')
        return json.dumps(records,cls=RecordEncoder)

class Game:
    """
    Charge the game service
    """

    # multi-player services manage
    manager = ServicesManager()

    def GET(self):
        # one ip can start one game at time
        ip = web.ctx.ip
        try:
            service = Game.manager.get_service_by_key(ip)
        except KeyError:

            # register game service
            Game.manager.register_service(ip)
            service = Game.manager.get_service_by_key(ip)

            # get players' names
            data = web.input()
            players_names = [data[str(x)] for x in range(len(data))]

            # init game service
            service.init_game(players_names)

        messages = [service.map_describe()]
        response = {
            'current_player': json.loads(json.dumps(service.current_player,cls=PlayerEncoder)),
            'messages': messages
        }
        web.header('Content-Type', 'application/json')
        return json.dumps(response)


    def POST(self):
        # get remote IP
        ip = web.ctx.ip

        # get game service
        try:
            service = Game.manager.get_service_by_key(ip)
        except KeyError:
            messages = {
                'messages': ['Games has not been inited!']
            }
            return json.dumps(messages)

        is_over = False
        if service.next_turn():
            # game over
            # store the winner's record
            DBHelper.update_record(service.current_player,service.sum_turns,strftime("%Y-%m-%d %H:%M:%S", localtime(time())))

            messages = ["Player %s has won the game in %d turns. CONGRATULATIONS!" %
                        (service.current_player.name,service.sum_turns)]

            # if broke a record, add a plus message
            if DBHelper.record_is_broken(service.sum_turns):
                plus = 'You Just Broken A Record! Have A Look!'
                messages.append(plus)

            # close game service
            Game.manager.close_service_by_key(ip)

            # tell front end that game is over
            is_over = True

        else:
            messages = service.messages
        response = {
            'is_over': is_over,
            'current_player': json.loads(json.dumps(service.current_player, cls=PlayerEncoder)),
            'messages': messages
        }
        web.header('Content-Type', 'application/json')
        return json.dumps(response)

# test
class GameImprove:

    def POST(self):
        # need to send the position list of player's moving
        response = {
            'is_over': False,
            'current_player': json.loads(json.dumps(Player('-1','jiangshizhi'),cls=PlayerEncoder)),
            'messages': ['test'],
            'positions': [1,2,3]
        }
        return response


# apache server config needs it
#web.wsgi.runwsgi = lambda func, addr=None: web.wsgi.runfcgi(func, addr)

if __name__ == "__main__":
    app.run()
