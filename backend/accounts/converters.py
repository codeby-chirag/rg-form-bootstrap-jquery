from django.core import signing


class SignedIntConverter:
    regex = r"[-a-zA-Z0-9_:=]+"

    def to_python(self, value):
        try:
            return signing.loads(value)
        except signing.BadSignature:
            raise ValueError("Invalid signed ID")

    def to_url(self, value):
        return signing.dumps(value)