# System Design – Adaptive Taxonomy Mapper

This document outlines design considerations and trade-offs for scaling, cost efficiency, and reliability in the Adaptive Taxonomy Mapper system.

---

## 1. Scaling to a Taxonomy with 5,000+ Categories

With a significantly larger taxonomy, a flat rule-based approach would not scale efficiently. The system would evolve to a hierarchical and retrieval-based design:

### Proposed Approach
- **Hierarchical filtering**
  - First classify at a coarse level (e.g., Romance, Thriller, Sci-Fi)
  - Then narrow down to relevant sub-genres
- **Embedding-based similarity search**
  - Generate embeddings for taxonomy nodes
  - Compare story embeddings against taxonomy embeddings
- **Hybrid decision flow**
  - Use embeddings to shortlist candidates
  - Apply rule-based validation and business constraints for final selection

### Benefits
- Reduces search space dramatically
- Maintains explainability
- Allows incremental taxonomy growth without rewriting rules

---

## 2. Minimizing LLM Costs at 1M Stories per Month

Calling an LLM for every input would be prohibitively expensive and unnecessary.

### Cost Optimization Strategies
- **Rule-first pipeline**
  - Apply deterministic heuristics before invoking LLMs
  - Skip LLM calls when confidence is high
- **Selective LLM usage**
  - Use LLMs only for ambiguous or low-confidence cases
- **Caching**
  - Cache repeated or similar inputs
- **Batch processing**
  - Process multiple stories in a single LLM request where possible

### Result
- LLM usage becomes the exception, not the default
- Predictable and controllable inference costs

---

## 3. Preventing Hallucinated Sub-Genres

Hallucination prevention is enforced through system design rather than prompt quality alone.

### Guardrail Mechanisms
- **Single source of truth**
  - All valid genres are loaded from `taxonomy.json`
- **Hard validation layer**
  - Any output not present in the taxonomy is rejected
- **LLM role restriction**
  - LLMs are limited to contextual extraction (themes, tone, setting)
  - LLMs never output or select genres
- **Fallback behavior**
  - Uncertain or invalid cases are explicitly marked as `[UNMAPPED]`

### Outcome
- The system cannot output non-existent categories
- Business constraints are always enforced

---

## Design Summary

- The system prioritizes **reliability over creativity**
- LLMs assist understanding but never control outcomes
- Rule-based logic ensures deterministic, auditable behavior
- The architecture scales while preserving explainability

This design reflects how production AI systems are built under real-world constraints.
