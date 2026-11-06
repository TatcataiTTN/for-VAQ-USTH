"""Module 06 concepts: active filters (Floyd 9e Ch.15)."""
from lib import K
M = 'm06'
K('m06-poles', M, ('Cực, bậc bộ lọc và tốc độ suy giảm', 'Poles, filter order and roll-off'),
  ('Mỗi cực là một mạch RC; bậc bộ lọc bằng số cực. Nhiều cực hơn thì sườn dốc hơn: −20 dB/decade cho mỗi cực (−6 dB/octave).', 'Each pole is one RC circuit; the filter order equals the number of poles. More poles give a steeper skirt: −20 dB/decade per pole (−6 dB/octave).'),
  facts=[('fc = 1/(2π·R·C)', ('Tần số cắt của một cực; tại fc độ lợi −3 dB.', 'Cutoff of one pole; the gain is −3 dB at fc.')), ('suy giảm = −20 dB/decade × (số cực)', ('Hai cực: −40 dB/decade; bốn cực: −80.', 'Two poles: −40 dB/decade; four: −80.'))],
  steps=[('Đếm số cực = số mạch RC.', 'Count the poles = number of RC sections.'), ('Suy giảm ở một tần số: số cực × 20 × log₁₀(f/fc).', 'Attenuation at a frequency: poles × 20 × log₁₀(f/fc).')],
  traps=[('Cho rằng suy giảm là −20 dB mỗi octave: đó là −6 dB/octave.', 'Quoting −20 dB per octave: it is −6 dB/octave.'), ('Quên rằng tại fc suy giảm chỉ 3 dB.', 'Forgetting the attenuation at fc is only 3 dB.')],
  angles=[('Bộ lọc 4 cực: suy giảm ở 10·fc?', '4-pole filter: attenuation at 10·fc?'), ('Bao nhiêu cực để đạt −60 dB/decade?', 'How many poles for −60 dB/decade?')],
  topics=['Filter responses and poles'], kw=['pole', 'poles', 'order', 'roll-off', 'db/decade', 'octave', 'skirt', 'cutoff frequency', 'attenuation', 'passband', 'stopband'], kwv=['số cực', 'bậc của bộ lọc', 'bộ lọc bậc', 'độ dốc', 'db/decade', 'octave', 'tần số cắt', 'dải thông', 'dải chắn', 'suy giảm'],
  src=['Floyd 9e §15–1'], related=['m06-characteristics', 'm06-sallen-key'], chk='poles')
K('m06-characteristics', M, ('Butterworth, Chebyshev, Bessel và hệ số tắt dần', 'Butterworth, Chebyshev, Bessel and the damping factor'),
  ('Ba đặc tính đáp ứng: Butterworth (dải thông phẳng nhất), Chebyshev (sườn dốc nhất, gợn trong dải thông), Bessel (pha tuyến tính, ít méo xung). Hệ số tắt dần DF quyết định bạn có đặc tính nào.', 'Three response characteristics: Butterworth (maximally flat passband), Chebyshev (steepest skirt, ripple in the passband), Bessel (linear phase, little pulse distortion). The damping factor DF decides which one you get.'),
  facts=[('DF = 2 − R1/R2 (mỗi tầng hai cực)', ('Butterworth hai cực: DF = 1,414 → R1/R2 = 0,586.', 'Two-pole Butterworth: DF = 1.414 → R1/R2 = 0.586.')), ('Butterworth 6 cực: DF = 1,932; 1,414; 0,518', ('R1/R2 = 0,068; 0,586; 1,482.', 'R1/R2 = 0.068; 0.586; 1.482.'))],
  steps=[('Chọn đặc tính theo yêu cầu: phẳng → Butterworth; dốc → Chebyshev; pha → Bessel.', 'Choose by need: flat → Butterworth; steep → Chebyshev; phase → Bessel.'), ('Lấy DF của từng tầng từ bảng rồi R1/R2 = 2 − DF.', 'Take each stage\'s DF from the table, then R1/R2 = 2 − DF.')],
  traps=[('Đổi chỗ: Bessel không phải loại dốc nhất.', 'Swapping them: Bessel is not the steepest.'), ('Dùng cùng DF cho mọi tầng khi ghép nhiều tầng.', 'Using the same DF for every stage in a cascade.')],
  angles=[('Đặc tính nào có dải thông phẳng nhất?', 'Which characteristic has the flattest passband?'), ('Tính R1/R2 cho bộ lọc Butterworth hai cực.', 'Find R1/R2 for a two-pole Butterworth filter.')],
  topics=['Butterworth, Chebyshev, Bessel; damping'], kw=['butterworth', 'chebyshev', 'bessel', 'damping factor', 'df', 'maximally flat', 'ripple', 'linear phase', 'q factor'], kwv=['butterworth', 'chebyshev', 'bessel', 'hệ số tắt dần', 'phẳng nhất', 'gợn sóng', 'pha tuyến tính'],
  src=['Floyd 9e §15–1, 15–2'], related=['m06-sallen-key', 'm06-cascade'], chk='characteristics')
