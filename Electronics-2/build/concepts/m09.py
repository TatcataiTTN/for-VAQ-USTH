"""Module 09 concepts: printed circuit boards and ESD (EASA M04 SM02)."""
from lib import K
M = 'm09'
K('m09-pcb-construction', M, ('Cấu tạo và vật liệu bảng mạch in', 'PCB construction and materials'),
  ('PCB là các đường dẫn mỏng trên nền cách điện (khoảng 1/16 inch = 1,5 mm, giấy tẩm epoxy hoặc vải sợi thuỷ tinh) đồng thời đỡ linh kiện; loại một lớp, hai lớp hoặc nhiều lớp.', 'A PCB is thin conductive tracks on a dielectric substrate (about 1/16 inch = 1.5 mm, epoxy-impregnated paper or fibreglass cloth) that also supports the components; it may be single, double or multi-layered.'),
  facts=[], steps=[('Làm mạch: ép nhiệt lá đồng → in mẫu bằng mực chống ăn mòn → ăn mòn phần đồng thừa (amoni persulfat hoặc sắt clorua) → phần đồng còn lại là đường dẫn.', 'Making a board: heat-press the copper foil → print the pattern with etch-resistive ink → etch away the unwanted copper (ammonium persulfate or ferric chloride) → the remaining copper is the traces.')],
  traps=[('Nhầm một lớp (đồng một mặt, linh kiện mặt kia) với hai lớp (đồng cả hai mặt).', 'Confusing single layer (copper on one side, parts on the other) with double layer (copper on both sides).')],
  angles=[('Ba loại PCB theo số lớp.', 'The three PCB types by number of layers.'), ('Các bước chế tạo đường dẫn.', 'The steps to make the tracks.')],
  topics=['PCB construction and materials'], kw=['pcb', 'printed circuit board', 'substrate', 'laminate', 'fibreglass', 'epoxy', 'copper', 'etching', 'single layer', 'double layer', 'multilayer', 'track', 'trace'], kwv=['bảng mạch in', 'pcb', 'nền cách điện', 'sợi thuỷ tinh', 'đồng', 'ăn mòn', 'một lớp', 'hai lớp', 'nhiều lớp'],
  src=['EASA M04 SM02 pp.2.1–2.3'], related=['m09-vias', 'm09-trace'])
K('m09-mounting', M, ('Công nghệ lắp linh kiện và hàn', 'Mounting technologies and soldering'),
  ('Lỗ xuyên, lỗ mạ xuyên (đồng trong lỗ dẫn điện và giữ chân chắc hơn) và dán bề mặt SMT (chân phẳng hàn lên pad, dùng được cả hai mặt); BGA có bi hàn dưới vỏ. Hàn tự động: sóng (flow) cho lỗ xuyên, hàn nóng chảy lại (reflow) cho SMT.', 'Through hole, plated through hole (copper in the hole conducts and holds the lead more firmly) and surface mount SMT (flat leads soldered to pads, both sides usable); BGA has solder balls under the package. Automated soldering: flow for through hole, reflow for SMT.'),
  facts=[], steps=[('Lỗ xuyên → hàn sóng: thiếc nóng chảy dâng qua lỗ mạ. SMT → bôi kem hàn lên pad, đặt linh kiện, nung trong lò reflow.', 'Through hole → flow soldering: molten solder rises through the plated holes. SMT → paste on the pads, place parts, melt in a reflow oven.')],
  traps=[('Dùng hàn sóng cho SMT hoặc ngược lại.', 'Using flow soldering for SMT or the reverse.'), ('Cho rằng SMT dễ hàn tay hơn: căn chỉnh và hàn khó hơn.', 'Thinking SMT is easier to hand solder: alignment and soldering are harder.')],
  angles=[('Ưu điểm của lỗ mạ xuyên?', 'Advantage of a plated through hole?'), ('Phương pháp hàn tự động cho SMT?', 'Automatic soldering method for SMT?')],
  topics=['Mounting technologies and soldering'], kw=['through hole', 'plated through hole', 'smt', 'surface mount', 'bga', 'soldering', 'reflow', 'flow soldering', 'solder paste', 'pad', 'lead'], kwv=['lỗ xuyên', 'lỗ mạ', 'dán bề mặt', 'smt', 'bga', 'hàn', 'reflow', 'kem hàn'],
  src=['EASA M04 SM02 pp.2.3–2.4'], related=['m09-pcb-construction'])
