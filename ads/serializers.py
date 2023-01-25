from rest_framework import serializers
from ads.models import Ad, Location, User

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class AdListSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ad
        fields = ["id","name","author_id","price"]

class AdDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ad
        fields = '__all__'

class AdCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False)
    
    class Meta:
        model= Ad
        fields = '__all__'

    def create(self, validated_data):
        ad = Ad.objects.create(**validated_data)
        ad.save()
        return ad

class AdUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model= Ad
        fields = '__all__'

    def save(self):
        ad = super().save()
        ad.save()
        return ad

class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False)
    
    locations = serializers.SlugRelatedField(
        required = False,
        many = True,
        queryset = Location.objects.all(),
        slug_field = "name"
    )

    class Meta:
        model= User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create(**validated_data)
        for location in self._locations:
            loc_obj, _ = Location.objects.get_or_create(name= location)
            user.location_id.add(loc_obj)
        user.save()
        return user