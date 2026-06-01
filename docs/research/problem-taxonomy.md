# Problem Taxonomy and Glossary

This glossary defines the key terms this project uses so contributors share a common vocabulary. The goal is project alignment and contributor onboarding, not an academic survey.

<br>

## MVP Scope Key 

| **Label** | **Meaning** |
| --- | --- |
| **In scope** | The MVP may report on this directly. |
| **Partial scope** | The MVP may mention or inspect this in a limited way, but should not claim to solve it. |
| **Out of scope** | Relevant to the problem space, but should not be promised by the first MVP. |

The MVP currently focuses on still images. Terms covering audio and video are included for shared vocabulary but are marked accordingly.

<br>

## Terms

### Deepfake

Media in which a real person's face, voice, or body is replaced, altered, or synthesized using deep learning. This includes both generative deepfakes, where content is created entirely by an AI model such as a GAN or diffusion model, and impersonation deepfakes, where a real person's identity is inserted into existing content through techniques like face-swap or lip-sync. This is a narrower term than *synthetic media*: a deepfake specifically involves a real person's identity.

- **Example:** A video where a politician's face is swapped onto another speaker using a generative model, with matching cloned audio.
- **MVP scope:** **Out of scope.** Full video, audio, and person-identity deepfake detection is out of scope for the MVP. However, still-image synthetic media and manipulation signals may still be relevant and are handled under AI-generated image and manipulation detection.
- **Source:** [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

---

### Synthetic Media

Any media, including images, audio, video, or text, generated or significantly modified by an AI model rather than captured directly from the physical world. Deepfakes are a subset of synthetic media, as are AI-generated images and voice clones. Synthetic media includes both fully generated content and heavily modified real content.

- **Example:** A photorealistic portrait of a person who does not exist, produced by a diffusion model.
- **MVP scope:** **Partial scope.** Still-image synthetic-media signals may be explored; broad synthetic media coverage across audio and video is a later phase.
- **Source:** [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

---

### Cheapfake

Misleading media produced with simple, non-AI techniques such as relabelling, mis-captioning, slowing down, speeding up, or basic editing. Cheapfakes are often more widespread and impactful than deepfakes because they require no technical skill.

- **Example:** A real video of a public figure slowed down to make them appear impaired, then shared with a misleading caption.
- **MVP scope:** **Out of scope.** The MVP should avoid claiming it can detect all misleading edits or context changes.
- **Source:** [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

---

### Face Swap

A specific deepfake technique where one person's face is replaced with another's in an image or video, typically while preserving the original expression, lighting, and head pose. Face swaps are one of the most common forms of deepfakes and can range from simple effects to full AI manipulations.

- **Example:** Swapping someones face onto the body of a celebrity, a movie character, or a historical figure.
- **MVP scope:** **Out of scope.** Video face-swap detection is a later phase. Still-image artifacts may be noted only if supported by a selected model.
- **Source:** [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

---

### Voice Clone

Synthetic audio that imitates a specific person's voice, tone, cadence, or speaking style. Modern neural voice cloning systems can learn to reproduce a person's voice from only a few audio samples, using deep learning techniques such as speaker adaptation and speaker encoding to capture speaker characteristics like pitch, speech rate, and accent.

- **Example:** A politician's voice is cloned from publicly available speech recordings and used to generate a fake audio clip of them announcing a policy position they never took, which is then shared on social media ahead of an election.
- **MVP scope:** **Out of scope.** Audio ingestion and voice-clone detection are not part of the image-first MVP.
- **Source:** [Arık et al. - "Neural Voice Cloning with a Few Samples" (NeurIPS, 2018)](https://proceedings.neurips.cc/paper_files/paper/2018/file/4559912e7a94a9c32b09d894f2bc3c82-Paper.pdf) | [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

---

### AI-generated image

An image produced entirely by a generative model such as a GAN or diffusion model, from a prompt or other input, with no underlying photograph. These images can be highly photorealistic and are increasingly difficult for people to distinguish from real photographs. This is distinct from an *AI-edited image*, which starts from a real photo.

- **Example:** A diffusion model creates a photorealistic image of a street protest or of a politician at a rally that never took place.
- **MVP scope:** **In scope.** A baseline generated-image signal is part of the image-first MVP.
- **Source:** [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

---

### AI-edited Image

A real photograph that has been modified using AI tools such as inpainting, outpainting, generative fill, or AI-based retouching. The base image is authentic, but parts have been altered, removed, or extended by a generative model. AI-edited images are distinct from fully AI-generated images because they start from a real
capture, making manipulation harder to detect.

- **Example:** A real news photo where a person has been removed using generative fill, with the surrounding background reconstructed seamlessly by a diffusion model.
- **MVP scope:** **Partial scope.** The MVP may report image-manipulation signals but should not promise reliable detection of every AI edit.
- **Source:** [Jiang et al. - "Image Inpainting Based on Generative Adversarial Networks" (IEEE Access, 2020)](https://ieeexplore.ieee.org/document/8974211) | [Wang et al. - "Continuous Image Outpainting with Neural ODE" (ACM TOMM, 2024)](https://dl.acm.org/doi/full/10.1145/3648367)

---

### Misinformation

False or misleading information shared without intent to deceive. The person sharing may sincerely believe it is true. Distinguished from *disinformation* by intent.

- **Example:** A user reposts an old storm photo believing it shows today's local flooding.
- **MVP scope:** **Out of scope.** The MVP may provide media evidence, but it should not decide whether a broader claim is true.
- **Source:** [Canadian Museum for Human Rights - "Misinformation, Disinformation and Malinformation"](https://humanrights.ca/resource-guide/misinformation-disinformation-and-malinformation#section_1)

---

### Disinformation

False or misleading information shared with intent to deceive, manipulate, or cause harm. The same content can be misinformation when shared by one person and disinformation when shared by another.

- **Example:** A coordinated account network distributes a fabricated image to discredit a public figure before an election.
- **MVP scope:** **Out of scope.** Intent and campaign attribution are not MVP responsibilities.
- **Source:** [Canadian Museum for Human Rights - "Misinformation, Disinformation and Malinformation"](https://humanrights.ca/resource-guide/misinformation-disinformation-and-malinformation#section_1)

---

### Provenance

Verifiable information about where a piece of media came from, who created or modified it, when, and how. Strong provenance is cryptographically signed and travels with the file. Provenance establishes origin and history but cannot confirm whether the content depicts something true. Additionally, missing provenance must not be treated as proof of fakery.

- **Example:** A news photo published with a Content Credentials manifest attached, showing the camera make, capture time, and a signed record of edits made before publication.
- **MVP scope:** **In scope.** Basic metadata and provenance checks can be reported when available, with clear limitations stated.
- **Source:** [C2PA - "C2PA Explainer"](https://spec.c2pa.org/specifications/specifications/1.3/explainer/_attachments/Explainer.pdf)

---

### Watermark

A unique identifier embedded in media to identify its source, authenticity, or AI-generated nature. Watermarks may be visible (logos, overlays) or invisible (hidden in pixel values or frequency components of the image). 

- **Example:** Google SynthID embeds an imperceptible signal into images produced by Imagen, which a compatible detector can later recognize.
- **MVP scope:** **Partial scope.** The MVP may report known metadata or provenance markers; robust watermark detection is a later phase unless a low-cost supported tool is available.
- **Source:** [Begum & Uddin - "Digital Image Watermarking Techniques: A Review" (MDPI, 2020)](https://www.mdpi.com/2078-2489/11/2/110)

---

### Manipulation Detection

The process of analyzing media to identify signs of editing, generation, or manipulation. Detection approaches fall into two broad categories: learning-based, where a model is trained to distinguish real from synthetic content; and artifact-based, where specific irregularities such as pixel correlations, compression patterns, or geometric inconsistencies are analyzed as signals of manipulation. Detection is an evidence signal, not a final truth judgment. Therefore, the absence of detected manipulation does not confirm that content is authentic.

- **Example:** A learning-based detector assigns a high probability score to an image as likely AI-generated, while an artifact-based technique separately identifies that parallel lines in the image fail to converge to a consistent vanishing point. This results in a geometric inconsistency common in synthetically generated images.
- **MVP scope:** **In scope.** Narrow image-focused manipulation or synthetic-media signals may be included, with confidence language and stated limitations.
- **Source:** [Farid - "Mitigating the harms of manipulated media" (PNAS Nexus, 2025)](https://academic.oup.com/pnasnexus/article/4/7/pgaf194/8209913)

<br>

## How These Terms Relate

- **Synthetic media** is the broad umbrella. **Deepfakes**, **face swaps**, **voice clones**, and **AI-generated images** are all kinds of synthetic media.
- **AI-edited images** sit between real and synthetic: a real capture with synthetic modifications.
- **Cheapfakes** are not synthetic media but belong to the same misleading-content problem space.
- **Misinformation** and **disinformation** describe how content is *used and shared*, not how it was made. A real photo can be misinformation; a deepfake is not automatically disinformation until it is shared deceptively.
- **Provenance** and **watermarks** are signals about *origin*. **Manipulation detection** is a signal about *content*. The MVP confidence report combines both kinds of signals.

<br>

## Usage Notes

- Do not use **deepfake** as a catch-all label for every suspicious image, edit, or false claim.
- Separate **media evidence** from **claim truth**. A manipulated image can support a true claim, and an authentic image can be used alongside a false caption.
- Separate **provenance** from **detection**. Provenance shows a media history when trustworthy data exists; detection estimates whether pixels, frames, or audio contain suspicious signals.
- Report uncertainty plainly. These terms describe evidence categories, not definitive verdicts.
