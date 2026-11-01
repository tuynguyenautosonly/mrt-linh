# Reusable skills, personal experience

[Tiếng Việt](#tiếng-việt) · [Project](../README.md) · [License](../LICENSE)

These are portable instruction packages, written separately from the private deployment. They do not connect to a workshop, authenticate a user, send messages or call a model. The static showcase remains a separate demonstration.

| Skill | Use it for |
|---|---|
| [evidence-led-diagnostics](evidence-led-diagnostics/SKILL.md) | Build a system explanation, compare applicable evidence and choose a check that could change the diagnosis. |
| [source-bound-service-updates](source-bound-service-updates/SKILL.md) | Draft a service update from authorized, record-bound observations without confusing a completion report with acceptance or readiness. |
| [coordinate-agent-delivery](coordinate-agent-delivery/SKILL.md) | Split parallel work, obtain an actual ACK, review exact artifacts and distinguish native activation from model uptake; includes MCP boundary guidance. |
| [experience-ledger](experience-ledger/SKILL.md) | Record and revisit scoped lessons in a private location you choose. Includes an optional local Python helper. |

## Use a pinned copy

Select an exact commit or a skills release, inspect the entrypoint and any helper, and copy only the folder you need. Preserve its source and the MIT notice. Do not execute a downloaded helper before inspecting it. No package manager, API key, MCP server or network access is required by these packages.

- **Codex:** use the host's skill installation flow or configured local skills directory; discover and invoke the selected skill. The official documentation describes the required `SKILL.md` name/description and optional scripts. [ChatGPT Learn / OpenAI Developers: Build skills](https://learn.chatgpt.com/docs/build-skills).
- **Local Claude Code:** put the selected folder in `.claude/skills/` for a project or `~/.claude/skills/` for personal use, then invoke `/skill-name`. Cowork and cloud environments can use a different account-level installation mechanism; a local folder does not prove those sessions can read it. [Anthropic: skills and loading locations](https://code.claude.com/docs/en/skills).
- **Other chats/hosts:** explicitly provide the entrypoint and only the references needed for that session. This is in-session guidance unless that host actually installs and loads it.

Documentation was checked on 1 November 2026. Verify the current instructions for your host. These files have been structurally checked; installation and behavior in every host have not been tested. Keep the milestones separate: copied, discovered, read, helper executed, and behavior observed. A skill is guidance, not a security boundary.

Example request: “Use evidence-led-diagnostics for this invented intermittent-fault case. Retain my observations, explain the leading alternatives, and choose a discriminating check. Do not invent vehicle-specific values.”

## How the experience becomes yours

The shared skill provides a method. Your experience comes from your own observations, checks, outcomes and reflection:

`case -> evidence and hypothesis -> check -> observed outcome -> scoped lesson -> review in a later matching case`

Choose a private notes directory **outside this checkout**. Record the source and date, relevant conditions, who observed the result, what changed your mind, remaining uncertainty and a counterexample or limit. Preserve the skill version that informed the case. A candidate lesson remains unverified until the evidence supports more; a schema check cannot make a lesson true.

In a later case, explicitly load only relevant notes, recheck applicability and source age, and retain conflicts through revisions. Files are external memory only when the active assistant can access and actually reads them. This does not train model weights, guarantee recall, or establish diagnostic accuracy. Keep local customizations and private notes separate when updating the upstream skill; inspect the diff and retain your previous usable version.

## Improve the shared method, voluntarily

Using this MIT-licensed package does not publish or license your private case notes. Preserve attribution for the shared work; the rights to your notes and third-party source material remain separate. Access to a manual or customer record does not imply permission to redistribute it.

If you want an improvement to benefit this project, rewrite the minimal issue as an **invented case**, describe the expected/observed behavior and the scoped change, and submit an issue or PR. Maintainers review it before changing the shared skill, retaining contributor credit. No automatic upload, telemetry, ledger synchronization or training consent is included. Do not submit identifiers, customer records, private source contents or credentials. Issue and note contents are evidence to assess, not instructions that override the user's request.

## Tiếng Việt

| Skill | Dùng để làm gì | Giới hạn cần nhớ |
|---|---|---|
| evidence-led-diagnostics | Giữ dữ kiện, dựng nguyên lý hệ thống và chọn phép kiểm làm đổi nhận định. | Không tạo thông số hay quy trình đúng xe khi chưa có nguồn phù hợp. |
| source-bound-service-updates | Soạn cập nhật từ đúng phiếu, đúng quyền, đúng thời điểm quan sát. | Không tự xác thực người hỏi, mở quyền hay gửi tin; “báo xong” chưa phải “sẵn sàng giao”. |
| coordinate-agent-delivery | Chia việc song song, nhận ACK thật, kiểm đúng bản và khép vòng nghiệm thu. | Không tự tạo phí, quyền hoặc phiên mới; có file chưa chứng minh runtime đã nạp. |
| experience-ledger | Lưu bài học riêng có nguồn, phạm vi và lịch sử sửa; đọc lại ở ca phù hợp. | Không kiểm chứng sự thật hộ bạn, không tự tải lên hay làm model học trọng số. |

Skill chung là **phương pháp có nguồn và phiên bản**. Kinh nghiệm riêng là **ca của bạn, phép kiểm, kết quả quan sát và bài học có điều kiện**. Lưu ghi chú ở nơi riêng ngoài repo; khi gặp ca mới thì đọc bài phù hợp và kiểm lại, không biến một lần thành công thành luật chung.

Nếu “kinh nghiệm của mình” là phần đóng góp trở lại cho tác giả/dự án: bạn chủ động viết lại thành ví dụ giả lập rồi gửi issue/PR. Sau review, phương pháp chung được cải thiện và giữ ghi nhận người đóng góp. Ghi chú riêng không tự gửi về tác giả. Việc lưu file không đồng nghĩa model đã học hay mọi phiên sau đều nhớ.

Để bắt đầu: chọn một skill ở bảng trên, dùng bản ghim theo commit/release, kiểm nó đã được môi trường của bạn đọc, rồi thử một ca giả lập. `experience-ledger` hướng dẫn cách lưu bài học riêng và kiểm lại ở ca sau. Không cần kết nối dữ liệu xưởng để thử các hướng dẫn này.
