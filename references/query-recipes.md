# Gmail query recipes

```
# Exact inbox total: use list_labels -> INBOX.threadsTotal

# Volume per category (pageSize 1, THREAD_VIEW_IDS_ONLY, read resultCountEstimate)
in:inbox category:promotions -is:starred
in:inbox category:updates -is:starred
in:inbox category:personal -is:starred

# A sender group
in:inbox -is:starred (from:a.example OR from:b.example)

# Everything except handled senders (next layer)
in:inbox -is:starred -(from:a.example OR from:b.example)

# Newsletters (run before receipts; they overlap)
in:inbox -is:starred (unsubscribe OR newsletter OR "view in browser")

# Receipts
in:inbox -is:starred (receipt OR invoice OR order OR payment)

# Label mail that is already archived
in:anywhere from:payroll.example

# Finished processes only
in:inbox -is:starred older_than:14d (from:careers.example OR from:jobs.example)

# Keep one item out of a group
... -subject:"order 12345"
```

Execution in Gmail: paste, tick the select-all box, choose "Select all conversations that match this search",
then Trash, or the label icon followed by Archive.
