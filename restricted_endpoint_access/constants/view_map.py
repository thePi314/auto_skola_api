METHODS = ["get", "post", "delete", "patch", "put"]

VIEW_MAP = {
    "GenericAPIView": [],
    "ListCreateAPIView": ["get", "post"],
    "ListAPIView": ["get"],
    "ModelViewSet": [],
    "APIView": []
}
