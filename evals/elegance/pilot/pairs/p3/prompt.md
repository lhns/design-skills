# Delivery exports for a farm cooperative

A grain cooperative records each delivery a member brings to its silo: ticket number, member id, date, weight in kg, grade, whether the load was rejected (with a reason), and the amount credited in cents (0 for rejected loads). Two exports are built from the same deliveries.

Constraints:

1. **Board report** for the regional produce board: accepted loads only; columns member id, ISO date, weight in whole kg, grade.
2. **Member statement** from the cooperative office: all loads, rejected ones included; columns member id, date as `dd.mm.yyyy`, weight in tonnes with 3 decimals, grade, reject reason (empty if accepted), amount, running total of amounts. Amounts use the existing `money(cents)` helper.
3. Both are sorted by date, then ticket number.
4. The board changes its required format by circular, roughly once a year. The cooperative office changes the statement whenever members ask. A change to one export must never alter the other's output.
5. Each export is called from exactly one place.

Two candidate implementations follow. Which one is the better design?
