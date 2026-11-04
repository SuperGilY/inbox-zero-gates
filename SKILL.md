---
name: inbox-zero-gates
description: Triage a Gmail inbox toward zero without blind deletion. Reads and groups mail by sender, passes every group through safety GATES, and hands the user paste-ready Gmail queries plus an HTML report. The user does the deleting.
---

# Inbox Zero with Gates

Get a cluttered Gmail inbox to near zero without losing anything that matters.
Claude reads, groups and judges. The user executes every delete or label in Gmail,
by pasting a query. Every claim passes through a gate before it reaches the user.

## What this skill will not do
- It does not trash, archive, label, send or draft anything unless the user asks for that specific action.
- It does not guess what a sender is from its name.
- It does not call a group "junk" because it is old, unread, or automated.

## The GATES (a conclusion must pass all of them)

Read `references/gates.md` for the reasoning and the incident behind each one.

| # | Gate | One-line rule |
|---|------|---------------|
| G1 | Read-only | No write action without an explicit, specific request. |
| G2 | Protected | Starred, replied-to, official, medical, insurance, tax, legal, pending bills, active job processes are never in a delete query without an explicit OK. |
| G3 | Sample before judging | Open 3 subjects per group before naming it. A sender name is not evidence. |
| G4 | Measure, do not assume | Test every heuristic (unread, age, size) with a count before using it. |
| G5 | Estimate honesty | Search counts are estimates, results carry no dates, bodies are unread. Say so. Use `list_labels` for exact totals. |
| G6 | Verify the query | Run every query before showing it. Check no protected sender appears. Parentheses around every OR group. |
| G7 | Right action type | Junk goes to Trash. Documents worth keeping get a label, then Archive. Archive is not a trash can. |
| G8 | Keepsakes | Mail the user sent to themselves, and very old personal mail, are memories. Ask once, then leave. |
| G9 | Active process | Recent job pipeline, unpaid bills, open claims and pending applications stay in the inbox. |
| G10 | Scam | Lookalike billing or "your account will be charged" mail from odd domains is phishing. Flag it, never reply, put it in Trash. |
| G11 | Tool limits | Per-thread trash tools ask approval on every call. Never loop them. Hand over a query instead. |
| G12 | One decision per group | Ask per sender group with buttons, recommended option first. Never per email. |
| G13 | Verify after | When the user says "done", re-run the same query, expect empty, report the exact inbox total. |
| G14 | Overlap | Groups overlap. State the order of execution and that totals are approximate. |
| G15 | Privacy | The report contains private subjects. Deliver it as a private file. Never publish it. |
| G16 | Know when to stop | Stop when what remains is owned by the user (starred, keepsakes, active items). Offer to stop. |

## Actions every group ends in
1. **Trash** - safe junk: promotions, shipping notices, verification codes, alerts, receipts for small purchases, expired offers.
2. **Label then Archive** - documents worth keeping: payslips, insurance, health, invoices, travel bookings, job application confirmations.
3. **Keep in inbox** - active, unpaid, protected, starred.
4. **Decide** - the user chooses. Always give a recommendation.

## First run: setup interview (do this before any scan)
The gates only protect what the skill knows is worth protecting. A stranger's inbox has different protected senders than yours, so learn them first.

**Step A - infer, read-only.** Build a candidate list from the mailbox itself:
- Senders the user has replied to: `in:sent` (sample recipients).
- Senders of starred mail: `is:starred`.
- Official-looking senders: banks, insurers, government, health providers, employers, schools (judge by sampled subjects, not by name - G3).
- Existing user labels from `list_labels`: they show how the user already thinks about their mail.

**Step B - confirm, with buttons.** Show the candidates as a short list and ask:
1. Which of these must never be touched? (multi-select; the inferred list is the recommended answer)
2. Which of your existing labels should I reuse for documents worth keeping?
3. Is there mail you keep for sentimental reasons (old personal mail, mail you sent to yourself)? Default: leave anything older than two years that is personal.
4. Are you job hunting or waiting on a process (claim, application, refund)? Those stay in the inbox (G9).
5. Language of the report, English or Hebrew?

**Step C - save the answers** as a small rules file the user keeps (protected senders, labels, keepsake rule, language). Offer it at the end of the session, and read it at the start of the next one so later runs only scan new mail.

Inference proposes, the user decides. Never treat an inferred sender as protected or as safe to delete without the confirmation in step B.

## Process
0. Confirm the account (`toRecipients` on a result). Run `list_labels` for the exact inbox total (`INBOX.threadsTotal`) and existing labels. Reuse the user's labels.
1. Estimate volume per category: `in:inbox category:updates|promotions|personal|social -is:starred` with `pageSize 1` and `THREAD_VIEW_IDS_ONLY`; read `resultCountEstimate`.
2. Sample: `THREAD_VIEW_MINIMAL`, 50 threads per slice. Find recurring senders. Exclude handled senders with `-(from:a OR from:b)` and sample again; each pass reveals the next layer.
3. For each sender group: its own count query plus 3 sample subjects (G3).
4. Classify every group into an action (above). Run it through all gates.
5. Build the final query. Run it (G6). Show it.
6. Ask per group with buttons (G12). Offer "show samples first" as an option.
7. After the user executes, verify (G13). Report the delta.
8. Repeat until G16 applies.

Do the age cut only for ambiguous personal mail. Safe junk needs no age cut.

## Gmail query rules
- `in:inbox -is:starred (from:a.com OR from:b.com)`. Parentheses around OR groups.
- `-(a b)` means NOT (a AND b). To exclude several, write `-(from:a OR from:b)`.
- Domains match subdomains in `from:` only when written as the bare domain. Test the exclusion; if the sender still appears, add the exact address.
- Hebrew subject filters match whole tokens.
- Keep one item: `-subject:"exact order number"`.
- Results over one page: tell the user to use "Select all conversations that match this search".
- `in:anywhere` for labeling archived mail.

## Report
Build with `scripts/build_report.py` from a JSON file (see `examples/example-groups.json`).
One card per group: action badge, estimated count, description, the query (always visible and selectable), a Copy button with a fallback, and a "done" checkbox saved in `localStorage` inside try/catch.
Right-to-left layout for Hebrew or Arabic. Light and dark themes. Works on a phone.

## Voice
Short, decisive, honest. Reply in the user's language, never mixed. A recommendation first, options after. State what is unknown.
