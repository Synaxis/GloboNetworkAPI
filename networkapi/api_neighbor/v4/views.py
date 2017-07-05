# -*- coding: utf-8 -*-
# Create your views here.
from django.db.transaction import commit_on_success
from networkapi.api_neighbor.v4.permissions import Read
from networkapi.api_neighbor.v4.permissions import Write
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from networkapi.api_neighbor.v4 import facade

from networkapi.api_neighbor.v4 import serializers
from networkapi.settings import SPECS
from networkapi.util.classes import CustomAPIView
from networkapi.util.decorators import logs_method_apiview
from networkapi.util.decorators import permission_classes_apiview
from networkapi.util.decorators import prepare_search
from networkapi.util.geral import render_to_json
from networkapi.util.json_validate import json_validate
from networkapi.util.json_validate import raise_json_validate


class NeighborDBView(CustomAPIView):

    @logs_method_apiview
    @raise_json_validate('')
    @permission_classes_apiview((IsAuthenticated, Read))
    @prepare_search
    def get(self, request, *args, **kwargs):
        """Returns a list of Neighbors by ids ou dict."""

        if not kwargs.get('obj_ids'):
            obj_model = facade.get_neighbor_by_search(self.search)
            neighbors = obj_model['query_set']
            only_main_property = False
        else:
            as_ids = kwargs.get('obj_ids').split(';')
            neighbors = facade.get_neighbor_by_ids(as_ids)
            only_main_property = True
            obj_model = None

        # serializer AS's
        serializer_as = serializers.NeighborV4Serializer(
            neighbors,
            many=True,
            fields=self.fields,
            include=self.include,
            exclude=self.exclude,
            kind=self.kind
        )

        # prepare serializer with customized properties
        data = render_to_json(
            serializer_as,
            main_property='neighbors',
            obj_model=obj_model,
            request=request,
            only_main_property=only_main_property
        )

        return Response(data, status=status.HTTP_200_OK)

    @logs_method_apiview
    @raise_json_validate('as_post')
    @permission_classes_apiview((IsAuthenticated, Write))
    @commit_on_success
    def post(self, request, *args, **kwargs):
        """Create new Neighbor."""

        # neighbors = request.DATA
        # json_validate(SPECS.get('as_post')).validate(neighbors)
        # response = list()
        # for as_ in neighbors['asns']:
        #
        #     as_obj = facade.create_as(as_)
        #     response.append({'id': as_obj.id})
        #
        # return Response(response, status=status.HTTP_201_CREATED)

        return Response({}, status=status.HTTP_200_OK)

    @logs_method_apiview
    @raise_json_validate('as_put')
    @permission_classes_apiview((IsAuthenticated, Write))
    @commit_on_success
    def put(self, request, *args, **kwargs):
        """Update Neighbor."""

        # neighbors = request.DATA
        # json_validate(SPECS.get('as_put')).validate(neighbors)
        # response = list()
        # for as_ in neighbors['asns']:
        #
        #     as_obj = facade.update_as(as_)
        #     response.append({
        #         'id': as_obj.id
        #     })
        #
        # return Response(response, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_200_OK)

    @logs_method_apiview
    @raise_json_validate('')
    @permission_classes_apiview((IsAuthenticated, Write))
    @commit_on_success
    def delete(self, request, *args, **kwargs):
        """Delete Neighbor."""

        # obj_ids = kwargs['obj_ids'].split(';')
        # facade.delete_as(obj_ids)
        #
        # return Response({}, status=status.HTTP_200_OK)

        return Response({}, status=status.HTTP_200_OK)
