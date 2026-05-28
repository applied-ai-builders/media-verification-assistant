# Deepfake Dataset Inventory & Classification Matrix

This inventory categorizes benchmark datasets used for training and evaluating Deepfake generation and detection algorithms. Datasets are organized by "Generation" eras, reflecting the evolution of manipulation complexity.

> **Note on "Generation" Grouping:** The "Generation 1/2/3" labels are a project-level organizing heuristic for this evaluation effort, not a formal academic taxonomy or chronological classification. They reflect relative maturity/sophistication of synthesis methods and dataset design philosophy, but dataset years and actual release dates may not align strictly with these groupings. Use these categories as a structuring aid for MVP planning, not as definitive temporal or methodological boundaries.

---

## 1. Generation 1: Standard Visual Manipulations
*Focus: Face-swapping and basic facial expression manipulation using early autoencoder architectures or traditional computer vision graphics.*

### UADFV (University at Albany DeepFake Video)
* **Description:** A localized dataset targeting physiological signals (specifically, unnatural blinking rates).
* **Composition:** 49 real videos, 49 fake videos.
* **Primary Utility:** Benchmark for early, artifact-based detection algorithms.
* **License:** Custom Academic/Research Use Only.
* **Access Link:** [Official UADFV Repository via kaggle](https://www.kaggle.com/datasets/adityakeshri9234/uadfv-dataset)

| Aspect | Details |
|--------|---------|
| **Media Type** | MP4 video (H.264 encoded) |
| **Approximate Size** | ~500 MB total (~5 MB per video average) |
| **Access Process** | Download via Kaggle dataset; requires Kaggle account and terms acceptance |
| **Strengths** | Small, manageable dataset; strong focus on physiological artifact detection; ground-truth labels; controlled Lab environment |
| **Weaknesses** | Very limited data volume (98 videos); all subjects appear to be from single source; low resolution; limited diversity; poor generalization to wild deepfakes |
| **Unclear/Blocked Terms** | Custom license restrictions not fully detailed; unclear if redistribution/derivative use permitted |
| **MVP Recommendation** | **Not recommended for primary MVP evaluation** — too small and non-representative; useful as sanity check only |

### DeepFakeTIMIT
* **Description:** Generated using an open-source autoencoder framework based on the Faceswap GitHub repository, manipulating the VidTIMIT database.
* **Composition:** 620 fake videos split across low-quality (`64×64`) and high-quality (`128×128`) resolutions.
* **Primary Utility:** Evaluating basic GAN and autoencoder face-swaps under controlled lighting.
* **License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0).
* **Access Link:** [IDIAP Research Institute DeepFakeTIMIT Portal](https://www.idiap.ch/en/dataset/deepfaketimit)

| Aspect | Details |
|--------|---------|
| **Media Type** | MP4 video (MPEG-4 codec) at two resolutions: 64×64 and 128×128 |
| **Approximate Size** | ~2 GB total (varies by resolution choice) |
| **Access Process** | Registration on IDIAP website; academic institution verification required; download via portal |
| **Strengths** | Controlled synthesis environment; consistent lighting/backgrounds; two quality levels for robustness testing; reproducible generation method (Faceswap) |
| **Weaknesses** | Limited resolution makes results less applicable to modern high-res videos; very small video pool; no audio; homogeneous lighting/expression conditions; outdated generation methodology |
| **Unclear/Blocked Terms** | CC BY-NC-SA 4.0 with institutional restrictions—unclear if derivative datasets can be published; modification restrictions ambiguous |
| **MVP Recommendation** | **Supplementary only** — useful for cross-dataset generalization testing, but too low-resolution and controlled for primary evaluation |

---

## 2. Generation 2: Large-Scale & Real-World Forgery Benchmarks
*Focus: Scaling data volume, tracking diverse generation networks, and introducing real-world environmental diversity (lighting, compression, angles, internet artifacts).*

### FaceForensics++ (FF++)
* **Description:** An industry-standard benchmark featuring thousands of video clips manipulated by four distinct automated techniques (Deepfakes, Face2Face, FaceSwap, and NeuralTextures).
* **Composition:** 1,000 pristine source videos, 4,000 manipulated videos across 3 compression levels (Raw, HQ, LQ).
* **Primary Utility:** Evaluating detection model robustness against real-world video compression and post-processing.
* **License:** FaceForensics Terms of Use (Strictly Non-Commercial / Academic Research Only via signed agreement).
* **Access Link:** [Official FaceForensics GitHub](https://github.com/ondyari/FaceForensics)

| Aspect | Details |
|--------|---------|
| **Media Type** | MP4 video (H.264) at multiple compression levels: Raw (no compression), HQ (c23 CRF), LQ (c40 CRF) |
| **Approximate Size** | ~500 GB total; ~50 GB per compression level; requires preprocessing/downsampling for practical use |
| **Access Process** | GitHub form submission for data access; manual review by maintainers; Terms of Use agreement; significant bandwidth required for download |
| **Strengths** | Industry-standard; multiple manipulation methods included; compression levels enable robustness testing; large-scale; diverse subjects; 1000 ground-truth source videos |
| **Weaknesses** | Very large download requirements; aging dataset (generated ~2018-2019); limited demographic diversity; 4 distinct methods may not cover newer generative techniques; licensing restrictions limit collaboration |
| **Unclear/Blocked Terms** | Exact redistribution and commercial use restrictions not fully documented; collaboration/publication terms somewhat opaque; export controls may apply |
| **MVP Recommendation** | **Recommended for primary evaluation** — industry standard with strong compression-robustness testing capabilities; suggests using HQ level for balanced complexity/accessibility |

### Celeb-DF (v2)
* **Description:** A high-quality dataset specifically designed to reduce standard visual artifacts (such as boundary blending issues and low-resolution face ghosting) seen in earlier datasets.
* **Composition:** 590 original celebrity videos, 5,639 high-quality synthesized deepfakes, and 300 additional YouTube-real videos.
* **Primary Utility:** Training models on seamless, modern visual fakes with minimized color mismatching.
* **License:** Custom Academic Research License Agreement.
* **Access Link:** [Celeb-DF via github](https://github.com/yuezunli/celeb-deepfakeforensics)

| Aspect | Details |
|--------|---------|
| **Media Type** | MP4 video (H.264) at high resolution; YouTube-sourced real videos |
| **Approximate Size** | ~250 GB total (~40 MB average per video); manageable in chunks via partial downloads |
| **Access Process** | GitHub form submission; requires academic affiliation verification; email-based distribution coordination; significant bandwidth needed |
| **Strengths** | High-quality, artifact-reduced synthesis; large fake corpus; includes real YouTube videos boosting realism; targeted for modern detection; good face identity diversity |
| **Weaknesses** | Celebrity-centric (demographic bias); limited audio tracks; custom license restrictions reduce collaboration potential; YouTube videos add uncontrolled variability |
| **Unclear/Blocked Terms** | Custom license terms not published online—unclear modification/redistribution policies; YouTube content music/copyright status unclear; institutional publication restrictions |
| **MVP Recommendation** | **Strongly recommended for primary evaluation** — represents state-of-the-art high-quality deepfakes; essential for assessing detection robustness against artifact-reduced fakes; focus on high-quality synthesis cases |

### WildDeepFake
* **Description:** A dataset harvested entirely from real-world internet sources rather than synthesized in a controlled lab environment. It features a vast diversity of expressions, angles, lighting conditions, and unknown baseline generation algorithms.
* **Composition:** 7,314 face sequences extracted from 707 internet-sourced deepfake videos, intentionally containing diverse synthesis anomalies.
* **Primary Utility:** Testing the generalization of detection models against practical, uncontrolled "wild" internet deepfakes and multi-person frames.
* **License:** Custom Research Use License.
* **Access Link:** [WildDeepFake Repository on GitHub](https://github.com/OpenTAI/wild-deepfake)

| Aspect | Details |
|--------|---------|
| **Media Type** | Extracted face sequences (crops) with variable formats; original sources from internet; no standardized encoding |
| **Approximate Size** | ~30-50 GB; smaller than FF++ but more manageable than Celeb-DF |
| **Access Process** | GitHub repository access; download via git clone; no formal registration required; pre-processed face crops provided |
| **Strengths** | Wild, uncontrolled diversity (real-world conditions); unknown/diverse generation methods; multiple lighting/angles/expressions; realistic deployment use case; smaller download size; face-crops enable faster experimentation |
| **Weaknesses** | No ground-truth generation method labels; source metadata sparse; quality variability extreme; copyright/source clearance uncertain; smaller total video count limits statistical significance |
| **Unclear/Blocked Terms** | Source video copyright status unclear; redistribution of face crops may violate platform ToS (Reddit, Twitter sourced); license scope under-specified |
| **MVP Recommendation** | **Strongly recommended for robustness/generalization testing** — complements controlled datasets; essential for evaluating "real-world" performance; recommend using alongside FF++ or Celeb-DF for comprehensive MVP validation |

---

## 3. Generation 3: Hyper-Realistic & Audio-Visual Forgeries
*Focus: Multi-modal fakes (synchronized audio-to-video manipulation) and large demographic diversity to eliminate model bias.*

### DFDC (DeepFake Detection Challenge)
* **Description:** Created by Facebook AI (now Meta) to incentivize global detection pipelines. Features diverse actors, varied lighting, shadows, and synthetic audio tracks. Includes consenting paid actors and multiple manipulation methods.
* **Composition:** 128,154 total videos (104,500 unique fake videos) generated using eight facial modification algorithms, sourced from 3,426 paid actors.
* **Primary Utility:** Global benchmark for commercial-grade detection software and multi-modal audio-visual evaluation.
* **License:** CC BY-NC 4.0 (Non-Commercial Research and Development).
* **Access Link:** [AI Commons / Kaggle DFDC Portal](https://ai.meta.com/datasets/dfdc/)

| Aspect | Details |
|--------|---------|
| **Media Type** | MP4 video (H.264); includes synchronized audio tracks; standardized frame rates and resolutions |
| **Approximate Size** | ~480 GB total; very large; downloadable in parts via Kaggle |
| **Access Process** | Kaggle dataset sign-up; Meta/AI Commons account required; Terms of Use acceptance; significant bandwidth for full download; allows partial download |
| **Strengths** | Largest-scale benchmark; 8 distinct generation methods; real actors (paid professional consent); diverse lighting/angles/expressions; audio-visual multi-modal data; standardized video specs; strict actor-independent train/test split |
| **Weaknesses** | Enormous data volume; all synthetics generated 2019-2020 (may not reflect current SOTA generative techniques); acting/scripted nature differs from organic videos; no fine-grained method attribution at inference-time |
| **Unclear/Blocked Terms** | CC BY-NC 4.0 clear, but commercial restrictions strictly enforced; actor identity/privacy statements under-detailed; video modification permission levels ambiguous |
| **MVP Recommendation** | **Recommended for scale/multi-modal testing** — use selective subset (e.g., all videos from 4 core methods) to manage compute; valuable for audio-visual synchronization detection; complements single-modality datasets |

### FakeAVCeleb
* **Description:** A novel audio-visual deepfake dataset introducing deepfake audio synced with manipulated facial videos across a multicultural demographic.
* **Composition:** Over 20,000 video clips utilizing methods like Wav2Lip, Faceswap, and SV2TTS.
* **Primary Utility:** Advancing multimodal (audio + video) deepfake tracking and reducing demographic bias in detection models.
* **License:** Creative Commons Attribution 4.0 International (CC BY 4.0).
* **Access Link:** [FakeAVCeleb Project Platform via GitHub](https://sites.google.com/view/fakeavcelebdash-lab/)

| Aspect | Details |
|--------|---------|
| **Media Type** | MP4 video (H.264) with embedded audio; WAV audio tracks available separately; multi-lingual speech content |
| **Approximate Size** | ~150-200 GB total; smaller than DFDC, larger than Celeb-DF; manageable in parts |
| **Access Process** | Project website form submission for access; email-based coordination; some content hosted via GitHub release pins |
| **Strengths** | Explicit audio-visual synthesis focus (Wav2Lip primary); multicultural demographic diversity; multiple audio generation methods (SV2TTS covers speaker cloning); explicit audio-visual synchronization testing target; modern generation techniques |
| **Weaknesses** | Smaller total corpus vs. DFDC; audio quality varies; celebrity-skewed source pool; less documented metadata than FF++; fewer generation method variations than DFDC; access process less automated |
| **Unclear/Blocked Terms** | CC BY 4.0 is permissive, but source celebrity identity/music copyright status unclear; Wav2Lip/SV2TTS model checkpoint licensing not specified; derivative dataset publication guidelines unclear |
| **MVP Recommendation** | **Recommended for audio-visual evaluation** — only major dataset explicitly enabling speech synthesis detection; useful for evaluating lip-sync and audio mismatch detection; combine with FF++ or Celeb-DF for balanced multi-modal MVP |

---

## Blocked/Inaccessible Datasets

Certain benchmark datasets were identified during research but are not available for this MVP evaluation:

### NIST/OpenMFC (OpenMedia Forensics Challenge)
* **Description:** NIST's open-source media forensics evaluation framework designed to facilitate development of systems that automatically detect and locate manipulations in imagery (images and videos) under controlled environments.
* **Composition:** Diverse datasets collected under controlled environments for benchmarking accuracy and robustness.
* **Primary Utility:** Media forensics benchmarking, manipulation detection/localization, and cross-format robustness evaluation.
* **License:** Custom data license agreement required per participant.
* **Access Link:** [NIST OpenMFC Official Portal](https://mfc.nist.gov/)
* **Status:** ⛔ **Blocked/Inaccessible for MVP**

| Aspect | Details |
|--------|---------|
| **Reason for Exclusion** | Data access requires: (1) registration on NIST website, (2) completion of custom data license agreement, (3) implied participation in challenge leaderboard framework. Access structure is competition-oriented rather than open research access; data availability is tied to active challenge cycles. Current status of OpenMFC 2022 data post-competition and accessibility for non-participating researchers unclear. Significant administrative overhead and unclear post-challenge availability make immediate MVP integration infeasible. |
| **Potential Future Value** | Valuable for controlled-environment forensics evaluation; diverse datasets under standardized collection conditions enable rigorous robustness testing; NIST-administered benchmarking provides credibility and rigor; could enable cross-domain generalization study if post-competition open access is confirmed |
| **Access Path** | Contact NIST MFC team (mfc_poc@nist.gov) to clarify: (1) current data availability outside active challenge windows, (2) license terms for non-competitive research use, (3) timeline for public archive release |

---

## 4. Comprehensive Technical Matrix

| Dataset | Media Type | Approximate Size | Version / Compression | Frame Sampling Method | Split Logic | License Type | Official Link |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **UADFV** | MP4 Video (H.264) | ~500 MB | v1.0 / Uncompressed (Raw) | Complete Sequence / Fixed Frame Window | Fixed Subject-based Split (Targeted Identities) | Custom Academic | [UADFV Source](https://www.kaggle.com/datasets/adityakeshri9234/uadfv-dataset) |
| **DeepFakeTIMIT** | MP4 Video (MPEG-4) | ~2 GB | v1.0 / Low-Q ($64^2$) & High-Q ($128^2$) | Full Sequence Tracking | Subject-Independent Split (VidTIMIT ID isolation) | CC BY-NC-SA 4.0 | [IDIAP Portal](https://www.idiap.ch/en/dataset/deepfaketimit) |
| **FaceForensics++** | MP4 Video (H.264) | ~500 GB | v1.0 / Raw (c0), HQ (c23), LQ (c40) | Evenly Spaced Intermittent Frame Extraction | 720 Train / 140 Validation / 140 Test (Videos) | Custom Restrictive | [FF++ Source](https://github.com/ondyari/FaceForensics) |
| **Celeb-DF v2** | MP4 Video (H.264) | ~250 GB | v2.0 / Standard MP4 Broadcast Compression | Face-Detection Anchored Sampling | Identity Cut-off (Diverse subjects isolated to Test set) | Custom Research | [Celeb-DF Project](https://github.com/yuezunli/celeb-deepfakeforensics) |
| **WildDeepFake** | PNG Cropped Images | ~30-50 GB | v1.0 / Variable Native Web Compression | Extracted Facial Crop Sequences (No-drop tracking) | 80% Train / 20% Test (Randomly split by sequence) | Research Only | [WildDF Repository](https://github.com/OpenTAI/wild-deepfake) |
| **DFDC** | MP4 Video (H.264) + Audio | ~480 GB | Final Production / Variable (Simulated Augmentation) | Randomized Stratified Chunk Selection | Strict Actor-Independent Split (No overlap across sets) | CC BY-NC 4.0 | [Meta AI Dataset](https://ai.meta.com/datasets/dfdc/) |
| **FakeAVCeleb** | MP4 Video (H.264) + Audio | ~150-200 GB | v1.0 / Standardized H.264 Web Compression | Audio-Frame Boundary Coordinated Extraction | 70% Train / 15% Validation / 15% Test (Demographic) | CC BY 4.0 | [FakeAVCeleb Source](https://sites.google.com/view/fakeavcelebdash-lab/) |
| **NIST/OpenMFC** | Mixed (Video + Images) | Variable | Variable / Controlled Collection Compression | Challenge-Defined Sampling | Challenge-Specified Train/Test Split | Custom (License Required) | [OpenMFC Portal](https://mfc.nist.gov/) |