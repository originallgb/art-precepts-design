# Image Toolbox: model exploration context

Date: 2026-09-30. Status: source research; project use and model choice remain open.

## Why this thread exists

Grant encountered AesFA through the Android FOSS app Image Toolbox while trying to understand its available models and whether any might help Art Precepts. This is an exploratory interest in model capabilities. It does not establish a style-transfer requirement, a preferred model, or an agreed place in the project. The separate interest in Simon Willison's `llm-clip` concerns an example of embedding data in a pipeline. Neither exploration must wait for the other. See the [corrected research brief](2026-09-30-research-intent-correction.md).

## What the app source establishes

The inspected Image Toolbox source explicitly registers **AesFA** under style transfer. Its processor loads separate `aesfa_style.onnx` and `aesfa_transform.onnx` files: one processes the reference image, and the other combines its style features with the content image to produce an altered image. The same catalogue includes **Arbitrary Style Transfer**, **MicroAST**, and **VGG19 Optimization**. These are alternative entries within the style-transfer category, rather than interchangeable names for every AI tool in the app. [Model catalogue][models]; [style-transfer processor][processor].

The AesFA authors describe a method that separates image information by frequency to extract aesthetic style features. In practical terms, the user supplies a content image and a style reference, and receives a stylized image. This offers something concrete to investigate: which characteristics move across, which remain recognizable, and whether that alteration helps a creative task. Its usefulness for Art Precepts has not been established. [Official AesFA repository][aesfa].

## A small map of different jobs

These are examples in the inspected app catalogue, not a complete inventory or a ranking. The job descriptions summarize the app's classifications and model descriptions. [Catalogue][models]; [app descriptions][strings].

| Job and examples | Input | Intended output |
|---|---|---|
| Style transfer: AesFA, MicroAST | Content image and style reference | A new image with transferred visual characteristics |
| Background removal: U2Net, BiRefNet | An image | Foreground separated from its background |
| Colourization: DDColor | A grayscale image | An image with predicted colour |
| Compression repair: FBCNN | An image with compression damage | An image with reduced compression artifacts |
| Denoising: SCUNet | A noisy image | An image with reduced noise |

The catalogue also exposes upscaling, enhancement, anime, scans, depth, and AI-detection categories. A category states an intended job; it does not establish accuracy or benefit on this collection. In particular, an appealing transformed image would not by itself demonstrate a reliable design precept. [Catalogue][models].

## Evidence limits and useful open questions

- This is a source snapshot at Image Toolbox revision `693eb0222eaf631d753f31b7bbb058e95a5aa8cf`. Grant's installed version, downloaded models, and actual use have not been inspected.
- App source confirms integration, not performance or equivalence between its exported model files and the authors' reference implementation. No model was installed or run for this note.
- The AesFA authors report over-stylization and line-shaped artifacts as limitations. Their published performance claims should not be assumed to describe Android behavior or Art Precepts images. [Authors' project page][project].
- Before choosing an experiment, the useful questions are: what does each candidate change or extract; what kind of creative question could that answer; and what would make the result misleading or unhelpful? “No useful role here” remains a valid finding.

[models]: https://github.com/T8RIN/ImageToolbox/blob/693eb0222eaf631d753f31b7bbb058e95a5aa8cf/feature/ai-tools/src/main/java/com/t8rin/imagetoolbox/feature/ai_tools/domain/model/NeuralModel.kt
[processor]: https://github.com/T8RIN/ImageToolbox/blob/693eb0222eaf631d753f31b7bbb058e95a5aa8cf/feature/ai-tools/src/main/java/com/t8rin/imagetoolbox/feature/ai_tools/data/StyleTransferProcessor.kt
[strings]: https://github.com/T8RIN/ImageToolbox/blob/693eb0222eaf631d753f31b7bbb058e95a5aa8cf/core/resources/src/main/res/values/strings.xml
[aesfa]: https://github.com/Sooyyoungg/AesFA
[project]: https://aesfa-nst.github.io/AesFA/
