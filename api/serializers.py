from rest_framework import serializers

from .models import NewReleases, Artist


class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = '__all__'


class NewReleasesSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(read_only=True, many=True)

    class Meta:
        model = NewReleases
        fields = ('artists', 'created_at')
