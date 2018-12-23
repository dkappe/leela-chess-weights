#!/usr/bin/python3
import random
import sys
import time
import traceback
from math import trunc

import chess
import chess.pgn


def place_kings(brd):
    while True:
        rank_white, file_white, rank_black, file_black = random.randint(0,7), random.randint(0,7), random.randint(0,7), random.randint(0,7)
        diff_list = [abs(rank_white - rank_black),  abs(file_white - file_black)]
        if sum(diff_list) > 2 or set(diff_list) == (0, 2):
            brd[rank_white][file_white], brd[rank_black][file_black] = "K", "k"
            break
 
def populate_board(brd, wp, bp, white_pieces, black_pieces):
    for pieces, num in zip((white_pieces, black_pieces), (wp, bp)):
        for piece in random.sample(pieces, num):
            row, col = random.randint(0, 7), random.randint(0, 7)
            while brd[row][col] != " " or pawn_on_promotion_square(piece, row):
                row, col = random.randint(0, 7), random.randint(0, 7)
            brd[row][col] = piece
 
def pawn_on_promotion_square(pc, pr):
    if pc == "P" and pr == 0:
        return True
    elif pc == "p" and pr == 7:
        return True
    return False
    
def fen_from_board(brd):
    fen = ""
    for x in brd:
        n = 0
        for y in x:
            if y == " ":
                n += 1
            else:
                if n != 0:
                    fen += str(n)
                fen += y
                n = 0
        if n != 0:
            fen += str(n)
        fen += "/" if fen.count("/") < 7 else ""
    fen += " w - - 0 1\n"
    return fen

def gen_board(piece_num = 6, pieces = ''):
    board = [[" " for x in range(8)] for y in range(8)]
    place_kings(board)
    if pieces == '':
        white_num = random.randint(0, piece_num - 2)
        black_num = piece_num - 2 - white_num
        white_pieces = ["R", "N", "B", "Q", "P"]*1000
        black_pieces = ["r", "n", "b", "q", "p"]*1000
        populate_board(board, 
                       white_num, 
                       black_num, 
                       white_pieces, 
                       black_pieces)
    else:
        white_pieces, black_pieces = pieces.split('v')
        white_pieces = white_pieces[1:]
        black_pieces = black_pieces[1:].lower()
        populate_board(board, 
                       len(white_pieces), 
                       len(black_pieces), 
                       white_pieces, 
                       black_pieces)
    return board

def main():
    board = chess.Board(fen=None)
    with open('prebad.epd', 'w') as out:
        
        for i in range(55000):
            #if not i%1000:
            #    print(i)
            wcount = 1 + (i%4)
            bcount = 4 - (i%4)

            wp = 'K'
            wp += ''.join(random.choices('QRBNP', k=wcount))
            bp = 'k'
            bp += ''.join(random.choices('rbnqp', k=bcount))
            fen = fen_from_board(gen_board(pieces=wp+'v'+bp))
            board.set_fen(fen)
            if not board.is_valid() or board.is_game_over(claim_draw=True):
                continue

            out.write(board.epd())
            out.write("\n")
            out.flush()
main()

