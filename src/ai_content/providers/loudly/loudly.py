import logging
import httpx
from pathlib import Path
from datetime import datetime, timezone

from ai_content.core.registry import ProviderRegistry
from ai_content.core.result import GenerationResult
from ai_content.core.exceptions import AuthenticationError, ProviderError
from ai_content.config import get_settings

logger = logging.getLogger(__name__)

@ProviderRegistry.register_music("loudly")
class LoudlyMusicProvider:
    """
    Loudly Music API provider.

    Features:
        - AI-based music generation from text prompts.
        - API-KEY authentication.
    """

    name = "loudly"
    supports_vocals = False # Loudly API docs don't mention explicit vocal support
    supports_reference_audio = False # Loudly API docs don't mention explicit reference audio support

    def __init__(self):
        self.settings = get_settings().loudly
        if not self.settings.api_key:
            raise AuthenticationError("loudly")
        self.base_url = self.settings.base_url

    def _get_headers(self) -> dict[str, str]:
        return {
            "API-KEY": self.settings.api_key,
            "Content-Type": "application/json",
        }

    async def generate(
        self,
        prompt: str,
        *,
        duration_seconds: int = 30,
        bpm: int | None = None,
        lyrics: str | None = None,
        reference_audio_url: str | None = None,
        output_path: str | None = None,
        test_mode: bool = False, # Added test_mode parameter
    ) -> GenerationResult:
        logger.info(f"🎵 Loudly: Generating music from prompt: {prompt[:50]}...")

        endpoint = f"{self.base_url}/ai/prompt/songs" # Correct endpoint for prompt-based generation

        payload = {
            "prompt": prompt,
            "duration": duration_seconds,
            "test": test_mode, # Pass test_mode
        }

        # The API docs mention duration >= 30 and <= 420
        if not (30 <= duration_seconds <= 420):
            logger.warning(f"Loudly API duration must be between 30 and 420 seconds. Adjusting {duration_seconds}s to 30s.")
            payload["duration"] = 30

        try:
            async with httpx.AsyncClient(timeout=self.settings.request_timeout) as client:
                response = await client.post(
                    endpoint,
                    json=payload,
                    headers=self._get_headers(),
                )
                response.raise_for_status()
                response_data = response.json()

                music_file_path = response_data.get("music_file_path")
                if not music_file_path:
                    raise ProviderError(self.name, "No 'music_file_path' found in Loudly API response.")

                # Download the audio file from the URL
                audio_response = await client.get(music_file_path)
                audio_response.raise_for_status()
                audio_data = audio_response.content

                # Save the audio data
                file_path = self._save_audio(audio_data, output_path)

                logger.info(f"✅ Loudly: Saved to {file_path}")

                return GenerationResult(
                    success=True,
                    provider=self.name,
                    content_type="music",
                    file_path=file_path,
                    data=audio_data,
                    metadata={
                        "prompt": prompt,
                        "duration": duration_seconds,
                        "loudly_song_id": response_data.get("id"),
                        "loudly_title": response_data.get("title"),
                    },
                )

        except httpx.HTTPStatusError as e:
            logger.error(f"Loudly generation failed: {e.response.status_code} {e.response.text}")
            raise ProviderError(self.name, f"{e.response.status_code} {e.response.text}")
        except Exception as e:
            logger.error(f"Loudly generation failed: {e}")
            raise ProviderError(self.name, str(e))

    def _save_audio(self, audio_data: bytes, output_path: str | None) -> Path:
        from datetime import datetime, timezone
        from ai_content.config import get_settings

        if output_path:
            file_path = Path(output_path)
        else:
            output_dir = get_settings().output_dir
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            file_path = output_dir / f"loudly_{timestamp}.mp3" # Assuming MP3

        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(audio_data)
        return file_path
