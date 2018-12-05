import chess
import chess.uci
import sys

logfile = open("dual.log", "w")
LOG = False

EGPCOUNT=16
TBPATH="/home/dkappe/deep1/chess/egtb"
LC0PATH="/home/dkappe/deep1/chess/bin/lc0.19"
ENDERPATH="/home/dkappe/deep1/chess/ender-test/ender128-83.pb"
LEELAPATH="/home/dkappe/work/chess/Arena/Engines/LeelaZero/192/weights_11258.txt.gz"

WEIGHTS_OPTION="WeightsFile"
EGTB_OPTION="SyzygyPath"
THREADS_OPTION="Threads"

MOVETIME=10000

def log(str):
    if LOG:
        logfile.write(str)
        logfile.write("\n")
        logfile.flush()

def send(str):
    log(">{}".format(str))
    sys.stdout.write(str)
    sys.stdout.write("\n")
    sys.stdout.flush()

def process_position(tokens):
    board = chess.Board()

    offset = 0

    if tokens[1] ==  'startpos':
        offset = 2
    elif tokens[1] == 'fen':
        fen = " ".join(tokens[2:8])
        board.set_fen(fen)
        offset = 8

    if offset >= len(tokens):
        return board

    if tokens[offset] == 'moves':
        for i in range(offset+1, len(tokens)):
            board.push_uci(tokens[i])

    return board

send("Dual")

#setup engines

def setOptions(engine, weights):
    options = {}
    options[WEIGHTS_OPTION] = weights
    options[EGTB_OPTION] = TBPATH
    options[THREADS_OPTION] = 2
    engine.setoption(options)
    #engine.isready()
    
leela = chess.uci.popen_engine(LC0PATH)
ender = chess.uci.popen_engine(LC0PATH)

setOptions(ender, ENDERPATH)
setOptions(leela, LEELAPATH)

board = chess.Board()

while True:
    line = sys.stdin.readline()
    line = line.rstrip()
    log("<{}".format(line))
    tokens = line.split()
    if len(tokens) == 0:
        continue

    if tokens[0] == "uci":
        send('id name Dual')
        send('id author Dietrich Kappe')
        send('uciok')
    elif tokens[0] == "quit":
        leela.quit()
        ender.quit()
        exit(0)
    elif tokens[0] == "isready":
        leela.isready()
        ender.isready()
        send("readyok")
    elif tokens[0] == "stop":
        leela.stop()
        ender.stop()
    elif tokens[0] == "ucinewgame":
        board = chess.Board()
        leela.ucinewgame()
        ender.ucinewgame()
    elif tokens[0] == 'position':
        board = process_position(tokens)
    elif tokens[0] == 'go':
        if (len(board.piece_map()) <= EGPCOUNT):
            send("info string ender")
            ender.position(board)
            (best, ponder) = ender.go(movetime=MOVETIME)
        else:
            send("info string leela")
            leela.position(board)
            (best, ponder) = leela.go(movetime=MOVETIME)
        send("bestmove {}".format(best))


logfile.close()
