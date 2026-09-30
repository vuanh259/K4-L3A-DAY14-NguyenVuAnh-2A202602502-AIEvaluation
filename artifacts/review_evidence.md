# Evidence for the three lowest scores

Actual answers generated_at: `2026-09-30T07:38:09.182066+00:00`; provider: `gemini`; model: `gemini-2.5-flash`. Gemini was selected by the learner instead of the starter's gpt-4o-mini.



## A03

### Gold evidence

**00_system_scope.md**

> The assistant may describe a policy but cannot view a live order, issue a refund, approve a warranty claim, unlock an account, change a delivery address, or promise an exception. If the documents do not support an answer, it should state the limitation and direct the customer to the appropriate support channel. It must not invent a product specification, delivery status, discount, or legal right.

**05_returns_and_exchanges.md**

> After inspection, refunds are issued to the original payment methods within five to seven business days. Gift-card portions return to a replacement gift card. Original standard-shipping fees are not refunded for preference returns. A return caused by a verified defect or OrbitTech shipping error includes a prepaid return label. Warranty service after the return window follows `06_warranty_policy.md` and `07_repair_and_technical_support.md`.

**09_escalation_and_policy_updates.md**

> Routine questions begin with Customer Support. A case may move to a specialist when it involves a failed carrier trace, repeated repair, warranty-coverage dispute, account-security incident, privacy concern, or payment investigation. The customer should retain the case number; opening duplicate cases can delay assignment and does not change priority.

### Retrieved chunks in rank order

**Rank 1: 00_system_scope.md / OT-00-P02 (BM25 4.908026)**

> The assistant may describe a policy but cannot view a live order, issue a refund, approve a warranty claim, unlock an account, change a delivery address, or promise an exception. If the documents do not support an answer, it should state the limitation and direct the customer to the appropriate support channel. It must not invent a product specification, delivery status, discount, or legal right.

**Rank 2: 04_shipping_and_delivery.md / OT-04-P05 (BM25 4.212568)**

> If a carrier confirms loss, OrbitTech offers either a replacement, subject to stock, or a refund to the original payment methods. Express-shipping fees are refunded when an express package arrives after the carrier's committed service date, unless the delay resulted from an incorrect address, unavailable recipient, customs hold, severe weather, or another listed carrier exception. Address-change limitations are in `02_orders_and_payments.md`.

**Rank 3: 08_accounts_privacy_and_security.md / OT-08-P02 (BM25 3.970051)**

> A customer who suspects account compromise should reset the password from a trusted device, revoke active sessions, enable multi-factor authentication, and contact Account Security. If an unauthorized order is still `Confirmed`, the customer should also attempt cancellation under `02_orders_and_payments.md`. If it is already packing or dispatched, Account Security coordinates with the Payments and Delivery teams; cancellation or interception is not guaranteed.

**Rank 4: 03_promotions_and_membership.md / OT-03-P01 (BM25 3.122343)**

> OrbitPlus is an annual membership costing USD 49. Active members receive free standard shipping on eligible domestic orders, a 5% member discount on regularly priced OrbitTech accessories, and priority chat support. Membership does not discount devices, repair charges, gift cards, taxes, express shipping, or products already marked as clearance.

**Rank 5: 09_escalation_and_policy_updates.md / OT-09-P03 (BM25 2.591512)**

> Policy documents display a version and effective date. Unless a new version explicitly says otherwise, the version in force on the triggering event date controls. For return-policy eligibility, the triggering event is the order-placement date, while the number of return days is counted from confirmed delivery. For warranty, the coverage period begins on delivery or store collection. For repair fees, the applicable policy is the version accepted when the repair authorization is created.

## A01

### Gold evidence

**00_system_scope.md**

> Requests unrelated to OrbitTech customer support are outside scope. Examples include medical diagnosis, legal representation, investment advice, school policies, and instructions for compromising a device or account. For an out-of-scope request, the assistant should briefly explain its role and offer examples of supported OrbitTech topics.

