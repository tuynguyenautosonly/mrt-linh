/* Original Vietnamese excerpts from stored controlled exercises; English is an editorial translation. */
export const reviewedQA = [
  {
    "id": "recorded-training-01",
    "titleVi": "Có số đo, vẫn cần biết mạch điều khiển",
    "titleEn": "Measurements still need circuit context",
    "questionVi": "Bài tập xe khác, không ghi hồ sơ: mô-tơ cửa kính chạy yếu. Khi đang có lệnh chạy, ắc quy 13,8 V; chân X so với âm ắc quy 13,4 V; chân Y so với âm ắc quy 1,7 V. Chưa có sơ đồ hoặc thông số kiểm tra. Anh cần một nhận định và bước kiểm tiếp ngắn để quyết định có sửa dây hay thay mô-tơ không.",
    "answerVi": "**Nhận định**\n\nChân X: 13,4 V so với âm ắc quy — chưa đánh giá được, chưa có ngưỡng cho phép sụt áp trên đường dương của mô-tơ cửa này.\n\nChân Y: 1,7 V so với âm ắc quy — chưa biết kiểu điều khiển. Có thể là mát thụ động bị trở kháng cao, có thể là PWM âm. Hai trường hợp cho cùng số đo nhưng kết luận ngược nhau — chưa đánh giá được.\n\nChưa có sơ đồ → chưa kết luận nhánh nào tốt hay hỏng.\n\n---\n\n**Bước kiểm tiếp**\n\nLấy sơ đồ điện xác nhận kiểu điều khiển chân Y trước — mát thụ động hay PWM âm. Đây là điều kiện để mọi bước đo tiếp theo có nghĩa.\n\nNếu Y là mát thụ động: đo sụt áp dọc đường mát (từng đoạn: chân Y → connector → mass point → âm ắc quy) khi đang có dòng, không đổi mạch.\n\nNếu Y là PWM âm: oscilloscope xem duty cycle, đối chiếu với lệnh tốc độ từ module.",
    "questionEn": "A different-vehicle exercise; do not save it as a real record: a power-window motor runs weakly. While it is commanded on, the battery measures 13.8 V, terminal X measures 13.4 V relative to battery negative, and terminal Y measures 1.7 V relative to battery negative. No wiring diagram or test specifications are available. I need a brief assessment and a useful next check before deciding to repair wiring or replace the motor.",
    "answerEn": "Assessment\n\nTerminal X: 13.4 V relative to battery negative — not yet assessable, because the allowable positive-side voltage-drop limit for this window motor is unknown.\n\nTerminal Y: 1.7 V relative to battery negative — its control arrangement is unknown. It could be a passive ground path with high resistance, or low-side PWM. The same reading could support different interpretations, so it is not yet assessable.\n\nWithout the diagram, neither branch can be declared good or faulty.\n\nNext check\n\nObtain the wiring diagram to identify terminal Y as passive ground or low-side PWM first. This gives meaning to the subsequent measurements.\n\nIf Y is passive ground: measure voltage drop along its sections under load, without altering the circuit.\n\nIf Y is low-side PWM: use an oscilloscope to inspect duty cycle and compare it with the module’s speed command.",
    "reviewVi": "Đã rà nguyên lý: chưa đủ sơ đồ/ngưỡng thì chưa chốt nhánh tốt hay hỏng; phân biệt đường mát thụ động với PWM. Không phải thông số hoặc quy trình OEM cho xe thật.",
    "reviewEn": "Reviewed principle: missing circuit context and limits prevent a pass/fail conclusion; passive ground and PWM control must be distinguished. This is not an OEM specification or a real-vehicle repair procedure.",
    "references": [
      {
        "title": "Fluke: voltage-drop testing",
        "url": "https://www.fluke.com/en-au/learn/blog/automotive/electrical-automotive-troubleshooting"
      },
      {
        "title": "Pico Automotive: PWM signals",
        "url": "https://www.picoauto.com/support/viewtopic.php?t=22356"
      }
    ]
  },
  {
    "id": "recorded-training-02",
    "titleVi": "Lỗi chập chờn: cần dữ kiện đúng lúc lỗi",
    "titleEn": "Intermittent faults need evidence at the failure",
    "questionVi": "Bài tập xe khác, không ghi hồ sơ: quạt PWM âm đôi khi dừng. Trước lúc dừng, nhánh dương đã đạt giới hạn bài tập và dạng sóng bám lệnh 42%. Chưa ghi được điện áp hoặc dạng sóng đúng thời điểm quạt dừng; tải cơ cũng chưa kiểm. Thợ cho rằng thế là đã loại hẳn nguồn và driver, nên thay mô-tơ. Em phản biện và chọn hướng kiểm tiếp ngắn giúp anh.",
    "answerVi": "**Phản biện**\n\nThợ kết luận loại hẳn nguồn và driver dựa trên hai dữ kiện: nhánh dương đạt giới hạn bài tập và dạng sóng bám lệnh 42% — cả hai đo được **trước lúc dừng**, không phải đúng lúc dừng.\n\nHai điểm chưa loại được:\n\n**Nguồn/mát:** Đạt tại điểm đo, tải và thời điểm đã kiểm — chỉ loại được trong phạm vi đó. Lỗi chập chờn có thể xuất hiện ở điểm khác hoặc thời điểm khác; chưa có dữ kiện đúng lúc quạt dừng thì chưa loại được.\n\n**Driver:** Dạng sóng bám lệnh trước lúc dừng không chứng minh driver hoạt động đúng đúng lúc lỗi. Driver vẫn là ứng viên chưa loại.\n\nTải cơ cũng chưa kiểm — kẹt cơ học gây dừng đột ngột là ứng viên song song.\n\n---\n\n**Hướng kiểm tiếp, không đổi mạch:**\n\nGhi đồng thời lệnh, dạng sóng PWM và dòng mô-tơ **đúng lúc quạt dừng** — scope hoặc data logger. Xem cái nào thay đổi trước: lệnh mất, dạng sóng mất, dòng tăng đột biến, hay dòng về 0 trong khi lệnh vẫn giữ. Kết quả đó mới phân biệt được driver, nguồn chập chờn và mô-tơ/tải cơ.",
    "questionEn": "A different-vehicle exercise; do not save a real record: a low-side PWM fan sometimes stops. Before it stops, the positive branch meets the exercise limit and the waveform follows the 42% command. No voltage or waveform has been captured at the moment of stopping; mechanical load has not been checked. A technician says this rules out the supply and driver, so the motor should be replaced. Challenge that conclusion and suggest a brief next check.",
    "answerEn": "Challenge\n\nThe supply and driver were ruled out using two observations: the positive branch met the exercise limit, and the waveform followed the 42% command. Both were captured before the stop, not at the failure.\n\nTwo things remain unexcluded:\n\nSupply/ground: the test passed at the point, load and time checked. An intermittent fault could occur elsewhere or at another time. Without data at the stop, it has not been ruled out.\n\nDriver: following the command before the stop does not prove correct operation during the failure. The driver remains a candidate.\n\nMechanical load has not been checked either; binding is another candidate.\n\nNext check, without altering the circuit\n\nRecord the command, PWM waveform and motor current simultaneously at the moment the fan stops, using a scope or data logger. Look for what changes first: loss of command, loss of waveform, a current spike, or current falling to zero while the command remains. That evidence can distinguish driver, intermittent supply and motor/mechanical-load hypotheses.",
    "reviewVi": "Đã rà phạm vi suy luận: kết quả trước lúc lỗi không tự loại lỗi chập chờn; driver và tải cơ vẫn cần đối chiếu. Chưa xác nhận một phụ tùng hỏng hoặc một ca sửa thành công.",
    "reviewEn": "Reviewed inference boundary: a pre-failure pass does not exclude an intermittent fault; the driver and mechanical load still need examination. No failed part or successful repair is established.",
    "references": [
      {
        "title": "Fluke: voltage-drop testing",
        "url": "https://www.fluke.com/en-au/learn/blog/automotive/electrical-automotive-troubleshooting"
      },
      {
        "title": "Pico Automotive: PWM signals",
        "url": "https://www.picoauto.com/support/viewtopic.php?t=22356"
      }
    ]
  }
];
