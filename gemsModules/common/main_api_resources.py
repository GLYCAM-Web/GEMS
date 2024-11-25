#!/usr/bin/env python3
import email
from email.message import EmailMessage
import mimetypes
from typing import Any, List, Literal, Optional
from pydantic import BaseModel, Field
from pathlib import Path
import urllib.request

from gemsModules.common.main_api_notices import Notices

from gemsModules.logging.logger import Set_Up_Logging


log = Set_Up_Logging(__name__)


class MimeEncodableResourceMixin:
    """Mixin for Resource mime encoding, coupled with yet separated from Resource for API clarity."""

    @property
    def is_mime_encoded(self):
        """Check if the payload is MIME encoded by GEMS."""
        if self.options is not None and "is_mime_encoded" in self.options:
            return self.options["is_mime_encoded"] in ["True", "true", True]

        return False

    def try_decode_mime(self, data):
        """If the payload is MIME encoded by GEMS or at all, try to decode it."""
        if self.is_mime_encoded or isinstance(data, bytes) and data.startswith(b"Content-Type:"):
            msg = email.parser.BytesParser().parsebytes(data)
            return msg.get_payload(decode=True)
        else:
            return data

    @classmethod
    def payload_from_path(
        cls,
        resource_path,
        resource_format,
        resource_role="undefined",
        encapulate_mime=False,
    ):
        if encapulate_mime:
            log.debug(f"Encapsulating MIME for {resource_path}")
            msg = EmailMessage()
            mime_type, _ = mimetypes.guess_type(resource_path)
            if mime_type is None:
                mime_type = "application/octet-stream"

            # Read the file content and attach it to the message
            with open(resource_path, "rb") as file:
                file_content = file.read()
                msg.set_content(
                    file_content,
                    maintype=mime_type.split("/")[0],
                    subtype=mime_type.split("/")[1],
                )

            content = msg.as_string()
        else:
            with open(resource_path, "rb") as file:
                content = file.read().decode("utf-8")

        obj = cls(
            locationType="Payload",
            resourceFormat=resource_format,
            payload=content,
            resourceRole=resource_role,
        )
        obj.options = {
            "is_mime_encoded": encapulate_mime,
            "filename": Path(resource_path).name,
        }

        return obj


# TODO: Generalize/Handle more than filesystem paths.
class FileSystemHelpersMixin:
    def copy_to(self, parent_dir: Path, filename=None):
        """Copy this resource to the destination directory."""
        filename = filename or self.filename

        if isinstance(parent_dir, str):
            path = Path(parent_dir) / filename

        payload = self.get_payload()
        maybe_binary = "b" if isinstance(payload, bytes) else ""

        log.debug(f"Copying resource {self} to {path}...")
        with open(path, "w" + maybe_binary) as f:
            if isinstance(payload, dict):
                payload = str(payload)
            f.write(payload)
            
        # return a resource for the new file
        return Resource(
            typename=self.typename,
            locationType="filesystem-path-unix",
            resourceFormat=self.resourceFormat,
            resourceRole=self.resourceRole,
            payload=str(path),
            options={"filename": filename, "binary": False}
        )
        
class Resource(BaseModel, MimeEncodableResourceMixin, FileSystemHelpersMixin):
    """Information describing a resource containing data.

    Payload could be a filesystem path or a download URL or an HTML header or
    anything else that could hold a file.  Location is intended to be a type, not the payload.

    The location type could be 'String' or 'Payload', in which case,
    the payload would be the actual info and not the address of the info.

    What to do with the info will vary a lot depending on the needs of the service.
    The resourceRole can be used by an Entity
    """

    typename: str = Field(
        "Unset",
        alias="type",
        title="Resource type",
        description="The name of the type of Resource.",
    )
    locationType: Literal['Payload', 'URL', 'File', 'filesystem-path-unix'] = Field( 
        None,
        title="Location Type",
        description="Supported locations will vary with each Entity.",
    )
    resourceFormat: str = Field(
        None,
        title="Resource Format",
        description="Supported formats will vary with each Entity.",
    )
    resourceRole: str = Field(
        None,
        title="Resource Role",
        description="Roles indicate the function or purpose of a Resource.",
    )
    payload: Any = Field(
        None,
        description="The thing that is described by the location and format.",
    )
    options: Optional[dict[str, str]] = Field(
        default_factory=dict,
        description="Key-value pairs that are specific to each entity, service, etc",
    )
    notices: Optional[Notices] = Field(
        default_factory=Notices,
        description="Notices associated with this resource",
    )

    @property
    def filename(self):
        """Filename from options or File payload."""
        if self.locationType == "filesystem-path-unix":
            return Path(self.payload).name
        elif self.options is not None and "filename" in self.options:
            return self.options["filename"]
        else:
            log.warning("Has no filename, attempting to use resourceRole")
            if self.resourceRole:
                return self.resourceRole
            else:
                # Maybe just append a notice here..
                raise ValueError(
                    "No filename specified, please set it with options['filename'] or use a File payload."
                )

    def get_payload(self, decode=False):
        """Return the data from the payload.

        - Can override and call super from subclass to extend location types.
        - Can also override the handlers to extend functionality.
        """
        if self.locationType == "filesystem-path-unix" or self.locationType == "File":
            payload = self._handle_file()
        elif self.locationType == "Payload" or self.locationType == "String":
            payload = self._handle_payload()
        elif self.locationType == "URL":
            payload = self._handle_url()
        else:
            raise ValueError(f"Unknown locationType {self.locationType}")

        if isinstance(payload, bytes) and decode:
            return payload.decode("utf-8")            
        else:
            return payload

    def _handle_file(self):
        with open(self.payload, "rb" if isinstance(self.payload, bytes) else "r") as f:
            file = f.read()

        return self.try_decode_mime(file)

    def _handle_payload(self):
        if isinstance(self.payload, dict):
            return self.payload
        
        return self.try_decode_mime(self.payload.encode("utf-8"))

    def _handle_url(self):
        with urllib.request.urlopen(self.payload) as f:
            return self.try_decode_mime(f.read())


    def convert_resource_format(self, resourceFormat: str):
        pass

    def convert_location_type(self, locationType: str):
        pass

    @classmethod
    def from_resource(cls, other):
        pass


class Resources(BaseModel):
    __root__: list[Resource] = Field(default_factory=list)

    def add_resource(self, resource: Resource, metadata_only=False):
        if metadata_only:
            resource.payload = None

        self.__root__.append(resource)

    def type_is_present(self, typename: str):
        if not self.__root__:
            return False

        for resource in self.__root__:
            if resource.typename == typename:
                return True

        return False

    def get_resource_by_type(self, typename: str) -> list[Resource]:
        if self.__root__ is None or self.__root__ == []:
            return []

        return [resource for resource in self.__root__ if resource.typename == typename]

    def clear_payloads(self, verbose_api=False):
        for resource in self:
            resource.payload = None
            if verbose_api:
                resource.options['cleared_payload'] = True

    def __getitem__(self, key):
        return self.__root__[key]

    def __setitem__(self, key, value):
        self.__root__[key] = value

    def __len__(self):
        if self.__root__ is None:
            return 0
        return len(self.__root__)

    def __iter__(self):
        return iter(self.__root__ or [])

    def __repr__(self):
        return f"{self.__root__}"


def generateSchema():
    print(Resource.schema_json(indent=2))


def generateJson():
    thisResource = Resource()
    thisResource.notices.addCommonParserNotice()
    print(thisResource.json(indent=2))
