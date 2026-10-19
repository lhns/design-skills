I've written the design to `answer.md`. It's 567 words, or 595 if symbols are counted too, so it's under the 600 limit either way. It's a design only; there's no code yet.

The main idea is that nothing recorded is ever overwritten. The share register becomes a dated list of share changes, and supplier corrections to import readings are added as new rows instead of replacing old ones. The month's allocation is then a calculation from the facts known at a given time, and every credit line sent to members and the supplier is stored exactly as sent.

That one change is what fixes the existing problems:
- **Auditor's re-runs:** re-running a month with only the facts known when it was issued gives the same figures, even after later share transfers or corrections.
- **Reprinted statements (#29):** statements are rebuilt from the stored lines, so a reprint always matches the original.
- **Late corrections:** at each monthly run, any earlier month with new facts is worked out again. The differences go on the next statement as plus or minus adjustment lines. This also catches the knock-on effect where one member's correction changes other members' share of redistributed credit.
- **Mid-month transfers (#14):** credit is split by the days shares are held (rule 4.2), so the 15th-of-the-month rule is no longer needed.
- **The January change (4.3):** no one is credited more than they imported, and what they can't use goes to the other members in the same proportions, repeated until nobody else is over their limit. Whatever no member can use is the kWh sold to the supplier. Credits are rounded so that credits plus kWh sold equal generation exactly (4.4), which removes the need for the community account.
- **Zero-kWh lines (#22):** these are simply left out of the supplier file, so the 5-share minimum can go and small shareholders are no longer excluded.

These are my own choices, each labelled in the document:
- **Transfers:** the person receiving shares holds them from the transfer date itself.
- **Missing import readings:** these count as zero for now and are flagged. Over-crediting is lost for good under the new terms, but under-crediting can be fixed with an adjustment later.
- **Adjustment lines:** these go to the supplier separately, not added into the current month's credit.
- **Time limit:** there's no limit on how far back a month can be corrected, because errors in the share register can turn up later than the supplier's three months.