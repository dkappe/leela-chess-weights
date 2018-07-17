#!/usr/bin/env bash

polyglot make-book -only-white -pgn white.pgn -bin w1.bin -max-ply 16 -min-game 50
polyglot make-book -only-white -pgn white.pgn -bin w2.bin -max-ply 60 -min-game 5
polyglot merge-book -in1 w1.bin -in2 w2.bin -out w12.bin

polyglot make-book -only-black -pgn black.pgn -bin b1.bin -max-ply 16 -min-game 50
polyglot make-book -only-black -pgn black.pgn -bin b2.bin -max-ply 60 -min-game 5
polyglot merge-book -in1 b1.bin -in2 b2.bin -out b12.bin

polyglot merge-book -in1 w12.bin -in2 b12.bin -out leela.bin
