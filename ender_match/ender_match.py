import time
import chess
import chess.pgn
import chess.uci
import chess.syzygy
import sys
import configparser
from random import randrange

def log(msg):
    print(msg)
    sys.stdout.flush()
    
config = configparser.ConfigParser()
config.read(sys.argv[1])

ENDER_PIECE_COUNT = int(config['DEFAULT']['Piece Count'])

class Engine:
    def __init__(self, name=None, cmd=None, options=None):
        super().__init__()
        self.name = name
        self.cmd = cmd
        self.options = options
        self.start_engine()
        log("name = {}".format(name))
        wfile = options.get("WeightsFile")
        if not wfile == None:
            log("WeightsFile = {}".format(options["WeightsFile"]))
        self.engine.uci()
        self.engine.isready()


    def start_engine(self):
        self.engine = chess.uci.popen_engine(self.cmd)
        self.engine.setoption(self.options)


class Openings:
    def __init__(self, pgnfile=None):
        super().__init__()
        self.openings = []
        if pgnfile != None:
            while True:
                game = chess.pgn.read_game(pgnfile)
                if game == None:
                    break
                else:
                    self.openings.append(game)

    def opening_count(self):
        return len(self.openings)

    def get_opening(self):
        random_index = randrange(len(self.openings))
        return self.openings[random_index]

class MatchGame:
    def __init__(self, white=None, black=None, egtb_path=None, tbadj=6, us_color=None):
        super().__init__()
        self.us_color = us_color
        self.white = white
        self.black = black
        self.tb = chess.syzygy.open_tablebases(egtb_path)
        self.tbadj = tbadj
        self.board = chess.Board()

    def adjudicate(self):
        if self.board.is_game_over(claim_draw=True):
            return False, None, None
        elif len(self.board.piece_map()) <= self.tbadj:
            result = self.tb.get_wdl(self.board)
            if result == None:
                return False, None, None
            side_to_move = self.board.turn
            if side_to_move: # white
                if result == 2:
                    return True, "1-0", "TB win for White."
                elif result == -2:
                    return True, "0-1", "TB win for Black"
                else:
                    return True, "1/2-1/2", "TB draw"
            else: # black
                if result == 2:
                    return True, "0-1", "TB win for Black."
                elif result == -2:
                    return True, "1-0", "TB win for White"
                else:
                    return True, "1/2-1/2", "TB draw"
        else:
            return False, None, None

    def game_over(self):
        if self.board.is_game_over(claim_draw=True):
            game = chess.pgn.Game.from_board(self.board)
            game.headers['Result'] = self.board.result(claim_draw=True)
            return True, game
        else:
            adjudicated, result, comment = self.adjudicate()
            if adjudicated:
                game = chess.pgn.Game.from_board(self.board)
                game.headers['Result'] = result
                node = game.end()
                node.comment = comment
                return True, game
            else:
                return False, None

    def populate_headers(self, game):
        game.headers['Event'] = 'Event'
        game.headers['Site'] = 'Site'
        game.headers['Date'] = '??'
        game.headers['White'] = self.white.name
        game.headers['Black'] = self.black.name
        game.headers['Round'] = 1

    def play(self, movetime=1000, enemytime=1000, opening=None):
        self.white.engine.ucinewgame()
        self.black.engine.ucinewgame()

        if self.us_color: # white
            white_time = movetime
            black_time = enemytime
        else:
            white_time = enemytime
            black_time = movetime

        if opening != None:
            moves = opening.main_line()
            for m in moves:
                self.board.push(m)

        while True:
            over, game = self.game_over()
            if over:
                self.populate_headers(game)
                return game
            if self.board.turn: #white
                try:
                    self.white.engine.position(self.board)
                    best, ponder = self.white.engine.go(movetime=white_time)
                    self.board.push(best)
                except:
                    self.white.start_engine()
                    self.white.engine.position(self.board)
                    best, ponder = self.white.engine.go(movetime=white_time)
                    self.board.push(best)
            else:
                try:
                    self.black.engine.position(self.board)
                    best, ponder = self.black.engine.go(movetime=black_time)
                    self.board.push(best)
                except:
                    self.black.start_engine()
                    self.black.engine.position(self.board)
                    best, ponder = self.black.engine.go(movetime=black_time)
                    self.board.push(best)
        
            log(best)

