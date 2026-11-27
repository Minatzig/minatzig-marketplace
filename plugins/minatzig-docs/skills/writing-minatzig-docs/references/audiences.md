# Audiences: customer vs internal

## Contents
- What each audience means
- Deciding the audience
- How to write each one
- Splitting mixed material into two documents
- Sensitive data

## What each audience means

| Audience | Who reads answers built from it | Found by |
|---|---|---|
| `customer` | The company's customers, via WhatsApp and email | Customer answers **and** the internal chat |
| `internal` | Only the company's own staff | Only the internal knowledge-base chat |

Internal questions search both kinds of document. So customer-facing facts belong only in the customer document, and the internal document adds what staff need on top.

## Deciding the audience

Decide without asking when the signal is clear:
- Clearly **customer**: FAQs, how-to guides for end users, product manuals, public policies (returns, plans, opening hours), anything the person says customers ask.
- Clearly **internal**: root causes, logs, database or backend details, internal tools and admin panels, escalation paths and on-call contacts, workarounds staff apply on the customer's behalf, commercial exceptions, anything the person calls internal, confidential or "for the team".

Ask one short question when the signal is mixed or absent, for example: "Is this for answering customers, only for your team, or both? If both, I'd suggest two documents: one for customers and one with the internal-only details." Ask once, before drafting.

## How to write each one

**Customer documents**
- Write as if explaining to the customer directly: short sentences, second person, no jargon.
- Only what the customer can see and do: screens, buttons, messages, outcomes.
- No staff names, internal systems, internal links, ticket numbers or backend causes.
- When the customer cannot solve something alone, say what to do ("Write to support with your client number"), not how staff solve it.

**Internal documents**
- Can be technical: causes, system and table names, error codes, logs to check, scripts, decision rules, escalation paths.
- Still one topic per document, still self-contained sections. Each section names the product and the screen or system it is about, because it is retrieved alone.
- Never say "as explained in the customer document". If a staff member needs a customer-facing step to make sense, restate it in one line.

## Splitting mixed material into two documents

When the material contains both kinds of content, suggest a split. Present it as two lists so the person can move items between them:

```
Customer document: <title>
- <section>: <one line>
- ...

Internal document: <title>
- <section>: <one line, what it adds for staff>
- ...
```

Rules for the split:
1. The customer document is complete for a customer on its own.
2. The internal document contains only the extra internal content (causes, internal fixes, escalation, exceptions). It does not copy the customer steps.
3. Both have their own `# H1`, a file name that says which is which (for example `clientes-alta-cliente-v2-3.md` and `clientes-alta-cliente-interno-v2-3.md`), and the same product and versions.
4. Each is checked for sensitive data against its own audience's criteria.
5. They are uploaded separately, customer first.

If the person prefers a single document, respect that. Choose the audience with them, and if it is `customer`, move or remove the internal-only parts.

## Sensitive data

Warn about these before upload. The server applies the same criteria and holds any document with a finding for human review.

**Both audiences**
- Credentials: passwords, API keys, tokens, connection strings, private URLs with embedded secrets.
- Customers' personal data: real names, emails, phone numbers, ID numbers, addresses, account or card numbers, including inside screenshots.

**Customer documents also**
- Staff names and direct contacts.
- Internal systems: admin panels, internal hostnames and URLs, database or table names, internal tool names.

For each finding, say where it is (section, or image file) and offer a fix: delete it, replace it with an obviously fictitious example (`cliente@ejemplo.com`, `Juan Pérez`), blur or recrop the screenshot, or for customer documents move it to the internal document. The person decides.
