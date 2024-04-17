import base64
import io
import sys
from uuid import uuid4

from django.core.files.uploadedfile import InMemoryUploadedFile

__all__ = ('parse_base64_string', 'base64_to_in_memory_uploaded_file')


def parse_base64_string(base64_string: str) -> tuple[str, bytes]:
    content_type, base64_file = base64_string.split(';base64')
    content_type = content_type.split(':')[1]
    return content_type, base64.b64decode(base64_file)


def base64_to_in_memory_uploaded_file(
        base64_string: str,
) -> InMemoryUploadedFile:
    content_type, content = parse_base64_string(base64_string)

    file_extension = content_type.split('/')[-1]
    file_name = f'{uuid4().hex}.{file_extension}'

    bytes_io = io.BytesIO(content)

    return InMemoryUploadedFile(
        file=bytes_io,
        field_name=None,
        name=file_name,
        content_type=content_type,
        size=sys.getsizeof(bytes_io),
        charset=None,
    )
