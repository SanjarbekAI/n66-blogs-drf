from django.contrib.auth.models import User
from rest_framework import serializers

from apps.blogs.models import Category, BlogPost
from apps.shared.exceptions.custom_exceptions import CustomException


class SimpleAuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True}
        }

    def validate_name(self, value):
        if not value or len(value) < 3:
            raise serializers.ValidationError("Name should be at least 3 char length")
        return value

    def validate_description(self, value):
        if value:
            words = ['spam', 'fake', 'scam']
            for word in words:
                if word.strip().lower() in value.lower():
                    raise CustomException(message_key="BLOG_TITLE_NUMERIC_ERROR")
        else:
            raise serializers.ValidationError("Description can not be none")
        return value


class BlogPostSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    tags_count = serializers.SerializerMethodField()
    author = SimpleAuthorSerializer(read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'title', 'content', 'status', 'author',
                  'category', 'created_at', 'tags_count', 'tags']
        extra_kwargs = {
            'author': {'read_only': True}
        }

    def get_tags_count(self, obj):
        return len(obj.tags.split(',')) if obj.tags else 0

    def validate_title(self, value):
        if value.strip()[0].isnumeric():
            raise CustomException(message_key="BLOG_TITLE_NUMERIC_ERROR")
        return value

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['author'] = user
        return BlogPost.objects.create(**validated_data)

    def update(self, instance, validated_data):
        status = validated_data.get('status', 'draft')
        if status == "published":
            if not instance.category_id:
                raise serializers.ValidationError('published post should have at least 1 category')
        return super().update(instance, validated_data)
