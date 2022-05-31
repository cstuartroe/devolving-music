from django.core.management.base import BaseCommand
from django.db.models.fields import BigAutoField, CharField, DateField, DateTimeField, BooleanField
from django.db.models.fields.related import ManyToManyField, ForeignKey
from django.db.models.fields.reverse_related import ManyToOneRel, ManyToManyRel

from devolving_music.models.artist import Artist
from devolving_music.models.song import Song
from devolving_music.models.event import Event
from devolving_music.models.song_submission import SongSubmission
from devolving_music.models.song_comparison import SongComparison


MODELS_TO_TRANSPILE = [
    Artist,
    Song,
    Event,
    SongSubmission,
    SongComparison,
]


OUTFILE = "src/models.ts"


class Command(BaseCommand):
    help = 'Transpiles Django models into a Typescript type definition file'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        contents = (
            "/* This file has been autogenerated.\n"
            "DO NOT manually edit it.\n"
            "Run `python manage.py transpile_models` to update it. */\n\n"
        )

        for model in MODELS_TO_TRANSPILE:
            model_string = f"export type {model.__name__} = {{\n"

            for field in model._meta.get_fields():
                t = type(field)
                type_string = None

                if t is ManyToOneRel or t is ManyToManyRel:
                    pass
                elif t is BigAutoField:
                    type_string = "number"
                elif t is CharField:
                    if field.choices is not None:
                        array_name = f"{model.__name__}_{field.name}"
                        contents += f"export const {array_name} = {[c for c, _ in field.choices]} as const;\n\n"
                        type_string = f"typeof {array_name}[number]"
                    else:
                        type_string = "string"
                elif t is DateField:
                    type_string = "string"
                elif t is DateTimeField:
                    type_string = "string"
                elif t is BooleanField:
                    type_string = "boolean"
                elif t is ForeignKey:
                    type_string = field.related_model.__name__
                elif t is ManyToManyField:
                    type_string = field.related_model.__name__ + "[]"
                else:
                    raise ValueError(f"Unknown field type: {t}")

                if type_string is not None:
                    model_string += f"  {field.name}: {type_string},\n"

            model_string += "}\n\n"

            contents += model_string

        with open(OUTFILE, "w") as fh:
            fh.write(contents)

