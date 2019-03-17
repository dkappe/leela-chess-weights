import time
import chess
import chess.pgn
import chess.uci
import chess.syzygy
import sys
import configparser
from random import randrange

MATE_VAL = 30000

config = configparser.ConfigParser()
config.read(sys.argv[1])

MOVE_NODES = int(config['DEFAULT']['MOVE_NODES'])
ENGINE_CMD = config['DEFAULT']['ENGINE_CMD']
ENGINE_OPTIONS = config['ENGINE OPTIONS']

class Engine:
    def __init__(self, name=None, cmd=None, options=None):
        super().__init__()
        self.name = name
        self.engine = chess.uci.popen_engine(cmd)
        self.info_handler = chess.uci.InfoHandler()
        self.engine.info_handlers.append(self.info_handler)
        self.engine.setoption(options)
        self.engine.uci()
        self.engine.isready()

    def analyze(self, board=None, nodes=None):
        # return move, score from white's perspective
        self.engine.position(board)
        move, ponder = self.engine.go(nodes=nodes)
        # get the score
        score = self.info_handler.info["score"][1].cp
        if score == None:
            if self.info_handler.info["score"][1].mate > 0:
                score = MATE_VAL-self.info_handler.info["score"][1].mate
            else:
                score = -MATE_VAL-self.info_handler.info["score"][1].mate

        # redo for white
        if not board.turn: # black
            score = -score
        return move, score

    def reset(self):
        self.engine.ucinewgame()

    def quit(self):
        self.engine.quit()




class GameAnalyzer:
    def __init__(self, engine=None):
        super().__init__()
        self.engine = engine

    def analyze_game(self, game=None, nodes=300000):
        self.engine.reset()
        game_node = game
        for move in game.main_line():
            game_node = game_node.variation(move)
            board = game_node.board()
            mv, score = self.engine.analyze(board, nodes)
            #sys.stderr.write("Processing comment:\n{}\n".format(board))
            game_node.comment = "[%eval {}]".format(score/100)





engine = Engine(name="sf10", cmd=ENGINE_CMD, options=ENGINE_OPTIONS)

ga = GameAnalyzer(engine=engine)
count = 0
while True:
    game = chess.pgn.read_game(sys.stdin)
    if game == None:
        break
    count = count + 1
    if count%20 == 0:
        sys.stderr.write("{}\n".format(count))
    ga.analyze_game(game=game, nodes=MOVE_NODES)
    print(game)
    print("")

engine.quit()
