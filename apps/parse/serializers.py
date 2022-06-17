from rest_framework import serializers
from apps.parse.parsing import DATA


class ParseProductSerializer(serializers.Serializer):
    class Meta:
        model = DATA
        fields = "__all__"

    def to_representation(self, instance):
        representation = instance
        representation['website'] = 'kivano.kg'
        return representation