K('m06-sallen-key', M, ('Bộ lọc thông thấp Sallen-Key hai cực', 'Two-pole Sallen-Key low-pass filter'),
  ('Hai mạch RC đặt fc, bộ chia R1/R2 ở mạch hồi tiếp đặt hệ số tắt dần. Đổi chỗ R và C thì thành bộ lọc thông cao với cùng fc và cùng đặc tính.', 'Two RC sections set fc, and the R1/R2 divider in the feedback sets the damping. Swapping the resistors and capacitors gives the high-pass filter with the same fc and characteristic.'),
  facts=[('fc = 1/(2π√(RA·RB·CA·CB))', ('Với R và C bằng nhau: fc = 1/(2πRC).', 'With equal R and C: fc = 1/(2πRC).')), ('Butterworth: DF = 1,414 → R1/R2 = 0,586', ('Độ lợi băng thông = 1 + R1/R2 = 1,586.', 'Passband gain = 1 + R1/R2 = 1.586.'))],
  steps=[('Chọn fc → chọn C, tính R = 1/(2π·fc·C).', 'Pick fc → choose C, compute R = 1/(2π·fc·C).'), ('Chọn R1/R2 = 2 − DF cho đặc tính mong muốn.', 'Choose R1/R2 = 2 − DF for the wanted characteristic.')],
  traps=[('Dùng chung một giá trị fc cho cả bộ thông thấp và bộ thông cao mà không đổi R/C.', 'Reusing fc for the low-pass and high-pass without swapping R and C.')],
  angles=[('Tính fc khi RA = RB = 10 kΩ, CA = CB = 15 nF.', 'Compute fc for RA = RB = 10 kΩ, CA = CB = 15 nF.'), ('Chọn R1/R2 để có đáp ứng Butterworth.', 'Choose R1/R2 for a Butterworth response.')],
  topics=['Low-pass filters', 'High-pass filters'], kw=['sallen-key', 'sallen key', 'low-pass', 'low pass', 'high-pass', 'high pass', 'active filter', 'two-pole', 'fc'], kwv=['sallen-key', 'thông thấp', 'thông cao', 'bộ lọc tích cực', 'hai cực'],
  src=['Floyd 9e §15–2, 15–3'], related=['m06-characteristics', 'm06-poles'], chk='sallenkey')