def doctor_game(game, side, piece_count):
    moves = game.main_line()
    board = chess.Board()
    for m in moves:
        board.push(m)
        if len(board.piece_map()) <= piece_count and board.turn == side:
            break
    if board.is_game_over(claim_draw=True):
        return None
    if len(board.piece_map()) > piece_count or board.turn != side:
        return None
    opening = chess.pgn.Game.from_board(board)
    return opening

def getMatchGame(color, us=None, them=None):
    if color: # white
        match_game = MatchGame(white=us, black=them, egtb_path=config['DEFAULT']['EGTB Path'], us_color=color)
    else:
        match_game = MatchGame(white=them, black=us, egtb_path=config['DEFAULT']['EGTB Path'], us_color=color)
    return match_game

with open(config['DEFAULT']['Output'], 'a+') as pgn, open(config['DEFAULT']['Openings'], 'r') as openings:
    log("Setup")
    movetime = int(config['DEFAULT']['Movetime'])
    enemytime = int(config['DEFAULT']['Enemytime'])
    count = int(config['DEFAULT']['Games'])
    if config['DEFAULT']['Color'] == 'White':
        color = chess.WHITE
    else:
        color = chess.BLACK

    book = Openings(openings)
    log(book.opening_count())
    enemy_name = config['DEFAULT']['Enemy']
    enemy_cmd = config['DEFAULT']['Enemy Command']
    enemy_options = config['Enemy Options']
    enemy = Engine(name=enemy_name, cmd=enemy_cmd, options=enemy_options)
    log(enemy.engine.name)

    ender_name = config['DEFAULT']['Ender']
    ender_cmd = config['DEFAULT']['Ender Command']
    ender_options = config['Ender Options']
    ender = Engine(name=ender_name, cmd=ender_cmd, options=ender_options)
    log(ender.engine.name)
    log("Ender conf")
    log(ender_options["WeightsFile"])
    
    time.sleep(1)

    leela_name = config['DEFAULT']['Leela']
    leela_cmd = config['DEFAULT']['Leela Command']
    leela_options = config['Leela Options']
    leela = Engine(name=leela_name, cmd=leela_cmd, options=leela_options)
    log(leela.engine.name)
    
    for i in range(count):
        log("playing game {}".format(count+1))
        log("\n")
        log("Leela")



        match_game = getMatchGame(color, us=leela, them=enemy)

        op = book.get_opening()
        log("kickoff play")
        game = match_game.play(movetime=movetime, enemytime=enemytime, opening=op)
        log("play done")
        game.headers['LeelaRatio'] = config['DEFAULT']['Leela Ratio']
        game.headers['TimeControl'] = "move/{}s".format(movetime/1000)


        next_opening = doctor_game(game, color, ENDER_PIECE_COUNT)

        if next_opening == None:
            # one more time
            log("ender replay")
            match_game = getMatchGame(color, us=leela, them=enemy)
            log("kickoff play")
            game = match_game.play(movetime=movetime, enemytime=enemytime, opening=op)
            log("play done")
            game.headers['LeelaRatio'] = config['DEFAULT']['Leela Ratio']
            game.headers['TimeControl'] = "move/{}s".format(movetime/1000)

            next_opening = doctor_game(game, color, ENDER_PIECE_COUNT)

        log("")

        if next_opening == None:
            log("Unsuitable game.\n")
            log(game)
        else:
            time.sleep(1)
            
            log("\n")
            log("Ender")

            match_game2 = getMatchGame(color, us=ender, them=enemy)

            game2 = match_game2.play(movetime=movetime, enemytime=enemytime, opening=next_opening)
            game2.headers['LeelaRatio'] = config['DEFAULT']['Leela Ratio']
            game2.headers['TimeControl'] = "move/{}s".format(movetime/1000)

            pgn.write("{}\n".format(game))
            pgn.write("\n")
            pgn.write("{}\n".format(game2))
            pgn.write("\n")
            pgn.flush()

            log(game.headers['Result'])
            log(game2.headers['Result'])

    enemy.engine.quit()
    leela.engine.quit()
    ender.engine.quit()

    pgn.flush()
    pgn.close()




