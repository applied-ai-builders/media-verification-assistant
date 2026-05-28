# Open-Source Detector and Tool Survey

Status: Draft for issue #8

Goal: identify open-source or publicly documented detector/tool candidates that could support the first media verification MVP. This survey should avoid treating any model output as a truth verdict. Detector outputs should be framed as evidence signals with clear limitations.

## Table of Contents
* [Current Recommendation](#current-recommendation)
* [Other Detectors](#other-detectors)
* [Architecture Implications For Issue #12](#architecture-implications-for-issue-12)
* [Working Conclusion Before Paper Review](#working-conclusion-before-paper-review)
* [DeepfakeBench Paper Review Impact](#deepfakebench-paper-review-impact)
* [Contributor Literature Notes From Jon](#contributor-literature-notes-from-jon)
* [Detector Summary Table](#detector-summary-table)
* [Candidate Details](#candidate-details)
* [PhotoHolmes](#photoholmes)
* [DeepfakeBench](#deepfakebench)
* [Effort-AIGI-Detection](#effort-aigi-detection)
* [capcheck/ai-human-generated-image-detection](#capcheckai-human-generated-image-detection)
* [SadraCoding/SDXL-Deepfake-Detector](#sadracodingsdxl-deepfake-detector)
* [c2patool / c2pa-rs](#c2patool--c2pa-rs)


## Current Recommendations

**Detector Recommendation:** [Effort](#effort-aigi-detection) is the strongest direct detector-adapter candidate inspected so far because it has a documented one-image/folder inference demo, checkpoints for both face deepfake detection and broader AI-generated image detection, and a successful local GenImage smoke test. Its main blockers are licensing and reproducible setup.

**Architecture Recommendation:** Local async worker MVP.

* Frontend creates job; API stores job metadata; local worker runs adapters; UI polls for report.
* The architecture should not hard-code the MVP around one detector. The safer design is a media-analysis pipeline with pluggable evidence adapters and a report aggregator.
* Design the UI/report around uncertainty: show evidence cards, caveats, and "what was checked," rather than a single real/fake badge.

See [here](#architecture-implications-for-issue-12) for further discussion.

[Back to Top](#table-of-contents)

## Other Detectors

**PhotoHolmes:** worth keeping in the candidate pool as an image-forensics evidence module, especially for educational exploration of heatmap-style evidence. It should not be treated as the main MVP detector unless the team is willing to own Docker-based packaging and careful result wording.

**DeepfakeBench:** useful as a detector landscape and benchmark reference. It should not be treated as the first integration target unless the team separately commits to dataset, weights, GPU/container setup, and license review.

**The Hugging Face CapCheck model:** is the easiest quick-baseline candidate inspected so far because it uses the standard Transformers image-classification path and appears Apache-2.0 licensed. Its main weakness is weaker training-data transparency and likely concept drift. Tiny local smoke tests ran successfully, but it classified all user-provided examples as `human`, including AI-generated face and non-face examples, so it should be treated as an integration baseline rather than a reliability baseline.

**capcheck/ai-human-generated-image-detection:** A short Hugging Face search sweep found related or comparable image classifiers, including `capcheck/ai-image-detection`, `VilaVision/AIgeneratedimagedetection`, and `AashishKumar/AIVisionGuard-v2`. Those results reinforce that Hugging Face image classifiers are technically easy baseline candidates, but most inspected options are CIFake-centered or weakly documented and do not clearly displace CapCheck.

**SadraCoding/SDXL-Deepfake-Detector:** A second Hugging Face search for deepfake-focused image classifiers found `SadraCoding/SDXL-Deepfake-Detector` as a stronger face-specific candidate on paper. Local smoke tests lowered confidence because it classified every tested file as `human`, including the AI face example. Keep it only as a face-focused research candidate pending controlled aligned-face-crop testing; do not treat it as the general MVP baseline.

**c2patool:** is not a detector, but it is a strong adjacent evidence tool for provenance/content credentials. It should be considered for the media verification report, but separated from model-only detector recommendations.

This survey now satisfies the "at least 3 candidates" acceptance criterion. The recommendation should stay provisional until the team reviews licenses, confirms checkpoint terms, fills in the local image source log, and repeats follow-up tests on a larger source-labeled image set.

[Back to Top](#table-of-contents)

## Architecture Implications For Issue #12

The architecture should not hard-code the MVP around one detector, even though Effort is the current leading prototype candidate. The safer design is a media-analysis pipeline with pluggable evidence adapters and a report aggregator.

Recommended architecture direction:

- Treat detector output as one evidence signal, not the product's final truth verdict.
- Define a model adapter interface that can wrap Effort first, then later support CapCheck, PhotoHolmes methods, c2patool, metadata checks, or other detectors.
- Use an async analysis-job boundary, even if the first implementation runs jobs locally, because model inference may be slow, memory-heavy, or eventually GPU-backed.
- Keep uploaded media storage temporary by default. Store report metadata, adapter outputs, timings, and caveats, but avoid retaining original user media in the public demo unless the user explicitly opts in.
- Separate "MVP local/prototype worker" from "later scalable worker." The MVP can use local CPU inference and a simple queue, while later phases can add GPU workers, external object storage, and stronger orchestration.
- Include source, license, checkpoint, preprocessing, and limitation fields in the report schema so the UI can explain why a score should not be treated as proof.
- Add a provenance/metadata adapter path separately from model detection. c2patool/C2PA findings and model scores should be shown as different evidence categories.
- Design the UI/report around uncertainty: show evidence cards, caveats, and "what was checked," rather than a single real/fake badge.

Feasible architecture directions for the team to choose from:

| Direction | Shape | Pros | Risks | Recommendation |
| --- | --- | --- | --- | --- |
| Synchronous local MVP | Frontend calls API; API runs analysis directly and returns report | Fastest walking skeleton; simplest to understand | Slow model inference can block requests; harder to scale; weaker isolation for model dependencies | Only use for a very early demo spike |
| Local async worker MVP | Frontend creates job; API stores job metadata; local worker runs adapters; UI polls for report | Best balance of simplicity, usability, and future flexibility; isolates Effort setup behind worker boundary | Slightly more moving parts than synchronous flow | Recommended default for issue #12 |
| Split model service / GPU worker | API queues jobs to a separate model service or GPU-backed worker | Better path for heavy models, larger checkpoints, and future scaling | More infrastructure and deployment complexity; may distract from first MVP | Later-phase direction, not first build |

Recommended default:

Start with the local async worker MVP. It supports the current Effort finding without making Effort the center of the system. The first implementation can still be simple: one machine, local temporary files, one worker process, and a lightweight job table or job JSON store.

System-design risks raised by this survey:

- Effort has the best current behavior, but setup required local patches and a large checkpoint. Architecture should isolate that complexity in a worker or adapter layer.
- CapCheck and SDXL were easy to run but weak on the local smoke tests. Architecture should support swapping baselines without rewriting the frontend/report schema.
- The compressed screenshot result from Effort suggests transformed media can change model behavior. The architecture should record preprocessing and media-quality facts alongside the score.
- Non-commercial or unclear licenses can affect deployment choices. Architecture docs should distinguish research prototype use from public/business-impact deployment.

Suggested issue #12 design question:

> What is the smallest walking skeleton that accepts an image, creates an analysis job, runs one model adapter plus one metadata/provenance placeholder, and returns a caveated evidence report without permanently storing the uploaded media?

[Back to Top](#table-of-contents)

## Working Conclusion Before Paper Review

Current hypothesis:

- Effort is the strongest direct detector-adapter candidate because it has a documented one-image/folder inference path and image-first checkpoints.
- DeepfakeBench is the strongest benchmark/reference source because it compares many detector families and emphasizes standardized evaluation.
- PhotoHolmes is a useful adjacent image-forensics evidence module, but it should not be treated as a deepfake detector.

Main decision pressure:

- If the MVP needs a runnable image detector soon, investigate Effort setup and licensing first.
- If the MVP needs careful model-selection justification, use the DeepfakeBench paper to understand detector families, preprocessing, and cross-dataset evaluation pitfalls.
- If the MVP wants explainable forensic evidence beyond a fake probability, keep PhotoHolmes as a possible secondary signal.

What the DeepfakeBench paper should help answer:

- Which detector families generalize best across datasets?
- Which metrics and preprocessing choices matter most?
- Does the paper make any candidate look more practical or less practical for a first MVP baseline?
- What caveats should we include so the app does not overstate detector reliability?

[Back to Top](#table-of-contents)

## DeepfakeBench Paper Review Impact

Paper reviewed:

- https://papers.nips.cc/paper_files/paper/2023/hash/0e735e4b4f07de483cbe250130992726-Abstract-Datasets_and_Benchmarks.html

The DeepfakeBench paper reinforces the current recommendation rather than changing it. It shows that detector comparison depends heavily on standardized preprocessing, training setup, evaluation data, augmentation choices, backbone architecture, and metric selection.

Practical impact on this survey:

- Keep DeepfakeBench as a benchmark/reference source, not the first direct MVP integration.
- Keep Effort as the leading direct detector-adapter candidate so far because it has a one-image/folder demo.
- Add training data, preprocessing assumptions, and evaluation distribution as important fields for every future candidate.
- Avoid recommending any detector based only on a high benchmark number.

Paper lessons to carry into the MVP:

- Within-domain performance can look strong while cross-domain or cross-manipulation performance degrades.
- Simpler CNN-style baselines can be competitive under consistent settings, so method complexity alone should not drive selection.
- Augmentation and compression choices can help or hurt depending on detector and dataset.
- Backbone and pretraining choices materially affect detector performance.
- Detector output should be framed as an evidence signal, not a proof of real/fake status.

[Back to Top](#table-of-contents)

## Contributor Literature Notes From Jon

Status: preliminary team contribution, incorporated as context for issue #8 and issue #12.

Contributor: Jon Rubin.

Primary sources he reviewed:

- FaceForensics++: https://arxiv.org/abs/1901.08971
- DeepFake Detection Challenge Dataset: https://arxiv.org/abs/2006.07397
- Dessa DeepFake-Detection repo: https://github.com/dessa-oss/DeepFake-Detection

General information on the datasets:

- FaceForensics++ is a face-manipulation benchmark, based on 1,000 original videos pulled from youtube. The original paper considers four manipulation methods (FaceSwap, DeepFakes, Face2Face, and NeuralTextures), and contained 1.8M images from 4,000 fake videos (see section 3 of the FF paper). Subsequent revisions added the FaceShifter method to the repository and added Google's DeepFakeDetection dataset, which is based on 363 videos from paid actors (see the repository https://github.com/ondyari/FaceForensics/tree/master).
- DeepFake Detection Challenge (DFDC) is a much larger face-manipulation benchmark, based on 100,000 videos produced by 3,426 paid actors. Videos were manipulated using the DeepFake Autoencoder (DFAE), MM/NN face swap, NTH, FSGAN, StyleGAN (see section 3.2 of the DFDC paper). The training set contains 119,154 clips, the validation set has 4,000 clips, and the private test set has 10,000 clips, all ten seconds long. For further information, see section 3.5 of the DFDC paper.

Main points to carry forward:

- Face-focused detector pipelines often use face extraction/cropping before classification. This matters because the detector may learn more useful face-region signals and avoid unrelated background variation.
- Transfer learning from strong pretrained visual backbones is a recurring pattern. FaceForensics++ combined face extraction with an XceptionNet classifier. Top DFDC challenge approaches used face detection plus large CNN backbones such as EfficientNet or Xception-family models, sometimes in ensembles.
- Dataset diversity and augmentation are central to generalization. Models trained on the FF++ dataset were strong within their benchmark setting, but later work such as Dessa's project emphasized that a detector trained on the FF++ benchmark may fail on real-world or unseen manipulation methods.
- Similarly, section 2 of the DFDC paper asserts that **models trained on datasets containing 1,000 to 10,000 videos do not usually generalize to detect deepfakes in the real world.**
- In particular, this remark applies to the models considered in the FF++ paper, and also to the models considered in some more recent papers on ViT deepfake detectors (e.g. in https://kclpure.kcl.ac.uk/portal/files/271171349/Deepfake_Image_Detection.pdf and https://creativity-ai.github.io/assets/papers/5.pdf, which trained models on Kaggle datasets with 190K and 140K images, respectively)
- DFDC is useful because it scaled the problem substantially and used consenting paid actors. It is a third-generation dataset based on 100,000 videos, and the paper analyzes the performance of Kaggle challenge submissions.
- The DFDC challenge results suggest that large varied datasets can improve generalization, but not that deepfake detection is solved. According to section 6.2 of the DFDC paper, the best submitted models ``achieved an average precision of 0.753 and a ROC-AUC score of 0.734, only on real videos, which demonstrates that training on the DFDC Dataset allows a
model to generalize to real videos.''
- Training a robust detector from scratch is probably out of scope for the first MVP. The more realistic path is to evaluate and wrap existing detectors, then build a report pipeline that can incorporate stronger models later.

Impact on issue #12 architecture:

- Avoid making the MVP face-only by default. Face extraction is important if the MVP narrows to face manipulation, but the current image-first media verification direction should still support non-face generated images and provenance/metadata signals.
- Add a possible face-preprocessing adapter or stage, but keep it optional.
- Keep the model adapter boundary because face-specific detectors, general image detectors, and provenance tools will have different preprocessing assumptions.
- Record preprocessing decisions in the report output, such as whether a face was detected/cropped, image resolution, compression or screenshot status, and which detector/checkpoint was used.
- Use existing pretrained detectors for the first MVP rather than planning to train a new detector.
- Make room for future dataset/evaluation work without blocking the initial walking skeleton.

[Back to Top](#table-of-contents)

## Detector Summary Table

| Candidate | Supported media | Detector type | License | Maintenance / activity | Setup difficulty | MVP fit |
| --- | --- | --- | --- | --- | --- | --- |
| PhotoHolmes | Still images | Image forgery/manipulation forensics toolkit | Apache-2.0 base project; method licenses vary | Local clone latest commit checked: 2025-02-03 | High on native Windows; Low on MacOS; workable in Docker with fixes | Possible evidence module, not main deepfake detector |
| DeepfakeBench | Face-focused images and videos | Benchmark framework with many deepfake detector implementations | CC BY-NC 4.0 | Local clone latest commit checked: 2025-08-20 | High | Strong reference and detector shortlist source; weak direct first-MVP integration |
| Effort-AIGI-Detection | Still images | CLIP/ViT-based AI-generated image detector | README badge says CC BY-NC 4.0; no local LICENSE file found | Local clone latest commit checked: 2025-07-14 | Medium-high; local smoke test successful after patches | Leading prototype detector adapter, pending license/setup reproducibility |
| capcheck/ai-human-generated-image-detection | Still images | Hugging Face ViT AI-generated image classifier | Apache-2.0 according to model cards | Parent model README updated about 1 month before review; checkpoint files about 1 year old | Low to medium | Quick integration baseline only; weak reliability evidence from local smoke tests |
| SadraCoding/SDXL-Deepfake-Detector | Face still images/crops | Hugging Face face-focused AI-generated/deepfake detector | MIT according to model card and license file | Hugging Face page showed latest README update about 3 months before review | Medium | Face-focused research candidate only; not recommended as baseline until controlled face-crop tests pass |
| c2patool / c2pa-rs | Images, video, audio, PDF read-only, C2PA sidecars | Provenance/content-credentials tool, not a detector | MIT OR Apache-2.0 for c2pa-rs | Active toolchain moved to `contentauth/c2pa-rs`; older `contentauth/c2patool` repo is archived | Low to medium | Strong adjacent evidence signal; not a model baseline |

[Back to Top](#table-of-contents)

## Candidate Details

Following are detailed notes on the various detectors.

### PhotoHolmes

Primary source:

- https://github.com/photoholmes/photoholmes

Local source reviewed:

- `personal/photoholmes/photoholmes`

Last visible activity checked:

- Local clone latest commit: `223762c`, dated 2025-02-03, "Merge pull request #9 from Articoking/main"

Supported media:

- Still images.

Detection target:

- Image forgery/manipulation evidence.
- Not specifically a general deepfake detector or AI-generated-image detector.

Model type or architecture:

- Toolkit with multiple implemented image-forensics methods behind a shared interface.
- Listed methods include Adaptive CFA Net, CAT-Net, DQ, EXIF as Language, FOCAL, Noisesniffer, PSCC-Net, Splicebuster, TruFor, and ZERO.
- Tested method: DQ, a classic JPEG double-quantization method based on DCT coefficient analysis. DQ produces a heatmap rather than a final real/fake label.
- Tested method: CAT-Net. Also produces a heatmap.

License:

- Base project license: Apache-2.0.
- Important caveat: individual methods can have their own licenses. The PhotoHolmes README warns that TruFor has method-specific license terms, including non-profit limitations.

Setup difficulty:

- Native Windows: high. Local install failed because `jpegio==0.2.8` could not build with Microsoft Visual C++.
- MacOS: easy on Tahoe (26.3.1) with M2 chips. `uv sync` successfully built a virtual environment from the `pyproject.toml` file, and after changing line 109 of `src/photoholmes/methods/base.py` to `weights_only=False`, the unpickling errors stopped and the CAT-Net CLI ran successfully.
- Docker/Linux: workable, but not plug-and-play. A successful DQ run used `python:3.10-slim`, additional OpenCV/JPEG system packages, and `numpy<2`.
- Practical implication: a contributor-friendly MVP integration would likely need a maintained Dockerfile or pinned dependency setup.

Hands-on result:

- DQ successfully ran in Docker on the PhotoHolmes sample JPEG.
- Output generated: `test_jpeg_image_dq_heatmap.png`.
- The heatmap highlighted regions with stronger JPEG compression-pattern evidence, mostly around object boundaries and high-detail areas.
- CAT-Net ran on MacOS and produced a strong heatmap indicating an image splice.

Strengths:

- MacOS setup is straightforward.
- Image-first, matching the current image-media MVP direction.
- Provides a CLI path for running a method on one image.
- Can output heatmap-style evidence that could map to an evidence-card UI.
- Includes multiple methods and benchmarking abstractions.
- Useful for learning how image-forensics signals differ from a simple fake/not-fake classifier.

Weaknesses:

- Not deepfake-specific.
- Native Windows setup failed in local testing.
- Docker setup required extra system packages and dependency pinning.
- Method-specific licenses need review before any production-style use.
- Some methods require pretrained weights and may have additional setup/licensing constraints.
- DQ heatmaps can be easy to overinterpret; strong edge responses are not proof of manipulation.

Recommendation:

- Keep PhotoHolmes as a research candidate and possible image-forensics evidence module.
- Do not choose it as the sole baseline detector for the MVP yet.
- If the team wants to pursue it further, create a separate packaging/setup issue for a reproducible Docker environment and test at least one additional PhotoHolmes method beyond DQ.

Plain-language caveat for future UI/reporting:

> This signal highlights regions with possible JPEG recompression or tampering evidence. It does not prove the image is fake, AI-generated, or misleading.

Open questions:

- Which PhotoHolmes methods have licenses compatible with the project?
- Which methods can run without large pretrained weights?
- Can the output be explained clearly to non-expert users?
- Is heatmap evidence useful for the MVP, or would it distract from a simpler first demo?
- Would the team accept Docker as the expected environment for this component?

[Back to Top](#table-of-contents)

### DeepfakeBench

Primary sources:

- https://github.com/SCLBD/DeepfakeBench
- Local clone: `personal/deepfakebench/DeepfakeBench`

Last visible activity checked:

- Local clone latest commit: `f188b1c`, dated 2025-08-20, "Update trainer.py"
- Official GitHub page showed 218 commits when checked.

Supported media:

- Face-focused image and video deepfake detection.
- The README describes 28 image detectors and 8 video detectors.
- A newer linked detector, Effort, is described by the README as supporting both face deepfake images and broader synthetic images, but that linked detector should be evaluated separately before we rely on that claim.

Detection target:

- Deepfake and face-forgery detection across benchmark datasets.
- Better framed as a benchmark/evaluation framework than as a single detector.

Model type or architecture:

- Multiple detector families, including CNN baselines, spatial detectors, frequency detectors, ViT/CLIP-style detectors, and temporal/video detectors.
- Examples listed by the README include Xception, MesoNet, EfficientNet-B4, Face X-ray, F3Net, SPSL, SRM, SBI, LSDA, Effort, TALL, I3D, FTCN, VideoMAE, and X-CLIP.

License:

- CC BY-NC 4.0.
- This is a major caveat because the non-commercial restriction may conflict with future business-impact or deployment goals.

Setup difficulty:

- High.
- Documented setup uses either a Conda environment with Python 3.7.2 or a CUDA-oriented Docker image.
- The README Docker example expects GPU support and `--shm-size 64G`.
- Local clone does not include detector weights or datasets.
- Evaluation requires detector config, pretrained weights, dataset files or LMDB, and dataset JSON metadata.

Hands-on result:

- No model run attempted.
- Reason: the local clone has no `training/weights`, no dataset files under `datasets/rgb` or `datasets/lmdb`, and the documented test path is benchmark-dataset oriented rather than a one-image inference demo.

Strengths:

- Broad survey value: many detector implementations in one repo.
- Strong benchmark/evaluation framing.
- Directly relevant to cross-dataset generalization and detector comparison.
- Provides pretrained-weight links and standard evaluation scripts.
- Useful for deciding which individual detector repos or papers deserve deeper inspection.

Weaknesses:

- Not a simple MVP component.
- Non-commercial license needs careful review.
- No obvious single-image or end-user inference path.
- Requires datasets, weights, and old/deep learning environment setup.
- Dataset rights and access terms are separate from the code license.
- Model outputs are benchmark predictions/metrics, not an explainable media verification report.

Recommendation:

- Keep DeepfakeBench as a high-value research and detector-shortlisting reference.
- Do not choose it as the first direct MVP integration target.
- Use it to identify one or two individual detectors to inspect next, such as Effort, SBI, or Xception.

Plain-language caveat for future UI/reporting:

> Benchmark performance does not mean a detector is reliable on arbitrary user-submitted media. The result depends on training data, preprocessing, compression, media type, and how similar the uploaded media is to the evaluation data.

Open questions:

- Which individual DeepfakeBench detector has the best license, setup, and output tradeoff?
- Can any candidate run without large dataset setup?
- Do pretrained weights have separate licensing or use restrictions?
- Is Effort a better standalone candidate than the benchmark framework itself?
- Should we treat DeepfakeBench as evaluation infrastructure rather than app infrastructure?

[Back to Top](#table-of-contents)

### Effort-AIGI-Detection

Primary sources:

- https://github.com/YZY-stack/Effort-AIGI-Detection
- https://arxiv.org/abs/2411.15633
- Local clone: `personal/effort-aigi-detection`

Last visible activity checked:

- Local clone latest commit: `96f5dea`, dated 2025-07-14, "Update __init__.py"
- Official GitHub page showed 36 commits when checked.

Supported media:

- Still images.
- The README describes checkpoints for face deepfake detection and broader AI-generated image detection.
- The demo script accepts one image or a folder of images.

Detection target:

- AI-generated images.
- Face deepfake images when using the FaceForensics++-trained checkpoint.
- Broader generated-image detection when using the GenImage or Chameleon checkpoints.

Model type or architecture:

- CLIP ViT-L/14 vision model.
- The Effort method applies SVD-based orthogonal subspace decomposition to self-attention linear layers, freezing principal components and adapting residual components.
- The implementation adds a binary classification head and returns fake probability.

License:

- The README badge says CC BY-NC 4.0.
- No `LICENSE` file was found in the local clone.
- Treat license status as a blocker until confirmed, especially because the non-commercial restriction may conflict with future business-impact or deployment goals.

Setup difficulty:

- Medium-high to high.
- `install.sh` uses older deep-learning dependencies, including PyTorch 1.12.0 with CUDA 11.3, dlib, transformers, and OpenAI CLIP from GitHub.
- Inference requires a checkpoint downloaded from Google Drive.
- The detector code expects a local CLIP model folder at `../models--openai--clip-vit-large-patch14`, so a clean setup likely needs a wrapper or code adjustment.

Hands-on result:

- Repo cloned and inspected.
- GenImage checkpoint downloaded from the README's Google Drive link and saved locally as `effort_genimage.pth`.
- SHA256 recorded: `7C32CEB4E66D303050E8FC5DC7543FA347693FB4EE6B5DF4D6EAF9F6A92FB813`.
- Non-face folder smoke test ran successfully after patching the ignored personal clone for lighter local inference.
- Results on four local images:
  - `ai-face-example.png`: fake probability 0.8544.
  - `ai-nonface-example.png`: fake probability 0.9828.
  - `compressed-ai-face-screenshot.png`: fake probability 0.3602.
  - `real-face-photo.jpg`: fake probability 0.0484.
- This is the best local detector behavior observed so far, but it remains a tiny smoke test rather than a benchmark. The compressed screenshot result suggests transformed media needs separate testing.

Strengths:

- Best direct inference path among the surveyed candidates so far.
- Image-first scope is closer to the likely MVP than video-only benchmark code.
- Provides separate checkpoints for face deepfake detection and broader AI-generated image detection.
- Outputs fake probability, which can map naturally to an evidence-card prototype.
- Based on recent research focused on generalization.

Weaknesses:

- License is a serious concern.
- No local license file was found.
- Manual checkpoint download required.
- Hardcoded local CLIP model path adds setup friction.
- Probability output still needs calibration and careful caveats.
- The demo is not an evidence report; it is a detector score.

Recommendation:

- Keep Effort as the leading direct detector-adapter candidate for a prototype.
- Do not integrate it into the MVP until license, checkpoint terms, and reproducible setup path are clarified.
- If the team wants to test it, start with the GenImage or Chameleon checkpoint for broader image verification, or FaceForensics++ only if the MVP narrows to face deepfake images.

Plain-language caveat for future UI/reporting:

> This score estimates whether the image resembles examples the detector learned as synthetic or fake. It is not proof that the image is fake, and reliability depends on the checkpoint, image type, preprocessing, compression, and training data.

Open questions:

- Can the detector run acceptably on CPU, or is GPU expected?
- Can the CLIP model dependency be loaded from Hugging Face instead of a hardcoded local folder?
- What are the checkpoint license and usage terms?
- Which checkpoint best matches the MVP: FaceForensics++, GenImage, or Chameleon?
- How should the UI phrase a fake probability without implying certainty?

[Back to Top](#table-of-contents)

### capcheck/ai-human-generated-image-detection

Primary sources:

- https://huggingface.co/capcheck/ai-human-generated-image-detection
- https://huggingface.co/dima806/ai_vs_human_generated_image_detection
- https://huggingface.co/dima806/ai_vs_human_generated_image_detection/tree/main

Supporting source reviewed by user:

- Kaggle notebook: "AI vs human generated images prediction ViT" by `dima806`

Supported media:

- Still images.

Detection target:

- Human-created vs AI-generated images.
- Not a video deepfake detector, provenance checker, or broad misinformation detector.

Model type or architecture:

- ViT-Base image classifier.
- About 85.8M parameters.
- 224x224 input size.
- Labels: `human`, `AI-generated`.

License:

- Apache-2.0 according to the CapCheck and parent Hugging Face model cards.
- Parent Kaggle notebook is also listed as Apache-2.0.

Setup difficulty:

- Low to medium.
- Uses standard Hugging Face `transformers.pipeline("image-classification")`.
- Parent model files include `config.json`, `model.safetensors`, `preprocessor_config.json`, and `training_args.bin`.
- Parent `model.safetensors` is about 343 MB.

Hands-on result:

- User inspected the Hugging Face model card, parent model files page, and Kaggle page.
- A local smoke test ran successfully in `personal/issue-8-model-test` using CPU PyTorch and the standard Hugging Face image-classification pipeline.
- Three user-provided files were tested: `human-photo.jpg`, `ai-generated-example.png`, and `compressed-screenshot.png`.
- The model classified all three as `human`, including `ai-generated-example.png` with score 0.9845.
- An expanded local test used `real-face-photo.jpg`, `ai-face-example.png`, `ai-nonface-example.png`, and `compressed-ai-face-screenshot.png`.
- The model again classified all files as `human`, including `ai-face-example.png` with score 0.9883 and `ai-nonface-example.png` with score 0.9845.
- This is not an accuracy benchmark, but it is an important caution: the model can be easy to integrate while still producing high-confidence misses on AI-generated images.

Related Hugging Face search sweep:

- `capcheck/ai-image-detection`: closely related CapCheck model with Apache-2.0 license, ViT architecture, `model.safetensors` around 343 MB, 4 commits, 1 contributor, and latest visible update about 5 months before review. Useful as related evidence, but not an independent top candidate.
- `VilaVision/AIgeneratedimagedetection`: MIT-licensed DenseNet121 classifier with classes for DALL-E generated, human-created, and other AI-generated images. It has raw PyTorch `.pth` weights around 28.4 MB and latest visible update over 1 year before review. Kept as a weak/maybe candidate because setup is less standardized and dataset/generalization evidence is thin.
- `AashishKumar/AIVisionGuard-v2`: Apache-2.0 ViT image classifier using `google/vit-base-patch16-224`, standard Hugging Face files, `model.safetensors` around 343 MB, 7 commits, 1 contributor, and latest visible update over 1 year before review. Kept as a maybe candidate, but it appears CIFake-centered and its model-card metrics are internally inconsistent.

Strengths:

- Easiest prototype candidate so far.
- Standard Transformers interface.
- Permissive license according to model cards.
- Can run on one image with a simple local inference call.
- Output labels and scores map easily to an evidence-card prototype.

Weaknesses:

- Training data is described only generally as "AI-generated vs human-created images."
- Parent model card warns about concept drift because image generators have improved since training.
- Parent model's high reported accuracy should not be treated as real-world reliability.
- Local smoke tests classified multiple user-provided AI-generated examples as `human` with high confidence.
- Compression can affect results.
- Works best on clear images at least 224x224 pixels.
- We have not verified dataset composition, generator coverage, leakage risk, or robustness.

Recommendation:

- Keep as a quick baseline candidate for early prototyping.
- Do not present it as a scientifically strong detector.
- Treat it as an integration baseline rather than a reliability baseline.
- If the team investigates it further, use a larger controlled set and treat current results as a warning against relying on model-card metrics.

Plain-language caveat for future UI/reporting:

> This model estimates whether an image resembles examples labeled as human-created or AI-generated in its training data. New generators, compression, resizing, and unfamiliar image types can change the result.

Open questions:

- What exact dataset was used for the parent model?
- Which generators and human-image sources are represented?
- How does it behave on screenshots, memes, social-media-compressed images, or edited photographs?
- Is a simple Hugging Face classifier good enough as a baseline if the report language is careful?
- Should this be used only as a low-cost comparison point against Effort?

[Back to Top](#table-of-contents)

### SadraCoding/SDXL-Deepfake-Detector

Primary source:

- https://huggingface.co/SadraCoding/SDXL-Deepfake-Detector

Supported media:

- Still images, specifically human face images or face crops.

Detection target:

- Artificial/AI-generated/deepfake faces vs human faces.
- Label mapping in the model card: `0` is `artificial`; `1` is `human`.

Model type or architecture:

- Hugging Face image-classification model.
- The model card describes a fine-tuned vision transformer; tags include `swin`, `vision-transformer`, `deepfake-detection`, and `fake-face-detection`.
- Model size shown by Hugging Face: about 86.8M parameters.

License:

- MIT according to the Hugging Face model card/tag and visible `LICENSE` file.

Setup difficulty:

- Medium.
- The model uses standard Hugging Face files: `config.json`, `model.safetensors`, `preprocessor_config.json`, and `training_args.bin`.
- `model.safetensors` is about 347 MB.
- The model card shows a simple local setup using `transformers`, `torch`, and `pillow`, with a `python predict.py --image path/to/image` workflow.
- Local testing found that the default Hugging Face `pipeline("image-classification")` path failed because the image processor metadata did not load cleanly. The runner needed `torchvision` plus a fallback using `AutoModelForImageClassification` and explicit `ViTImageProcessor`.

Last visible activity checked:

- Hugging Face files page showed 25 commits and 1 contributor.
- Latest visible README update was about 3 months before review.
- Core model files and license were uploaded about 6 months before review.
- Model page showed 83 downloads in the previous month when reviewed.

Training/evaluation notes:

- Model card says it is fine-tuned on `xhlu/140k-real-and-fake-faces`.
- Self-reported evaluation result: 86% accuracy on `140k Real and Fake Faces`.
- Treat the accuracy as model-card evidence only, not as proof of real-world reliability.

Hands-on result:

- A local smoke test ran successfully only after adding a fallback loader.
- The same three files used in the CapCheck smoke test were used: `human-photo.jpg`, `ai-generated-example.png`, and `compressed-screenshot.png`.
- The model classified all three as `human`, including `ai-generated-example.png` with score 0.9958.
- An expanded local test used `real-face-photo.jpg`, `ai-face-example.png`, `ai-nonface-example.png`, and `compressed-ai-face-screenshot.png`.
- The model again classified all files as `human`, including `ai-face-example.png` with score 1.0000 and `ai-nonface-example.png` with score 0.9958.
- Because this is a face-focused model and the files may not match its expected aligned-face-crop distribution, this should be treated as a scope-boundary finding rather than a fair benchmark. The AI face result still lowers confidence until tested with controlled face crops.

Strengths:

- More face/deepfake-specific than generic AI-image classifiers.
- Permissive license.
- Standard Hugging Face file layout.
- Simple local inference path.
- Explicit limitation language.
- Useful if the MVP narrows to aligned face-image verification.

Weaknesses:

- Narrow scope: trained primarily on frontal, well-lit, aligned face crops.
- Less plug-and-play than expected because the default pipeline path failed during local testing.
- Local smoke tests classified the user-provided AI face example as `human` with high confidence.
- The model card warns it may underperform on low-resolution, blurry, occluded, or non-frontal faces.
- The model card also warns it may underperform on GAN-generated faces such as StyleGAN2/3.
- It is not a general image provenance tool, video deepfake detector, or broad misinformation detector.
- Reported metrics are self-reported on a specific dataset.

Recommendation:

- Keep as a solid face-focused Hugging Face baseline candidate.
- Do not choose it as the general MVP baseline.
- Require a proper follow-up test with controlled real and synthetic aligned face crops before recommending it for a face-focused MVP path.
- If tested further, compare it against CapCheck and at least one obvious non-face AI-generated image to understand scope boundaries.

Plain-language caveat for future UI/reporting:

> This model estimates whether a face image resembles examples labeled as artificial or human in its training data. It is not forensic proof, and results may degrade on blurry, low-resolution, occluded, non-frontal, or non-face images.

Open questions:

- Does the MVP want face-crop-only behavior, or general image upload behavior?
- Would we need a face detector/cropper before this model?
- How does it behave on full-scene images with small faces?
- Are the dataset and model license terms sufficient for the project's future use cases?
- Does it outperform CapCheck on face-focused examples?

[Back to Top](#table-of-contents)

### c2patool / c2pa-rs

Primary sources:

- https://opensource.contentauthenticity.org/docs/c2patool/docs/usage/
- https://opensource.contentauthenticity.org/docs/c2patool/docs/supported-formats/
- https://github.com/contentauth/c2pa-rs

Supported media:

- Images: JPEG, PNG, AVIF, GIF, HEIC/HEIF, JXL, SVG, TIFF, WebP, DNG.
- Video: AVI, MP4, MOV.
- Audio: FLAC, M4A, MP3, WAV.
- PDF is supported read-only.
- `.c2pa` manifest stores are supported.

Detection target:

- Not a detector.
- Reads and validates C2PA/content-credentials manifests.
- Can report manifest data, validation status, certificate chains, trust status, assertion structure, and ingredients.

Model type or architecture:

- No model.
- Command-line provenance and manifest tooling backed by the C2PA SDK.

License:

- `contentauth/c2pa-rs` is MIT OR Apache-2.0.
- The older `contentauth/c2patool` repo is archived and points users to `contentauth/c2pa-rs`.

Setup difficulty:

- Low to medium, depending on install path.
- `c2patool` is not currently installed locally.

Useful read-only commands if installed:

```powershell
c2patool path\to\image.jpg --info
c2patool path\to\image.jpg --tree
c2patool path\to\image.jpg -d
c2patool path\to\image.jpg --certs
```

Strengths:

- Standards-based provenance signal.
- No model weights or training data.
- Complements detector outputs well.
- Broad media support.
- Can help the MVP report "credentials found and validated" vs "no credentials found" vs "credentials found but validation failed."

Weaknesses:

- Not a deepfake detector.
- Many real-world files will have no C2PA metadata.
- Absence of a manifest does not mean fake.
- Presence of a manifest does not prove the content is true or contextually non-misleading.
- Trust-list and certificate interpretation can be confusing.

Recommendation:

- Keep c2patool as an adjacent evidence-pipeline candidate.
- Do not count it as a model baseline.
- Consider a separate issue or subsection for provenance checks if the MVP report includes multiple evidence signals.

Plain-language caveat for future UI/reporting:

> Content credentials can describe where media came from or how it was edited when that information is present and verifiable. Missing credentials do not prove the media is fake, and valid credentials do not prove the media is being used honestly.

Open questions:

- Should the first MVP include a C2PA/provenance check by default?
- Should "no C2PA credentials found" appear as a report field?
- Should trust-list validation be in scope for the first demo?
- Should provenance tools live in this model survey or a separate evidence-signal survey?

[Back to Top](#table-of-contents)
