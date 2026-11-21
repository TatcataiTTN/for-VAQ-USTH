# -*- coding: utf-8 -*-
"""Nguon su that duy nhat cua site AE2.021: thong tin mon, sach, bo slide, danh sach module va anh xa nguon.
So lieu doc tu: de cuong .docx, PyMuPDF (so trang slide, bookmark Floyd), mat khau noi dung cac module cu (data/module_content.py).
Anh xa module-chuong la ban nhap cap chuong cua phien truoc; P0/P2 se kiem lai bang anh trang. CO/CLO gan cho module la DE XUAT cua site (de cuong khong gan)."""
COURSE = dict(code='AE2.021', vi='Hệ thống điện tử: Hệ thống analog và hệ thống kỹ thuật số', en='Electronics Systems: Analog Systems and Digital Systems',
              ects=4, hours=dict(lecture=50, lab=8, tutorial=0, total=58), prereq='AE2.025 Electronics 2', title_short_vi='Hệ thống điện tử số & máy tính hàng không',
              title_short_en='Aircraft Digital Electronics & Computer Systems')

CO = {  # nguyen van de cuong (tieng Anh); ban Viet la dich cua site
    'CO1': dict(en='To provide students with Basic knowledge on the operations of analog systems and digital systems in aircraft', vi='Cung cấp kiến thức cơ bản về vận hành của các hệ thống analog và hệ thống số trên tàu bay'),
    'CO2': dict(en='Convert numbers between decimal, binary, octal, and hexadecimal number systems, explain the operation of digital logic gates.', vi='Đổi số giữa hệ thập phân, nhị phân, bát phân và thập lục phân; giải thích hoạt động của các cổng logic số.'),
    'CO3': dict(en='Use Boolean algebra to express logic operations as a equations, use Karnaugh maps to minimize Boolean equations', vi='Dùng đại số Boolean biểu diễn phép logic dưới dạng phương trình; dùng bản đồ Karnaugh để tối giản phương trình Boolean.'),
    'CO4': dict(en='Understand the structure and operation of data conversion circuit and semiconductor memories', vi='Hiểu cấu trúc và hoạt động của mạch chuyển đổi dữ liệu và bộ nhớ bán dẫn.'),
    'CO5': dict(en='Define and describe the basic operation of computer system, microprocessor, and microcontroller', vi='Định nghĩa và mô tả hoạt động cơ bản của hệ máy tính, vi xử lý và vi điều khiển.'),
}
CLO = {
    'CLO1': dict(en='providing an overview of flight instruments and cockpit layouts', vi='Tổng quan về dụng cụ bay và bố trí buồng lái.'),
    'CLO2': dict(en='describes the fabrication technology and application of a wide variety of modern integrated circuits', vi='Mô tả công nghệ chế tạo và ứng dụng của nhiều loại vi mạch tích hợp hiện đại.'),
    'CLO3': dict(en='introduction to a variety of different avionic systems based on digital electronics and computers', vi='Giới thiệu các hệ avionics dựa trên điện tử số và máy tính.'),
    'CLO4': dict(en='provides an introduction to electromagnetic compatibility (EMC) and provides examples of measures that can be taken to both reduce EMI and improve EMC', vi='Giới thiệu tương thích điện từ (EMC) và các biện pháp giảm EMI và tăng EMC.'),
}

BOOKS = {
    'tooley': dict(short='Tooley', full='Mike Tooley, Aircraft Digital Electronic and Computer Systems: Principles, Operation and Maintenance, Third Edition, Routledge (bản quét 416 trang; đề cương ghi 2007)',
                   syllabus_ref=1, pdf='Latest -24 Aircraft Digital Electronic.pdf'),
    'floyd': dict(short='Floyd', full='Thomas L. Floyd, Digital Fundamentals, 11th ed., Pearson, 2015 (PDF 953 trang, 186 bookmark)', syllabus_ref=2, pdf='1667892328Digital_Fundamentals_11ed_by_Thomas_L.Floyd.pdf'),
    'aerogates': dict(short='AeroGATES M05', full='Module 05, Digital Techniques-Electronic Instrument Systems, AeroGATES PART-66 (KHÔNG có file trong thư mục: không trích)', syllabus_ref=3, pdf=None),
    'var': dict(short='VAR Part 7', full='VAR Part 7 - Aircraft Maintenance Basic Cat B1+B2, M13.04 (KHÔNG có file trong thư mục: không trích)', syllabus_ref=4, pdf=None),
}

