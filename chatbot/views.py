from rest_framework.decorators import api_view
from rest_framework.response import Response
from .chatbot import handle_query
from rest_framework import status


@api_view(['GET'])
def get_chatbot_response(request):
    query = request.query_params.get('query', '')
    
    # Check if the query is empty
    if not query:
        return Response({"error": "Query parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
    
    # Get response from the chatbot
    response = handle_query(query)
    
    # Return the response
    return Response({'response': response})
