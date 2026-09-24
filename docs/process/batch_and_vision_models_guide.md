# Guide: Gemini 2.5 Pro Batch API & Vision Model Landscape

This reference document outlines the technical requirements for running **Gemini 2.5 Pro via the Batch API** (50% discount), alongside a comparative survey of alternative image analysis and multimodal models available across Google Cloud and direct frontier APIs.

---

## Part 1: Gemini 2.5 Pro Batch API Requirements

Both **Google Cloud Vertex AI** and the **Google AI Studio Gemini Developer API** offer asynchronous Batch Prediction with a flat **50% discount** on all input and output tokens.

### 1. Cost Comparison (800 Artworks at ~1,150 Tokens/Work)
* **Standard Interactive Pricing**: $\sim \$3.80$ total ($\$1.25/\text{1M input}, \$5.00/\text{1M output}$).
* **Batch API Pricing (50% Off)**: $\mathbf{\sim \$1.90\text{ total}}$ ($\$0.625/\text{1M input}, \$2.50/\text{1M output}$).

---

### 2. Technical Ingestion Specifications (Vertex AI)

To submit an 800-image batch job on Vertex AI:

#### A. Input Format (`.jsonl`)
Requests must be serialized as a JSON Lines file in a Google Cloud Storage bucket (`gs://your-bucket/requests.jsonl`). Each line contains an independent `generateContent` request object:

```json
{"request": {"contents": [{"role": "user", "parts": [{"fileData": {"fileUri": "gs://lgb-art-corpus/images/0801_tower_liberties.jpg", "mimeType": "image/jpeg"}}, {"text": "Evaluate through the 5 Angles..."}]}], "systemInstruction": {"parts": [{"text": "You are an elite design critic..."}]}, "generationConfig": {"temperature": 0.2, "responseMimeType": "application/json", "responseSchema": {...}}}}
```

> [!TIP]
> **GCS URIs vs. Inline Base64**:
> While small batches can accept `inlineData` with base64 strings, for 800 high-res images ($\sim 188\text{ MB}$), using `fileData` referencing `gs://...` URIs in a Cloud Storage bucket is strongly recommended to keep the `.jsonl` manifest under 50 MB and prevent payload serialization timeouts.

#### B. Execution Commands

**Via Python SDK (`google-genai`):**
```python
from google import genai

client = genai.Client(vertexai=True, project="<gcp-project>", location="us-central1")

batch_job = client.batches.create(
    model="gemini-2.5-pro",
    src="gs://lgb-art-corpus/batch_input.jsonl",
    dest="gs://lgb-art-corpus/batch_output/"
)
print(f"Batch Job ID: {batch_job.name}")
```

**Via Google Cloud CLI (`gcloud`):**
```bash
gcloud ai batch-prediction-jobs create \
  --project=<gcp-project> \
  --region=us-central1 \
  --display-name="catalogue-precepts-800-pro" \
  --model="publishers/google/models/gemini-2.5-pro" \
  --input-dataset="gs://lgb-art-corpus/batch_input.jsonl" \
  --output-dataset="gs://lgb-art-corpus/batch_output/"
```

#### C. SLAs & Operational Constraints
* **Turnaround SLA**: Jobs are scheduled during idle cluster capacity. Most jobs complete in **20 to 60 minutes**, with a formal SLA window of up to 24 hours.
* **Partial Failures**: The output directory produces both `predictions.jsonl` (successful outputs) and `errors.jsonl` (failed rows with error codes).

---

## Part 2: Multimodal & Vision Model Landscape

When analyzing visual art, design systems, and architectural composition, models differ dramatically in their training data, aesthetic sensitivity, and cost.

### Comparative Matrix: Vision Models

| Platform | Model Name | Primary Strength for Art & Design | Bounding / Spatial Accuracy | Schema Compliance | Est. Cost (800 Works) |
| :--- | :--- | :--- | :---: | :---: | :---: |
| **Google Cloud** | **Gemini 2.5 Flash** *(Selected)* | Instant speed, massive visual training, excellent compositional grip. | High | Exceptional (`responseSchema`) | **$\sim \$0.30$** (Interactive)<br>$\sim \$0.15$ (Batch) |
| **Google Cloud** | **Gemini 2.5 Pro** | Frontier art-historical reasoning, nuanced cultural semiotics, and deep architectural critiques. | Very High | Exceptional | **$\sim \$3.80$** (Interactive)<br>$\sim \$1.90$ (Batch) |
| **Google Cloud** | **Cloud Vision API** | Traditional computer vision: Label detection, OCR, dominant color palette, safe search, web entities. | Moderate (Object boxes) | Static JSON | $\sim \$1.50$ (Rule-based; lacks LLM reasoning) |
| **GCP Model Garden** | **Qwen2-VL 72B** | Open-weights leader for fine-grained visual reasoning and dense document/map understanding. | Very High | Moderate | Self-hosted VM ($\sim \$1.50/hr$ on A100/L4) |
| **GCP Model Garden** | **PaliGemma 2 (10B/28B)** | Research-grade visual grounding and spatial coordinate localization. | Extreme (Tokenized boxes) | Basic text completion | Self-hosted VM |
| **Direct API** | **Claude 3.5 Sonnet** | Peerless aesthetic and architectural vocabulary; writes poetic, rigorous design critiques. | High | High (Tool calling) | $\sim \$3.60$ (Batch 50% off)<br>$\sim \$7.20$ (Interactive) |
| **Direct API** | **GPT-4o** | Strong general visual recognition and clear functional UI heuristic extraction. | High | High (Structured Outputs) | $\sim \$2.50$ (Batch 50% off)<br>$\sim \$5.00$ (Interactive) |
| **Direct API** | **Mistral Pixtral Large** | Open frontier vision model with native 128k context and arbitrary aspect-ratio handling. | High | High | $\sim \$2.00$ |

---

### Model Archetypes: Which Model for What Task?

1. **For Bulk Architectural & Precept Extraction**:
   * **Gemini 2.5 Flash** is unmatched in cost-to-performance ratio ($\sim \$0.30$ total). Its native handling of Google Arts & Culture CDN images is immediate, sharp, and respects structured JSON schemas 100% of the time.
2. **For Philosophical Synthesis & Playbook Generation**:
   * **Gemini 2.5 Pro** or **Claude 3.5 Sonnet** are best suited for the final step where cluster groups are summarized into design manifestos (`design.md`), as they possess the deepest philosophical and stylistic vocabulary.
3. **For Embedding & Spatial Clustering (Stage 2)**:
   * **CLIP (ViT-L/14)** or **Google SigLIP**: Best for extracting raw visual feature vectors to feed UMAP / HDBSCAN without incurring text token costs.
