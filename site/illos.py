#!/usr/bin/env python3
"""The six illustrations shown on the landing page.

Each comes from a different layout in the spotkit system and a different
industry, which is the point being demonstrated: the layouts are the system,
only the content changes.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from build import *   # noqa

BRANDS = ['#C25E3E', '#2F9468', '#5C82CE', '#B08A3E', '#8A6BC0']


# 1 -- LOGISTICS -- timeline. Stages of a delivery, current one accented.
def delivery():
    uid = 'delivery'
    b = panel(uid, 28, 104, 8, back='offset')
    ys = [56, 78, 100]
    b += rail(44, ys, tail=20)
    for i, y in enumerate(ys):
        b += bar(58, y - 7, [26, 20, 23][i], 4.2)
        b += bar(58, y + 0.6, [50, 44, 47][i], 5.2)
    b += bar(102, 22, 18, 4.6) + kebab(124, 24.5)
    chip = card(18, 14, 74, 22, 8, uid) + icon('truck', 27, 19, 13) + bar(46, 22.4, 32, 4.6)
    return uid, 'Out for delivery', svg(uid, 'Out for delivery', b, chip)


# 2 -- WAREHOUSING -- matrix. Items against bin zones.
def putaway():
    uid = 'putaway'
    b = panel(uid, 21, 118, 8, back='none')
    cols = [92, 108, 124]
    for x in (84, 100, 116, 132):
        b += vrule(x, 48, 124, 0.55)
    for i, x in enumerate(cols):
        b += icon(['barcode', 'package', 'storefront'][i], x - 5.5, 50, 11, SOFT)
    b += rule(30, 132, 66)
    for r, cells in enumerate([[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 0]]):
        y = 76 + r * 13
        b += icon('package', 31, y - 6.5, 13, SOFT)
        b += bar(48, y - 2.5, 26, 5)
        for x, on in zip(cols, cells):
            b += dot(x, y, 3, on)
    chip = card(13, 16, 62, 22, 8, uid) + icon('path', 22, 21, 12) + bar(39, 24.4, 26, 4.6)
    return uid, 'Putaway to bins', svg(uid, 'Putaway to bins', b, chip)


# 3 -- B2B FINANCE -- window. An invoice table with statuses.
def invoices():
    uid = 'invoices'
    b = panel(uid, 13, 134, 8, chrome=True, back='twin')
    states = [(ACC, True), (FILL, True), (FILL, False)]
    for i in range(3):
        y = 34 + i * 22
        c, paid = states[i]
        b += card(21, y, 118, 18, 6, uid, lift=(i == 0))
        b += icon('receipt', 26, y + 3, 12, SOFT)
        b += bar(44, y + 6.6, 20, 4.4)
        b += vrule(71, y + 4, y + 14, 0.7)
        b += bar(78, y + 6.6, 24, 4.4)
        b += vrule(109, y + 4, y + 14, 0.7)
        b += dot(117, y + 9, 3, paid, c)
        b += bar(124, y + 6.6, 8, 4.4)
        b += kebab(136, y + 9)
    return uid, 'Invoices and status', svg(uid, 'Invoices and status', b)


# 4 -- PAYMENTS -- stacked cards. Money arriving.
def payouts():
    uid = 'payouts'
    b = panel(uid, 26, 108, 30, h=100, mode='contained', back='offset')
    b += card(38, 80, 92, 32, 10, uid, lift=False)
    b += f'<circle cx="53" cy="96" r="9.5" fill="{BRANDS[1]}" opacity="0.75"/>'
    b += icon('bank', 47, 90, 12, SURF)
    b += bar(69, 89, 30, 4.8) + bar(69, 98.5, 46, 5.4)
    f = card(16, 44, 112, 34, 10, uid)
    f += f'<circle cx="33" cy="61" r="10" fill="{BRANDS[2]}" opacity="0.75"/>'
    f += icon('currency-circle-dollar', 26.5, 54.5, 13, SURF)
    f += bar(50, 52, 36, 5) + bar(50, 62, 58, 5.6)
    f += bar(50, 71.5, 22, 4.4, ACC)
    return uid, 'Payouts received', svg(uid, 'Payouts received', b, f)


# 5 -- SUPPORT -- constellation. One inbox, several teams.
def routing():
    uid = 'routing'
    b = panel(uid, 21, 118, 8, back='plate')
    for x, y in [(28, 34), (28, 82), (112, 34), (112, 82)]:
        sx, ex = (44, 63) if x < 80 else (112, 97)
        cx = (sx + ex) / 2
        b += (f'<path d="M{sx if x<80 else x} {y+8}C{cx} {y+8} {cx} 63 {ex if x<80 else 97} 63" '
              f'fill="none" stroke="{LINE}" stroke-width="{SW}" stroke-dasharray="2.4 3" '
              f'stroke-linecap="round"/>')
        b += tile(x, y)
    b += bar(52, 104, 56, 5) + bar(62, 114, 36, 4.4)
    hub = card(63, 46, 34, 34, 11, uid) + icon('ticket', 71, 54, 18)
    return uid, 'Ticket routing', svg(uid, 'Ticket routing', b, hub)


# 6 -- E-COMMERCE -- fanned cards. Variants of one product.
def variants():
    uid = 'variants'
    b = panel(uid, 16, 128, 44, h=92, mode='contained', back='none')
    for i, x in enumerate((22, 92)):
        b += card(x, 54, 46, 50, 9, uid, lift=False)
        b += f'<circle cx="{x+23}" cy="70" r="9.5" fill="{BRANDS[i*2]}" opacity="0.35"/>'
        b += bar(x + 11, 86, 24, 4.2) + bar(x + 8, 93, 30, 4.2)
    b += bar(48, 112, 64, 5) + bar(58, 121, 44, 4.4)
    mid = card(55, 32, 50, 60, 11, uid)
    mid += f'<circle cx="80" cy="52" r="12" fill="{ACC}" opacity="0.2"/>'
    mid += icon('swatches', 72.5, 44.5, 15, ACC)
    mid += bar(65, 70, 30, 4.8) + bar(61, 78.5, 38, 4.8)
    return uid, 'Product variants', svg(uid, 'Product variants', b, mid)


PROMPTS = [
    ('Out for delivery',  'track an order from the warehouse to the door', delivery),
    ('Putaway to bins',   'assign incoming stock to bin locations',        putaway),
    ('Invoices',          'issued, paid and overdue in one place',         invoices),
    ('Payouts',           'money landing in a connected account',          payouts),
    ('Ticket routing',    'send each issue to the right team',             routing),
    ('Product variants',  'sizes and colours of a single product',         variants),
]

if __name__ == '__main__':
    for _, _, fn in PROMPTS:
        uid, label, doc = fn()
        print(f'  {uid:<12} {label}')
