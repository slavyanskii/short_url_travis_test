from marshmallow import Schema, fields, ValidationError, validates, validates_schema


# Here goes serializers for validating input data

class UrlSerializer(Schema):
    full_url = fields.Url(required=True)