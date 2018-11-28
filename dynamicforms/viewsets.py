from django.http import Http404

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from dynamicforms.settings import TEMPLATE
from .renderers import TemplateHTMLRenderer
from .settings import BSVER_MODAL


class NewMixin(object):
    """
    Provides support for retrieving default values for a new record.

    Caution: Do not use directly. This is only a mixin and is used in final ViewSet derivatives.
    """

    def new_object(self: viewsets.ModelViewSet):
        """
        Returns a new model instance. If you need it pre-populated with default values, this is the method to override.

        :return: model instance
        """
        # TODO: Tukaj moraš paziti, da je objekt pravilno postavljen glede na pravila
        # Primer: če se plačnik nastavi iz pilota in tukaj prednapolniš pilota, potem poskrbi, da boš prednapolnil
        # tudi plačnika.
        #
        # Kako pa to lahko naredimo?
        # Predlog: retrieve, ko pokliče to funkcijo, naj tudi izvede "onchange" event za vsako polje in tako to napolni
        return self.get_queryset().model()

    # noinspection PyUnresolvedReferences
    def retrieve(self: viewsets.ModelViewSet, request, *args, **kwargs):
        try:
            return super().retrieve(request, *args, **kwargs)
        except Http404:
            lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
            filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
            if filter_kwargs.get('pk', None) == 'new':
                instance = self.new_object()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                raise


class ModelViewSet(NewMixin, viewsets.ModelViewSet):
    """
    In addition to all the functionality, provided by DRF, DynamicForms ViewSet has some extra features:

    * Separate templates for rendering list or single record
    * You can request a "new" record and even have it pre-populated with values
    * To render viewset as API or JSON use the same method as in DRF: To render it in HTML just add ".html" to the URL.
    * Standard DRF router URL patterns apply:

       * To render a new record use pk=new.
       * To render an existing record (for editing) use pk={record_id}.
    """

    template_context = {}
    """
    template_context provides configuration to templates being rendered
    """

    template_name = TEMPLATE + 'base_list.html'  #: template filename for listing multiple records (html renderer)

    # noinspection PyAttributeOutsideInit
    def initialize_request(self, request, *args, **kwargs):
        # Caution: just to be sure for any future debugging: the request parameter to this function is a WSGIRequest
        #  while the return Request is actually DRF Request
        #  As a consequence, form values don't get parsed until you actually call super().initialize_request
        #  There's no "request.data", etc. Just saying. So you don't debug for two hours next time. By "you" I mean me

        # Force render using a given render path (full page, table, table rows, form, dialog with form)
        self.render_type = request.META.get('HTTP_X_DF_RENDER_TYPE', request.GET.get('df_render_type', 'page'))

        # This is an additional table records load
        # TODO: change this to X-DF-RENDER-TYPE
        self.render_rows_only = hasattr(request, 'query_params') and request.query_params.get('cursor', '') != ''

        if request.method.lower() == 'post' and request.POST.get('data-dynamicforms-method', None):
            # This is a hack because HTML forms can only do POST & GET. This way we also get PUT & PATCH
            request.method = request.POST.get('data-dynamicforms-method')
        return super().initialize_request(request, *args, **kwargs)

    def finalize_response(self, request, response, *args, **kwargs):
        res = super().finalize_response(request, response, *args, **kwargs)

        if isinstance(res.accepted_renderer, TemplateHTMLRenderer):
            if isinstance(res.data, dict) and 'next' in res.data and 'results' in res.data and \
                    isinstance(res.data['results'], (ReturnList, ReturnDict)):
                serializer = res.data['results'].serializer
            else:
                serializer = res.data.serializer

            if isinstance(serializer, ListSerializer):
                serializer.child.render_type = self.render_type
            else:
                serializer.render_type = self.render_type

            if self.render_type in ('table', 'table rows'):
                serializer.data_template = self.template_name
            elif self.render_type == 'dialog':
                serializer.data_template = BSVER_MODAL
                res.template_name = BSVER_MODAL
            elif self.render_type == 'form':
                serializer.data_template = res.data.serializer.template_name
            elif self.render_rows_only:
                serializer.data_template = self.template_name
                res.template_name = self.template_name
                serializer.render_rows_only = self.render_rows_only
            else:
                if isinstance(serializer, ListSerializer):
                    serializer.child.render_type = 'table'
                    serializer.child.data_template = self.template_name
                else:
                    serializer.render_type = 'form'
                    serializer.data_template = serializer.template_name

        return res

    @staticmethod
    def generate_paged_loader(page_size: int = 30):
        from rest_framework.pagination import CursorPagination
        ps = page_size

        class MyCursorPagination(CursorPagination):
            ordering = 'id'
            page_size = ps

        return MyCursorPagination
