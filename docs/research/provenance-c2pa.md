# C2PA and Content Credentials for Provenance

Status: Draft

## Owner

@JonSalv2

## Date

2026-08-07

## Research Question

Should provenance checks be part of the first evidence-backed report, or saved until after the image-analysis MVP works?

Related backlog item: DF-009. Related prior brief: [broadcast-provenance-authentication-notes.md](broadcast-provenance-authentication-notes.md).

## Summary

- C2PA is an open technical standard for cryptographically bound metadata ("manifests") that records how a piece of media was created and edited. Content Credentials are the user-facing implementation of that standard.
- Verification establishes that a manifest is well-formed, bound to the asset, and untampered. It does not establish that the claims in the manifest are true, nor that the media depicts a real event.
- Provenance and deepfake detection answer different questions and are complementary rather than interchangeable. Detection is probabilistic and cannot be guaranteed robust against new generators; provenance is deterministic about the narrower question of whether a manifest validates.
- Missing provenance is the common case, not a signal of manipulation. Platforms, messaging apps, and ordinary re-encoding routinely strip manifests, and most existing media predates C2PA-capable tooling.
- Viable open-source implementation paths exist today and are permissively licensed: `c2pa-python`, `c2pa-rs`, and `c2patool`, all maintained by the Content Authenticity Initiative. None require a hosted API or paid credentials for read and validate operations.
- **Recommendation:** build read-and-verify into the MVP using `c2pa-python`; defer manifest signing and writing to Phase 2 because of key management and Certificate Authority overhead. The main design risk is report wording, not engineering effort — a passing check must never be rendered to the user as "authentic."

## Sources

Sources already tracked in [source-log.md](source-log.md) are referenced by SRC ID. Sources marked new should be appended to the log in this PR.

| Source | Type | Date | Link | Notes |
| --- | --- | --- | --- | --- |
| C2PA Technical Specification v2.4 (SRC-002) | Standard / specification | 2026-05-02 | https://spec.c2pa.org/specifications/specifications/2.4/specs/C2PA_Specification.html | Primary source. Dense; versioned spec. |
| CAI `c2patool` documentation (SRC-010) | Official docs | 2026-05-02 | https://opensource.contentauthenticity.org/docs/c2patool/c2patool-index/ | Official CAI tooling docs. |
| `contentauth/c2pa-rs` repository (SRC-011) | Tool repo | 2026-05-02 | https://github.com/contentauth/c2pa-rs | Official CAI repo. Apache-2.0 / MIT. |
| Khan and Dang-Nguyen, Deepfake Detection Generalization (SRC-015) | Peer-reviewed paper | 2026-05-02 | https://doi.org/10.1109/ACCESS.2023.3348450 | IEEE Access; cross-dataset detector evaluation. |
| Nadimpalli and Rattani, On Improving Cross-Dataset Generalization of Deepfake Detectors (SRC-016) | CVPRW paper | 2026-05-03 | https://openaccess.thecvf.com/content/CVPR2022W/WMF/html/Nadimpalli_On_Improving_Cross-Dataset_Generalization_of_Deepfake_Detectors_CVPRW_2022_paper.html | CVF open-access workshop paper. |
| Simmons and Winograd, Interoperable Provenance Authentication of Broadcast Media (SRC-018) | Technical paper / preprint | 2026-05-03 | https://arxiv.org/abs/2405.12336 | arXiv / IBC paper. Authors affiliated with Verance, a watermarking company; weigh product claims accordingly. Scope is the metadata–watermark interplay for broadcast provenance; does not cover deepfake detection. |
| C2PA and Content Credentials Explainer v2.4 (SRC-025, new) | Standard / explainer | 2026-08-07 | https://spec.c2pa.org/specifications/specifications/2.4/explainer/Explainer.html | Primary source. Plain-language companion to the spec. |
| `contentauth/c2pa-python` repository (SRC-026, new) | Tool repo | 2026-08-07 | https://github.com/contentauth/c2pa-python | Official CAI repo. Apache-2.0 / MIT. License confirmed. |
| Vilesov et al., Solutions to Deepfakes: Can Camera Hardware, Cryptography, and Deep Learning Verify Real Images? (SRC-027, new) | Technical paper / preprint | 2026-08-07 | https://arxiv.org/abs/2407.04169 | UCLA authors; ACM-formatted. Documents the recapture / analog-hole limitation. |
| Trattner et al., C2PA Provenance Labels Increase Trust in News Platforms Across Western Countries (SRC-028, new) | Peer-reviewed conference paper (ICWSM 2026) | 2026-08-07 | https://ojs.aaai.org/index.php/ICWSM/article/download/42749/50309 | N = 6,114 across NOR/UK/US. Studies news-platform labelling, not upload-analysis tools. |

