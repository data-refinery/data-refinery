##
# Contains ProcessorJobListView, ProcessorJobDetailView, and the needed serializer
##

from django.utils.decorators import method_decorator
from rest_framework import filters, generics, serializers

from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from data_refinery_api.exceptions import InvalidFilters
from data_refinery_api.utils import check_filters
from data_refinery_common.models import ProcessorJob
from data_refinery_common.utils import get_nomad_jobs


class ProcessorJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProcessorJob
        fields = (
            "id",
            "pipeline_applied",
            "num_retries",
            "retried",
            "worker_id",
            "ram_amount",
            "volume_index",
            "worker_version",
            "failure_reason",
            "nomad_job_id",
            "success",
            "original_files",
            "datasets",
            "start_time",
            "end_time",
            "created_at",
            "last_modified",
        )


@method_decorator(
    name="get",
    decorator=swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                name="sample_accession_code",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="List the processor jobs associated with a sample",
            ),
            openapi.Parameter(
                name="nomad",
                in_=openapi.IN_QUERY,
                type=openapi.TYPE_STRING,
                description="Only return jobs that are in the nomad queue currently",
            ),
        ]
    ),
)
class ProcessorJobListView(generics.ListAPIView):
    """
    List of all ProcessorJobs.
    """

    model = ProcessorJob
    serializer_class = ProcessorJobSerializer
    filter_backends = (
        DjangoFilterBackend,
        filters.OrderingFilter,
    )
    filterset_fields = ProcessorJobSerializer.Meta.fields
    ordering_fields = ("id", "created_at")
    ordering = ("-id",)

    def get_queryset(self):
        invalid_filters = check_filters(self, ["sample_accession_code", "nomad"])

        if invalid_filters:
            raise InvalidFilters(invalid_filters=invalid_filters)

        queryset = ProcessorJob.objects.all()

        sample_accession_code = self.request.query_params.get("sample_accession_code", None)
        if sample_accession_code:
            queryset = queryset.filter(
                original_files__samples__accession_code=sample_accession_code
            ).distinct()

        nomad = self.request.query_params.get("nomad", None)
        if nomad:
            running_nomad_jobs_ids = [
                job["ID"] for job in get_nomad_jobs() if job["Status"] == "running"
            ]
            queryset = queryset.filter(nomad_job_id__in=running_nomad_jobs_ids)

        return queryset


class ProcessorJobDetailView(generics.RetrieveAPIView):
    """ Retrieves a ProcessorJob by ID """

    lookup_field = "id"
    model = ProcessorJob
    queryset = ProcessorJob.objects.all()
    serializer_class = ProcessorJobSerializer