K('m06-cascade', M, ('Ghép bộ lọc để tăng bậc', 'Cascading filters for higher order'),
  ('Ghép các tầng hai cực thì số cực cộng lại (2 + 2 = 4 cực → −80 dB/decade). Mỗi tầng dùng DF riêng để tổng là Butterworth.', 'Cascading two-pole stages adds their poles (2 + 2 = 4 poles → −80 dB/decade). Each stage uses its own DF so the total is Butterworth.'),
  facts=[('Số cực tổng = Σ số cực từng tầng', ('Tốc độ suy giảm theo số cực tổng.', 'Roll-off follows the total pole count.'))],
  steps=[('Chia bậc thành các tầng hai cực (cộng một tầng một cực nếu lẻ).', 'Split the order into two-pole stages (plus a one-pole stage if odd).'), ('Tra DF của từng tầng theo bậc.', 'Look up each stage DF for the order.')],
  traps=[('Dùng DF = 1,414 cho mọi tầng của bộ lọc bậc cao.', 'Using DF = 1.414 for every stage of a high-order filter.')],
  angles=[('Cần mấy tầng hai cực cho bộ lọc 6 cực?', 'How many two-pole stages for a 6-pole filter?')],
  topics=['Filter responses and poles', 'Butterworth, Chebyshev, Bessel; damping'], kw=['cascade', 'cascaded filters', 'four-pole', 'six-pole', 'higher order', 'second-order stages'], kwv=['ghép tầng bộ lọc', 'bốn cực', 'sáu cực', 'bậc cao'],
  src=['Floyd 9e §15–2'], related=['m06-characteristics', 'm06-poles'], chk='cascadefilter')
K('m06-bandpass', M, ('Bộ lọc thông dải và chắn dải', 'Band-pass and band-stop filters'),
  ('Thông dải chỉ cho qua một dải quanh f0; Q = f0/BW. Có thể ghép thông thấp với thông cao (fc thấp < fc cao) hoặc dùng mạch hồi tiếp nhiều đường; chắn dải là tổng ngõ ra thông thấp và thông cao cách xa nhau.', 'A band-pass passes only a band around f0; Q = f0/BW. Build it by cascading a low-pass and a high-pass (HP fc < LP fc) or with a multiple-feedback circuit; a band-stop is the sum of a low-pass and a high-pass output that are well separated.'),
  facts=[('f0 = (1/2πC)√((R1 + R3)/(R1·R2·R3)) ,  BW = 1/(π·R2·C) ,  Q = f0/BW', ('Thông dải hồi tiếp nhiều đường, hai tụ bằng nhau.', 'Multiple-feedback band-pass with two equal capacitors.')), ('f0 = √(fc1·fc2)', ('Tần số trung tâm là trung bình nhân hai tần số cắt.', 'The centre frequency is the geometric mean of the two cutoffs.'))],
  steps=[('BW = fc2 − fc1; Q = f0/BW.', 'BW = fc2 − fc1; Q = f0/BW.'), ('Đặt R2 theo BW rồi chọn R1, R3 theo f0 và độ lợi.', 'Set R2 from BW, then R1, R3 from f0 and the gain.')],
  traps=[('Dùng trung bình cộng thay vì trung bình nhân cho f0.', 'Using the arithmetic instead of the geometric mean for f0.'), ('Nhầm Q lớn với dải rộng: Q lớn là dải HẸP.', 'Mixing up high Q with a wide band: high Q is a NARROW band.')],
  angles=[('fc1 = 1 kHz, fc2 = 4 kHz: f0, BW, Q?', 'fc1 = 1 kHz, fc2 = 4 kHz: f0, BW, Q?'), ('Chắn dải hoạt động thế nào?', 'How does a band-stop work?')],
  topics=['Band-pass and band-stop filters'], kw=['band-pass', 'band pass', 'band-stop', 'notch', 'band-reject', 'center frequency', 'bandwidth', 'q', 'multiple-feedback', 'state-variable', 'quality factor'], kwv=['thông dải', 'chắn dải', 'notch', 'tần số trung tâm', 'băng thông', 'hệ số phẩm chất', 'hồi tiếp nhiều đường'],
  src=['Floyd 9e §15–4, 15–5'], related=['m06-sallen-key', 'm06-poles'], chk='bandpass')
