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

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'
class UserCreateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required = False)
    
    location_id = serializers.SlugRelatedField(
        required = False,
        many = True,
        queryset = Location.objects.all(),
        slug_field = "id"
    )

    class Meta:
        model= User
        fields = ["id","first_name","last_name","username","password","role","age","location_id"]



class UserUpdateSerializer(serializers.ModelSerializer):
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

    
class UserDestroySerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = '__all__'