from django_filters import FilterSet, NumberFilter
import logging

from arosaje.models import Plants

from arosaje.services.calculate_distance import move_latitude, move_longitude

logger = logging.getLogger(__name__)

class PlantsFilterSet(FilterSet):
    center_lat = NumberFilter(method="filter_by_distance")
    center_lng = NumberFilter(method="filter_by_distance")
    radius = NumberFilter(method="filter_by_distance")

    class Meta:
        model = Plants
        fields = []

    def filter_by_distance(self, queryset, name, value):
        lat = float(self.data.get("center_lat"))
        lon = float(self.data.get("center_lng"))
        radius = float(self.data.get("radius"))

        logging.debug(f"{lat}, {lon}, {radius}")
        if not (lat and lon and radius):
            return queryset

        if lat and lon and radius:
            try:
                return queryset.filter(
                    lat__lte=(move_latitude(lat, radius)),
                    lat__gte=(move_latitude(lat, -radius)),
                    lon__lte=(move_longitude(lat, lon, radius)),
                    lon__gte=(move_longitude(lat, lon, -radius))
                )
            except (ValueError, TypeError):
                pass

        return queryset
