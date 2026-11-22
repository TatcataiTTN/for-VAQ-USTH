# -*- coding: utf-8 -*-
"""Bang ma Tooley Phu luc 5 (thap phan, bat phan, thap luc, nhi phan, ASCII 0 den 127 va ten). Cot so tinh bang Python (hai cach: format() va tu cong tay), ten theo cot 'Meaning' cua sach (kiem bang OCR + anh trang 391-393)."""
CTRL = ['NUL Null', 'SOH Start of heading', 'STX Start of text', 'ETX End of text', 'EOT End of transmission', 'ENQ Enquiry', 'ACK Acknowledgement', 'BEL Bell', 'BS Backspace', 'HT Horizontal tab', 'LF Line feed', 'VT Vertical tab', 'FF Form feed', 'CR Carriage return', 'SO Shift out', 'SI Shift in',
        'DLE Data line escape', 'DC1 Device control 1', 'DC2 Device control 2', 'DC3 Device control 3', 'DC4 Device control 4', 'NAK Negative acknowledgement', 'SYN Synchronous idle', 'ETB End of transmit block', 'CAN Cancel', 'EM End of medium', 'SUB Substitute', 'ESC Escape', 'FS File separator', 'GS Group separator', 'RS Record separator', 'US Unit separator']
PRINT = {32: 'Space', 33: 'Exclamation mark', 34: 'Double quotes', 35: 'Number', 36: 'Dollar', 37: 'Percent', 38: 'Ampersand', 39: 'Single quote', 40: 'Open parenthesis', 41: 'Close parenthesis', 42: 'Asterisk', 43: 'Plus', 44: 'Comma', 45: 'Hyphen', 46: 'Full stop', 47: 'Divide',
         58: 'Colon', 59: 'Semicolon', 60: 'Less than', 61: 'Equals', 62: 'Greater than', 63: 'Question mark', 64: 'At symbol'}
DIG = ['Zero', 'One', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine']
def meaning(n):
    if n < 32: return CTRL[n].split(' ', 1)[1]
    if n == 127: return 'Delete'
    if n in PRINT: return PRINT[n]
    if 48 <= n <= 57: return DIG[n - 48]
    if 65 <= n <= 90: return f'Uppercase {chr(n)}'
    if 97 <= n <= 122: return f'Lowercase {chr(n)}'
    return OTHER[n]
OTHER = {91: 'Opening bracket', 92: 'Backslash', 93: 'Closing bracket', 94: 'Caret', 95: 'Underscore', 96: 'Grave accent', 123: 'Opening brace', 124: 'Vertical bar', 125: 'Closing brace', 126: 'Tilde'}
def symbol(n): return CTRL[n].split(' ', 1)[0] if n < 32 else 'DEL' if n == 127 else chr(n)
def row_a(n): return (n, format(n, '03o'), format(n, '02X'), format(n, '08b'), symbol(n), meaning(n))
def row_b(n):
    o = ''; x = n
    while x: o = str(x % 8) + o; x //= 8
    h = ''; x = n
    while x: h = '0123456789ABCDEF'[x % 16] + h; x //= 16
    b = ''; x = n
    while x: b = str(x % 2) + b; x //= 2
    return (n, o.zfill(3), h.zfill(2), b.zfill(8), symbol(n), meaning(n))
rows = [row_a(n) for n in range(128)]
