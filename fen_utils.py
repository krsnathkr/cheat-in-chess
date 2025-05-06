
def board_to_fen(board, side_to_move="w"):
    fen_rows = []
    for row in board:
        fen_row = ""
        empty_count = 0
        for cell in row:
            if cell == ".":
                empty_count += 1
            else:
                if empty_count > 0:
                    fen_row += str(empty_count)
                    empty_count = 0
                fen_row += cell
        if empty_count > 0:
            fen_row += str(empty_count)
        fen_rows.append(fen_row)

    placement = "/".join(fen_rows)
    return f"{placement} {side_to_move} - - 0 1"
