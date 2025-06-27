from django_filters import FilterSet, NumberFilter, BooleanFilter
import logging

from arosaje.models import Plants, Consentments

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


class ConsentmentsFilterSet(FilterSet):
    required = BooleanFilter(field_name="required")
    not_signed = BooleanFilter(method="filter_not_signed")

    class Meta:
        model = Consentments
        fields = ["required"]

    def filter_not_signed(self, queryset, name, value):
        if value:
            return queryset.exclude(acceptances__user=self.request.user)
        return queryset
