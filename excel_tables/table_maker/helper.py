def get_column_letter(col_idx):
    """
    Convert a zero-indexed column number to an Excel column letter.
    """
    if col_idx < 0:
        raise ValueError("Column index must be non-negative")
    
    col_letter = ''
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        col_letter = chr(65 + remainder) + col_letter
    return col_letter