K('m09-vias', M, ('PCB nhiều lớp và via', 'Multilayer boards and vias'),
  ('Via là ống dẫn như đinh tán rỗng nối các lớp (thường một lớp là Vcc, một lớp là đất). Có via xuyên, via mù, via chôn và via dẫn nhiệt (mảng via tản nhiệt).', 'A via is like a hollow rivet joining layers (typically one layer is Vcc and one is ground). Types: through-hole via, blind via, buried via and thermal via (an array carrying heat away).'),
  facts=[], steps=[('Chọn kiểu via theo lớp cần nối: cả hai mặt (xuyên), một mặt ngoài (mù), chỉ lớp trong (chôn).', 'Pick the via type by the layers to join: both faces (through), one outer face (blind), inner layers only (buried).')],
  traps=[('Lẫn via mù (lộ một mặt) với via chôn (không lộ mặt nào).', 'Confusing a blind via (exposed on one side) with a buried via (exposed on neither).')],
  angles=[('Via chôn nối những lớp nào?', 'Which layers does a buried via join?')],
  topics=['Multilayer boards and vias'], kw=['via', 'blind via', 'buried via', 'thermal via', 'multilayer', 'inner layer', 'vcc', 'ground plane'], kwv=['via', 'via mù', 'via chôn', 'nhiều lớp', 'lớp trong', 'mặt phẳng đất'],
  src=['EASA M04 SM02 pp.2.4–2.5'], related=['m09-pcb-construction'])
K('m09-trace', M, ('Vật lý đường dẫn PCB', 'PCB trace physics'),
  ('Đường dẫn đồng có điện trở R = ρ·L/(w·t); đường mảnh và dài có điện trở lớn hơn, ở tần số cao ghép điện dung/điện cảm giữa các lớp gây nhiễu nên phải mô phỏng.', 'A copper trace has resistance R = ρ·L/(w·t); thin, long traces have higher resistance, and at high frequency capacitive/inductive coupling between layers causes interference, so modelling is needed.'),
  facts=[('R = ρ·L/(w·t)', ('ρ: điện trở suất của đồng (≈ 1,7·10⁻⁸ Ω·m); L: chiều dài; w: bề rộng; t: độ dày.', 'ρ: copper resistivity (≈ 1.7·10⁻⁸ Ω·m); L: length; w: width; t: thickness.'))],
  steps=[('Đổi mọi kích thước về mét rồi tính R.', 'Convert every dimension to metres, then compute R.')],
  traps=[('Quên đổi mm, μm sang m.', 'Forgetting to convert mm, μm to metres.')],
  angles=[('Điện trở đường dẫn dài 10 cm, rộng 0,25 mm, dày 35 μm.', 'Resistance of a trace 10 cm long, 0.25 mm wide, 35 μm thick.')],
  topics=['PCB trace physics'], kw=['trace resistance', 'resistivity', 'width', 'thickness', 'length', 'copper trace', 'coupling', 'interference', 'ρ', 'ohm'], kwv=['điện trở đường dẫn', 'điện trở suất', 'bề rộng', 'độ dày', 'chiều dài', 'ghép điện dung'],
  src=['EASA M04 SM02 (physics example, not in the text)'], related=['m09-pcb-construction'], chk='trace')
