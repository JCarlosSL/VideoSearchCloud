from rest_framework import serializers

class UploadSerializer(serializers.Serializer):
    file = serializers.FileField(required=True)

    class Meta:
        fields = '__all__'

    def create(self, validated_data):
        raise NotImplementedError('`create()` must be wtf.')