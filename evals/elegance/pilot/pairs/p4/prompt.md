# Support ticket routing

A help desk for a home-insurance broker routes each new ticket to a queue. A ticket has `subject`, `customer_tier` (`"standard"` or `"enterprise"`), `channel` (`"email"`, `"phone"` or `"chat"`), `language` (a language code such as `"en"` or `"de"`) and `amount` (the disputed amount, or `None`).

Constraints, in priority order (the first that applies wins):

1. Enterprise customers go to `enterprise-desk`.
2. A subject mentioning "refund" goes to `billing-escalations` if the amount is over 500, else to `billing`.
3. A subject mentioning "invoice" or "receipt" goes to `billing`.
4. A subject mentioning "password" or "login" goes to `security` when it came by phone, else to `self-service`.
5. A ticket not in English goes to `localized`.
6. Everything else goes to `general`.

Subject matching ignores case. The rules change a few times a year. They are changed only by the engineers who own this service, through normal code review and deploy. There is no plan for anyone else to edit them.

Two candidate implementations follow. Which one is the better design?
