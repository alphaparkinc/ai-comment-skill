"""
ai-comment-skill: Client SDK
Decision-intent marketing via AI-generated social media comments.
"""

from __future__ import annotations
import os
import json
import re
import random
from typing import Literal

Platform = Literal["reddit", "twitter", "youtube", "linkedin", "tiktok", "instagram"]
Tone = Literal["helpful", "curious", "enthusiastic", "neutral", "expert"]


class AiCommentClient:
    """
    SDK for generating authentic, intent-driven marketing comments
    that blend naturally into social media conversations.
    """

    TONE_PREFIXES = {
        "helpful": [
            "I was in the same situation and found that",
            "Honestly, what worked for me was",
            "Not sure if you've tried it, but",
        ],
        "curious": [
            "Has anyone else tried",
            "Quick question -- did you consider",
            "Wondering if anyone knows whether",
        ],
        "enthusiastic": [
            "Oh this is actually perfect timing!",
            "You HAVE to check this out --",
            "Genuinely love this topic because",
        ],
        "neutral": [
            "For reference,",
            "Worth noting that",
            "Just to add context,",
        ],
        "expert": [
            "From a technical standpoint,",
            "Having worked in this space for years,",
            "The key differentiator here is",
        ],
    }

    PLATFORM_STYLES = {
        "reddit": {"max_chars": 1200, "cta_style": "link in bio or search"},
        "twitter": {"max_chars": 280, "cta_style": "check the link"},
        "youtube": {"max_chars": 500, "cta_style": "link in description"},
        "linkedin": {"max_chars": 800, "cta_style": "worth a look"},
        "tiktok": {"max_chars": 150, "cta_style": "check it out"},
        "instagram": {"max_chars": 300, "cta_style": "link in bio"},
    }

    def __init__(self, openai_api_key: str | None = None, model: str = "gpt-4o-mini"):
        self.api_key = openai_api_key or os.environ.get("OPENAI_API_KEY")
        self.model = model

    def generate_comment(
        self,
        product_name: str,
        product_url: str,
        product_features: list[str],
        platform: Platform = "reddit",
        tone: Tone = "helpful",
        thread_context: str = "",
        num_variants: int = 3,
    ) -> dict:
        """
        Generate marketing comment variants for a given product and platform.

        Args:
            product_name:      The product/service to promote.
            product_url:       Destination URL for traffic.
            product_features:  Key selling points.
            platform:          Social platform (affects length/style).
            tone:              Voice of the comment.
            thread_context:    (Optional) Thread title or original post for context.
            num_variants:      Number of distinct comment variants to generate.

        Returns:
            dict with keys: platform, tone, product, variants (list of comment strings)
        """
        style = self.PLATFORM_STYLES.get(platform, self.PLATFORM_STYLES["reddit"])
        max_chars = style["max_chars"]
        cta = style["cta_style"]
        features_str = "; ".join(product_features)
        prefixes = self.TONE_PREFIXES.get(tone, self.TONE_PREFIXES["neutral"])

        if self.api_key:
            variants = self._generate_via_openai(
                product_name, product_url, product_features,
                platform, tone, thread_context, max_chars, cta, num_variants
            )
        else:
            variants = self._generate_offline(
                product_name, product_url, features_str,
                max_chars, cta, prefixes, num_variants
            )

        return {
            "platform": platform,
            "tone": tone,
            "product": product_name,
            "product_url": product_url,
            "variants": variants,
        }

    def _generate_offline(
        self, product_name, product_url, features_str,
        max_chars, cta, prefixes, num_variants
    ) -> list[str]:
        """Rule-based generation when no LLM API key is available."""
        templates = [
            "{prefix} {product} has been a game changer for me. Key things: {features}. Definitely worth checking out ({cta}: {url})",
            "{prefix} {product} actually solves this well. It covers: {features}. ({cta}: {url})",
            "{prefix} give {product} a look -- {features}. Here: {url}",
        ]
        variants = []
        for i in range(min(num_variants, len(templates))):
            prefix = random.choice(prefixes)
            comment = templates[i].format(
                prefix=prefix,
                product=product_name,
                features=features_str,
                cta=cta,
                url=product_url,
            )
            if len(comment) > max_chars:
                comment = comment[:max_chars - 3] + "..."
            variants.append(comment)
        return variants

    def _generate_via_openai(
        self, product_name, product_url, product_features,
        platform, tone, thread_context, max_chars, cta, num_variants
    ) -> list[str]:
        """Call OpenAI API to generate high-quality comment variants."""
        import urllib.request

        context_line = f"Thread context: {thread_context}" if thread_context else ""
        features_str = ", ".join(product_features)

        system_prompt = (
            f"You are an expert social media marketer writing authentic {platform} comments. "
            f"Tone: {tone}. Max length: {max_chars} chars each. CTA style: '{cta}'. "
            "Do NOT sound like an ad. Sound like a genuine community member."
        )
        user_prompt = (
            f"Generate {num_variants} distinct comment variants promoting '{product_name}'.\n"
            f"URL: {product_url}\n"
            f"Key features: {features_str}\n"
            f"{context_line}\n\n"
            "Output as JSON array of strings only."
        )

        payload = json.dumps({
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.9,
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.openai.com/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            result = json.loads(resp.read())

        raw = result["choices"][0]["message"]["content"].strip()
        match = re.search(r"\[.*?\]", raw, re.DOTALL)
        if match:
            return json.loads(match.group())
        return [line.strip().strip('"') for line in raw.split("\n") if line.strip()]

    def batch_generate(self, campaigns: list[dict]) -> list[dict]:
        """
        Run generate_comment for multiple campaigns at once.

        Args:
            campaigns: List of dicts, each with keys matching generate_comment params.

        Returns:
            List of result dicts.
        """
        results = []
        for campaign in campaigns:
            result = self.generate_comment(**campaign)
            results.append(result)
        return results
