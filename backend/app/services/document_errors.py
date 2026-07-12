"""Internal document (PDF) extraction errors with sanitized API mappings."""


class DocumentEmptyFileError(Exception):
    """The uploaded file contained no bytes."""


class DocumentTooLargeError(Exception):
    """The uploaded file exceeds the configured maximum upload size."""


class DocumentInvalidTypeError(Exception):
    """The uploaded content does not start with a valid PDF signature."""


class DocumentEncryptedError(Exception):
    """The PDF is password-protected/encrypted and cannot be processed."""


class DocumentParsingError(Exception):
    """The PDF could not be parsed due to a structural or library error."""


class DocumentNoTextError(Exception):
    """No extractable text was found anywhere in the PDF."""


class DocumentTextTooShortError(Exception):
    """Extracted text is shorter than the Notes workflow minimum (50 chars)."""


class DocumentTextTooLongError(Exception):
    """Extracted text is longer than the Notes workflow maximum (20,000 chars)."""
