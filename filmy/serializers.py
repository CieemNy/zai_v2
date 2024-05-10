from rest_framework import serializers
from .models import Film


class FilmSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    tytul = serializers.CharField(required=True, allow_blank=False, max_length=64)
    rok = serializers.IntegerField(allow_null=False)
    opis = serializers.CharField(style={'base_template': 'textarea.html'})
    premiera = serializers.DateField(allow_null=True)
    imdb_points = serializers.DecimalField(max_digits=4, decimal_places=2, allow_null=True)

    def create(self, validated_data):
        return Film.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tytul = validated_data.get('tytul', instance.tytul)
        instance.rok = validated_data.get('rok', instance.rok)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.premiera = validated_data.get('premiera', instance.premiera)
        instance.imdb_points = validated_data.get('imdb_points', instance.imdb_points)
        instance.save()
        return instance


class FilmModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = '__all__'

    def create(self, validated_data):
        return Film.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.tytul = validated_data.get('tytul', instance.tytul)
        instance.rok = validated_data.get('rok', instance.rok)
        instance.opis = validated_data.get('opis', instance.opis)
        instance.premiera = validated_data.get('premiera', instance.premiera)
        instance.imdb_points = validated_data.get('imdb_points', instance.imdb_points)
        instance.save()
        return instance
