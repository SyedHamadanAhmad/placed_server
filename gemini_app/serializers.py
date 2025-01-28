from rest_framework import serializers

# Serializer for the course generation data
class GenerateCourseSerializer(serializers.Serializer):
    topic = serializers.CharField(max_length=255)
    level = serializers.CharField(max_length=255)
    depth = serializers.FloatField()
    area = serializers.CharField(max_length=255)
    contents = serializers.ListField(
        child=serializers.CharField(max_length=500)  # This defines that each element in the list will be a string
    )

    

    def validate_depth(self, value):
        """Ensure 'depth' is between 0 and 100."""
        if not (0 <= value <= 100):
            raise serializers.ValidationError("Depth must be between 0 and 1.")
        return value


class YoutubeQuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=400)

    def validate_query(self, query):
        if len(query) > 0:
            return query
        else:
            raise serializers.ValidationError("The query field cannot be empty.")