## Findings

### Finding 1: What C2PA is

The Coalition for Content Provenance and Authenticity (C2PA) is an open technical standard designed to establish the origin, history, and edits of digital content (SRC-025). Formed by a consortium of technology and media companies, it provides a cryptographically secure framework that lets creators, publishers, and consumers verify how a piece of media was created and edited (SRC-025).

### Finding 2: What Content Credentials are, and what verification does and does not establish

Content Credentials are the user-facing implementation of the C2PA standard (SRC-025). Technically, they are cryptographically bound metadata structures (called manifests) attached to an image, video, audio file, or document (SRC-002). When users inspect a Content Credential, they see verified claims about who created the asset, when it was made, what tools were used, and whether generative AI was involved (SRC-025).

Verification confirms that these claims are well-formed, bound to the asset, and untampered; it does not establish that the claims themselves are true (SRC-025). In practice, this means a passing check tells a user the recorded history is intact, not that the image shows a real event. The report should keep those two statements separate.

A practical illustration: photographing a synthetic image displayed on a screen with a C2PA-enabled camera produces a manifest that validates successfully, because the capture itself was genuine (SRC-027). The credential is accurate about the capture and silent about what was captured.

### Finding 3: Provenance and deepfake detection are complementary, not substitutes

Provenance and deepfake detection are two fundamentally different approaches to media integrity. Vilesov et al. structure their survey of image verification around exactly this contrast (SRC-027):

- **Provenance (cryptographic, applied at creation):** relies on cryptographically binding assertions to media at the point of creation and throughout its editing lifecycle.
- **Deepfake detection (forensic, applied after the fact):** analyzes media to infer manipulation by hunting for visual artifacts, forensic signals, or algorithmic inconsistencies.

Detection models score or classify media probabilistically, and their performance degrades substantially on datasets they were not trained on (SRC-015, SRC-016). Because detectors and generators form an adversarial pair, a detector cannot be guaranteed robust against generators refined against it (SRC-027). Provenance is deterministic about a narrower question — whether a manifest validates — rather than about whether the content is authentic. The two are complements rather than substitutes: the C2PA explainer itself positions Content Credentials as complementary to media literacy, fact-checking, and digital forensics approaches such as deepfake detection (SRC-025).

### Finding 4: Missing provenance is the common case and is not evidence of manipulation

Missing provenance does not imply that a piece of media is fake, manipulated, or malicious. The C2PA explainer states this directly: adding provenance is opt-in, and no assumption should be made about an asset's trustworthiness purely based on its use of Content Credentials (SRC-025). Absence merely means that no verifiable cryptographic history is attached to the asset.

Because container-level metadata (including C2PA manifests) is relatively easy to remove and is routinely lost to ordinary content processing such as platform transcoding and re-encoding, the absence of provenance is currently common (SRC-018). A lack of Content Credentials should be treated as neutral rather than suspicious.

### Finding 5: Open-source implementation paths exist today

For building out backend infrastructure — particularly when using Python-based frameworks like FastAPI — the most direct implementation path relies on the official open-source ecosystem maintained by the Content Authenticity Initiative (CAI):

| Tool | Source | License | Notes |
| --- | --- | --- | --- |
| `c2pa-python` | SRC-026 | Apache-2.0 / MIT | Python binding for the core Rust library. Reads, validates, creates, and signs manifests natively within Python applications. |
| `c2pa-rs` | SRC-011 | Apache-2.0 / MIT | The core Rust SDK that powers the broader C2PA tooling. |
| `c2patool` | SRC-010 | Apache-2.0 / MIT | Command-line utility useful for testing, debugging, and inspecting manifests during development. |

None of these require a hosted API or paid credentials for read and validate operations.

### Finding 6: C2PA is not the only provenance approach

Cryptographic manifests are one mechanism among several. The most developed complement is watermarking: because container-level metadata is routinely stripped by ordinary platform processing, a watermark embedded in the media itself can survive transformations that destroy a manifest, and can be used to look up the authoritative metadata again (SRC-018).

The architectural point in that work is worth carrying forward. Watermarks serve as a durable lookup mechanism, not as a root of trust — metadata retrieved via a watermark still has to be cryptographically validated before it means anything (SRC-018). The C2PA specification itself recognizes a second soft-binding mechanism alongside watermarking: fingerprint lookup, where a perceptual hash computed from the content is used to rediscover the associated credential (SRC-025).

None of these are candidates for the image-first MVP. Watermark detection requires either broadcast-scale infrastructure or cooperation from content producers, and fingerprint lookup depends on registry infrastructure and adoption that do not yet exist at consumer scale. They matter here mainly as context: C2PA is the approach with usable open-source tooling today, but the report's provenance section should be structured so that a second provenance signal could be added later without reshaping the output.