# 9 bo slide cua giang vien (so trang do bang PyMuPDF 21/11/2026)
DECKS = {
    'num':   dict(pdf='Number system.pdf', pages=27, vi='Hệ đếm', en='Number system'),
    'logic': dict(pdf='logic circuit_version 2026.pdf', pages=60, vi='Mạch logic', en='Logic circuit'),
    'icmux': dict(pdf='integrated circuit and multiplexing version 2026.pdf', pages=60, vi='Mạch tích hợp và dồn kênh', en='Integrated circuit and multiplexing'),
    'cpu':   dict(pdf='Basic computer structure and microprocessor PDA version 2026.pdf', pages=52, vi='Cấu trúc máy tính và vi xử lý', en='Basic computer structure and microprocessor'),
    'bus':   dict(pdf='Data buses aircraft - ver 2026 v2.pdf', pages=18, vi='Bus dữ liệu tàu bay', en='Data buses aircraft'),
    'disp':  dict(pdf='Electronic displays - ver 2026.pdf', pages=36, vi='Màn hình điện tử', en='Electronic displays'),
    'fib':   dict(pdf='Optic_Fiber_ver 2026.pdf', pages=37, vi='Cáp quang', en='Optic fiber'),
    'emc':   dict(pdf='Cours_EMC_Aircraft_ver2026.pdf', pages=46, vi='EMC trên tàu bay', en='EMC and aircraft'),
    'swc':   dict(pdf='software management control.pdf', pages=6, vi='Quản lý kiểm soát phần mềm (EASA Part-66 5.13)', en='Software management control (EASA Part-66 5.13)'),
}

