from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import utils
from .serializers import GenerateCourseSerializer, YoutubeQuerySerializer


# View for generating Table of Contents (TOC)
class TOCView(APIView):
    def post(self, request):
        try:
            # Extract data from the request
            data = request.data  # Use request.data for POST payloads

            # Extract individual fields from the request or use defaults
            topic = data.get('topic')
            level = data.get('level')
            depth = data.get('depth')
            area = data.get('area')

            # Call the utility function to generate the table of contents
            model = utils.init_gemini()  
            response = utils.make_table_of_contents(model, topic=topic, level=level, depth=depth, area=area)
            image=utils.search_image(topic)
            response['course_image']=image
            print(response)
            # Return a JSON response with the contents
            return Response(response, status=status.HTTP_200_OK)

        except Exception as e:
            # Handle any exceptions and return a 500 error
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# View for generating the course based on the provided data
class GenerateCourseView(APIView):
    def post(self, request):
        # Validate incoming data using the GenerateCourseSerializer
        serializer = GenerateCourseSerializer(data=request.data)
        
        # Check if the data is valid
        if serializer.is_valid():
            try:
                # If the data is valid, use the validated data to generate the course
                validated_data = serializer.validated_data
                topic=validated_data["topic"]
                contents = validated_data["contents"]  # You may need to handle the topic differently
                level = validated_data["level"]
                depth = validated_data["depth"]
                area = validated_data["area"]
                model=utils.init_gemini()
                # Call the course generation function from utils.py (or wherever it's defined)
                response = utils.generate_course(model, contents, level, depth, topic)
                
               
            
               
                # Return the generated course as a JSON response
                return Response(response, status=status.HTTP_200_OK)

            except Exception as e:
                # Handle any exceptions and return a 500 error
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # If the data is invalid, return a 400 error with validation errors
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class YoutubeQueryView(APIView):
    def post(self, request):
        serializer=YoutubeQuerySerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                validated_data=serializer.validated_data
                
                query=validated_data["query"]
                print("query:", query)
                search_results=utils.search_youtube(query)

                print(search_results)
                return Response({'search_results': search_results}, status=status.HTTP_200_OK)

            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)