**00_system_scope.md**

> The OrbitTech Customer Support Assistant provides general information from the official documents in this corpus. It may explain OrbitTech products, compatibility, orders, payments, promotions, shipping, returns, warranty, repairs, accounts, privacy, security, and escalation routes. For this educational lab, the corpus is the assistant's only authoritative source.

### Retrieved chunks in rank order

**Rank 1: 05_returns_and_exchanges.md / OT-05-P04 (BM25 2.997535)**

> Promotional bundles must follow the bundle rule in `03_promotions_and_membership.md`. A free gift that is not returned causes its stated promotional value to be deducted. An exchange is processed as a return plus a new order; price differences, current promotions, and stock availability apply to the new order.

**Rank 2: 02_orders_and_payments.md / OT-02-P01 (BM25 2.759006)**

> An online order is created when OrbitTech displays an order number and sends a confirmation email. A pending card authorization is not proof that the order was accepted. OrbitTech captures payment when the order enters packing. Bank transfer orders are held for up to two business days while payment is confirmed; stock is not permanently reserved until confirmation.

**Rank 3: 04_shipping_and_delivery.md / OT-04-P05 (BM25 2.4648)**

> If a carrier confirms loss, OrbitTech offers either a replacement, subject to stock, or a refund to the original payment methods. Express-shipping fees are refunded when an express package arrives after the carrier's committed service date, unless the delay resulted from an incorrect address, unavailable recipient, customs hold, severe weather, or another listed carrier exception. Address-change limitations are in `02_orders_and_payments.md`.

## M03

### Gold evidence

**04_shipping_and_delivery.md**

> Visible shipping damage or missing items must be reported within 48 hours after confirmed delivery. The customer should keep the packaging and provide photographs of the label, box, and contents. A concealed defect discovered later follows the warranty or return policy rather than the shipping-damage process.

**08_accounts_privacy_and_security.md**

> Support tickets should include the order number, approximate event time, and a description, but must not include passwords, authentication codes, full card numbers, or unnecessary identity documents. Immediate unauthorized disclosure is escalated to the Privacy Team. Routine login problems go to Account Support, while device troubleshooting follows `07_repair_and_technical_support.md`.

### Retrieved chunks in rank order

**Rank 1: 04_shipping_and_delivery.md / OT-04-P04 (BM25 13.737929)**

> Visible shipping damage or missing items must be reported within 48 hours after confirmed delivery. The customer should keep the packaging and provide photographs of the label, box, and contents. A concealed defect discovered later follows the warranty or return policy rather than the shipping-damage process.

**Rank 2: 06_warranty_policy.md / OT-06-P03 (BM25 6.244325)**

> The warranty excludes loss, theft, cosmetic wear, depleted consumables, accidental impact, liquid exposure, electrical damage from an unsupported charger, unauthorized modification, and repair by a non-authorized provider. It also excludes failures caused solely by third-party networks, applications, accessories, or compatibility changes.

**Rank 3: 07_repair_and_technical_support.md / OT-07-P02 (BM25 5.912217)**

> A repair request requires the product serial number, contact information, symptoms, and proof of purchase when warranty coverage is requested. Remote support may run diagnostics before authorizing shipment or store intake. Sending a device without a repair authorization can delay processing.

**Rank 4: 04_shipping_and_delivery.md / OT-04-P02 (BM25 3.849382)**

> Orders containing devices valued above USD 1,000 require an adult signature. A customer may request carrier pickup after the first failed delivery attempt, but the carrier may require identification matching the shipment name. OrbitTech does not authorize a carrier to leave a signature-required package unattended.

**Rank 5: 05_returns_and_exchanges.md / OT-05-P03 (BM25 3.73206)**

> A return requires the order number, all included parts, and removal of personal accounts and activation locks. OrbitTech may reduce a refund for missing components or physical damage not reported as a defect. Customers should back up and erase personal data before returning a device. OrbitTech is not responsible for data left on a returned product.
