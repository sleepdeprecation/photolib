import arrow
import mimetypes
import os
from datetime import datetime
from PIL import Image as PilImage
from PIL.ExifTags import TAGS as ExifTags
from rawkit.raw import Raw

class Image():
    JPEG_TYPES = [
        "image/jpeg",
        ".jpg",
        ".jpeg",
    ]

    RAW_TYPES = [
        ".raf",
    ]

    @classmethod
    def from_file(cls, path):
        mime_guess, _ = mimetypes.guess_type(path, strict = False)
        if mime_guess:
            img_type = mime_guess
        else:
            _, extension = os.path.splitext(path)
            img_type = extension.lower()

        if img_type in cls.JPEG_TYPES:
            return cls.from_jpg(path)
        if img_type in cls.RAW_TYPES:
            return cls.from_raw(path)

        return None

    @classmethod
    def from_raw(cls, path):
        with Raw(path) as raw:
            return cls(
                path,
                timestamp = raw.metadata.timestamp,
                camera_make = raw.metadata.make.decode("utf8"),
                camera_model = raw.metadata.model.decode("utf8"),
                aperture = round(raw.metadata.aperture, 1),
                focal_length = round(raw.metadata.focal_length),
                iso = round(raw.metadata.iso),
            )

    @classmethod
    def from_jpg(cls, path):
        with PilImage.open(path) as img:
            raw_exif = img._getexif()
            metadata = {}
            for tag, value in raw_exif.items():
                if tag in ExifTags:
                    metadata[ExifTags[tag]] = value

            focal_length_raw = metadata["FocalLength"]
            focal_length = round(focal_length_raw[0] / focal_length_raw[1])

            aperture_raw = metadata["ApertureValue"]
            aperture = round(aperture_raw[0] / aperture_raw[1], 1)

            # exif/pillow returns dumb things
            # format: "YYYY:MM:DD HH:mm:ss"
            timestamp = datetime.strptime(
                metadata["DateTimeOriginal"],
                "%Y:%m:%d %H:%M:%S"
            )
            return cls(
                path,
                timestamp = timestamp.timestamp(),
                camera_make = metadata["Make"],
                camera_model = metadata["Model"],
                aperture = aperture,
                focal_length = focal_length,
                iso = metadata["ISOSpeedRatings"],
            )

    def __init__(self, path, timestamp = None, camera_make = None,
            camera_model = None, aperture = None, shutter = None,
            focal_length = None, iso = None):
        self.path = path
        self.timestamp = timestamp
        self.camera_make = camera_make
        self.camera_model = camera_model
        self._aperture = aperture
        self.shutter = shutter
        self.focal_length = focal_length
        self.iso = iso

    @property
    def aperture(self):
        if not self._aperture:
            return None
        if self._aperture % 1 == 0:
            return round(self._aperture)
        else:
            return self._aperture

    def __str__(self):
        return "{path} \n\tf{aperture} / {focal}mm / iso{iso}\n\tTaken with {make} {model} at {date}".format(
            path = self.path,
            aperture = self.aperture,
            focal = self.focal_length,
            iso = self.iso,
            make = self.camera_make,
            model = self.camera_model,
            date = arrow.get(self.timestamp).to("local").format('YYYY-MM-DD HH:mm:ss ZZ'),
        )
