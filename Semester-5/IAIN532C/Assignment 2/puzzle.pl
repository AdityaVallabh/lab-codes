is_safe(Hu,Bm,Sm):-
    Hu >= 0, Hu =< 3,
    Bm >= 0, Bm =< 1,
    Sm >= 0, Sm =< 2,
    (
        Hu is Bm + Sm;
        Hu =:= 0;
        Hu =:= 3
    ).

get_all_moves(Hu,Bm,Sm,OBo,Moves):-
    Bo is OBo * -1,
    (
        OBo =:= 1 ->
            Moves = [
                [Hu-2,Bm,Sm,Bo],
                [Hu-1,Bm,Sm,Bo],
                [Hu,Bm-1,Sm,Bo],
                [Hu-1,Bm-1,Sm,Bo],
                [Hu-1,Bm,Sm-1,Bo],
                [Hu,Bm-1,Sm-1,Bo]
            ];
            Moves = [
                [Hu+2,Bm,Sm,Bo],
                [Hu+1,Bm,Sm,Bo],
                [Hu,Bm+1,Sm,Bo],
                [Hu+1,Bm+1,Sm,Bo],
                [Hu+1,Bm,Sm+1,Bo],
                [Hu,Bm+1,Sm+1,Bo]
            ]
    ).

perform_move(Vis,[[OHu,OBm,OSm,Bo]|Moves]):-
    Hu is OHu, Bm is OBm, Sm is OSm,
    (
        (
            is_safe(Hu,Bm,Sm),
            not(memberchk([Hu,Bm,Sm,Bo], Vis)),
            solve(Hu,Bm,Sm,Bo,Vis),
            write(Hu), write(' '), write(Bm), write(' '), write(Sm), write(' '), write(Bo), nl
        );
        perform_move(Vis,Moves)
    ).

solve(0,0,0,-1,_).
solve(Hu,Bm,Sm,Bo,Vis):-
    get_all_moves(Hu,Bm,Sm,Bo,Moves),
    perform_move([[Hu,Bm,Sm,Bo]|Vis],Moves).

% solve(3,1,2,1,[]).