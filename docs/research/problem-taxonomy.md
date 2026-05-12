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

Media in which a real person's face, voice, or body is replaced, altered, or synthesized using deep learning to make them appear to say or do something they did not. In this project we use it as a narrower term than *synthetic media*: a deepfake specifically involves a real person's identity.

- **Example:** A video where a politician's face is swapped onto another speaker using a generative model, with matching cloned audio.
- **MVP scope:** **Out of scope.** Full deepfake detection, especially for video and audio, is not the first target. The MVP may mention deepfakes as context but should not claim to detect them.
- **Source:** [datacamp - "What Are Deepfakes? Examples, Applications, Ethical Challenges"](https://www.datacamp.com/blog/deepfakes?utm_cid=22660585401&utm_aid=181540419795&utm_campaign=230119_1-ps-other~dsa-tofu~blog_2-b2c_3-nam_4-prc_5-na_6-na_7-le_8-pdsh-go_9-nb-e_10-na_11-na&utm_loc=9001538-&utm_mtd=-c&utm_kw=&utm_source=google&utm_medium=paid_search&utm_content=ps-other~nam-en~dsa~tofu~blog~artificial-intelligence&gad_source=1&gad_campaignid=22660585401&gbraid=0AAAAADQ9WsHdXIRc0YRXYNjTY4im2oyEa&gclid=CjwKCAjwtvvPBhBuEiwAPMijr4_F8znIhtS60GzaMXTnRG1G4vNwtYQyEDuRNJgh8c7w_2MR1npidBoCl-YQAvD_BwE)

---

### Synthetic Media

Any media (image, audio, video, or text) generated or significantly modified by an algorithm rather than captured directly from the physical world. Deepfakes are a subset of synthetic media, as are AI-generated images and voice clones.

- **Example:** A photorealistic portrait of a person who does not exist, produced by a diffusion model.
- **MVP scope:** **Partial scope.** Still-image synthetic-media signals may be explored; broad synthetic media coverage across audio and video is a later phase.
- **Source:** [D-iD - "Synthetic Media"](https://www.d-id.com/resources/glossary/synthetic-media/)

---

### Cheapfake

Misleading media produced with simple, non-AI techniques such as relabelling, mis-captioning, slowing down, speeding up, or basic editing. Cheapfakes are often more widespread and impactful than deepfakes because they require no technical skill.

- **Example:** A real video of a public figure slowed down to make them appear impaired, then shared with a misleading caption.
- **MVP scope:** **Out of scope.** The MVP should avoid claiming it can detect all misleading edits or context changes.
- **Source:** [Data & Society - "Deepfakes and Cheap Fakes"](https://datasociety.net/library/deepfakes-and-cheap-fakes/)

---

### Face Swap

A specific deepfake technique where one person's face is replaced with another's in an image or video, typically while preserving the original expression, lighting, and head pose. Face swaps can range from simple effects to full AI manipulations.

- **Example:** A celebrity's face inserted onto an actor's body in an existing film.
- **MVP scope:** **Out of scope.** Video face-swap detection is a later phase. Still-image artifacts may be noted only if supported by a selected model.
- **Source:** [ui42 - "What is Faceswap"](https://www.ui42.com/dictionary/faceswap)

---

### Voice Clone

Synthetic audio that imitates a specific person's voice, tone, cadence, or speaking style, typically generated from a sample of their real speech.

- **Example:** A scam caller uses generated audio that sounds like a company executive requesting an urgent money transfer.
- **MVP scope:** **Out of scope.** Audio ingestion and voice-clone detection are not part of the image-first MVP.
- **Source:** [rws - "What is voice cloning?"](https://www.rws.com/blog/what-is-voice-cloning/)

---

### AI-generated image

An image produced entirely by a generative model from a prompt or other input, with no underlying photograph. Distinct from an *AI-edited image*, which starts from a real photo.

- **Example:** A diffusion model creates a photorealistic image of a street protest that never happened.
- **MVP scope:** **In scope.** A baseline generated-image signal is part of the image-first MVP.
- **Source:** [Cloudflare - "What is AI image generation"](https://www.cloudflare.com/learning/ai/ai-image-generation/)

---

### AI-edited image

A real photograph that has been modified using AI tools such as inpainting, outpainting, generative fill, or AI-based retouching. The base image is authentic, but parts have been altered or extended by a model.

- **Example:** A real news photo where a person has been removed using generative fill.
- **MVP scope:** **Partial scope.** The MVP may report image-manipulation signals but should not promise reliable detection of every AI edit.
- **Source:** [Narrative - "AI Editing Explained: A Game Changer For Photographers"](https://narrative.so/blog/ai-editing-explained-a-game-changer-for-photographers) | [Artsmart - "What Is Inpainting and Outpainting? A Guide to AI’s Creative Magic"](https://artsmart.ai/blog/what-is-inpainting-and-outpainting/)

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

Verifiable information about where a piece of media came from, who created or modified it, when, and how. Strong provenance is cryptographically signed and travels with the file. Missing provenance must not be treated as proof of fakery.

- **Example:** Digital photo Metadata that records the original camera settings, the exact time the photo was taken, and any subsequent edits made in software like Photoshop.
- **MVP scope:** **In scope.** Basic metadata and provenance checks can be reported when available, with clear limitations stated.
- **Source:** [Numbers Protocol - "What is provenance and how does it work?"](https://docs.numbersprotocol.io/introduction/faq/what-is-provenance-and-how-does-it-work/)

---

### Watermark

A unique identifoer embedded in media to identify its source, authenticity, or AI-generated nature. Watermarks may be visible (logos, overlays) or invisible (hidden in the color patterns of an image or video,). 

- **Example:** Google SynthID embeds an imperceptible signal into images produced by Imagen, which a compatible detector can later recognize.
- **MVP scope:** **Partial scope.** The MVP may report known metadata or provenance markers; robust watermark detection is a later phase unless a low-cost supported tool is available.
- **Source:** [Box - "What is a digital watermark?"](https://www.box.com/resources/what-is-a-digital-watermark)

---

### Manipulation Detection

Techniques and models that identify whether media has been altered or synthesized, regardless of whether provenance information is available. Includes classical forensics (compression artifacts, error level analysis, sensor noise) and learned detectors trained on synthetic versus real media. It is an evidence signal, not a final truth judgment.

- **Example:** A model flags facial regions as likely face-swapped based on inconsistent blending, lighting, and compression artifacts.
- **MVP scope:** **In scope.** Narrow image-focused manipulation or synthetic-media signals may be included, with confidence language and stated limitations.
- **Source:** [Pindrop - "Deepfake Detection"](https://www.pindrop.com/glossary/deepfake-detection/#:~:text=Comparing%20audio%20with%20lip%20movements,platforms%20adapt%20to%20new%20threats.)

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
