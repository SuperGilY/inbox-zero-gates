# The gates, and the incident behind each

Each gate exists because the opposite assumption failed in a real session while taking a real inbox from about 5,400 threads to about 270.

## G1 Read-only
Reading and judging are free. Changing the mailbox is not. The user asked for a reviewer, not a janitor.

## G2 Protected
A short list kept the user safe through every pass: starred mail, anything the user replied to, government and tax bodies, insurers, medical forms and replies, universities, a credit union, an unpaid utility bill, a vehicle license receipt, and every recruiter or company the user applied to. These senders were excluded from queries by default and only released on an explicit "yes".

## G3 Sample before judging
Incident: a sender group was described as "login notices" from its name. Opening subjects showed most of it was purchase receipts. The label was wrong, the recommendation changed.
Rule: three real subjects per group before naming it.

## G4 Measure, do not assume
Incident: the assumption "the bulk is mail that was never opened" was untested. A count showed zero unread mail older than two years, so the criterion was dropped.
Rule: before using a heuristic, count it.

## G5 Estimate honesty
- `resultCountEstimate` is an estimate and drifts.
- Search results carry no dates, so never claim a date range. Use only years that appear in subjects.
- `list_labels` returns exact `threadsTotal` per label. Use it for the inbox total and for deltas.
- Bodies are not read unless a group cannot be judged otherwise.

## G6 Verify the query
Incidents:
- `a OR b` without parentheses bound wrongly and produced false leftovers.
- `-from:(a b)` excludes only mail from both, so nothing was excluded. Use `-(from:a OR from:b)`.
- A bare `from:domain` exclusion did not match a subdomain sender in one case. Test the exclusion.
Rule: run every query, scan the first page for protected senders, then show it.

## G7 Right action type
Incident: a first plan put payslips, insurance reports and utility invoices into Archive, and the user said Archive had become a trash can. A label scheme (payslips, insurance and pension, health, invoices, housing and car, trips, job search) was better: the mail stays findable and leaves the inbox.
Rule: trash only what the user would never search for.

## G8 Keepsakes
Incident: mail the user sent to themselves looked like gibberish ("cjcjc") and was proposed for Trash. The user kept it as memories. Very old personal mail, photos and CVs from friends were left alone on purpose.
Rule: ask once. Honor the answer for the rest of the session.

## G9 Active process
A job pipeline with interviews, an unpaid electricity bill and a pending benefit claim stayed in the inbox. Finished processes older than 14 days were labeled and archived.

## G10 Scam
Incident: a message claimed a membership auto-renewed for hundreds of dollars and gave a phone number, from a lookalike domain. It was phishing. Flag it, never reply, put it in Trash.

## G11 Tool limits
Incident: 50 parallel per-thread trash calls each needed approval; 11 succeeded and the user interrupted. The switch to paste-ready queries that the user runs was faster and safer.

## G12 One decision per group
Buttons with a recommended first option kept sessions moving. A single question covering several groups worked as well as one per group when the recommendations agreed.

## G13 Verify after
After "done", re-run the identical query. Expect empty. A few leftovers usually mean a partial selection, not an error. Report exact totals from `list_labels`.

## G14 Overlap
Newsletter markers and receipt markers overlap. Run newsletters first, then receipts. Group totals do not add up exactly.

## G15 Privacy
The report holds private subjects and sender names. It is a private file for the user. Do not publish it, paste it into a public repo, or share it without asking.

## G16 Know when to stop
The last stretch is not a sender problem. What remained was starred mail, keepsakes and active items, each the user's call. Offer to stop there instead of pushing to a literal zero.

## Practical notes from the field
- The clipboard API may be blocked where the report is previewed. The query must be visible and selectable, with a fallback.
- Trash is recoverable for 30 days. Say so.
- Ask the user to confirm label names once, then reuse them.
- "Select all conversations that match this search" is required when a query spans more than one page.