## Implications for MVP

For the media-verification-assistant project, C2PA integration should be split across development phases.

### Build for MVP: read and verify

Because the core purpose of the assistant is media verification, reading existing Content Credentials is a foundational feature. We can integrate `c2pa-python` into a FastAPI backend to extract and validate manifests from uploaded media. Where a manifest is present, this gives a verifiable record of origin that a detection model cannot provide. As noted above, manifests will be absent for most inputs, so the value is less in how often the check fires than in handling the "no manifest found" state correctly.

There is also evidence that displaying provenance changes how users judge media. A controlled experiment with 6,114 participants across Norway, the UK, and the US found that provenance labels significantly increased perceived image credibility and trust in the source, with larger gains for sources that began with lower public trust (SRC-028). That study measured news organizations labelling their own images, which is a different context from a tool analyzing media a user uploads, so the effect should not be assumed to transfer directly.

### Build for Phase 2: sign and write

Building the capability to inject or update C2PA manifests (for example, logging the verification steps the assistant performed and signing the output) involves complex key management and Certificate Authority (CA) requirements (SRC-002). This cryptographic overhead is better deferred until the core verification functionality and architecture are stable.

## Risks and Limitations

**A valid manifest does not rule out a staged capture.** Photographing a synthetic image displayed on a screen using a C2PA-enabled camera produces a manifest that validates, because the capture genuinely occurred (SRC-027). For this project, that means a passing provenance check must never be surfaced as "authentic" or "verified real" — only as a statement that the recorded capture history is intact. This is the single most important constraint on how the provenance result is worded in the report.

**A valid signature from an unknown signer is not the same as one from a known publisher.** Validation confirms the certificate chain and that the asset has not been altered since signing; it does not tell the user whether the signing identity is one they should trust. Presenting all validated manifests with identical confidence would flatten a meaningful distinction. How the report communicates signer identity and trust status is an unsolved design problem that should be settled before any provenance UI ships.

**Treating absent provenance as suspicious would cause active harm.** Because manifests are stripped by ordinary platform processing and most existing media predates C2PA entirely (SRC-018), a report that flags "no Content Credentials" as a negative signal would misclassify the overwhelming majority of authentic inputs. It would also feed the liar's dividend, giving cover to dismiss genuine media for lacking a credential it was never going to have.

**The specification is versioned and the ecosystem is still moving.** This brief is written against C2PA v2.4 (SRC-002, SRC-025). Tooling versions must be tracked against the manifest versions actually encountered in the wild, and conclusions here should be re-checked when the spec revises.

**The user-trust evidence is drawn from a different context.** SRC-028 measured news organizations labelling their own images, not a tool analyzing media a user uploads. An earlier study cited in that paper found that provenance labelling helped users detect manipulative content but also reduced trust in credible sources, so the effect of displaying provenance is not uniformly positive. The size and direction of the effect in this project's context should not be assumed.

**Source-affiliation caveats.** SRC-018 is an industry technical paper by authors at Verance, a watermarking company, so its architectural recommendations carry a commercial interest. The Content Authenticity Initiative is Adobe-adjacent, and product copy should describe C2PA as a standard rather than appearing to endorse a single vendor's ecosystem.

**This brief is desk research.** No tooling has been run against real images. The implementation recommendation in Finding 5 and the MVP recommendation above are based on documentation and licensing review only, and should be validated by a spike before any commitment is made.

## Recommended Follow-Up Issues

- [ ] **Run C2PA tooling against sample images.** Test `c2pa-python` and `c2patool` against a small fixture set — camera-captured, edited, AI-generated, and platform re-uploaded — and record the output shape and failure modes. Validates the recommendation in this brief before any implementation commitment.
- [ ] **Draft provenance result states for the evidence report.** Define the states the report can return (manifest valid, manifest present but validation failed, no manifest found, not checked) and, for each, what the app can and cannot conclude. Output: `docs/research/provenance-result-states.md`. Already proposed in [broadcast-provenance-authentication-notes.md](broadcast-provenance-authentication-notes.md).
- [ ] **Define provenance fields in the analysis result schema.** Coordinate with the Analysis Result JSON Schema work so provenance has a defined shape in the report output rather than being bolted on later.
- [ ] **Settle confidence language for provenance states.** Agree the exact wording used for each provenance state so the report does not overclaim, particularly for the "validation passed" and "no manifest found" cases.
- [ ] **Survey non-C2PA provenance approaches in depth.** Finding 6 sketches watermarking and hash-registry schemes at a high level only. A dedicated brief should assess whether any of them are viable for this project's scale, and what the report schema would need to accommodate a second provenance signal.
