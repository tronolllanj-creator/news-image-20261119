from PIL import Image, ImageDraw, ImageFont
import os, sys
W, H = 1024, 1024
PAPER = (247,241,227)
INK = (20,33,61)
RED = (193,39,45)
NAVY = (27,42,74)
TEAL = (14,124,123)
GOLD = (217,164,65)
WHITE = (255,255,255)
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
_fc = {}
def font(path, size):
    key = (path, size)
    if key not in _fc:
        _fc[key] = ImageFont.truetype(path, size)
    return _fc[key]
def text_w(d, s, f):
    return d.textbbox((0,0), s, font=f)[2]
def wrap_text(d, text, f, maxw):
    words = text.split()
    lines, cur = [], []
    for w in words:
        test = ' '.join(cur + [w])
        if text_w(d, test, f) <= maxw:
            cur.append(w)
        else:
            if cur: lines.append(' '.join(cur))
            cur = [w]
    if cur: lines.append(' '.join(cur))
    return lines
def draw_wrapped(d, xy, lines, f, fill, leading):
    x, y = xy
    for ln in lines:
        d.text((x, y), ln, font=f, fill=fill)
        y += leading
def rect(d, box, fill):
    d.rectangle(box, fill=fill)
def line(d, p1, p2, width, fill):
    d.line([tuple(map(int, p1)), tuple(map(int, p2))], fill=fill, width=width)
