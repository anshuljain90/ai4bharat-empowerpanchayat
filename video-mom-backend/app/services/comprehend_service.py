import json
import logging
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)

ANALYSIS_PROMPT = """Analyze the following citizen issue text. Return ONLY valid JSON with this exact structure:
{
  "sentiment": {"label": "POSITIVE|NEGATIVE|NEUTRAL|MIXED", "score": 0.0, "scores": {"positive": 0.0, "negative": 0.0, "neutral": 0.0, "mixed": 0.0}},
  "keyPhrases": ["phrase1", "phrase2"],
  "suggestedPriority": "URGENT|NORMAL"
}

Rules:
- sentiment.label: The dominant sentiment
- sentiment.score: Confidence of dominant sentiment (0-1)
- sentiment.scores: All sentiment scores (must sum to ~1.0)
- keyPhrases: Top key phrases (max 10)
- suggestedPriority: URGENT if the issue involves health, safety, infrastructure damage, or strong negative sentiment. NORMAL otherwise.
- Return ONLY the JSON, no explanation.

Text to analyze:
"""


class ComprehendService:
    """Issue analysis using Amazon Bedrock (Nova Lite) for sentiment and key phrase extraction."""

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            kwargs = {"service_name": "bedrock-runtime", "region_name": settings.AWS_REGION}
            if settings.AWS_ACCESS_KEY_ID:
                kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            self.client = boto3.client(**kwargs)
            logger.info("[IssueAnalyzer] Bedrock client initialized for issue analysis")
        except Exception as e:
            logger.error(f"[IssueAnalyzer] Failed to initialize: {e}")

    def analyze_issue(self, text: str, language: str = "en") -> dict:
        """Analyze issue text for sentiment and key phrases using Bedrock."""
        if not self.client or not text or not text.strip():
            return {"sentiment": None, "keyPhrases": []}

        result = {"sentiment": None, "keyPhrases": []}

        try:
            response = self.client.converse(
                modelId=settings.BEDROCK_MODEL_ID,
                messages=[{
                    "role": "user",
                    "content": [{"text": ANALYSIS_PROMPT + text[:5000]}],
                }],
                inferenceConfig={"maxTokens": 1024, "temperature": 0.1},
            )

            response_text = response["output"]["message"]["content"][0]["text"]

            # Extract JSON from response (handle markdown code blocks)
            json_text = response_text.strip()
            if json_text.startswith("```"):
                json_text = json_text.split("```")[1]
                if json_text.startswith("json"):
                    json_text = json_text[4:]
                json_text = json_text.strip()

            parsed = json.loads(json_text)
            result["sentiment"] = parsed.get("sentiment")
            result["keyPhrases"] = parsed.get("keyPhrases", [])[:10]
            result["suggestedPriority"] = parsed.get("suggestedPriority", "NORMAL")

            logger.info(
                f"[IssueAnalyzer] Analyzed: sentiment={result['sentiment']['label']}, "
                f"phrases={len(result['keyPhrases'])}, priority={result['suggestedPriority']}"
            )

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"[IssueAnalyzer] Failed to parse Bedrock response: {e}")
        except ClientError as e:
            logger.error(f"[IssueAnalyzer] Bedrock error: {e}")

        return result

    def batch_analyze(self, texts: list) -> list:
        """Analyze multiple issues sequentially via Bedrock."""
        if not self.client:
            return []

        results = []
        for item in texts:
            text = item.get("text", "")
            language = item.get("language", "en")
            analysis = self.analyze_issue(text, language)
            analysis["id"] = item.get("id")
            results.append(analysis)

        return results

    def is_available(self) -> bool:
        return self.client is not None


comprehend_service = ComprehendService()