K('m09-esd-physics', M, ('Tĩnh điện và ESD', 'Static electricity and ESD'),
  ('Tĩnh điện sinh ra do ma sát; đi trên thảm tạo 1 500 V (độ ẩm 65 %) đến 35 000 V (độ ẩm 20 %); nhựa 5 000–10 000 V. Độ ẩm càng thấp thì điện tích càng lớn; cảm ứng tĩnh điện cũng nhiễm điện cho vật khác.', 'Static electricity comes from friction; walking on carpet gives 1,500 V (65 % RH) to 35,000 V (20 % RH); plastics 5,000–10,000 V. The lower the humidity the larger the charge; electrostatic induction also charges other objects.'),
  facts=[('Độ nhạy: lưỡng cực 380–7 000 V; CMOS 250–3 000 V; EPROM tới 100 V', ('Người chỉ cảm thấy tia lửa từ khoảng 3 000 V.', 'A person feels a spark only from about 3,000 V.')), ('MIL-STD-1686C: Class I = 100–1 000 V; Class II = 1 001–4 000 V', ('Phân loại độ nhạy ESD.', 'ESD susceptibility classes.'))],
  steps=[('So điện áp tĩnh có thể có với ngưỡng hỏng của linh kiện.', 'Compare the static voltage that can exist with the part\'s damage threshold.')],
  traps=[('Nghĩ không thấy tia lửa nghĩa là an toàn: vài trăm volt đã hỏng CMOS.', 'Believing no spark means safe: a few hundred volts already kill CMOS.'), ('Quên ESD gây hỏng tiềm ẩn chỉ lộ ra sau.', 'Forgetting ESD can cause latent defects that appear later.')],
  angles=[('Điện áp tĩnh khi đi trên thảm ở độ ẩm thấp?', 'Static voltage walking on carpet at low humidity?'), ('Linh kiện nào nhạy ESD nhất?', 'Which device is the most ESD-sensitive?')],
  topics=['Static electricity and ESD'], kw=['esd', 'static electricity', 'electrostatic discharge', 'friction', 'humidity', 'induction', 'triboelectric', 'susceptibility', 'mil-std-1686c', 'cmos', 'eprom'], kwv=['tĩnh điện', 'esd', 'phóng tĩnh điện', 'ma sát', 'độ ẩm', 'cảm ứng', 'độ nhạy'],
  src=['EASA M04 SM02 pp.2.6–2.9'], related=['m09-esd-protection', 'm01-families'], chk='esdtable')
K('m09-esd-protection', M, ('Chống ESD và thao tác', 'ESD protection and handling'),
  ('Tĩnh điện chỉ có thể kiểm soát, không loại bỏ: nối đất người và bàn qua điện trở 1 MΩ, dùng thảm, bao bì dẫn điện/chắn, bộ ion hoá cho vật cách điện và tránh vật liệu cách điện gần linh kiện.', 'Static can only be controlled, not eliminated: ground the person and bench through 1 MΩ, use mats, conductive/shielded packaging, ionizers for insulators, and keep insulating materials away from parts.'),
  facts=[], steps=[('Trước khi mở bao: nối dây đeo cổ tay đã nối đất. Điện trở 1 MΩ bảo vệ người nếu đất bị mang điện.', 'Before opening a bag: put on the grounded wrist strap. The 1 MΩ resistor protects the person if the ground becomes live.')],
  traps=[('Nối dây đeo cổ tay thẳng xuống đất không qua điện trở.', 'Wiring the wrist strap straight to ground without the resistor.'), ('Để nylon, mylar, nhựa gần linh kiện.', 'Leaving nylon, mylar or plastic near the parts.')],
  angles=[('Vì sao dây đeo cổ tay có điện trở 1 MΩ?', 'Why does the wrist strap contain a 1 MΩ resistor?'), ('Bao bì nào dùng để vận chuyển linh kiện nhạy ESD?', 'Which packaging carries ESD-sensitive parts?')],
  topics=['ESD protection and handling', 'PCB repair and LRMs'], kw=['wrist strap', 'mat', 'ionizer', 'shielded bag', 'grounding', 'antistatic', 'anti-static', '1 mω', 'lrm', 'lru', 'line replaceable', 'repair'], kwv=['dây đeo cổ tay', 'thảm', 'bộ ion hoá', 'bao chắn', 'nối đất', 'chống tĩnh điện', 'sửa chữa', 'lrm'],
  src=['EASA M04 SM02 pp.2.5–2.9'], related=['m09-esd-physics'])
