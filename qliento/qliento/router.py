from research.viewsets import ResearchViewSet
from rest_framework import routers

router = routers.DefaultRouter()
router.register('researches', ResearchViewSet, basename='research')