# id, slug (GIU NGUYEN URL CU), tieu de, CLO/CO de xuat, bo slide, sach (cap chuong), nguon. status: 'live' co noi dung, 'planned' chua co.
MODS = [
    dict(id='m01', slug='01-number-systems', vi='Hệ đếm trong hệ thống số hàng không', en='Number systems in aircraft digital data', co=['CO2'], clo=[], slides=[('num', 1, 27)], blank_slides=[],
         books=dict(tooley='Ch.2 (tr.25-38)', floyd='Ch.2 (tr.65-124)'), status='live'),
    dict(id='m02', slug='02-logic-boolean', vi='Cổng logic và đại số Boolean', en='Logic gates and Boolean algebra', co=['CO2', 'CO3'], clo=[], slides=[('logic', 1, 60)], blank_slides=[],
         books=dict(tooley='Ch.5 (tr.70-94)', floyd='Ch.3 (tr.125-190), Ch.4 (tr.191-260); chốt bistable: Ch.7'), status='live'),
    dict(id='m03', slug='03-ic-multiplexing', vi='Mạch tích hợp (IC) và kỹ thuật dồn kênh', en='Integrated circuits and multiplexing', co=[], clo=['CLO2'], slides=[('icmux', 1, 60)], blank_slides=[],
         books=dict(tooley='Ch.8-9 (tr.139-164)', floyd='Ch.6 (tr.313-386); công nghệ IC: Ch.15'), status='live'),
    dict(id='m04', slug='04-computer-cpu', vi='Cấu trúc máy tính và vi xử lý (CPU)', en='Computer structure and microprocessors (CPU)', co=['CO4', 'CO5'], clo=['CLO3'], slides=[('cpu', 1, 52)], blank_slides=[],
         books=dict(tooley='Ch.6-7 (tr.95-138)', floyd='Ch.11 Data Storage (tr.627-696)'), status='live'),
    dict(id='m05', slug='05-data-buses', vi='Bus dữ liệu hàng không', en='Aircraft data buses', co=[], clo=['CLO3'], slides=[('bus', 1, 18)], blank_slides=[],
         books=dict(tooley='Ch.4 (tr.53-69)', floyd='Ch.13 §13-6 đến 13-10 (bus chung, không phải bus hàng không)'), status='live'),
    dict(id='m06', slug='06-electronic-displays', vi='Màn hình điện tử và hệ thống thông tin buồng lái', en='Electronic displays and flight deck information systems', co=[], clo=['CLO1'], slides=[('disp', 1, 36)], blank_slides=[],
         books=dict(tooley='Ch.1; Ch.11; Ch.15 §15.1-15.3', floyd='Ch.4 Applied Logic (tr.244-249); Ch.6 §6-5, §6-8 (7 đoạn)'), status='live'),
    dict(id='m07', slug='07-software-control', vi='Quản lý kiểm soát phần mềm hàng không', en='Aircraft software management control', co=[], clo=['CLO3'], slides=[('swc', 1, 6)], blank_slides=[],
         books=dict(tooley='Ch.13 (tr.207-217)', floyd='§2-12 mã lỗi; §11-11 checksum'), status='live'),
    dict(id='m08', slug='08-fibre-optics', vi='Cáp quang trên máy bay', en='Fibre optics in aircraft', co=[], clo=[], slides=[('fib', 1, 37)], blank_slides=[],
         books=dict(tooley='Ch.10 (tr.165-177)', floyd='Ch.13 §13-1 (tr.740-745)'), status='live', outside='Đề cương không nêu cáp quang trong CO/CLO nào; giữ vì có bộ slide của giảng viên.'),
    dict(id='m09', slug='09-emc', vi='Tương thích điện từ (EMC) trên máy bay', en='Electromagnetic compatibility (EMC) in aircraft', co=[], clo=['CLO4'], slides=[('emc', 1, 46)], blank_slides=[],
         books=dict(tooley='Ch.14 (tr.218-237)', floyd='§13-1 (nhiễu xuyên âm), §6-11 (tụ tách), §15-3 (biên nhiễu)'), status='live'),
    # ---- module thêm theo quyết định 4b (21/11/2026): KHÔNG có slide của giảng viên, dựng từ sách. Tooley Ch.12 ESD (tr.197-206) gắn vào m09 như phần mở rộng. ----
    dict(id='m10', slug='10-data-conversion', vi='Chuyển đổi dữ liệu A/D và D/A', en='Data conversion: A/D and D/A', co=['CO4'], clo=[], slides=[], blank_slides=[],
         books=dict(tooley='Ch.3 (tr.39-52)', floyd='Ch.12 Signal Conversion and Processing (PDF tr.698-739)'), status='planned', noslide=True),
    dict(id='m11', slug='11-sequential-logic', vi='Mạch tuần tự: latch, flip-flop, thanh ghi dịch, bộ đếm, logic khả trình', en='Sequential logic: latches, flip-flops, shift registers, counters, programmable logic', co=[], clo=[], slides=[], blank_slides=[],
         books=dict(tooley='§5.6-5.8 (monostable, bistable, họ logic)', floyd='Ch.7 (PDF tr.388), Ch.8 (450), Ch.9 (498), Ch.10 (562)'), status='planned', noslide=True),
    dict(id='m12', slug='12-avionic-systems', vi='Hệ thống avionics số: fly-by-wire, FMS, GPS, IRS, TCAS, thiết bị thử', en='Digital avionic systems: fly-by-wire, FMS, GPS, IRS, TCAS, test equipment', co=[], clo=['CLO3'], slides=[], blank_slides=[],
         books=dict(tooley='§15.4-15.10 (tr.250-259)', floyd='không có'), status='planned', noslide=True),
    dict(id='m13', slug='13-data-networks-ima', vi='Mạng dữ liệu tàu bay, AFDX và IMA', en='Aircraft data networks, AFDX and IMA', co=[], clo=['CLO3'], slides=[], blank_slides=[],
         books=dict(tooley='Ch.16 (tr.261-275), Ch.18 (tr.294-306)', floyd='Ch.13 §13-6 đến 13-10 (bus chung, nền Ethernet/LAN là Tooley)'), status='planned', noslide=True),
    dict(id='m14', slug='14-vhdl', vi='Hệ logic cỡ lớn và ngôn ngữ mô tả phần cứng VHDL', en='Large-scale logic systems and VHDL', co=[], clo=['CLO2'], slides=[], blank_slides=[],
         books=dict(tooley='Ch.17 (tr.277-293)', floyd='Ch.10 Programmable Logic (PDF tr.562; phần HDL)'), status='planned', noslide=True),
    dict(id='m15', slug='15-cabin-information', vi='Hệ thống cabin và hệ thống thông tin tàu bay', en='Cabin systems and aircraft information systems', co=[], clo=['CLO3'], slides=[], blank_slides=[],
         books=dict(tooley='Ch.19 (tr.307-316), Ch.20 (tr.317-335)', floyd='không có'), status='planned', noslide=True),
]
for _m in MODS:
    _m['src'] = [f"Slide: {DECKS[d]['en']} tr.{a}-{b}" for d, a, b in _m['slides']] + [f"Tooley {_m['books']['tooley']}", f"Floyd {_m['books']['floyd']}"]
    if _m.get('noslide'): _m['src'].insert(0, 'Không có slide của giảng viên cho mục này (dựng từ sách)')
BYID = {m['id']: m for m in MODS}
LIVE = [m for m in MODS if m['status'] == 'live']

def slides_of(m):
    return [(d, p) for d, a, b in m['slides'] for p in range(a, b + 1)]

def check():
    """Cong P1: moi trang slide thuoc dung mot module; so trang khop DECKS."""
    seen = {}
    for m in MODS:
        for d, p in slides_of(m):
            assert (d, p) not in seen, f'slide {d} {p} thuoc hai module: {m["id"]} va {seen[(d,p)]}'
            seen[(d, p)] = m['id']
    for d, info in DECKS.items():
        miss = [p for p in range(1, info['pages'] + 1) if (d, p) not in seen]
        assert not miss, f'bo {d}: trang chua co module {miss[:5]}'
    return len(seen)

if __name__ == '__main__':
    print('slide co module:', check(), 'tren', sum(i['pages'] for i in DECKS.values()))