def chip(d, x, y, maxw, label, colour):
    f = font(BOLD, 14)
    tw = text_w(d, label, f)
    w = min(tw + 16, maxw)
    r = 12
    bbox = [x, y, x + w, y + 24]
    d.rounded_rectangle(bbox, radius=r, fill=colour)
    d.text((x + (w - tw)//2, y + 4), label, font=f, fill=WHITE)
    return y + 24
def main():
    variant = sys.argv[1] if len(sys.argv) > 1 else '1'
    fn = globals().get('draw_variant' + variant)
    if fn is None:
        print('no variant', variant)
        return
    fn()
def draw_variant1():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Masthead
    rect(d, (0, 0, W, 100), NAVY)
    f_mast = font(BOLD, 36)
    tw = text_w(d, 'THE WORLD IN ONE IMAGE', f_mast)
    d.text(((W - tw)//2, 18), 'THE WORLD IN ONE IMAGE', font=f_mast, fill=WHITE)
    f_date = font(BOLD, 20)
    tw = text_w(d, 'THURSDAY 19 NOVEMBER 2026', f_date)
    d.text(((W - tw)//2, 62), 'THURSDAY 19 NOVEMBER 2026', font=f_date, fill=GOLD)
    # Lead story
    y = 110
    f_lead_h = font(BOLD, 32)
    lead_head = 'Trump, Xi and Putin hold first three-way meeting in Shenzhen; joint declaration denounces nuclear war'
    lead_lines = wrap_text(d, lead_head, f_lead_h, 960)
    draw_wrapped(d, (32, y), lead_lines[:2], f_lead_h, INK, 40)
    y += len(lead_lines[:2]) * 40 + 10
    f_lead_s = font(REG, 20)
    lead_sum = 'APEC summit yields four-point "Declaration toward Peace" on nuclear arms control and global security'
    sum_lines = wrap_text(d, lead_sum, f_lead_s, 960)
    draw_wrapped(d, (32, y), sum_lines[:2], f_lead_s, INK, 28)
    # 2x2 grid
    grid_top = 380
    cell_w = 480
    cell_h = 190
    gap = 24
    stories = [
        ('JUSTICE', 'ICJ rules Myanmar committed genocide against Rohingya', '9-6 vote in Gambia v. Myanmar over 2017 atrocities'),
        ('CONFLICT', 'Iran widens Gulf attacks on Kuwait and Bahrain', 'IEA calls Hormuz crisis greatest ever threat to energy security'),
        ('EUROPE', 'EU Commission proposes 45 billion euro loan for Ukraine', 'New aid package to support Kyiv through 2027'),
        ('CONFLICT', 'Israeli tanks cross Gaza ceasefire line in Nuseirat', 'Operation targets Hamas tunnel in central Gaza')
    ]
    for i, (cat, head, line) in enumerate(stories):
        col = i % 2
        row = i // 2
        x = 22 + col * (cell_w + gap)
        y = grid_top + row * (cell_h + 10)
        f_chip = font(BOLD, 14)
        y2 = chip(d, x, y, cell_w, cat, RED if cat=='CONFLICT' else TEAL if cat=='JUSTICE' else NAVY)
        f_gh = font(BOLD, 20)
        h_lines = wrap_text(d, head, f_gh, cell_w - 10)
        draw_wrapped(d, (x, y2 + 6), h_lines[:1], f_gh, INK, 26)
        f_gl = font(REG, 16)
        l_lines = wrap_text(d, line, f_gl, cell_w - 10)
        draw_wrapped(d, (x, y2 + 36), l_lines[:1], f_gl, INK, 22)
    # Bottom ticker strip
    ticker_y = 800
    rect(d, (0, ticker_y, W, 950), NAVY)
    f_tchip = font(BOLD, 14)
    chip(d, 22, ticker_y + 12, 300, 'CULTURE', GOLD)
    f_th = font(BOLD, 18)
    d.text((22, ticker_y + 40), 'Van Gogh painting sells for record $190.4 million', font=f_th, fill=WHITE)
    f_tt = font(REG, 16)
    d.text((22, ticker_y + 70), 'Auction sets a new record price for the artist', font=f_tt, fill=WHITE)
    # One ticker item from story 7
    d.text((540, ticker_y + 40), '• US Senate rejects Iran war-powers resolution 51-48', font=f_tt, fill=WHITE)
    d.text((540, ticker_y + 64), '• Mongolia President Khurelsukh resigns', font=f_tt, fill=WHITE)
    d.text((540, ticker_y + 88), '• Denmark approves Greenland defence deal 109-0', font=f_tt, fill=WHITE)
    # Footer
    f_foot = font(REG, 14)
    foot = 'All stories first reported 19 November 2026'
    tw = text_w(d, foot, f_foot)
    d.text(((W - tw)//2, 980), foot, font=f_foot, fill=INK)
    img.save('out_1.png')
    print('wrote out_1.png 1024x1024 bytes ' + str(os.path.getsize('out_1.png')))

def draw_variant2():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # Top navy date banner
    banner_h = 90
    rect(d, (0, 0, W, banner_h), NAVY)
    date_font = font(BOLD, 36)
    date_text = 'THURSDAY 19 NOVEMBER 2026'
    tw = text_w(d, date_text, date_font)
    d.text(((W - tw)//2, (banner_h - 36)//2), date_text, font=date_font, fill=WHITE)
    # Grid setup
    top = banner_h + 10
    panel_w = (W - 40)//3
    panel_h = (H - top - 10)//2
    gap = 10
    stories = [
        ('LEAD', RED, 'Trump, Xi, Putin hold first three-way meeting in Shenzhen', 'Joint "Declaration toward Peace" on nuclear arms control'),
        ('JUSTICE', NAVY, 'ICJ rules Myanmar committed genocide against Rohingya', '9-6 vote in Gambia v. Myanmar, 2017 atrocities'),
        ('CONFLICT', TEAL, 'Iran widens Gulf strikes on Kuwait and Bahrain', 'IEA calls Hormuz crisis greatest energy threat ever'),
        ('EUROPE', GOLD, 'EU Commission proposes 45 billion euro Ukraine loan', 'New support package for Kyiv'),
        ('CONFLICT', RED, 'Israeli tanks cross Gaza ceasefire line at Nuseirat', 'Operation targets Hamas tunnel in central Gaza'),
        ('CULTURE', TEAL, 'Van Gogh painting sells for record $190.4 million', 'Historic auction price for the artist'),
    ]
    for idx, (label, color, headline, summary) in enumerate(stories):
        row = idx // 3
        col = idx % 3
        x = 10 + col * (panel_w + gap)
        y = top + row * (panel_h + gap)
        # Panel background
        rect(d, (x, y, x + panel_w, y + panel_h), WHITE)
        d.rectangle([x, y, x + panel_w, y + panel_h], outline=INK, width=2)
        # Header chip
        chip_y = chip(d, x + 10, y + 10, panel_w - 20, label, color)
        # Headline
        h_font = font(BOLD, 20)
        h_lines = wrap_text(d, headline, h_font, panel_w - 20)
        draw_wrapped(d, (x + 10, chip_y + 8), h_lines[:2], h_font, INK, 26)
        # Summary
        s_font = font(REG, 16)
        s_lines = wrap_text(d, summary, s_font, panel_w - 20)
        sy = chip_y + 8 + len(h_lines[:2]) * 26 + 6
        draw_wrapped(d, (x + 10, sy), s_lines[:1], s_font, INK, 22)
        # Geometric icon bottom-right
        ir = 28
        ix = x + panel_w - ir - 12
        iy = y + panel_h - ir - 12
        if idx == 0:  # three circles for three leaders
            d.ellipse([ix-20, iy, ix-4, iy+16], outline=color, width=2)
            d.ellipse([ix-12, iy-4, ix+4, iy+12], outline=color, width=2)
            d.ellipse([ix-4, iy, ix+12, iy+16], outline=color, width=2)
        elif idx == 1:  # scales of justice
            d.line([ix, iy+16, ix+8, iy], fill=color, width=2)
            d.line([ix+8, iy, ix+16, iy+16], fill=color, width=2)
            d.line([ix+8, iy, ix+8, iy+20], fill=color, width=2)
            d.ellipse([ix-2, iy+18, ix+6, iy+26], outline=color, width=2)
            d.ellipse([ix+10, iy+18, ix+18, iy+26], outline=color, width=2)
        elif idx == 2:  # flame/strike
            d.polygon([(ix+8, iy), (ix+12, iy+12), (ix+4, iy+12)], fill=color)
            d.polygon([(ix+6, iy+4), (ix+10, iy+14), (ix+2, iy+14)], fill=(255,200,0))
        elif idx == 3:  # euro sign simplified
            d.ellipse([ix, iy, ix+16, iy+16], outline=color, width=2)
            d.line([ix-2, iy+6, ix+18, iy+6], fill=color, width=2)
            d.line([ix-2, iy+10, ix+14, iy+10], fill=color, width=2)
        elif idx == 4:  # tank silhouette
            rect(d, (ix, iy+10, ix+20, iy+18), fill=color)
            rect(d, (ix+4, iy+4, ix+16, iy+12), fill=color)
            d.ellipse([ix+2, iy+14, ix+6, iy+22], fill=color)
            d.ellipse([ix+14, iy+14, ix+18, iy+22], fill=color)
        else:  # paintbrush
            d.line([ix, iy+20, ix+16, iy], fill=color, width=3)
            d.polygon([(ix+14, iy+2), (ix+20, iy-2), (ix+18, iy+4), (ix+12, iy+8)], fill=RED)
    img.save('out_2.png')
    print('wrote out_2.png 1024x1024 bytes ' + str(os.path.getsize('out_2.png')))
def draw_variant3():
    img = Image.new('RGB', (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # date bar
    rect(d, (0, 0, W, 64), NAVY)
    f_date = font(BOLD, 28)
    date_text = 'THURSDAY 19 NOVEMBER 2026'
    tw = text_w(d, date_text, f_date)
    d.text(((W - tw)//2, 18), date_text, font=f_date, fill=WHITE)
    # lead headline
    f_huge = font(BOLD, 42)
    lead = 'TRUMP, XI AND PUTIN ISSUE JOINT DECLARATION AT APEC SUMMIT'
    lines = wrap_text(d, lead, f_huge, W - 80)
    y = 80
    for ln in lines:
        tw = text_w(d, ln, f_huge)
        d.text(((W - tw)//2, y), ln, font=f_huge, fill=INK)
        y += 48
    # 2-line summary
    f_sum = font(REG, 22)
    sum_lines = wrap_text(d, 'First-ever three-way summit in Shenzhen yields four-point Declaration toward Peace denouncing nuclear war and urging arms control.', f_sum, W - 100)
    for ln in sum_lines:
        tw = text_w(d, ln, f_sum)
        d.text(((W - tw)//2, y), ln, font=f_sum, fill=INK)
        y += 30
    # red rule
    y += 8
    line(d, (60, y), (W - 60, y), 3, RED)
    y += 18
    # five brief rows
    briefs = [
        ('ICJ', TEAL, 'ICJ RULES MYANMAR COMMITTED GENOCIDE AGAINST ROHINGYA', '9-6 verdict in Gambia v. Myanmar over 2017 atrocities'),
        ('IRAN', RED, 'IRAN ESCALATES GULF STRIKES ON KUWAIT AND BAHRAIN', 'IEA calls Hormuz crisis greatest ever threat to energy security'),
        ('EU', GOLD, 'EU PROPOSES 45 BILLION EURO LOAN FOR UKRAINE', 'New Commission package aims to sustain Kyiv through 2027'),
        ('GAZA', RED, 'ISRAELI TANKS CROSS CEASEFIRE LINE IN NUSEIRAT', 'Operation targets Hamas tunnel in central Gaza'),
        ('ART', NAVY, 'VAN GOGH SELLS FOR RECORD $190.4 MILLION', 'Record price for a Van Gogh at auction'),
    ]
    f_chip = font(BOLD, 14)
    f_brief_h = font(BOLD, 20)
    f_brief_s = font(REG, 18)
    for label, col, head, summ in briefs:
        # chip
        cy = chip(d, 60, y, 120, label, col)
        # headline
        d.text((200, y), head, font=f_brief_h, fill=INK)
        # summary (up to two lines)
        sum_w = W - 220
        s_lines = wrap_text(d, summ, f_brief_s, sum_w)
        for j, sl in enumerate(s_lines[:2]):
            d.text((200, y + 28 + j * 24), sl, font=f_brief_s, fill=INK)
        y = max(cy, y + 108)
    # ticker strip
    strip_h = 140
    strip_y = H - strip_h
    rect(d, (0, strip_y, W, H), NAVY)
    f_tick = font(REG, 18)
    f_foot = font(BOLD, 16)
    tick1 = 'US Senate rejects Iran war-powers resolution 51-48'
    tick2 = 'Mongolia president resigns | Denmark approves Greenland deal 109-0 | APEC adopts Shenzhen Outlook'
    # draw ticker lines centered
    for i, t in enumerate([tick1, tick2]):
        tw = text_w(d, t, f_tick)
        tx = (W - tw)//2
        ty = strip_y + 18 + i * 36
        d.text((tx, ty), t, font=f_tick, fill=WHITE)
    # footer
    foot = 'All stories first reported 19 November 2026'
    tw = text_w(d, foot, f_foot)
    d.text(((W - tw)//2, strip_y + 104), foot, font=f_foot, fill=GOLD)
    img.save('out_3.png')
    print('wrote out_3.png 1024x1024 bytes ' + str(os.path.getsize('out_3.png')))
if __name__ == '__main__':
    main()