from typing import Any

from dify_plugin import ToolProvider
from dify_plugin.errors.tool import ToolProviderCredentialValidationError


class GenPdfProvider(ToolProvider):
    def _validate_credentials(self, credentials: dict[str, Any]) -> None:
        """
        Validate provider credentials.

        This tool does not require any credentials, so validation always passes.

        Args:
            credentials: Dictionary of credentials (not used)

        Raises:
            ToolProviderCredentialValidationError: If validation fails
        """
        # No credentials required for PDF generation
        pass
