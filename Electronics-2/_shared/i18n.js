/* UI strings by <html lang>. Content text comes from data, never from here. */
(function(){
var L=(document.documentElement.lang||'vi').slice(0,2);
var S={
vi:{score:'Điểm',done:'câu đã làm',correct:'✅ Chính xác!',wrongAns:'❌ Chưa đúng. Đáp án đúng: ',retryOne:'↺ Làm lại câu này',retryAll:'↺ Làm lại toàn bộ bài',confirmAll:'Xóa kết quả và làm lại từ đầu?',
 panel:'Bảng điều khiển',source:'Nguồn:',all:'Tất cả',orig:'Câu gốc từ sách',gen:'Bổ sung (sinh tự động)',level:'Mức độ:',l1:'Cơ bản (1)',l2:'Vừa (2)',l3:'Khó (3)',topic:'Chủ đề:',type:'Dạng:',onlyWrong:' chỉ câu đã làm sai',
 shuffle:'🔀 Xáo trộn thứ tự',reset:'↺ Làm lại toàn bộ (xóa kết quả)',confirmReset:'Xóa toàn bộ kết quả của ngân hàng này và làm lại từ đầu?',origOrder:'⟲ Về thứ tự gốc',
 progress:function(a,n,c){return 'Tiến độ: đã làm '+a+'/'+n+' câu · đúng '+c+' · sai '+(a-c)+(a?' · tỉ lệ đúng '+Math.round(100*c/a)+'%':'')},
 mcq:'Trắc nghiệm',ess:'Tự luận',showing:function(n,p,P){return 'Hiển thị '+n+' câu — trang '+p+'/'+P},prev:'◀ Trang trước',next:'Trang sau ▶',
 origTag:'📎 Câu gốc · ',genTag:'➕ Bổ sung · ',lvl:'mức ',essIntro:'Tự luận: tự làm nháp trước, rồi bấm "Xem lời giải" để đối chiếu.',
 showSol:'👁 Xem lời giải',hideSol:'🙈 Ẩn lời giải',mark:'Đánh dấu: tôi đã làm được',marked:'✔ Đã làm được (bấm để bỏ)',essDone:function(d,n){return 'Đã làm được '+d+'/'+n+' bài tự luận'},
 set:'Đề',minutes:'phút',qs:'câu',timeLeft:'Thời gian còn lại: ',submit:'Nộp bài',retrySet:'↺ Làm lại đề này',ok:'✅ Đúng',noAns:'⚪ Chưa trả lời. Đáp án: ',bad:'❌ Sai. Đáp án đúng: ',
 result:function(s,n){return 'Kết quả: '+s+'/'+n+' câu đúng ('+(s*10/n).toFixed(2)+' điểm thang 10).'},kinds:{mcq:'Trắc nghiệm',tf:'Đúng/Sai',ca:'Mạch – tăng/giảm'},
 prevS:'◀ Trước',nextS:'Sau ▶',fs:'⛶ Toàn màn hình',expl:'📖 Giải thích cho người mới bắt đầu'},
en:{score:'Score',done:'answered',correct:'✅ Correct!',wrongAns:'❌ Not quite. Correct answer: ',retryOne:'↺ Retry this question',retryAll:'↺ Restart the whole quiz',confirmAll:'Clear results and start over?',
 panel:'Control panel',source:'Source:',all:'All',orig:'Original (textbook)',gen:'Generated (extra)',level:'Level:',l1:'Basic (1)',l2:'Medium (2)',l3:'Hard (3)',topic:'Topic:',type:'Type:',onlyWrong:' only questions I got wrong',
 shuffle:'🔀 Shuffle',reset:'↺ Reset all (clear results)',confirmReset:'Clear all results of this bank and start over?',origOrder:'⟲ Original order',
 progress:function(a,n,c){return 'Progress: '+a+'/'+n+' answered · '+c+' correct · '+(a-c)+' wrong'+(a?' · '+Math.round(100*c/a)+'% correct':'')},
 mcq:'Multiple choice',ess:'Worked problems',showing:function(n,p,P){return 'Showing '+n+' questions — page '+p+'/'+P},prev:'◀ Previous page',next:'Next page ▶',
 origTag:'📎 Original · ',genTag:'➕ Generated · ',lvl:'level ',essIntro:'Worked problems: solve on paper first, then click "Show solution" to compare.',
 showSol:'👁 Show solution',hideSol:'🙈 Hide solution',mark:'Mark: I solved it',marked:'✔ Solved (click to undo)',essDone:function(d,n){return 'Solved '+d+'/'+n+' problems'},
 set:'Set',minutes:'min',qs:'questions',timeLeft:'Time left: ',submit:'Submit',retrySet:'↺ Retry this set',ok:'✅ Correct',noAns:'⚪ Not answered. Answer: ',bad:'❌ Wrong. Correct answer: ',
 result:function(s,n){return 'Result: '+s+'/'+n+' correct ('+(s*10/n).toFixed(2)+' / 10).'},kinds:{mcq:'Multiple choice',tf:'True/False',ca:'Circuit action'},
 prevS:'◀ Prev',nextS:'Next ▶',fs:'⛶ Full screen',expl:'📖 Explanation for beginners'}};
window.T=S[L]||S.vi;window.LETTERS='ABCDEF';
})();
