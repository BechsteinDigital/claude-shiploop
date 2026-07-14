# Interview Guide

A catalog, not a script: adapt wording to the pitch and previous answers.
Never re-ask questions already answered.

## Round A — Core
1. What concrete problem does this solve? How does the problem show today?
2. Who exactly has the problem (role, situation)? Who is the first real user?
3. What is the one sentence that carries the idea? (Offer a proposal, have it confirmed)
4. How will you know in 3 months that it works? (success criterion)

## Round B — Scope
1. What must the very first usable version be able to do? (→ 3–7 must-have outcomes, phrased verifiably)
2. What is expressly NOT included — even if it seems obvious? (→ at least 3 non-goals; actively offer candidates)
3. Is there an even smaller version that already delivers value? (test the MVP cut)
4. What already exists (code, data, accounts, designs)?

## Round C — Frame
1. Time horizon: when should something usable exist?
2. Cost: may paid services/APIs be used? Up to what limit?
3. Tech constraints: specific language/platform/hosting — or does the agent decide? ("agent decides" is a valid answer to record explicitly)
4. Target environment: web, mobile, CLI, desktop? Where does it run (local, server, cloud)?

## Round D — Autonomy contract
1. Read out the standard escalation rules (brief template) — is that fine, or stricter/looser?
2. Extension budget: how many extra ideas may be activated per milestone at most? (default: 1)
3. May the agent deploy/publish, or does autonomy end at local runnability?
4. Milestone behavior: report only and continue (default) — or stop at each milestone?

## Definition of Ready
Only start once every item is answered or covered by a confirmed default:

- [ ] Core idea in one sentence, confirmed by the user
- [ ] Target user and core problem clear
- [ ] 3–7 verifiable must-have outcomes
- [ ] at least 3 explicit non-goals
- [ ] Time horizon and cost frame
- [ ] Tech constraints or explicitly "agent decides"
- [ ] Autonomy contract incl. deployment limit confirmed
- [ ] Extension budget set
- [ ] Success criterion from the user's perspective

## Handling answer types
- **Vague answer** ("it should just be simple"): translate into verifiable form and have the translation confirmed.
- **Contradiction** (e.g. a must-have outcome collides with a non-goal): name it immediately, let the user decide.
- **Feature list instead of core**: ask "If only ONE of these were possible — which?" and propose the rest as non-goal or IDEAS candidates.
