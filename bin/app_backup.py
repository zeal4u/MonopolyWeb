import web
from bin.stuff import DBHelper
from services import *
from time import strftime,localtime,time

urls = (
    '/','Index',
    '/game','Game',
    '/record','Record'
)

app = web.application(urls,globals())

if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'),
                                  {'player_names': None
                                   })
    web.config._session = session
else:
    session = web.config._session

render = web.template.render('templates/',base="layout",globals={'context': session})

class Index:

    def GET(self):
        return render.index()

    def POST(self):
        form = web.input(player_name="Nobody")
        # need
        session.player_names = []

        for name in form.player_name.split(','):
            session.player_names.append(name)
        raise web.seeother('/game')

class Game:
    # class attr
    service = Service()
    print "Service start"

    one_round_end =False

    def GET(self):
        Game.service.init_game(session.player_names)
        messages = [Game.service.map_describe()]

        # init game status
        Game.one_round_end = False

        return render.game(current_player=Game.service.current_player,messages=messages)

    def POST(self):
        # one round end, so we enter game page in init status, stop user return back
        if Game.one_round_end:
            raise web.seeother('/game')

        if Game.service.next_turn():
            DBHelper.update_record(Game.service.current_player,Game.service.sum_turns,strftime("%Y-%m-%d %H:%M:%S", localtime(time())))

            messages = ["Player %s has won the game in %d turns. CONGRATULATIONS!" %
                        (Game.service.current_player.name,Game.service.sum_turns)]

            if DBHelper.record_is_broken(Game.service.sum_turns):
                plus = 'You Just Broken A Record! Have A Look!'
                messages.append(plus)

            # Current game finish
            Game.one_round_end = True

            return render.gameover(messages=messages)
        else:
            current_player = Game.service.current_player
            messages = Game.service.messages

        return render.game(current_player=current_player,messages=messages)

class Record:

    def GET(self):
        records = DBHelper.get_by_mapcode_from_records_ranked(1)
        return render.record(records = records)

    def POST(self):
        pass

if __name__ == "__main__":
    app.run()
