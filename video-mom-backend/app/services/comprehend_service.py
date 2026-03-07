import logging
import boto3
from botocore.exceptions import ClientError
from app.core.config import settings

logger = logging.getLogger(__name__)


class ComprehendService:
    """Amazon Comprehend for sentiment analysis and key phrase extraction."""

    # Comprehend supported languages
    SUPPORTED_LANGUAGES = {"en", "hi", "es", "de", "it", "fr", "pt", "ar", "zh", "ko", "ja"}

    def __init__(self):
        self.client = None
        self._init_client()

    def _init_client(self):
        try:
            kwargs = {"region_name": settings.AWS_REGION}
            if settings.AWS_ACCESS_KEY_ID:
                kwargs["aws_access_key_id"] = settings.AWS_ACCESS_KEY_ID
                kwargs["aws_secret_access_key"] = settings.AWS_SECRET_ACCESS_KEY
            self.client = boto3.client("comprehend", **kwargs)
            logger.info("[Comprehend] Client initialized")
        except Exception as e:
            logger.error(f"[Comprehend] Failed to initialize: {e}")

    def analyze_issue(self, text: str, language: str = "en") -> dict:
        """Analyze issue text for sentiment and key phrases."""
        if not self.client or not text or not text.strip():
            return {"sentiment": None, "keyPhrases": []}

        lang_code = language[:2].lower()
        if lang_code not in self.SUPPORTED_LANGUAGES:
            lang_code = "en"  # Fallback to English

        result = {"sentiment": None, "keyPhrases": []}

        try:
            # Detect sentiment
            sentiment_response = self.client.detect_sentiment(
                Text=text[:5000],  # Comprehend limit
                LanguageCode=lang_code,
            )
            result["sentiment"] = {
                "label": sentiment_response["Sentiment"],
                "score": sentiment_response["SentimentScore"].get(
                    sentiment_response["Sentiment"].capitalize(), 0
                ),
                "scores": {
                    "positive": sentiment_response["SentimentScore"].get("Positive", 0),
                    "negative": sentiment_response["SentimentScore"].get("Negative", 0),
                    "neutral": sentiment_response["SentimentScore"].get("Neutral", 0),
                    "mixed": sentiment_response["SentimentScore"].get("Mixed", 0),
                }
            }

            # Extract key phrases
            phrases_response = self.client.detect_key_phrases(
                Text=text[:5000],
                LanguageCode=lang_code,
            )
            result["keyPhrases"] = [
                kp["Text"]
                for kp in phrases_response.get("KeyPhrases", [])
                if kp.get("Score", 0) > 0.7
            ][:10]  # Top 10 high-confidence phrases

            # Determine if urgent based on sentiment
            if (result["sentiment"]["label"] == "NEGATIVE"
                    and result["sentiment"]["scores"]["negative"] > 0.7):
                result["suggestedPriority"] = "URGENT"
            else:
                result["suggestedPriority"] = "NORMAL"

            logger.info(
                f"[Comprehend] Analyzed: sentiment={result['sentiment']['label']}, "
                f"phrases={len(result['keyPhrases'])}"
            )

        except ClientError as e:
            logger.error(f"[Comprehend] Analysis error: {e}")

        return result

    def batch_analyze(self, texts: list[dict]) -> list[dict]:
        """Batch analyze multiple texts. Each item: {id, text, language}."""
        if not self.client:
            return []

        results = []
        # Comprehend batch supports up to 25 documents
        for i in range(0, len(texts), 25):
            batch = texts[i:i + 25]
            batch_texts = [item["text"][:5000] for item in batch]
            lang_code = batch[0].get("language", "en")[:2].lower()
            if lang_code not in self.SUPPORTED_LANGUAGES:
                lang_code = "en"

            try:
                sentiment_batch = self.client.batch_detect_sentiment(
                    TextList=batch_texts,
                    LanguageCode=lang_code,
                )
                phrases_batch = self.client.batch_detect_key_phrases(
                    TextList=batch_texts,
                    LanguageCode=lang_code,
                )

                for j, item in enumerate(batch):
                    sentiment_result = sentiment_batch["ResultList"][j] if j < len(sentiment_batch["ResultList"]) else {}
                    phrases_result = phrases_batch["ResultList"][j] if j < len(phrases_batch["ResultList"]) else {}

                    result = {
                        "id": item.get("id"),
                        "sentiment": {
                            "label": sentiment_result.get("Sentiment", "NEUTRAL"),
                            "score": sentiment_result.get("SentimentScore", {}).get(
                                sentiment_result.get("Sentiment", "Neutral").capitalize(), 0
                            ),
                        },
                        "keyPhrases": [
                            kp["Text"]
                            for kp in phrases_result.get("KeyPhrases", [])
                            if kp.get("Score", 0) > 0.7
                        ][:10],
                    }
                    results.append(result)

            except ClientError as e:
                logger.error(f"[Comprehend] Batch analysis error: {e}")

        return results

    def is_available(self) -> bool:
        return self.client is not None


comprehend_service = ComprehendService()
