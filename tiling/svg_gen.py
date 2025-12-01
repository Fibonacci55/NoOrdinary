# svg_gen.py
from abc import ABC, abstractmethod
from dataclasses import dataclass
import base64
import os
import svg  # Assumes existence of an 'svg' library (e.g. svg.py)


@dataclass
class DocumentOptions:
    """Configuration options for the SVG document."""
    width: int
    height: int
    unit: str


class SvgCreator(ABC):
    """Abstract interface for creating SVG documents."""

    @abstractmethod
    def create_document(self, name: str, options: DocumentOptions) -> object:
        """Creates a SVG document. Returns the canvas object."""

    @abstractmethod
    def create_group(self) -> int:
        """Creates a new group of the document, returns the id of the group."""

    @abstractmethod
    def save_document(self) -> None:
        """Saves a SVG document to disk."""

    @abstractmethod
    def create_image(self, img_source: str, width: int, height: int, ulx: int, uly: int) -> object:
        """
        Creates an SVG image with dimension width x height.
        Upper left position at (ulx, uly).
        """

    @abstractmethod
    def add_to_image(self, element: object) -> None:
        """Adds an element to the image canvas."""

    @abstractmethod
    def add_to_group(self, grp_id: int, element: object) -> None:
        """Adds an element to the group with id grp_id."""

    @abstractmethod
    def get_group(self, grp_id: int) -> object:
        """Retrieves group with id grp_id."""


class SvgDraw(SvgCreator):
    """Concrete implementation of SvgCreator using the 'svg' library."""

    def __init__(self):
        self.groups = []
        self.name = None
        self.options = None
        self.canvas = None

    def create_document(self, name: str, options: DocumentOptions) -> object:
        """Initializes the SVG canvas."""
        self.name = name
        self.options = options
        # Initialize canvas with ViewBox
        self.canvas = svg.SVG(
            svg.ViewBoxSpec(0, 0, options.width, options.height),
            elements=[]
        )
        return self.canvas

    def add_to_image(self, element: object) -> None:
        """Appends an element to the main canvas elements list."""
        if self.canvas is None:
            raise RuntimeError("Document not created. Call create_document first.")
        self.canvas.elements.append(element)

    def create_group(self) -> int:
        """Creates a new SVG Group (<g>) and returns its index."""
        self.groups.append(svg.G(elements=[]))
        return len(self.groups) - 1

    def create_image(self, img_source: str, width: int, height: int, ulx: int, uly: int) -> object:
        """
        Creates an SVG Image element.
        If img_source is a local file, it embeds it as base64.
        Otherwise, it treats it as a URL.
        """
        href_val = img_source

        # Attempt to embed image if it exists locally
        if os.path.exists(img_source):
            try:
                with open(img_source, "rb") as image_file:
                    encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    # Simple extension detection for MIME type
                    ext = os.path.splitext(img_source)[1].lower().replace('.', '')
                    # Default to png if unknown, or handle specific cases like svg+xml
                    mime_type = f"image/{ext}" if ext != 'svg' else "image/svg+xml"
                    href_val = f"data:{mime_type};base64,{encoded_string}"
            except OSError as e:
                print(f"Warning: Could not read image file {img_source}: {e}")
                # Fallback to linking the file path directly if read fails

        # Use 'href' (modern) instead of 'xlink__href'
        svg_img = svg.Image(
            href=href_val,
            x=ulx,
            y=uly,
            width=width,
            height=height
        )
        return svg_img

    def add_to_group(self, grp_id: int, element: object) -> None:
        """Adds an element to a specific group with bounds checking."""
        if 0 <= grp_id < len(self.groups):
            self.groups[grp_id].elements.append(element)
        else:
            raise IndexError(f"Group ID {grp_id} is out of range.")

    def get_group(self, grp_id: int) -> object:
        """Returns the group object by ID with bounds checking."""
        if 0 <= grp_id < len(self.groups):
            return self.groups[grp_id]
        else:
            raise IndexError(f"Group ID {grp_id} is out of range.")

    def save_document(self) -> None:
        """Writes the SVG content to the file specified in create_document."""
        if not self.name:
            raise ValueError("Document name not set. Call create_document first.")

        # Add groups to canvas before saving
        # (Assuming groups need to be part of the canvas to be rendered)
        for grp in self.groups:
            self.canvas.elements.append(grp)

        # Use 'w' mode for writing and context manager for safety
        try:
            with open(self.name, 'w', encoding='utf-8') as outf:
                # Convert canvas to string (assuming svg library supports __str__)
                outf.write(str(self.canvas))
        except IOError as e:
            print(f"Error saving document: {e}")


def create_svg_creator() -> SvgCreator:
    """Factory function to get an SvgCreator instance."""
    return SvgDraw()
