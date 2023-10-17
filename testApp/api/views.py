# coding: utf-8
from contextlib import nullcontext
from select import select
from django.http import request
from django_filters import rest_framework as filters
from rest_framework import generics, pagination, viewsets, status
from django.db import connection
from django.db.models import Q
from django.conf import settings
from testApp.models import *
from testApp.api.serializer import *
from rest_framework.response import Response

from rest_framework.views import APIView
import pandas as pd
import numpy as np
from django.http.response import JsonResponse
import json
import re
import psycopg2.extras
import datetime


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 10


class LargeResultsSetPagination(pagination.PageNumberPagination):
    page_size = 100


class StfdbStaffViewSet(generics.ListCreateAPIView):
    queryset = StfdbStaff.objects.all()
    serializer_class = StfdbStaffSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class MstStaffAPIView(APIView):
    def get(self, Request):
        with connection.cursor() as cursor:

            pSql = (
                'SELECT staff_no ,concat(search_full_name,\'(\',t_m_01_section.section_name,\')\') disp_name ,search_full_name ,t_m_01_section.section_cd ,t_m_01_section.section_name '
                'FROM t_m_02_staff '
                'LEFT JOIN t_m_01_section ON t_m_01_section.section_cd = t_m_02_staff.section_cd '
                'WHERE t_m_02_staff.deleted_flg = 0 AND staff_no not in(201820,208064) AND t_m_01_section.section_cd not in(\'91004\',\'91900\',\'99993\',\'99994\',\'99995\',\'99996\',\'99998\',\'99999\',\'99997\',\'91005\',\'99997\',\'90990\') AND search_full_name not like \'%計上%\' AND search_full_name not like \'%マイナビ%\' AND search_full_name not like \'%集計%\' AND search_full_name not like \'%自社%\' '
                'ORDER BY t_m_01_section.disp_order,t_m_02_staff.disp_order '
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


# マスタ
# public
class PubTM01SectionViewSet(generics.ListCreateAPIView):
    queryset = PubTM01Section.objects.all()
    serializer_class = PubTM01SectionSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('section_cd', 'section_name')


class MstSectionAPIView(APIView):
    def get(self, Request):
        with connection.cursor() as cursor:

            pSql = (
                'SELECT t_m_01_section.section_cd ,t_m_01_section.section_name '
                'FROM t_m_01_section '
                'WHERE deleted_flg = 0 AND t_m_01_section.srvc_fld_cd = \'03\' AND last_effective_dt > now() AND section_cd not in(\'90003\',\'90004\',\'90005\') '
                'ORDER BY t_m_01_section.disp_order '
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


class MstSectionAPIView(APIView):
    def get(self, Request):
        with connection.cursor() as cursor:

            pSql = (
                'SELECT t_m_01_section.section_cd ,t_m_01_section.section_name '
                'FROM t_m_01_section '
                'WHERE deleted_flg = 0 AND t_m_01_section.srvc_fld_cd = \'03\' AND last_effective_dt > now() AND section_cd not in(\'90003\',\'90004\',\'90005\') '
                'ORDER BY t_m_01_section.disp_order '
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


class PubTM02StaffViewSet(generics.ListCreateAPIView):
    queryset = PubTM02Staff.objects.all()
    serializer_class = PubTM02StaffSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('staff_no', 'search_full_name')


# cp2
class Cp2MstuserViewSet(generics.ListCreateAPIView):
    queryset = Cp2Mstuser.objects.all()
    serializer_class = Cp2MstuserSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('userid', 'username')


class MstCp2UserAPIView(APIView):
    def get(self, Request):
        dispdata = (0, 0, '設定なし', '設定なし', None, None)
        with connection.cursor() as cursor:

            pSql = (
                'SELECT row_number() over(order by mteam.disporder,muser.disporder) as disporder ,muser.userid ,concat(muser.username,\'(\',mteam.teamname,\')\') disp_name ,muser.username ,mteam.teamid ,mteam.teamname '
                'FROM cp2.mstuser muser '
                'LEFT JOIN cp2.mstteam mteam ON mteam.teamid = muser.teamid '
                'WHERE muser.userid not in(8698,8006,8630,8009,8011,8013,8495,8614,8578,8562,8564,8616,8607,8606,8620,8619,8618,8615,8608,9001,9999) AND mteam.teamid not in(104,106,107,108,492) AND muser.username not like \'%計上%\' AND muser.username not like \'%マイナビ%\' AND muser.username not like \'%集計%\' AND muser.username not like \'%自社%\' AND muser.username not like \'%ＲＯＢＯ%\' AND muser.username not like \'%使用不可%\' '
                'ORDER BY mteam.disporder,muser.disporder '
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            result.insert(0, dispdata)

            resultData = [dict(zip(returtColumns, row))for row in result]

            # resultData = resultData.insert(0,dispData)

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


class Cp2MstteamViewSet(generics.ListCreateAPIView):
    queryset = Cp2Mstteam.objects.all()
    serializer_class = Cp2MstteamSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


# pjm
class MstPrefViewSet(generics.ListCreateAPIView):
    queryset = MstPref.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstPrefSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstApproachStatusViewSet(generics.ListCreateAPIView):
    queryset = MstApproachStatus.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstApproachStatusSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstContactWaysViewSet(generics.ListCreateAPIView):
    queryset = MstContactWays.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstContactWaysSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstMediaViewSet(generics.ListCreateAPIView):
    queryset = MstMedia.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstMediaSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstCityViewSet(generics.ListCreateAPIView):
    queryset = MstCity.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstCitySerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstDispOrderViewSet(generics.ListCreateAPIView):
    queryset = MstDispOrder.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstDispOrderSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


# 職種マスタ
class MstOccupationAPIView(APIView):
    def get(self, Request):
        with connection.cursor() as cursor:

            pSql = (
                'SELECT moccupation01.id_01 , moccupation01.name ,moccupation01.disp_order '
                'FROM pjm.mst_occupation_01 moccupation01 '
                'WHERE moccupation01.deleted_flg = 0 '
                'ORDER BY moccupation01.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData1 = {}
            resultData1 = [dict(zip(returtColumns, row))for row in result]

        with connection.cursor() as cursor:

            pSql = (
                'SELECT moccupation02.id_01 ,moccupation02.id_02,  moccupation02.name ,moccupation02.disp_order '
                'FROM pjm.mst_occupation_02 moccupation02 '
                'WHERE moccupation02.deleted_flg = 0 '
                'ORDER BY moccupation02.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData2 = [dict(zip(returtColumns, row))for row in result]

        with connection.cursor() as cursor:

            pSql = (
                'SELECT moccupation03.id ,moccupation03.id_01 ,moccupation03.id_02 ,moccupation03.id_03, moccupation03.name ,moccupation03.disp_order ,null "checked" '
                'FROM pjm.mst_occupation_03 moccupation03 '
                'WHERE moccupation03.deleted_flg = 0 '
                'ORDER BY moccupation03.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData3 = [dict(zip(returtColumns, row))for row in result]

        # -------------------------結合作業開始
        data_1 = []  # 最終的なデータ
        # print(resultData1)
        for i, resultrecord2 in enumerate(resultData2):

            resultrecord2_sk = resultrecord2['id_02']

            resultrecord1_sk = resultrecord2['id_01']

            resultrecord2_name = resultrecord2['name']

            disp_order = resultrecord2['disp_order']

            resultrecord3 = [resultrecord3 for resultrecord3 in resultData3 if resultrecord3['id_01']
                             == resultrecord1_sk and resultrecord3['id_02'] == resultrecord2_sk]

            industory_data = {
                "id_01": resultrecord1_sk,
                "id_02": resultrecord2_sk,
                "name": resultrecord2_name,
                "disp_order": disp_order,
                "industory_03": resultrecord3,
            }

            # 最終的な配列に詰め込む
            data_1.append(industory_data)

        data = []

        for i, resultrecord1 in enumerate(resultData1):

            resultrecord1_sk = resultrecord1['id_01']

            resultrecord1_name = resultrecord1['name']

            disp_order = resultrecord1['disp_order']

            data_3 = [recordresult for recordresult in data_1 if recordresult["id_01"] == resultrecord1_sk]

            # print(resultrecord1_sk)
            # print(data_1)
            industory_data = {
                "id": resultrecord1_sk,
                "name": resultrecord1_name,
                "disp_order": disp_order,
                "industory_02": data_3,
            }

            # 最終的な配列に詰め込む
            data.append(industory_data)

            # ヘッダー作成

        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': data,
            # 'results' : data_1
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


class MstCareerStatusViewSet(generics.ListCreateAPIView):
    queryset = MstCareerStatus.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstCareerStatusSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstLastSchoolViewSet(generics.ListCreateAPIView):
    queryset = MstLastSchool.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstLastSchoolSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstEnglishLevelViewSet(generics.ListCreateAPIView):
    queryset = MstEnglishLevel.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstEnglishLevelSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


class MstOtherLangageViewSet(generics.ListCreateAPIView):
    queryset = MstOtherLangage.objects.order_by("disp_order").filter(deleted_flg=0)
    serializer_class = MstOtherLangageSerializer
    pagination_class = LargeResultsSetPagination
    filter_fields = ('id', 'name',  'disp_order')


# 資格マスタAPI
class MstLicenseAPIView(APIView):
    def get(self, Request):
        with connection.cursor() as cursor:
            pSql = (
                'SELECT mstlicense01.id , mstlicense01.name ,mstlicense01.disp_order '
                'FROM pjm.mst_license_01 mstlicense01 '
                'WHERE mstlicense01.deleted_flg = 0 '
                'ORDER BY mstlicense01.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData1 = [dict(zip(returtColumns, row))for row in result]

        with connection.cursor() as cursor:

            pSql = (
                'SELECT mstlicense02.id , mstlicense02.name ,mstlicense02.id_01 ,mstlicense02.disp_order ,null "checked"'
                'FROM pjm.mst_license_02 mstlicense02 '
                'WHERE mstlicense02.deleted_flg = 0 '
                'ORDER BY mstlicense02.disp_order'
            )
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData2 = [dict(zip(returtColumns, row))for row in result]

        data = []  # 最終的なデータ
        for i, resultrecord1 in enumerate(resultData1):

            resultrecord1_sk = resultrecord1['id']

            resultrecord1_name = resultrecord1['name']

            disp_order = resultrecord1['disp_order']

            resultrecord = [resultrecord2 for resultrecord2 in resultData2 if resultrecord2['id_01'] == resultrecord1_sk]

            industory_data = {
                "id": resultrecord1_sk,
                "name": resultrecord1_name,
                "disp_order": disp_order,
                "license_02": resultrecord,
            }

            # 最終的な配列に詰め込む
            data.append(industory_data)

        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': data,
            # 'results' : data_1
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

# 業種マスタ取得API


class MstIndustryAPIView(APIView):
    def get(self, Request):
        with connection.cursor() as cursor:

            pSql = (
                'SELECT mind01.id , mind01.name ,mind01.disp_order '
                'FROM pjm.mst_industry_lbc_01 mind01 '
                'WHERE mind01.deleted_flg = 0 '
                'ORDER BY mind01.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData1 = {}
            resultData1 = [dict(zip(returtColumns, row))for row in result]

        with connection.cursor() as cursor:

            pSql = (
                'SELECT mind02.id_01, mind02.id, mind02.name ,mind02.disp_order '
                'FROM pjm.mst_industry_lbc_02 mind02 '
                'WHERE mind02.deleted_flg = 0 '
                'ORDER BY mind02.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData2 = [dict(zip(returtColumns, row))for row in result]

        with connection.cursor() as cursor:

            pSql = (
                'SELECT mind03.id_01,mind03.id_02, mind03.id ,mind03.name ,mind03.disp_order ,mind03.id_full ,null "checked" '
                'FROM pjm.mst_industry_lbc_03 mind03 '
                'WHERE mind03.deleted_flg = 0 '
                'ORDER BY mind03.disp_order'
            )
            # cursor.execute(pSql,[orderSk])
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData3 = [dict(zip(returtColumns, row))for row in result]

        # -------------------------結合作業開始
        data_1 = []  # 最終的なデータ
        for i, resultrecord2 in enumerate(resultData2):

            resultrecord2_sk = resultrecord2['id']

            resultrecord1_sk = resultrecord2['id_01']

            resultrecord2_name = resultrecord2['name']

            disp_order = resultrecord2['disp_order']

            resultrecord3 = [resultrecord3 for resultrecord3 in resultData3 if resultrecord3['id_02'] == resultrecord2_sk]

            industory_data = {
                "id": resultrecord2_sk,
                "id_01": resultrecord1_sk,
                "name": resultrecord2_name,
                "disp_order": disp_order,
                "industory_03": resultrecord3,
            }

            # 最終的な配列に詰め込む
            data_1.append(industory_data)

        data = []

        for i, resultrecord1 in enumerate(resultData1):

            resultrecord1_sk = resultrecord1['id']

            resultrecord1_name = resultrecord1['name']

            disp_order = resultrecord1['disp_order']

            data_3 = [recordresult for recordresult in data_1 if recordresult["id_01"] == resultrecord1_sk]

            industory_data = {
                "id": resultrecord1_sk,
                "name": resultrecord1_name,
                "disp_order": disp_order,
                "industory_02": data_3,
            }

            # 最終的な配列に詰め込む
            data.append(industory_data)

            # ヘッダー作成

        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': data,
            # 'results' : data_1
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


# トランザクション
class Cp2TrnclientViewSet(generics.ListCreateAPIView):
    queryset = Cp2Trnclient.objects.all()
    serializer_class = Cp2TrnclientSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnClientViewSet(generics.ListCreateAPIView):
    queryset = TrnClient.objects.all()
    serializer_class = TrnClientSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('trn_client_sk', 'lbc_cd', 'client_name_full', 'industry_id_01', 'industry_id_02', 'industry_id_03', 'address_full', 'employee_number',
                     'foundation_ym', 'capital', 'amount_sales', 'url', 'tel', 'keep_flg', 'keep_updated_staff_no', 'keep_updated_staff_no', 'keep_updated_at')


class TrnClientMatchViewSet(generics.ListCreateAPIView):
    queryset = TrnClientMatch.objects.all()
    serializer_class = TrnClientMatchSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnClientContactHistoryViewSet(generics.ListCreateAPIView):
    queryset = TrnClientContactHistory.objects.all()
    serializer_class = TrnClientContactHistorySerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('contact_date', 'staff_no',
                     'action_id', 'contact_ways_id', 'body')


class TrnClientCustomTelViewSet(generics.ListCreateAPIView):
    queryset = TrnClientCustomTel.objects.all()
    serializer_class = TrnClientCustomTelSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')

    def put(self, request):
        with connection.cursor() as cursor:
            # lbcCd = self.request.query_params.get( 'lbc_cd' , None )
            lbcCd = ['888888']
            pSql = (
                'UPDATE pjm.trn_client '
                'SET trn_client_custom_tel_sk = %s '
                ',audit_updated_at = now() '
                'WHERE trn_client_custom_tel_sk = 56 '
            )
            cursor.execute(pSql, lbcCd)

# 求人詳細情報取得API


class TrnOrderViewSet(generics.ListCreateAPIView):
    queryset = TrnOrder.objects.all()
    serializer_class = TrnOrderSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('trn_order_sk', 'media_id', 'title', 'job_description',
                     'annual_income_min', 'annual_income_max', 'url', 'regist_date')


class TrnOrderMatchViewSet(generics.ListCreateAPIView):
    queryset = TrnOrderMatch.objects.all()
    serializer_class = TrnOrderMatchSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnOrderOccupationViewSet(generics.ListCreateAPIView):
    queryset = TrnOrderOccupation.objects.all()
    serializer_class = TrnOrderOccupationSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnOrderWorkLocationViewSet(generics.ListCreateAPIView):
    queryset = TrnOrderWorkLocation.objects.all()
    serializer_class = TrnOrderWorkLocationSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnCareerViewSet(generics.ListCreateAPIView):
    queryset = TrnCareer.objects.all()
    serializer_class = TrnCareerSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('career_id', 'birthday', 'gender_id')


class TrnCareerMatchViewSet(generics.ListCreateAPIView):
    queryset = TrnCareerMatch.objects.all()
    serializer_class = TrnCareerMatchSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnCareerWishOccupationViewSet(generics.ListCreateAPIView):
    queryset = TrnCareerWishOccupation.objects.all()
    serializer_class = TrnCareerWishOccupationSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnCareerWishWorkPrefViewSet(generics.ListCreateAPIView):
    queryset = TrnCareerWishWorkPref.objects.all()
    serializer_class = TrnCareerWishWorkPrefSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')


class TrnCareerLicenseViewSet(generics.ListCreateAPIView):
    queryset = TrnCareerLicense.objects.all()
    serializer_class = TrnCareerLicenseSerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('mits_username', 'mits_password')

# 保存検索条件取得、保存API


class TrnSearchParameterViewSet(generics.ListCreateAPIView):
    queryset = TrnSearchParameter.objects.all()
    serializer_class = TrnSearchParameterSerializer

    def get(self, Request):
        if not 'data_obj' in Request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )

        staff_no = Request.session['data_obj']['user_records']['staff_no']
        trn_search_parameter_sk = self.request.query_params.get("trn_search_parameter_sk", None)

        with connection.cursor() as cursor:
            pSql = (
                'SELECT '
                'trn_search_parameter_sk "trn_search_parameter_sk" '
                ',staff_no "staff_no" '
                ',title  "title" '
                ',content "content" '
                ',disp_order "disp_order" '
                ',audit_created_at "audit_created_at" '
                'FROM pjm.trn_search_parameter '
                'WHERE deleted_flg = 0 '
                'AND staff_no = ' + str(staff_no) + ' '
            )
            if trn_search_parameter_sk:
                pSql += 'AND trn_search_parameter_sk in (\'' + trn_search_parameter_sk + '\') '
            pSql += 'ORDER BY '
            pSql += 'disp_order '
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

    def create(self, request):
        if not 'data_obj' in request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )
        # 継承元クラスのcreateメソッドがvalidationなどの処理を一括で実行する
        now = datetime.datetime.now() + datetime.timedelta(hours=9)  # 9時間問題

        user_stuff_id = request.session['data_obj']['user_records']['mits_username']
        delete_flg = 0
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        data = request.data
        data['audit_created_at'] = now
        data['audit_updated_at'] = now
        data['deleted_flg'] = delete_flg
        data['audit_created_by'] = user_stuff_id
        data['audit_updated_by'] = user_stuff_id
        data['staff_no'] = request.session['data_obj']['user_records']['staff_no']
        data['title'] = self.request.query_params.get('title', None)
        data['content'] = self.request.query_params.get('content', None)
        data['type'] = 0
        data['copy_sk'] = None
        data['original_sk'] = None
        data['disp_order'] = 0
        # シリアライザオブジュエクトを作成
        serializer = TrnSearchParameterSerializer(data=data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request):
        if not 'data_obj' in request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )
        now = datetime.datetime.now() + datetime.timedelta(hours=9)  # 9時間問題
        now = now.strftime("%Y-%m-%d %H:%M:%S")
        user_stuff_id = request.session['data_obj']['user_records']['mits_username']
        trn_search_parameter_sk = self.request.query_params.get("trn_search_parameter_sk", None)
        staff_no = request.session['data_obj']['user_records']['staff_no']
        title = self.request.query_params.get("title", None)
        disp_order = self.request.query_params.get("disp_order", None)
        deleted_flg = int(self.request.query_params.get("deleted_flg", None))
        with connection.cursor() as cursor:
            pSql = (
                'UPDATE pjm.trn_search_parameter '
                'SET audit_updated_at = %s '
                ",audit_updated_by = '" + user_stuff_id + "' "
            )
            if deleted_flg == 1:
                pSql += ',deleted_flg = 1 '
                pSql += 'WHERE trn_search_parameter_sk = ' + trn_search_parameter_sk + ' '
                cursor.execute(pSql, [now])

                response_header: dict = {
                    'HTTP-response-code': status.HTTP_200_OK
                }

                # ボディ作成
                response_data: dict = {
                    'trn_search_parameter_sk': trn_search_parameter_sk,
                    'staff_no': staff_no,
                    'deleted_flg': 1,
                    'audit_updated_at': now,
                    'audit_updated_by': user_stuff_id,
                }

                return JsonResponse(
                    status=status.HTTP_200_OK,
                    headers=response_header,
                    data=response_data,
                    safe=False,
                    json_dumps_params={'ensure_ascii': False}
                )

            else:
                if title:
                    pSql += ",title = '" + title + "' "
                if disp_order:
                    pSql += ',disp_order = ' + disp_order + ' '
                pSql += 'WHERE trn_search_parameter_sk = ' + trn_search_parameter_sk + ' '

                cursor.execute(pSql, [now])

                response_header: dict = {
                    'HTTP-response-code': status.HTTP_200_OK
                }

                # ボディ作成
                response_data: dict = {
                    'trn_search_parameter_sk': trn_search_parameter_sk,
                    'staff_no': staff_no,
                    'title': title,
                    'disp_order': disp_order,
                    'audit_updated_at': now,
                    'audit_updated_by': user_stuff_id,
                }

                return JsonResponse(
                    status=status.HTTP_200_OK,
                    headers=response_header,
                    data=response_data,
                    safe=False,
                    json_dumps_params={'ensure_ascii': False}
                )


# 検索履歴取得API
class TrnSearchLatestHistoryViewSet(generics.ListCreateAPIView):
    queryset = TrnSearchLatestHistory.objects.all()
    serializer_class = TrnSearchLatestHistorySerializer
    pagination_class = StandardResultsSetPagination
    filter_fields = ('trn_search_latest_history_sk',
                     'staff_no', 'content', 'audit_updated_at')


# 求人検索結果取得API
class SearchAPIView(APIView):
    def get(self, Request):
        if not 'data_obj' in Request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )
        # ログインユーザ情報
        staff_no = str(Request.session['data_obj']['user_records']['staff_no'])
        staff_name = str(Request.session['data_obj']['user_records']['staff_name'])
        staff_section = str(Request.session['data_obj']['user_records']['staff_section'])

        # param展開する
        new_flg_client = self.request.query_params.get("new_flg_client", None)  # 20231004 新井追記
        new_flg_order = self.request.query_params.get("new_flg_order", None)  # 20231004 新井追記

        op_mediums = self.request.query_params.getlist("op_mediums[]", None)
        op_mediums_text = ','.join(op_mediums)

        key_words = self.request.query_params.get("key_words", None)
        industries = self.request.query_params.getlist("industries[]", None)

        industries_text = '\',\''.join(industries)

        honsya_prefs = self.request.query_params.getlist("honsya_prefs[]", None)
        honsya_prefs_text = ','.join(honsya_prefs)

        kinmu_prefs = self.request.query_params.getlist("kinmu_prefs[]", None)
        kinmu_prefs_text = ','.join(kinmu_prefs)

        income_min = self.request.query_params.get("income_min", None)
        income_max = self.request.query_params.get("income_max", None)
        occupation = self.request.query_params.getlist("occupation[]", None)
        occupation_text = '\',\''.join(occupation)

        keep_status = self.request.query_params.getlist("keep_status[]", None)

        keep_status_text = ','.join(keep_status)

        cp2_client_raids = self.request.query_params.getlist("cp2_client_raids[]", None)
        cp2_client_raids_text = ','.join(cp2_client_raids)

        approach_date_start = self.request.query_params.get("approach_date_start", None)
        approach_date_end = self.request.query_params.get("approach_date_end", None)

        except_approach_date_start = self.request.query_params.get("except_approach_date_start", None)
        except_approach_date_end = self.request.query_params.get("except_approach_date_end", None)

        approach_status = self.request.query_params.getlist("approach_status[]", None)
        approach_status_text = ','.join(approach_status)

        approach_users = self.request.query_params.getlist("approach_users[]", None)
        approach_users_text = ','.join(approach_users)

        approach_sections = self.request.query_params.getlist("approach_sections[]", None)
        approach_sections_text = '\',\''.join(approach_sections)

        cp2_client_id = self.request.query_params.get("cp2_client_id", None)

        lbc_code = self.request.query_params.get("lbc_code", None)
        lbc_code_text = lbc_code.replace(',', '\',\'')
        exit_nomach = self.request.query_params.get("exit_nomach", None)
        exit_nopublic = self.request.query_params.get("exit_nopublic", None)
        sort_id = self.request.query_params.get("sort_id", None)

        # ここから求職者マッチング情報----------------------
        lead_active = self.request.query_params.get("lead_active", None)
        lead_status = self.request.query_params.getlist("lead_status[]", None)
        lead_status_text = ','.join(lead_status)

        lead_age_from = self.request.query_params.get("lead_age_from", None)
        lead_age_to = self.request.query_params.get("lead_age_to", None)
        lead_gender = self.request.query_params.getlist("lead_gender[]", None)
        lead_gender_text = ','.join(lead_gender)

        lead_occupation = self.request.query_params.getlist("lead_occupation[]", None)
        lead_occupation_text = '\',\''.join(lead_occupation)

        lead_prefs = self.request.query_params.getlist("lead_prefs[]", None)
        lead_prefs_tmp = ','.join(lead_prefs)
        lead_prefs_text = lead_prefs_tmp.replace(',', '\',\'')

        lead_last_school = self.request.query_params.getlist("lead_last_school[]", None)
        lead_last_school_text = ','.join(lead_last_school)

        lead_english_level = self.request.query_params.getlist("lead_english_level[]", None)
        lead_english_level_text = ','.join(lead_english_level)

        lead_now_income_min = self.request.query_params.get("lead_now_income_min", None)
        lead_now_income_max = self.request.query_params.get("lead_now_income_max", None)
        lead_hope_income_min = self.request.query_params.get("lead_hope_income_min", None)
        lead_hope_income_max = self.request.query_params.get("lead_hope_income_max", None)
        lead_company_history_min = self.request.query_params.get("lead_company_history_min", None)
        lead_company_history_max = self.request.query_params.get("lead_company_history_max", None)
        lead_languages = self.request.query_params.getlist("lead_languages[]", None)
        lead_languages_text = ','.join(lead_languages)

        lead_skills = self.request.query_params.getlist("lead_skills[]", None)
        lead_skills_text = '\',\''.join(lead_skills)

        with connection.cursor() as cursor:
            countSql = (
                'with v_client_list as ( '
                'SELECT DISTINCT '
                '    clbase.lbc_cd "lbc_cd" '
                '    , crCntClMatch.match_count "count" '
                '    , clbase.latest_contact_date "contact_date" '
                '    , orbaseRegDate.regist_date "regist_date" '
                '    , case when clmatch.trn_client_match_sk is not null then 1 end client_ids '
            )

            if sort_id == '7' or sort_id == '8':
                countSql += ', count(distinct crMatch.career_id) matchCount '

            countSql += (
                'FROM '
                '    pjm.trn_client clbase  '
                '    LEFT JOIN pjm.trn_order orbase on clbase.trn_client_sk = orbase.trn_client_sk  '
                '    LEFT JOIN pjm.trn_client_match clmatch on clmatch.lbc_cd = clbase.lbc_cd  '
                '    LEFT JOIN pjm.trn_client_contact_history clcntcthist on clcntcthist.lbc_cd = clbase.lbc_cd  '
                '    LEFT JOIN public.t_m_02_staff clcntcthistStaff on clcntcthistStaff.staff_no = clcntcthist.staff_no  '
                '    LEFT JOIN public.t_m_01_section clcntcthistSection on clcntcthistSection.section_cd = clcntcthistStaff.section_cd  '
                '    LEFT JOIN pjm.mst_industry_lbc_01 mind01 on clbase.industry_id_01 = mind01.id  '
                '    LEFT JOIN pjm.mst_industry_lbc_02 mind02 on clbase.industry_id_02 = mind02.id and mind01.id = mind02.id_01  '
                '    LEFT JOIN pjm.mst_industry_lbc_03 mind03 on clbase.industry_id_03 = mind03.id and mind01.id = mind03.id_01 and mind02.id = mind03.id_02  '
                '    LEFT JOIN t_m_02_staff staff on staff.staff_no = clbase.keep_updated_staff_no  '
                '    LEFT JOIN t_m_01_section section on section.section_cd = staff.section_cd  '
                '    LEFT JOIN cp2.trnclient clcp2 on clmatch.client_id = clcp2.client_id  '
                '    LEFT JOIN cp2.mstuser muser on muser.userid = clcp2.charge_id  '
                '    LEFT JOIN cp2.mstteam mteam on mteam.teamid = clcp2.chargeteam_id  '
                '    LEFT JOIN public.t_m_02_staff staffhist on staffhist.staff_no = clcntcthist.staff_no  '
                '    LEFT JOIN public.t_m_01_section sectionhist on sectionhist.section_cd = staffhist.section_cd  '
                '    LEFT JOIN pjm.trn_order_occupation orOccupSearch ON orOccupSearch.trn_order_sk = orbase.trn_order_sk  '
                '    LEFT join cp2.mstuser clRa on clRa.userid = clcp2.charge_id  '
                '    LEFT JOIN (  '
                '        select '
                '            trn_client_sk '
                '            , max(regist_date) regist_date  '
                '        from '
                '            pjm.trn_order  '
                '        group by '
                '            trn_client_sk '
                '    ) orbaseRegDate on orbaseRegDate.trn_client_sk = orbase.trn_client_sk  '
                '    LEFT JOIN pjm.trn_order_work_location orwklocationSearch on orwklocationSearch.trn_order_sk = orbase.trn_order_sk  '
                '    LEFT JOIN pjm.trn_count_match_career_by_client crCntClMatch ON crCntClMatch.trn_client_sk = clbase.trn_client_sk '
            )

            if except_approach_date_start or except_approach_date_end:
                countSql += (
                    '    LEFT JOIN (  '
                    '    select '
                    '        clHist.lbc_cd '
                    '    from '
                    '        pjm.trn_client_contact_history clhist '
                    '    where '
                )
                if except_approach_date_start and except_approach_date_end:
                    countSql += ' clhist.contact_date between \'' + \
                        except_approach_date_start.replace('T', ' ') + '\' and \'' + except_approach_date_end.replace('T', ' ') + '\'  '
                elif except_approach_date_start and not except_approach_date_end:
                    countSql += ' clhist.contact_date > \'' + except_approach_date_start.replace('T', ' ') + '\''
                elif not except_approach_date_start and except_approach_date_end:
                    countSql += ' clhist.contact_date < \'' + except_approach_date_end.replace('T', ' ') + '\''

                countSql += (
                    '   ) clHistExcept on clHistExcept.lbc_cd = clbase.lbc_cd '
                )

            if sort_id == '7' or sort_id == '8':
                countSql += (
                    # 候補求職者数
                    'LEFT JOIN  ( '
                    '	select '
                    '		distinct '
                    '		crMatch.trn_order_sk, '
                    '		crBase.career_id  '
                    '	from '
                    '		pjm.trn_career_match crMatch '
                    '		left join pjm.trn_career crBase on crBase.career_id = crMatch.career_id '
                    '		left join pjm.trn_order orBase on orBase.trn_order_sk = crMatch.trn_order_sk '
                    '		left join pjm.trn_client clBase on clBase.trn_client_sk = orBase.trn_client_sk '
                    '		left join pjm.trn_career_wish_occupation crWishOccup on crWishOccup.career_id = crBase.career_id '
                    '		left join pjm.trn_career_wish_work_pref crWishWorkPref on crWishWorkPref.career_id = crBase.career_id '
                    '		left join pjm.trn_career_license crLicense on crLicense.career_id = crBase.career_id '
                    # '       LEFT JOIN ('
                    # '            select '
                    # '                 career_id '
                    # '                 ,regexp_split_to_table(crbase.wishwkarea_id,\'/\') wishwkarea_id '
                    # '            from '
                    # '                 cp2.trncareer crbase '
                    # '       ) crbasepref on crbasepref.career_id = crBase.career_id '
                    '	where '
                    '		crMatch.deleted_flg = 0 '
                )

                # 有効/非有効
                if lead_active:
                    countSql += 'and crBase.valid_flg = (' + lead_active + ') '

                # 求職者ステータス
                if lead_status:
                    countSql += 'and crBase.career_status in (' + lead_status_text + ') '
                # 年齢
                if lead_age_from:
                    countSql += 'and Date_Part(\'year\',age(crBase.birthday)) >= ' + lead_age_from + ' '
                if lead_age_to:
                    countSql += 'and Date_Part(\'year\',age(crBase.birthday)) <= ' + lead_age_to + ' '
                # 性別
                if lead_gender:
                    countSql += 'and crBase.gender_id in (' + lead_gender_text + ') '
           #    希望職種
                if lead_occupation:
                    countSql += 'and crWishOccup.occupation_id in (\'' + lead_occupation_text + '\') '
                # 希望勤務地
                if lead_prefs:
                    countSql += 'and crWishWorkPref.pref_id in (\'' + lead_prefs_text + '\') '
                # 最終学歴
                if lead_last_school:
                    countSql += 'and crBase.last_school_id in (' + lead_last_school_text + ') '
                # 経験社数
                if lead_company_history_min:
                    countSql += 'and crBase.exp_company_num >= ' + lead_company_history_min + ' '
                if lead_company_history_max:
                    countSql += 'and crBase.exp_company_num <= ' + lead_company_history_max + ' '
                # 英語レベル
                if lead_english_level:
                    countSql += 'and crBase.english_level_id in (' + lead_english_level_text + ') '
                # 現在年収
                if lead_now_income_min and lead_now_income_max:
                    countSql += 'and crBase.current_salary between ' + lead_now_income_min + ' and ' + lead_now_income_max + ' '
                elif lead_now_income_min and not lead_now_income_max:
                    countSql += 'and crBase.current_salary >= ' + lead_now_income_min + ' '
                elif not lead_now_income_min and lead_now_income_max:
                    countSql += 'and crBase.current_salary <= ' + lead_now_income_max + ' '
                # 希望年収
                if lead_hope_income_min and lead_hope_income_max:
                    countSql += 'and crBase.wish_salary between ' + lead_hope_income_min + ' and ' + lead_hope_income_max + ' '
                elif lead_hope_income_min and not lead_hope_income_max:
                    countSql += 'and crBase.wish_salary >= ' + lead_hope_income_min + ' '
                elif not lead_hope_income_min and lead_hope_income_max:
                    countSql += 'and crBase.wish_salary <= ' + lead_hope_income_max + ' '

                # その他言語
                if lead_languages:
                    countSql += 'and ( '
                    countSql += 'other_langage_1_id in (' + lead_languages_text + ') '
                    countSql += 'or other_langage_2_id in (' + lead_languages_text + ') '
                    countSql += 'or other_langage_3_id in (' + lead_languages_text + ') '
                    countSql += ' ) '
                # 資格
                if lead_skills:
                    countSql += 'and crLicense.license_id in (\'' + lead_skills_text + '\') '

                countSql += ') crMatch on crMatch.trn_order_sk = orbase.trn_order_sk '

            countSql += 'where clbase.deleted_flg = 0 and ( orBase.deleted_flg = 0 or orBase.deleted_flg is null ) and clbase.sales_status_id = 0 '

            # 新着フラグ(企業)  20231004 新井追記
            if new_flg_client == 'true':
                countSql += 'and clbase.new_flg = 1 '

            # 企業名
            if key_words:
                # 全角に変換
                full_key_words = key_words.translate(str.maketrans({chr(0x0021 + i): chr(0xFF01 + i) for i in range(94)}))
                countSql += 'and ( clbase.client_name_full like \'%' + key_words + '%\' '
                countSql += 'or clbase.client_name_full like \'%' + full_key_words + '%\' ) '
                # 業種
            if industries:
                countSql += 'and ( clbase.industry_id_01 in (\'' + industries_text + '\') '
                countSql += 'or clbase.industry_id_02 in (\'' + industries_text + '\') '
                countSql += 'or clbase.industry_id_03 in (\'' + industries_text + '\') ) '
                # 本社都道府県
            if honsya_prefs:
                countSql += 'and clbase.pref_id in (' + honsya_prefs_text + ') '

            # キープステータス
            if not not keep_status:
                countSql += 'and ( '
                # フラグがついていて自分所有のもの ※定数にしたい
                if '1' in keep_status_text:
                    countSql += ' (clbase.keep_flg = 1 and clbase.keep_updated_staff_no = ' + staff_no + ' ) '
                # フラグがついていて自分所有でないもの　※定数にしたい
                if '2' in keep_status_text and '1' not in keep_status_text:
                    countSql += ' (clbase.keep_flg = 1 and clbase.keep_updated_staff_no <> ' + staff_no + ' ) '
                elif '2' in keep_status_text and '1' in keep_status_text:
                    countSql += ' or (clbase.keep_flg = 1 and clbase.keep_updated_staff_no <> ' + staff_no + ' ) '
                # フラグがついてないもの　※定数にしたい
                if '3' in keep_status_text and '1' not in keep_status_text and '2' not in keep_status_text:
                    countSql += 'clbase.keep_flg = 0 '
                elif '3' in keep_status_text and ('1' in keep_status_text or '2' in keep_status_text):
                    countSql += 'or (clbase.keep_flg = 0 ) '
                countSql += ') '

            # LBCコード
            if lbc_code:
                countSql += 'and clbase.lbc_cd in( \'' + lbc_code_text + '\' )'

            # アプローチ日時
            if approach_date_start and approach_date_end:
                countSql += 'and clcntcthist.contact_date between \'' + \
                    approach_date_start.replace('T', ' ') + '\' and \'' + approach_date_end.replace('T', ' ') + '\' '
            elif approach_date_start and not approach_date_end:
                countSql += 'and clcntcthist.contact_date >= \'' + approach_date_start.replace('T', ' ') + '\''
            elif not approach_date_start and approach_date_end:
                countSql += 'and clcntcthist.contact_date <= \'' + approach_date_end.replace('T', ' ') + '\''

            # アプローチ日時(指定期間アプローチなし検索)
            if except_approach_date_start or except_approach_date_end:
                countSql += ' and clHistExcept.lbc_cd is null '

            # アプローチ者
            if approach_users:
                countSql += 'and clcntcthist.staff_no in (' + approach_users_text + ') '
            # アプローチ者所属部署
            if approach_sections:
                countSql += 'and clcntcthistSection.section_cd in (\'' + approach_sections_text + '\') '
            # アプローチ最新結果
            if approach_status:
                countSql += 'and clcntcthist.approach_id in (' + approach_status_text + ') '

            # CP2企業RA
            if cp2_client_raids:
                if cp2_client_raids_text == '0':
                    countSql += ' and clmatch.client_id is null '
                elif '0' in cp2_client_raids:
                    countSql += ' and ( clmatch.client_id is null or clcp2.charge_id in ( ' + cp2_client_raids_text + ' )) '
                else:
                    countSql += ' and clcp2.charge_id in ( ' + cp2_client_raids_text + ' ) '

            # CP2企業ID
            if cp2_client_id:
                countSql += ' and clmatch.client_id in( ' + str(cp2_client_id) + ') '
            # 掲載中求人がない企業の除外
            if exit_nopublic == 'checked' or exit_nopublic == 'true':
                countSql += 'and orbase.trn_order_sk is not null '

            # ================= 求人情報 =========================
            # 新着フラグ(求人) 20231004 新井追記
            if new_flg_order == 'true':
                countSql += 'and orbase.new_flg = 1 '

            # 求人媒体
            if op_mediums:
                countSql += 'and orbase.media_id in (' + op_mediums_text + ') '

            # 職種
            if occupation:
                countSql += 'and orOccupSearch.occupation_id in (\'' + occupation_text + '\') '

             # 勤務地都道府県
            if kinmu_prefs:
                countSql += 'and orwklocationSearch.pref_id in (' + kinmu_prefs_text + ') '

             # 年収
            if income_min != '0' and income_max != '1000000000':
                countSql += 'and ( '
                countSql += 'orbase.annual_income_min >= ' + income_min + ' '
                countSql += 'and orbase.annual_income_max <= ' + income_max + ' '
                countSql += ') '
            elif income_min == '0' and income_max != '1000000000':
                countSql += 'and ( '
                countSql += '(orbase.annual_income_min is null or orbase.annual_income_min >= ' + income_min + ') '
                countSql += 'and orbase.annual_income_max <= ' + income_max + ' '
                countSql += ') '
            elif income_min != '0' and income_max == '1000000000':
                countSql += 'and ( '
                countSql += 'orbase.annual_income_min >= ' + income_min + ' '
                countSql += 'and (orbase.annual_income_max is null or orbase.annual_income_max <= ' + income_max + ') '
                countSql += ') '

            # マッチング求職者がいない求人の除外　
            if exit_nomach == 'checked' or exit_nomach == True:
                countSql += 'and (crCntClMatch.match_count is not null or crCntClMatch.match_count > 0) '
            # ==================================================

            if sort_id == '7' or sort_id == '8':
                countSql += (
                    '    group by '
                    '       clbase.lbc_cd '
                    '       , crCntClMatch.match_count '
                    '       , clbase.latest_contact_date '
                    '       , orbaseRegDate.regist_date '
                    '       , clmatch.trn_client_match_sk '
                )

            countSql += ') select * from v_client_list '

            # 並び替え
            if sort_id == '1':
                countSql += 'ORDER BY client_ids NULLS FIRST, count DESC NULLS LAST '
            elif sort_id == '2':
                countSql += 'ORDER BY client_ids NULLS FIRST, count ASC'
            elif sort_id == '3':
                countSql += 'ORDER BY client_ids NULLS FIRST, contact_date DESC NULLS LAST '
            elif sort_id == '4':
                countSql += 'ORDER BY client_ids NULLS FIRST, contact_date ASC '
            elif sort_id == '5':
                countSql += 'ORDER BY client_ids NULLS FIRST, regist_date DESC NULLS LAST '
            elif sort_id == '6':
                countSql += 'ORDER BY client_ids NULLS FIRST, regist_date ASC '
            elif sort_id == '7':
                countSql += 'ORDER BY client_ids NULLS FIRST, matchCount DESC NULLS LAST '
            elif sort_id == '8':
                countSql += 'ORDER BY client_ids NULLS FIRST, matchCount ASC '
            else:
                countSql += 'ORDER BY client_ids NULLS FIRST, count DESC '

        cursor = connection.cursor()
        cursor.execute(countSql)
        returnColumns = [col[0] for col in cursor.description]
        countData = pd.DataFrame(cursor.fetchall(), columns=returnColumns)  # Decimal対策
        countData = countData.fillna('')

        # ここから求職者マッチング情報----------------------

        countData["lbc_cd"] = countData["lbc_cd"].astype(str)
        totalCount = len(countData["lbc_cd"])

        countLbcList = countData["lbc_cd"].to_list()

        pageNum = int(self.request.query_params.get("page_num", None))

        # スライスNOを計算する
        if pageNum == 1:
            x = pageNum-1
        else:
            x = (pageNum-1) * 10
        y = pageNum * 10

        # 対象のLBC取得
        LbcList = countLbcList[x:y]

        if not LbcList:
            LbcList = ['']

        print('----------------------LbcList---------------------------------------')
        LbcList_text = '\',\''.join(LbcList)

        print('-------------------------------------------------------------')

        # 企業求人情報を取得する
        with connection.cursor() as cursor:
            temp = ''
            for i, lbcCode in enumerate(LbcList):
                # if lbcCode != None:
                temp += ' WHEN %s THEN ' + str(i)

            pSql = (
                'with v_client as ('
                'SELECT clbase.trn_client_sk "trn_client_sk" '
                ', clbase.lbc_cd "lbc_cd" '
                ', clbase.client_name_full "client_name" '
                ', mstind.indname "industry" '
                ', clbase.address_full "address_full" '
                ', clbase.employee_number "employee_number" '
                ', clbase.foundation_ym "foundation_ym" '
                ', clbase.capital "capital" '
                ', clbase.amount_sales "amount_sales" '
                ', clbase.url "url" '
                ', clbase.tel "tel_lbc" '
                ', clMediaTel.tel "tel_doda" '
                ', clcstmtel.tel "tel_custom" '
                ',  CASE WHEN ( SELECT count(pjm.trn_client_contact_history.trn_client_contact_history_sk) FROM pjm.trn_client_contact_history WHERE pjm.trn_client_contact_history.lbc_cd=clbase.lbc_cd AND pjm.trn_client_contact_history.approach_id=6 AND pjm.trn_client_contact_history.deleted_flg=0 ) > 0 THEN 1 ELSE 0 END "alert_flg" '
                ', clbase.keep_flg "keep_disp_flg" '
                ', staff.staff_no "keep_disp_staff_no" '
                ', staff.search_full_name "keep_disp_staff_name" '
                ', tmsection.section_name "keep_disp_section_name" '
                ', clbase.keep_updated_at "keep_disp_date" '
                ', orbase.trn_order_sk "order_trn_order_sk" '
                ', oroccupation.name "order_occupation_name" '
                ', orwklocation.pref_name "order_work_location" '
                ', orbase.annual_income_min "order_annual_income_min" '
                ', orbase.annual_income_max "order_annual_income_max" '
                ', ormatch.cp2_order_id "order_cp2_order_id" '
                ', (SELECT COUNT(crmatch.trn_career_match_sk) FROM pjm.trn_career_match crmatch WHERE crmatch.deleted_flg=0 AND crmatch.trn_order_sk = orbase.trn_order_sk) "order_career_count" '
                ', ormatch.match_value_01 "order_match_01" '
                ', ormatch.match_value_02 "order_match_02" '
                ', ormatch.match_value_03 "order_match_03" '
                ', orbase.media_id "order_media_id"  '
                ', clcstmtel_info.tel_custom_disp_update_info "tel_custom_disp_update_info"   '
                ', coalesce(crMatch.matchCount,0) "match_count" '
                ', clbase.new_flg "new_flg_client" '    # 20231004 新井追記
                ', orbase.new_flg "new_flg_order" '    # 20231004 新井追記
                'FROM pjm.trn_client clbase  '
                'LEFT JOIN pjm.trn_client_custom_tel clcstmtel on clcstmtel.lbc_cd = clbase.lbc_cd and clcstmtel.trn_client_custom_tel_sk = clbase.latest_custom_tel_sk '
                'LEFT JOIN ( SELECT  clcstmtel.lbc_cd,  concat(clcstmtel.audit_created_at,\' \', tmsection.section_name,\' \', staff.search_full_name) tel_custom_disp_update_info  FROM ( SELECT clcstmtel.lbc_cd  ,max(clcstmtel.audit_created_at) audit_created_at FROM pjm.trn_client_custom_tel clcstmtel GROUP BY clcstmtel.lbc_cd ) clcstmtel LEFT JOIN  pjm.trn_client_contact_history clhist ON clhist.lbc_cd = clcstmtel.lbc_cd LEFT JOIN public.t_m_02_staff staff on staff.staff_no = clhist.staff_no LEFT JOIN public.t_m_01_section tmsection on tmsection.section_cd = staff.section_cd   ) clcstmtel_info on clcstmtel_info.lbc_cd = clbase.lbc_cd '
                # 'LEFT JOIN(select clbase.lbc_cd ,concat(mstind01.name,\',\',mstind02.name,\',\',mstind03.name) indname from pjm.trn_client clbase LEFT JOIN pjm.mst_industry_lbc_03 mstind01 on mstind01.id_full = clbase.industry_id_01 LEFT JOIN pjm.mst_industry_lbc_03 mstind02 on mstind02.id_full = clbase.industry_id_02 LEFT JOIN pjm.mst_industry_lbc_03 mstind03 on mstind03.id_full = clbase.industry_id_03) mstind on mstind.lbc_cd = clbase.lbc_cd  '
                'LEFT JOIN ( '
                '    select clbase.lbc_cd '
                '   ,TRIM(\',\' FROM concat( '
                '        mstind01.name '
                '        ,case when mstind02.name <> mstind01.name and mstind02.name is not null then  \',\' || mstind02.name end '
                '        ,case when (mstind03.name <> mstind01.name and mstind03.name <> mstind02.name) and mstind03.name is not null then  \',\' || mstind03.name end '
                '    )) indname '
                '   from pjm.trn_client clbase '
                '       LEFT JOIN pjm.mst_industry_lbc_03 mstind01 on mstind01.id_full = clbase.industry_id_01 '
                '       LEFT JOIN pjm.mst_industry_lbc_03 mstind02 on mstind02.id_full = clbase.industry_id_02 '
                '       LEFT JOIN pjm.mst_industry_lbc_03 mstind03 on mstind03.id_full = clbase.industry_id_03 '
                ')mstind on mstind.lbc_cd = clbase.lbc_cd  '

                'LEFT JOIN public.t_m_02_staff staff on staff.staff_no = clbase.keep_updated_staff_no  '
                'LEFT JOIN public.t_m_01_section tmsection on tmsection.section_cd = staff.section_cd  '
                # 'LEFT JOIN pjm.trn_order orbase on clbase.trn_client_sk = orbase.trn_client_sk  '

                'LEFT JOIN ('
                'select '
                ' orbase.* '
                'from '
                '    pjm.trn_order orbase '
                '    LEFT JOIN pjm.trn_order_occupation orOccupSearch on orOccupSearch.trn_order_sk = orbase.trn_order_sk '
                '    LEFT JOIN pjm.trn_order_work_location orwklocationSearch on orwklocationSearch.trn_order_sk = orbase.trn_order_sk '
                'where '
                '     orbase.deleted_flg = 0 '
            )
            # 求人媒体
            if op_mediums:
                pSql += 'and orbase.media_id in (' + op_mediums_text + ') '
            # 職種
            if occupation:
                pSql += 'and orOccupSearch.occupation_id in (\'' + occupation_text + '\') '

            # 勤務地都道府県
            if kinmu_prefs:
                pSql += 'and orwklocationSearch.pref_id in (' + kinmu_prefs_text + ') '
             # 年収
            if income_min != '0' and income_max != '1000000000':
                pSql += 'and ( '
                pSql += 'orbase.annual_income_min >= ' + income_min + ' '
                pSql += 'and orbase.annual_income_max <= ' + income_max + ' '
                pSql += ') '
            elif income_min == '0' and income_max != '1000000000':
                pSql += 'and ( '
                pSql += '(orbase.annual_income_min is null or orbase.annual_income_min >= ' + income_min + ') '
                pSql += 'and orbase.annual_income_max <= ' + income_max + ' '
                pSql += ') '
            elif income_min != '0' and income_max == '1000000000':
                pSql += 'and ( '
                pSql += 'orbase.annual_income_min >= ' + income_min + ' '
                pSql += 'and (orbase.annual_income_max is null or orbase.annual_income_max <= ' + income_max + ') '
                pSql += ') '

            pSql += (
                ') orbase on clbase.trn_client_sk = orbase.trn_client_sk '
                'LEFT JOIN( select oroccupation.trn_order_sk , string_agg(oroccupation.occupation_id,\',\') as occupation_id , case when string_agg(mstoccupation03.name,\',\') is not null then string_agg(mstoccupation03.name,\',\') else \'その他職種\' end as name from pjm.trn_order_occupation oroccupation LEFT JOIN pjm.mst_occupation_03 mstoccupation03 on mstoccupation03.id = oroccupation.occupation_id group by oroccupation.trn_order_sk ) oroccupation on oroccupation.trn_order_sk = orbase.trn_order_sk  '
                'LEFT JOIN ( SELECT orwklocation.trn_order_sk, string_agg(mpref.name,\',\') pref_name FROM pjm.trn_order_work_location orwklocation LEFT JOIN pjm.mst_pref mpref on mpref.id = orwklocation.pref_id GROUP BY orwklocation.trn_order_sk ) orwklocation on orwklocation.trn_order_sk = orbase.trn_order_sk  '
                'LEFT JOIN pjm.trn_order_match ormatch ON ormatch.trn_order_match_sk =(SELECT tmp_ormatch.trn_order_match_sk FROM pjm.trn_order_match tmp_ormatch WHERE tmp_ormatch.deleted_flg=0 AND tmp_ormatch.trn_order_sk = orbase.trn_order_sk and tmp_ormatch.match_value_sum > 0 ORDER BY match_value_sum DESC,cp2_order_id DESC LIMIT 1)  '
                'LEFT JOIN pjm.trn_order_work_location orwklocationSearch on orwklocationSearch.trn_order_sk = orbase.trn_order_sk '
                'LEFT JOIN pjm.trn_client_media_tel clMediaTel on clMediaTel.media_id = 2 and clMediaTel.lbc_cd = clbase.lbc_cd '

                # 候補求職者数
                'LEFT JOIN  ( '
                '	select '
                '		distinct '
                '		crMatch.trn_order_sk, '
                '		count(distinct crBase.career_id) matchCount  '
                '	from '
                '		pjm.trn_career_match crMatch '
                '		left join pjm.trn_career crBase on crBase.career_id = crMatch.career_id '
                '		left join pjm.trn_order orBase on orBase.trn_order_sk = crMatch.trn_order_sk '
                '		left join pjm.trn_client clBase on clBase.trn_client_sk = orBase.trn_client_sk '
                '		left join pjm.trn_career_wish_occupation crWishOccup on crWishOccup.career_id = crBase.career_id '
                '		left join pjm.trn_career_wish_work_pref crWishWorkPref on crWishWorkPref.career_id = crBase.career_id '
                '		left join pjm.trn_career_license crLicense on crLicense.career_id = crBase.career_id '
                # '       LEFT JOIN ('
                # '            select '
                # '                 career_id '
                # '                 ,regexp_split_to_table(crbase.wishwkarea_id,\'/\') wishwkarea_id '
                # '            from '
                # '                 cp2.trncareer crbase '
                # '       ) crbasepref on crbasepref.career_id = crBase.career_id '
                '	where '
                '		crMatch.deleted_flg = 0 and clbase.sales_status_id = 0 '
            )
            pSql += ' and clBase.lbc_cd in (\'' + LbcList_text + '\') '

            # 有効/非有効
            if lead_active:
                pSql += 'and crBase.valid_flg = (' + lead_active + ') '

            # 求職者ステータス
            if lead_status:
                pSql += 'and crBase.career_status in (' + lead_status_text + ') '
            # 年齢
            if lead_age_from:
                pSql += 'and Date_Part(\'year\',age(crBase.birthday)) >= ' + lead_age_from + ' '
            if lead_age_to:
                pSql += 'and Date_Part(\'year\',age(crBase.birthday)) <= ' + lead_age_to + ' '
            # 性別
            if lead_gender:
                pSql += 'and crBase.gender_id in (' + lead_gender_text + ') '
           # 希望職種
            if lead_occupation:
                pSql += 'and crWishOccup.occupation_id in (\'' + lead_occupation_text + '\') '
            # 希望勤務地
            if lead_prefs:
                pSql += 'and crWishWorkPref.pref_id in (\'' + lead_prefs_text + '\') '
            # 最終学歴
            if lead_last_school:
                pSql += 'and crBase.last_school_id in (' + lead_last_school_text + ') '
            # 経験社数
            if lead_company_history_min:
                pSql += 'and crBase.exp_company_num >= ' + lead_company_history_min + ' '
            if lead_company_history_max:
                pSql += 'and crBase.exp_company_num <= ' + lead_company_history_max + ' '
            # 英語レベル
            if lead_english_level:
                pSql += 'and crBase.english_level_id in (' + lead_english_level_text + ') '
            # 現在年収
            if lead_now_income_min and lead_now_income_max:
                pSql += 'and crBase.current_salary between ' + lead_now_income_min + ' and ' + lead_now_income_max + ' '
            elif lead_now_income_min and not lead_now_income_max:
                pSql += 'and crBase.current_salary >= ' + lead_now_income_min + ' '
            elif not lead_now_income_min and lead_now_income_max:
                pSql += 'and crBase.current_salary <= ' + lead_now_income_max + ' '
            # 希望年収
            if lead_hope_income_min and lead_hope_income_max:
                pSql += 'and crBase.wish_salary between ' + lead_hope_income_min + ' and ' + lead_hope_income_max + ' '
            elif lead_hope_income_min and not lead_hope_income_max:
                pSql += 'and crBase.wish_salary >= ' + lead_hope_income_min + ' '
            elif not lead_hope_income_min and lead_hope_income_max:
                pSql += 'and crBase.wish_salary <= ' + lead_hope_income_max + ' '

            # その他言語
            if lead_languages:
                pSql += 'and ( '
                pSql += 'other_langage_1_id in (' + lead_languages_text + ') '
                pSql += 'or other_langage_2_id in (' + lead_languages_text + ') '
                pSql += 'or other_langage_3_id in (' + lead_languages_text + ') '
                pSql += ' ) '
            # 資格
            if lead_skills:
                pSql += 'and crLicense.license_id in (\'' + lead_skills_text + '\') '

            pSql += '	group by '
            pSql += '		crMatch.trn_order_sk '
            pSql += ') crMatch on crMatch.trn_order_sk = orbase.trn_order_sk '
            pSql += ' WHERE clbase.lbc_cd in (\'' + LbcList_text + '\') '

            pSql += 'ORDER BY '
            pSql += ' CASE clbase.lbc_cd'

            pSql += temp
            pSql += (' END ) select distinct clBase.* '
                     '                from v_client clBase '
                     '                   LEFT JOIN pjm.trn_order_occupation orOccupSearch on orOccupSearch.trn_order_sk = clBase.order_trn_order_sk '
                     '                   LEFT JOIN pjm.trn_order_work_location orwklocationSearch on orwklocationSearch.trn_order_sk = clBase.order_trn_order_sk '
                     '                   LEFT JOIN pjm.trn_count_match_career_by_client crCntClMatch ON crCntClMatch.trn_client_sk = clbase.trn_client_sk '
                     '                where clBase.trn_client_sk is not null '
                     )

            # マッチング求職者がいない求人の除外　
            if exit_nomach == 'checked' or exit_nomach == True:
                pSql += 'and (crCntClMatch.match_count is not null or crCntClMatch.match_count > 0) '

            # 新着フラグ降順 20231004 新井追記
            pSql += 'ORDER BY '
            pSql += '   clBase.new_flg_order DESC '
            pSql += ' ;'

            params = []
            # params.append(LbcList)

            print('------------------------pSql--------------------------')
            for lbcCode in LbcList:
                params.append(lbcCode)

            # SQLを取得し、実行する
            cursor.execute(pSql, params)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]
            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            print('----------------------resultData---------------------------------------')

        # CP2担当者情報を取得する
        with connection.cursor() as cursor:
            cp2pSql = (
                ' SELECT clbase.lbc_cd "lbc_cd", clmatch.client_id "cp2_client_id", clcp2.charge_id "cp2_client_ra_user_id", muser.username "cp2_client_ra_user_name", clcp2.chargeteam_id "cp2_client_ra_team_id", mteam.teamname "cp2_client_ra_team_name" '
                ' FROM pjm.trn_client clbase  '
                ' LEFT JOIN pjm.trn_client_match clmatch on clmatch.lbc_cd = clbase.lbc_cd  '
                ' LEFT JOIN cp2.trnclient clcp2 on clmatch.client_id = clcp2.client_id  '
                ' LEFT JOIN cp2.mstuser muser on muser.userid = clcp2.charge_id  '
                ' LEFT JOIN cp2.mstteam mteam on mteam.teamid = clcp2.chargeteam_id  '
                ' WHERE clbase.lbc_cd = any(%s) '
                ' ORDER BY '
                ' CASE clbase.lbc_cd'
            )

            cp2pSql += temp
            cp2pSql += ' END '
            params = []
            params.append(LbcList)
            print('------------------------cp2pSql--------------------------')
            # print(cp2pSql)
            for lbcCode in LbcList:
                params.append(lbcCode)
            # SQLを取得し、実行する
            cursor.execute(cp2pSql, params)

            # カラム名を取得する
            cp2ReturtColumns = [col[0] for col in cursor.description]
            result = cursor.fetchall()

            cp2ResultData = [dict(zip(cp2ReturtColumns, row))for row in result]

        # 連絡履歴情報を取得する
        with connection.cursor() as cursor:
            contactpSql = (
                ' SELECT * '
                ' FROM ( SELECT (SELECT count(con_history.trn_client_contact_history_sk) FROM pjm.trn_client_contact_history con_history WHERE con_history.deleted_flg=0 AND con_history.lbc_cd = clcntcthist.lbc_cd) "contact_history_total_count", clcntcthist.lbc_cd "lbc_cd" ,clcntcthist.trn_client_contact_history_sk "contact_history_trn_client_contact_history_sk" ,clcntcthist.contact_date "contact_history_contact_date" ,section.section_name "contact_history_section_name" ,staff.search_full_name "contact_history_staff_name" ,mst_approach.name "contact_history_approach_name" ,clcntcthist.body "contact_history_body" ,clcntcthist.scheduled_date "contact_history_scheduled_date",ROW_NUMBER() OVER (PARTITION BY clcntcthist.lbc_cd ORDER BY clcntcthist.contact_date DESC  NULLS LAST ) AS rank FROM pjm.trn_client_contact_history clcntcthist LEFT JOIN pjm.mst_approach_status mst_approach ON mst_approach.id = clcntcthist.approach_id LEFT JOIN t_m_02_staff staff ON staff.staff_no = clcntcthist.staff_no LEFT JOIN t_m_01_section section ON section.section_cd = staff.section_cd WHERE clcntcthist.deleted_flg = 0 AND clcntcthist.lbc_cd = any(%s) ) tmp1'
                ' WHERE rank <= 2'
                ' ORDER BY lbc_cd DESC, contact_history_contact_date DESC NULLS LAST'
            )
            # SQLを取得し、実行する
            cursor.execute(contactpSql, [LbcList])
            # カラム名を取得する
            contactReturtColumns = [col[0] for col in cursor.description]
            result = cursor.fetchall()

            contactResultData = [dict(zip(contactReturtColumns, row))for row in result]

        # -------------------------結合作業開始

        resultData1 = resultData  # 企業求人
        resultData2 = cp2ResultData  # LBC－連絡履歴
        resultData3 = contactResultData  # LBC-CP2client

        data = []  # 最終的なデータ

        # カウント回り⇒dip_orderはdataの中
        page_num = 1
        page_count = totalCount // 10
        if totalCount % 10 != 0:
            page_count = page_count + 1

        # Lbcコード郡で回す
        for i, lbc_code in enumerate(LbcList):

            disp_order = i

            # まずは企業の配列を作成
            target_dicts = [target_data for target_data in resultData1 if target_data["lbc_cd"] == lbc_code]

            if len(target_dicts) == 0:  # 存在していなかったらスキップ
                continue

            target_dict = target_dicts[0]
            client_data = {
                "disp_order": disp_order,
                "trn_client_sk":                        target_dict["trn_client_sk"],
                "lbc_cd":                               target_dict["lbc_cd"],
                "client_name":                          target_dict["client_name"],
                "industry":                             target_dict["industry"],
                "address_full":                         target_dict["address_full"],
                "employee_number":                      target_dict["employee_number"],
                "foundation_ym":                        target_dict["foundation_ym"],
                "capital":                              target_dict["capital"],
                "amount_sales":                         target_dict["amount_sales"],
                "url":                                  target_dict["url"],
                "tel_lbc":                              target_dict["tel_lbc"],
                "tel_doda":                             target_dict["tel_doda"],
                "tel_custom":                           target_dict["tel_custom"],
                "alert_flg":                            target_dict["alert_flg"],
                "keep_disp_flg":                        target_dict["keep_disp_flg"],
                "keep_disp_staff_no":                   target_dict["keep_disp_staff_no"],
                "keep_disp_staff_name":                 target_dict["keep_disp_staff_name"],
                "keep_disp_section_name":               target_dict["keep_disp_section_name"],
                "keep_disp_date":                       target_dict["keep_disp_date"],
                "tel_custom_disp_update_info":          target_dict["tel_custom_disp_update_info"],
                "new_flg_client":                       target_dict["new_flg_client"],  # 20231004 新井追記
            }

            # 次に求人の配列作成
            order_data = []
            for order_dict in target_dicts:
                params = {
                    "order_trn_order_sk":               order_dict["order_trn_order_sk"],
                    "order_occupation_name":            order_dict["order_occupation_name"],
                    "order_work_location":              order_dict["order_work_location"],
                    "order_cp2_order_id":               order_dict["order_cp2_order_id"],
                    "order_annual_income_min":          order_dict["order_annual_income_min"],
                    "order_annual_income_max":          order_dict["order_annual_income_max"],
                    "order_match_01":                   order_dict["order_match_01"],
                    "order_match_02":                   order_dict["order_match_02"],
                    "order_match_03":                   order_dict["order_match_03"],
                    "order_media_id":                   order_dict["order_media_id"],
                    "order_career_count":               order_dict["match_count"],
                    "new_flg_order":                    order_dict["new_flg_order"],  # 20231004 新井追記
                }
                order_data.append(params)

            # 求人-企業合体
            client_data.setdefault("order", order_data)

            # 次にCP2企業
            cp2_client_data = []
            target_dicts2 = [target_data for target_data in resultData2 if target_data["lbc_cd"] == lbc_code]
            for cp2_client_dict in target_dicts2:
                params = {
                    "cp2_client_id":                cp2_client_dict["cp2_client_id"],
                    "cp2_client_ra_user_name":      cp2_client_dict["cp2_client_ra_user_name"],
                    "cp2_client_ra_team_name":      cp2_client_dict["cp2_client_ra_team_name"],
                }
                cp2_client_data.append(params)

            cp2_client_ids = [cp2_client_record["cp2_client_id"] for cp2_client_record in cp2_client_data]
            cp2_client_ra_names = [cp2_client_record["cp2_client_ra_user_name"]
                                   for cp2_client_record in cp2_client_data if cp2_client_record["cp2_client_ra_user_name"] is not None]
            cp2_client_ra_teams = [cp2_client_record["cp2_client_ra_team_name"]
                                   for cp2_client_record in cp2_client_data if cp2_client_record["cp2_client_ra_team_name"] is not None]

            cp2_client_ras = []

            for ra_name, ra_team in zip(cp2_client_ra_names, cp2_client_ra_teams):
                context = ra_name + "(" + ra_team + ")"
                cp2_client_ras.append(context)

            if len(cp2_client_ids) > 0:
                cp2_client_id = ",".join(map(str, cp2_client_ids))
                cp2_client_ra = ",".join(cp2_client_ras)
            else:
                cp2_client_id = ""
                cp2_client_ra = ""

            # CP2企業-企業合体
            client_data.setdefault("cp2_client", cp2_client_data)
            client_data.setdefault("cp2_client_id", cp2_client_id)
            client_data.setdefault("cp2_client_ra", cp2_client_ra)

            # 次に連絡履歴
            contact_histry_data = []
            target_dicts3 = [target_data for target_data in resultData3 if target_data["lbc_cd"] == lbc_code]

            # 先にトータルだけ宣言しておく
            contact_history_total_count = 0

            for contact_dict in target_dicts3:
                contact_history_total_count = contact_dict["contact_history_total_count"]
                contact_history_page_num = 1
                contact_history_page_count = contact_history_total_count // 2
                if contact_history_total_count % 2 != 0:
                    contact_history_page_count = contact_history_page_count + 1
                params = {
                    "contact_history_total_count": contact_history_total_count,
                    "contact_history_page_num": contact_history_page_num,
                    "contact_history_page_count": contact_history_page_count,
                    "contact_history_trn_client_contact_history_sk":    contact_dict["contact_history_trn_client_contact_history_sk"],
                    "contact_history_contact_date":                     contact_dict["contact_history_contact_date"],
                    "contact_history_section_name":                     contact_dict["contact_history_section_name"],
                    "contact_history_staff_name":                       contact_dict["contact_history_staff_name"],
                    "contact_history_approach_name":                    contact_dict["contact_history_approach_name"],
                    "contact_history_body":                             contact_dict["contact_history_body"],
                    "contact_history_body_tippy":                       '',
                    "contact_history_scheduled_date":                   contact_dict["contact_history_scheduled_date"],

                }
                contact_histry_data.append(params)

            client_data.setdefault("contact_history_total_count", contact_history_total_count)

            # 連絡履歴-企業合体
            client_data.setdefault("contact_histry", contact_histry_data)

            # 最終的にすべて結合
            data.append(client_data)

        # -------------------------結合作業ここまで

            # ヘッダー作成
        response_header: dict = {
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'total_count': totalCount,
            'page_num': 1,
            'page_count': 1,
            'login_staff_no': staff_no,
            'login_staff_name': staff_name,
            'login_staff_section': staff_section,
            'LbcList': LbcList,
            'results': data,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


# 連絡履歴取得、保存API
class ContactHistoryAPIView(generics.ListCreateAPIView):
    queryset = TrnClientContactHistory.objects.all()
    serializer_class = TrnClientContactHistorySerializer

    def get(self, Request):
        with connection.cursor() as cursor:

            pageNum = self.request.query_params.get('page_num', None)
            lbcCd = self.request.query_params.get('LbcCd', None)
            pSql = (
                'WITH A AS (SELECT clhist.lbc_cd ,clhist.contact_date "contact_history_contact_date" ,tmsection.section_name "contact_history_section_name" ,staff.search_full_name "contact_history_staff_name" ,mAppStatus.name "contact_history_approach_name" ,clhist.body "contact_history_body" ,clhist.scheduled_date "contact_history_scheduled_date" ,clhist.audit_created_at "audit_created_at" '
                'FROM pjm.trn_client_contact_history clhist '
                'LEFT JOIN pjm.mst_approach_status mAppStatus on mAppStatus.id = clhist.approach_id '
                'LEFT JOIN public.t_m_02_staff staff on staff.staff_no = clhist.staff_no '
                'LEFT JOIN public.t_m_01_section tmsection on tmsection.section_cd = staff.section_cd '
                "WHERE clhist.lbc_cd = '" + lbcCd + "' "
                'ORDER BY contact_date DESC NULLS LAST, audit_created_at DESC) '
                'SELECT (SELECT count(*) FROM A) "total_count" ,* '
                'FROM A '
            )

            pSql = pSql + 'limit 2 offset ' + str((int(pageNum) - 1) * 2)

            cursor.execute(pSql)
            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]
            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

        # ヘッダー作成
        response_header: dict = {
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'page_num': pageNum,
            'page_num': resultData[0]["total_count"],
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

    def create(self, request):
        if not 'data_obj' in request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )
        # 継承元クラスのcreateメソッドがvalidationなどの処理を一括で実行する
        now = datetime.datetime.now() + datetime.timedelta(hours=9)  # 9時間問題

        user_stuff_id = request.session['data_obj']['user_records']['mits_username']

        staff_no = request.session['data_obj']['user_records']['staff_no']
        approach_id = self.request.query_params.get('approach_id', None)
        lbc_cd = self.request.query_params.get('lbc_cd', None)
        delete_flg = 0
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        data = request.data
        data['audit_created_at'] = now
        data['audit_updated_at'] = now
        data['deleted_flg'] = delete_flg
        data['audit_created_by'] = user_stuff_id
        data['audit_updated_by'] = user_stuff_id
        data['staff_no'] = staff_no
        data['lbc_cd'] = lbc_cd
        data['body'] = self.request.query_params.get('approach_comment', None)
        data['approach_id'] = approach_id

        # アプローチ日付調整
        approach_date_str = self.request.query_params.get('approach_date', None)
        approach_date_date = datetime.datetime.strptime(approach_date_str, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)  # 9時間問題
        approach_date = approach_date_date.strftime("%Y-%m-%d %H:%M:%S")
        data['contact_date'] = approach_date

        data['regist_type'] = 0  # 標準固定

        if self.request.query_params.get('appoint_date', None):
            scheduled_date_str = self.request.query_params.get('appoint_date', None)
            scheduled_date_date = datetime.datetime.strptime(scheduled_date_str, '%Y-%m-%d %H:%M:%S') + datetime.timedelta(hours=9)  # 9時間問題
            scheduled_date = scheduled_date_date.strftime("%Y-%m-%d %H:%M:%S")
            data['scheduled_date'] = scheduled_date

        # 継承元クラスのcreateメソッドがvalidationなどの処理を一括で実行する

        # シリアライザオブジュエクトを作成
        serializer = TrnClientContactHistorySerializer(data=data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()

        with connection.cursor() as cursor:
            pSql = (
                'UPDATE pjm.trn_client '
                'SET latest_contact_staff_no = %s '
                ',latest_contact_date = %s '
                ',latest_contact_approach_id = %s '
                ',latest_contact_audit_created_at = %s '
                'WHERE lbc_cd = %s '
            )

            cursor.execute(pSql, [staff_no, approach_date_str, approach_id, now, lbc_cd])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# マッチング求職者取得API
class MatchCareerAPIView(APIView):
    def get(self, Request):
        # ここから求職者マッチング情報----------------------
        lead_active = self.request.query_params.get("lead_active", None)
        lead_status = self.request.query_params.getlist("lead_status[]", None)
        lead_status_text = ','.join(lead_status)

        lead_age_from = self.request.query_params.get("lead_age_from", None)
        lead_age_to = self.request.query_params.get("lead_age_to", None)
        lead_gender = self.request.query_params.getlist("lead_gender[]", None)
        lead_gender_text = ','.join(lead_gender)

        lead_occupation = self.request.query_params.getlist("lead_occupation[]", None)
        lead_occupation_text = '\',\''.join(lead_occupation)

        lead_prefs = self.request.query_params.getlist("lead_prefs[]", None)
        lead_prefs_tmp = ','.join(lead_prefs)
        lead_prefs_text = lead_prefs_tmp.replace(',', '\',\'')

        lead_last_school = self.request.query_params.getlist("lead_last_school[]", None)
        lead_last_school_text = ','.join(lead_last_school)

        lead_english_level = self.request.query_params.getlist("lead_english_level[]", None)
        lead_english_level_text = ','.join(lead_english_level)

        lead_now_income_min = self.request.query_params.get("lead_now_income_min", 0)
        lead_now_income_max = self.request.query_params.get("lead_now_income_max", 0)
        lead_hope_income_min = self.request.query_params.get("lead_hope_income_min", 0)
        lead_hope_income_max = self.request.query_params.get("lead_hope_income_max", 0)
        lead_company_history_min = self.request.query_params.get("lead_company_history_min", None)
        lead_company_history_max = self.request.query_params.get("lead_company_history_max", None)
        lead_languages = self.request.query_params.getlist("lead_languages[]", None)
        lead_languages_text = ','.join(lead_languages)

        lead_skills = self.request.query_params.getlist("lead_skills[]", None)
        lead_skills_text = '\',\''.join(lead_skills)

        with connection.cursor() as cursor:
            orderSk = self.request.query_params.get('trn_order_sk', None)
            orderSk = int(orderSk)
            pSql = (
                'SELECT '
                'distinct '
                'crBase.career_id "career_id"  '
                ',date_part(\'year\',age(current_date,crBase.birthday)) "age"  '
                ',CASE  '
                '  WHEN crBase.gender_id = 1 THEN \'男性\'  '
                '  WHEN crBase.gender_id = 2 THEN \'女性\'  '
                '  ELSE \'-\' END "gender_name" '
                ',CASE '
                '  WHEN moccupation03.name is null THEN \'-\' '
                '  ELSE moccupation03.name END "occupation_name"  '
                ',CASE '
                '  WHEN mPref.name is null THEN \'-\' '
                '  ELSE mPref.name END "pref_name"  '
                'FROM '
                'pjm.trn_career_match crmatch '
                'LEFT JOIN '
                'pjm.trn_career crBase ON crmatch.career_id = crbase.career_id '
                'LEFT JOIN pjm.mst_pref mPref on mPref.id = crBase.pref_id  '
                'LEFT JOIN pjm.mst_occupation_03 moccupation03 on moccupation03.id = crBase.exp_occupation_1_id  '
                'LEFT JOIN pjm.trn_career_license crLicense on crLicense.career_id = crBase.career_id '
                'LEFT JOIN pjm.trn_career_wish_occupation crWishOccup on crWishOccup.career_id = crBase.career_id '
                'left join pjm.trn_career_wish_work_pref crWishWorkPref on crWishWorkPref.career_id = crBase.career_id '
                # 'LEFT JOIN ('
                # '        select '
                # '            career_id '
                # '            ,regexp_split_to_table(crbase.wishwkarea_id,\'/\') wishwkarea_id '
                # '        from '
                # '            cp2.trncareer crbase '
                # ') crbasepref on crbasepref.career_id = crBase.career_id '
                'WHERE '
                'crmatch.trn_order_sk = %s '
            )
            # 有効/非有効
            if lead_active:
                pSql += 'and crBase.valid_flg = (' + lead_active + ') '

            # 求職者ステータス
            if lead_status:
                pSql += 'and crBase.career_status in (' + lead_status_text + ') '
            # 年齢
            if lead_age_from:
                pSql += 'and Date_Part(\'year\',age(crBase.birthday)) >= ' + lead_age_from + ' '
            if lead_age_to:
                pSql += 'and Date_Part(\'year\',age(crBase.birthday)) <= ' + lead_age_to + ' '

            # 性別
            if lead_gender:
                pSql += 'and crBase.gender_id in (' + lead_gender_text + ') '
            # 希望職種 ★ここ直してほしい
            if lead_occupation:
                pSql += 'and crWishOccup.occupation_id in (\'' + lead_occupation_text + '\') '
            # 希望勤務地
            if lead_prefs:
                pSql += 'and crWishWorkPref.pref_id in (\'' + lead_prefs_text + '\') '
            # 最終学歴
            if lead_last_school:
                pSql += 'and crBase.last_school_id in (' + lead_last_school_text + ') '
            # 経験社数
            if lead_company_history_min:
                pSql += 'and crBase.exp_company_num >= ' + lead_company_history_min + ' '
            if lead_company_history_max:
                pSql += 'and crBase.exp_company_num <= ' + lead_company_history_max + ' '
            # 英語レベル
            if lead_english_level:
                pSql += 'and crBase.english_level_id in (' + lead_english_level_text + ') '

            # 現在年収
            if lead_now_income_min and lead_now_income_max:
                pSql += 'and crBase.current_salary between ' + lead_now_income_min + ' and ' + lead_now_income_max + ' '
            elif lead_now_income_min and not lead_now_income_max:
                pSql += 'and crBase.current_salary >= ' + lead_now_income_min + ' '
            elif not lead_now_income_min and lead_now_income_max:
                pSql += 'and crBase.current_salary <= ' + lead_now_income_max + ' '
            # 希望年収
            if lead_hope_income_min and lead_hope_income_max:
                pSql += 'and crBase.wish_salary between ' + lead_hope_income_min + ' and ' + lead_hope_income_max + ' '
            elif lead_hope_income_min and not lead_hope_income_max:
                pSql += 'and crBase.wish_salary >= ' + lead_hope_income_min + ' '
            elif not lead_hope_income_min and lead_hope_income_max:
                pSql += 'and crBase.wish_salary <= ' + lead_hope_income_max + ' '

            # その他言語
            if lead_languages:
                pSql += 'and ( '
                pSql += 'crBase.other_langage_1_id in (' + lead_languages_text + ') '
                pSql += 'or crBase.other_langage_2_id in (' + lead_languages_text + ') '
                pSql += 'or crBase.other_langage_3_id in (' + lead_languages_text + ') '
                pSql += ' ) '
            # 資格
            if lead_skills:
                pSql += 'and crLicense.license_id in (\'' + lead_skills_text + '\') '

            pSql += 'ORDER BY '
            pSql += 'career_id DESC '
            cursor.execute(pSql, [orderSk])

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

# カスタム電話番号取得、保存API


class CustomTelAPIView(generics.ListCreateAPIView):
    queryset = TrnClientCustomTel.objects.all()
    serializer_class = TrnClientCustomTelSerializer

    def get(self, Request):
        with connection.cursor() as cursor:
            lbcCd = self.request.query_params.get('lbc_cd', None)
            pSql = (
                'SELECT  clcustomtel.trn_client_custom_tel_sk "trn_client_custom_tel_sk", clcustomtel.lbc_cd "lbc_cd", clcustomtel.tel "tel", staff.search_full_name "staff_name", tmsection.section_name "section_name", clcustomtel.audit_created_at "audit_created_at" '
                'FROM pjm.trn_client_custom_tel clcustomtel '
                'LEFT JOIN public.t_m_02_staff staff on staff.staff_no = clcustomtel.staff_no '
                'LEFT JOIN public.t_m_01_section tmsection on tmsection.section_cd = staff.section_cd '
                "WHERE clcustomtel.lbc_cd = '" + lbcCd + "' "
                'ORDER BY audit_created_at DESC '
            )
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

        params = []

        # 整形作業
        for resultrecord in resultData:
            disp_update_info = ""

            disp_update_info_date = datetime.datetime.strptime(str(resultrecord["audit_created_at"]), '%Y-%m-%d %H:%M:%S')
            disp_update_info_date = disp_update_info_date.strftime("%Y/%m/%d %H:%M")
            disp_update_info = str(resultrecord["tel"]) + "(" + str(disp_update_info_date) + " " + \
                resultrecord["section_name"] + " " + resultrecord["staff_name"] + ")"
            disp_update_disp = str(disp_update_info_date) + " " + resultrecord["section_name"] + " " + resultrecord["staff_name"]
            tel_data = {
                "trn_client_custom_tel_sk": resultrecord["trn_client_custom_tel_sk"],
                "lbc_cd": resultrecord["lbc_cd"],
                "tel": resultrecord["tel"],
                "staff_name": resultrecord["staff_name"],
                "section_name": resultrecord["section_name"],
                "audit_created_at": resultrecord["audit_created_at"],
                "disp_update_info": disp_update_info,
                "disp_update_disp": disp_update_disp
            }

            params.append(tel_data)

        # ヘッダー作成
        response_header: dict = {
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': params,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

    def create(self, request):
        if not 'data_obj' in request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )
        # 継承元クラスのcreateメソッドがvalidationなどの処理を一括で実行する
        now = datetime.datetime.now() + datetime.timedelta(hours=9)  # 9時間問題

        user_stuff_id = request.session['data_obj']['user_records']['mits_username']
        staff_no = request.session['data_obj']['user_records']['staff_no']

        delete_flg = 0
        now = now.strftime("%Y-%m-%d %H:%M:%S")

        data = request.data
        data['audit_created_at'] = now
        data['audit_updated_at'] = now
        data['deleted_flg'] = delete_flg
        data['audit_created_by'] = user_stuff_id
        data['audit_updated_by'] = user_stuff_id
        data['staff_no'] = staff_no
        data['lbc_cd'] = self.request.query_params.get('lbc_cd', None)
        data['tel'] = self.request.query_params.get('tel', None)
        # シリアライザオブジュエクトを作成
        serializer = TrnClientCustomTelSerializer(data=data)
        # バリデーション
        serializer.is_valid(raise_exception=True)
        # モデルオブジェクトを登録
        serializer.save()

        telSk = serializer.data['trn_client_custom_tel_sk']
        with connection.cursor() as cursor:
            lbcCd = self.request.query_params.get('lbc_cd', None)
            pSql = (
                'UPDATE pjm.trn_client '
                'SET latest_custom_tel_sk = %s '
                ',audit_updated_at = %s '
                ',audit_updated_by = %s '
                'WHERE lbc_cd = %s '
            )
            cursor.execute(pSql, [telSk, now, user_stuff_id, lbcCd])

        return Response(serializer.data, status=status.HTTP_201_CREATED)


# キープ取得、保存API
class KeepClientAPIView(generics.ListCreateAPIView):
    queryset = TrnClient.objects.all()
    serializer_class = TrnClientSerializer

    def get(self, Request):
        with connection.cursor() as cursor:
            lbcCd = self.request.query_params.getlist("lbc_cd[]", None)
            lbc_code_text = '\',\''.join(lbcCd)

            pSql = (
                'SELECT clBase.lbc_cd "lbc_cd" ,clBase.keep_updated_at "keep_date" ,staff.search_full_name  "staff_name" ,tmsection.section_name "section_name" ,tmsection.section_cd "section_cd" ,clBase.keep_updated_staff_no "staff_no" ,clBase.keep_flg "keep_flg" '
                'FROM pjm.trn_client clBase '
                'LEFT JOIN public.t_m_02_staff staff on staff.staff_no = clBase.keep_updated_staff_no '
                'LEFT JOIN public.t_m_01_section tmsection on tmsection.section_cd = staff.section_cd  '
                'WHERE clBase.lbc_cd in ( \'' + lbc_code_text + '\' )'
            )
            cursor.execute(pSql)

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )

    def put(self, request):
        keep_flg = self.request.query_params.get('update_keep_flg', None)
        if not 'data_obj' in request.session:
            return JsonResponse(
                status=status.HTTP_401_UNAUTHORIZED,
                headers='',
                data='',
                safe=False,
                json_dumps_params={'ensure_ascii': False}
            )

        if keep_flg == '1':
            maxKeepCount = settings.MAX_KEEP_VALUE
            with connection.cursor() as cursor:
                staffNo = request.session['data_obj']['user_records']['staff_no']
                pSql = (
                    'SELECT COUNT(clBase.lbc_cd) keep_count '
                    'FROM pjm.trn_client clBase '
                    'WHERE clBase.keep_updated_staff_no =  ' + str(staffNo) + ' '
                    'and clBase.keep_flg = 1 '
                    'and clBase.deleted_flg = 0'
                )
                cursor.execute(pSql)

                returtColumns = [col[0] for col in cursor.description]

                result = cursor.fetchall()

                resultData = [dict(zip(returtColumns, row))for row in result]

                keepCount = resultData[0]['keep_count']

            if resultData[0]['keep_count'] >= maxKeepCount:
                response_header: dict = {
                    'HTTP-response-code': status.HTTP_200_OK
                }
                # ボディ作成
                response_data: dict = {
                    'keep_flg': 0,
                    'keep_updated_staff_no': None,
                    'keep_updated_at': None,
                    'audit_updated_at': None,
                    'audit_updated_by': None,
                    'max_keep_count': maxKeepCount,
                    'error_code': 'keep_limit_over'
                }
                return JsonResponse(
                    status=status.HTTP_200_OK,
                    headers=response_header,
                    data=response_data,
                    safe=False,
                    json_dumps_params={'ensure_ascii': False}
                )

        with connection.cursor() as cursor:
            keep_flg = self.request.query_params.get('update_keep_flg', None)
            staffNo = request.session['data_obj']['user_records']['staff_no']
            staffid = request.session['data_obj']['user_records']['mits_username']
            lbcCd = self.request.query_params.get('lbc_cd', None)
            now = datetime.datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")

            pSql = (
                'UPDATE pjm.trn_client '
                'SET keep_flg = %s '
                ',keep_updated_staff_no = %s '
                ',keep_updated_at = %s '
                ',audit_updated_at = %s '
                ',audit_updated_by = %s '
                'WHERE lbc_cd = %s '
            )
            cursor.execute(pSql, [keep_flg, staffNo, now, now, staffid, lbcCd])

        response_header: dict = {
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'keep_flg': keep_flg,
            'keep_updated_staff_no': staffNo,
            'keep_updated_at': now,
            'audit_updated_at': now,
            'audit_updated_by': staffNo,

        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )


# 求職者情報取得API
class GetCareerAPIView(APIView):
    queryset = TrnClient.objects.all()
    serializer_class = TrnClientSerializer

    def get(self, Request):
        with connection.cursor() as cursor:
            crId = self.request.query_params.get('trn_career_sk', None)
            pSql = (
                'select '
                'crBase.career_id "career_id" '
                ',concat(crReg.regstatusname||\'/\',date_part(\'year\',age(current_date,crBase.birth_date)),\'歳\'||\'/\',crSex.sexname) "career_data" '
                ',crlstschl.lstschlname "lstschlname" '
                ',crBase.expcomp_num "expcomp_num" '
                ',concat(mstindsctg_1.indsctgname, chr(10)||mstindsctg_2.indsctgname, chr(10)||mstindsctg_3.indsctgname, chr(10)||mstindsctg_4.indsctgname, chr(10)||mstindsctg_5.indsctgname) "exp_industry" '
                ',concat(mstocup3class_1.ocup3classname, chr(10)||mstocup3class_2.ocup3classname, chr(10)||mstocup3class_3.ocup3classname, chr(10)||mstocup3class_4.ocup3classname, chr(10)||mstocup3class_5.ocup3classname) "exp_occupation" '
                ',concat(wishmstindsctg_1.indsctgname, \'/\'||wishmstindsctg_2.indsctgname,\'/\'||wishmstindsctg_3.indsctgname,\'/\'||wishmstindsctg_4.indsctgname, \'/\'||wishmstindsctg_5.indsctgname) "wish_industry"  '
                ',concat(wishmstocup3class_1.ocup3classname,\'/\'||wishmstocup3class_2.ocup3classname,\'/\'||wishmstocup3class_3.ocup3classname,\'/\'||wishmstocup3class_4.ocup3classname,\'/\'||wishmstocup3class_5.ocup3classname) "wish_occupation" '
                ',crbasepref.wishwkareaname                                        "wish_wkpref" '
                ',crBase.wishsalary_num "wishannualincm_num" '
                ',max(case when crbusicr.busicr_id = 1 and (crbusicr.wkperiods_date is not null or crbusicr.wkperiode_date is not null) then concat(to_char(crbusicr.wkperiods_date, \'yyyy/mm\'),\'~\',to_char(crbusicr.wkperiode_date, \'yyyy/mm\')) end)"wkperiode_date1" '
                ',max(case when crbusicr.busicr_id = 1 then crbusicr.compname end) "compname1" '
                ',max(case when busicr_id = 1 then crbusicr.dept end) "dept1" '
                ',max(case when busicr_id = 1 then indsbusicr.indsctgname end) "indsctgname1" '
                ',max(case when busicr_id = 1 then crbusicr.annualincm end) "annualincm1" '
                ',max(case when busicr_id = 1 then crbusicr.wkcontents end) "wkcontents1" '
                ',max(case when crbusicr.busicr_id = 2 and (crbusicr.wkperiods_date is not null or crbusicr.wkperiode_date is not null) then concat(to_char(crbusicr.wkperiods_date, \'yyyy/mm\'),\'~\',to_char(crbusicr.wkperiode_date, \'yyyy/mm\')) end)"wkperiode_date2" '
                ',max(case when crbusicr.busicr_id = 2 then crbusicr.compname end) "compname2" '
                ',max(case when busicr_id = 2 then crbusicr.dept end) "dept2" '
                ',max(case when busicr_id = 2 then indsbusicr.indsctgname end) "indsctgname2" '
                ',max(case when busicr_id = 2 then crbusicr.annualincm end) "annualincm2" '
                ',max(case when busicr_id = 2 then crbusicr.wkcontents end) "wkcontents2" '
                ',max(case when crbusicr.busicr_id = 3 and (crbusicr.wkperiods_date is not null or crbusicr.wkperiode_date is not null) then concat(to_char(crbusicr.wkperiods_date, \'yyyy/mm\'),\'~\',to_char(crbusicr.wkperiode_date, \'yyyy/mm\')) end)"wkperiode_date3" '
                ',max(case when crbusicr.busicr_id = 3 then crbusicr.compname end) "compname3" '
                ',max(case when busicr_id = 3 then crbusicr.dept end) "dept3" '
                ',max(case when busicr_id = 3 then indsbusicr.indsctgname end) "indsctgname3" '
                ',max(case when busicr_id = 3 then crbusicr.annualincm end) "annualincm3" '
                ',max(case when busicr_id = 3 then crbusicr.wkcontents end) "wkcontents3" '
                ',max(case when crbusicr.busicr_id = 4 and (crbusicr.wkperiods_date is not null or crbusicr.wkperiode_date is not null) then concat(to_char(crbusicr.wkperiods_date, \'yyyy/mm\'),\'~\',to_char(crbusicr.wkperiode_date, \'yyyy/mm\')) end)"wkperiode_date4" '
                ',max(case when crbusicr.busicr_id = 4 then crbusicr.compname end) "compname4" '
                ',max(case when busicr_id = 4 then crbusicr.dept end) "dept4" '
                ',max(case when busicr_id = 4 then indsbusicr.indsctgname end) "indsctgname4" '
                ',max(case when busicr_id = 4 then crbusicr.annualincm end) "annualincm4" '
                ',max(case when busicr_id = 4 then crbusicr.wkcontents end) "wkcontents4" '
                ',max(case when crbusicr.busicr_id = 5 and (crbusicr.wkperiods_date is not null or crbusicr.wkperiode_date is not null) then concat(to_char(crbusicr.wkperiods_date, \'yyyy/mm\'),\'~\',to_char(crbusicr.wkperiode_date, \'yyyy/mm\')) end)"wkperiode_date5" '
                ',max(case when crbusicr.busicr_id = 5 then crbusicr.compname end) "compname5" '
                ',max(case when busicr_id = 5 then crbusicr.dept end) "dept5" '
                ',max(case when busicr_id = 5 then indsbusicr.indsctgname end) "indsctgname5" '
                ',max(case when busicr_id = 5 then crbusicr.annualincm end) "annualincm5" '
                ',max(case when busicr_id = 5 then crbusicr.wkcontents end) "wkcontents5" '
                ',max(case when crSchcl.schlcr_id = 1 then concat(crSchcl.entranceyr,\'/\'||crSchcl.entrancemon,\'~\'||crSchcl.gradyr,\'/\'||crSchcl.gradmon) end) "Schcperiode_date1" '
                ',max(case when crSchcl.schlcr_id = 1 then crGrad.gradname end) "gradname1" '
                ',max(case when crSchcl.schlcr_id = 1 then crSchcl.schlname end) "schlname1" '
                ',max(case when crSchcl.schlcr_id = 1 then crSchcl.schldeptname end) "schldeptname1" '
                ',max(case when crSchcl.schlcr_id = 2 then concat(crSchcl.entranceyr,\'/\'||crSchcl.entrancemon,\'~\'||crSchcl.gradyr,\'/\'||crSchcl.gradmon) end) "Schcperiode_date2" '
                ',max(case when crSchcl.schlcr_id = 2 then crGrad.gradname end) "gradname2" '
                ',max(case when crSchcl.schlcr_id = 2 then crSchcl.schlname end) "schlname2" '
                ',max(case when crSchcl.schlcr_id = 2 then crSchcl.schldeptname end) "schldeptname2" '
                ',max(case when crSchcl.schlcr_id = 3 then concat(crSchcl.entranceyr,\'/\'||crSchcl.entrancemon,\'~\'||crSchcl.gradyr,\'/\'||crSchcl.gradmon) end) "Schcperiode_date3" '
                ',max(case when crSchcl.schlcr_id = 3 then crGrad.gradname end) "gradname3" '
                ',max(case when crSchcl.schlcr_id = 3 then crSchcl.schlname end) "schlname3" '
                ',max(case when crSchcl.schlcr_id = 3 then crSchcl.schldeptname end) "schldeptname3" '
                ',max(case when crSchcl.schlcr_id = 4 then concat(crSchcl.entranceyr,\'/\'||crSchcl.entrancemon,\'~\'||crSchcl.gradyr,\'/\'||crSchcl.gradmon) end) "Schcperiode_date4" '
                ',max(case when crSchcl.schlcr_id = 4 then crGrad.gradname end ) "gradname4" '
                ',max(case when crSchcl.schlcr_id = 4 then crSchcl.schlname end ) "schlname4" '
                ',max(case when crSchcl.schlcr_id = 4 then crSchcl.schldeptname end ) "schldeptname4" '
                ',max(case when crSchcl.schlcr_id = 5 then concat(crSchcl.entranceyr,\'/\'||crSchcl.entrancemon,\'~\'||crSchcl.gradyr,\'/\'||crSchcl.gradmon) end) "Schcperiode_date5" '
                ',max(case when crSchcl.schlcr_id = 5 then crGrad.gradname end ) "gradname5" '
                ',max(case when crSchcl.schlcr_id = 5 then crSchcl.schlname end ) "schlname5" '
                ',max(case when crSchcl.schlcr_id = 5 then crSchcl.schldeptname end ) "schldeptname5" '
                ',crLicense1.licensename "licensename1" '
                ',concat(crQual1.qualyr,\'/\'||crQual1.qualmon) "qual_date1" '
                ',crLicense2.licensename "licensename2" '
                ',concat(crQual2.qualyr,\'/\'||crQual2.qualmon) "qual_date2" '
                ',crLicense3.licensename "licensename3" '
                ',concat(crQual3.qualyr,\'/\'||crQual3.qualmon) "qual_date3" '
                ',crLicense4.licensename "licensename4" '
                ',concat(crQual4.qualyr,\'/\'||crQual4.qualmon) "qual_date4" '
                ',crLicense5.licensename "licensename5" '
                ',concat(crQual5.qualyr,\'/\'||crQual5.qualmon) "qual_date5" '
                ',concat(crLang.toeicy||\'/\',crLang.toeicm||\'取得\',crLang.toeic||\'点\') "toeic" '
                ',concat(crLang.toefly||\'/\',crLang.toeflm||\'取得\',crLang.toefl||\'点\') "toefl" '
                ',englishLanguagelevel.languagelevelname "english_level" '
                ',case when mstlang1.otrlangname is not null then concat(mstlang1.otrlangname,\':\'||languagelevel1.languagelevelname) end "otrlang1" '
                ',case when mstlang2.otrlangname is not null then concat(mstlang2.otrlangname,\':\'||languagelevel2.languagelevelname) end "otrlang2" '
                ',case when mstlang3.otrlangname is not null then concat(mstlang3.otrlangname,\':\'||languagelevel3.languagelevelname) end "otrlang3" '
                'from '
                'cp2.trncareer crBase '
                'left join cp2.mstsex crSex on crSex.sexid = crBase.sex_flg '
                'left join cp2.mstregstatus crReg on crReg.regstatusid = crBase.regstatus_id '
                'left join cp2.mstlstschl crlstschl on crlstschl.lstschlid = crBase.lstschl_id '
                'left join cp2.mstindsctg mstindsctg_1 on mstindsctg_1.indsctgid = crBase.expindsctg1_id '
                'left join cp2.mstindsctg mstindsctg_2 on mstindsctg_2.indsctgid = crBase.expindsctg2_id '
                'left join cp2.mstindsctg mstindsctg_3 on mstindsctg_3.indsctgid = crBase.expindsctg3_id '
                'left join cp2.mstindsctg mstindsctg_4 on mstindsctg_4.indsctgid = crBase.expindsctg4_id '
                'left join cp2.mstindsctg mstindsctg_5 on mstindsctg_5.indsctgid = crBase.expindsctg5_id '
                'left join cp2.mstocup3class mstocup3class_1 on mstocup3class_1.ocupctgid = crBase.expocupctg1_id '
                'left join cp2.mstocup3class mstocup3class_2 on mstocup3class_2.ocupctgid = crBase.expocupctg2_id '
                'left join cp2.mstocup3class mstocup3class_3 on mstocup3class_3.ocupctgid = crBase.expocupctg3_id '
                'left join cp2.mstocup3class mstocup3class_4 on mstocup3class_4.ocupctgid = crBase.expocupctg4_id '
                'left join cp2.mstocup3class mstocup3class_5 on mstocup3class_5.ocupctgid = crBase.expocupctg5_id '
                'left join cp2.mstindsctg wishmstindsctg_1 on wishmstindsctg_1.indsctgid = crBase.wishindsctg1_id '
                'left join cp2.mstindsctg wishmstindsctg_2 on wishmstindsctg_2.indsctgid = crBase.wishindsctg2_id '
                'left join cp2.mstindsctg wishmstindsctg_3 on wishmstindsctg_3.indsctgid = crBase.wishindsctg3_id '
                'left join cp2.mstindsctg wishmstindsctg_4 on wishmstindsctg_4.indsctgid = crBase.wishindsctg4_id '
                'left join cp2.mstindsctg wishmstindsctg_5 on wishmstindsctg_5.indsctgid = crBase.wishindsctg5_id '
                'left join cp2.mstocup3class wishmstocup3class_1 on wishmstocup3class_1.ocupctgid = crBase.wishocupctg1_id '
                'left join cp2.mstocup3class wishmstocup3class_2 on wishmstocup3class_2.ocupctgid = crBase.wishocupctg2_id '
                'left join cp2.mstocup3class wishmstocup3class_3 on wishmstocup3class_3.ocupctgid = crBase.wishocupctg3_id '
                'left join cp2.mstocup3class wishmstocup3class_4 on wishmstocup3class_4.ocupctgid = crBase.wishocupctg4_id '
                'left join cp2.mstocup3class wishmstocup3class_5 on wishmstocup3class_5.ocupctgid = crBase.wishocupctg5_id '
                'left join '
                '    ( '
                '    select '
                '        crbasepref.career_id '
                '        ,string_agg(mpref.prefname ,\'/\') wishwkareaname '
                '    from '
                '        ( '
                '        select '
                '            career_id '
                '            ,regexp_split_to_table(crbase.wishwkarea_id,\'/\') wishwkarea_id '
                '        from '
                '            cp2.trncareer crbase '
                '        ) crbasepref '
                '    left join cp2.mstpref mpref on crbasepref.wishwkarea_id = cast(mpref.prefid as text) '
                '    group by '
                '        crbasepref.career_id '
                '    )crbasepref on crbasepref.career_id = crBase.career_id '
                'left join cp2.trnbusicr crBusicr on crBusicr.career_id = crBase.career_id '
                'left join cp2.mstindsctg indsbusicr on indsbusicr.indsctgid = crBusicr.indsctg_id '
                'left join cp2.trnschlcr crSchcl on crSchcl.career_id = crBase.career_id '
                'left join cp2.mstgrad crGrad on crGrad.gradid = crSchcl.grad_flg '
                'left join cp2.trnqual crQual1 on crQual1.career_id = crBase.career_id and crQual1.ql_id = 1 '
                'left join cp2.trnqual crQual2 on crQual2.career_id = crBase.career_id and crQual2.ql_id = 2 '
                'left join cp2.trnqual crQual3 on crQual3.career_id = crBase.career_id and crQual3.ql_id = 3 '
                'left join cp2.trnqual crQual4 on crQual4.career_id = crBase.career_id and crQual4.ql_id = 4 '
                'left join cp2.trnqual crQual5 on crQual5.career_id = crBase.career_id and crQual5.ql_id = 5 '
                'left join cp2.trnqual crQual6 on crQual6.career_id = crBase.career_id and crQual6.ql_id = 6 '
                'left join cp2.mstlicense crLicense1 on crLicense1.licenseid = crQual1.license_id '
                'left join cp2.mstlicense crLicense2 on crLicense2.licenseid = crQual2.license_id '
                'left join cp2.mstlicense crLicense3 on crLicense3.licenseid = crQual3.license_id '
                'left join cp2.mstlicense crLicense4 on crLicense4.licenseid = crQual4.license_id '
                'left join cp2.mstlicense crLicense5 on crLicense5.licenseid = crQual5.license_id '
                'left join cp2.mstlicense crLicense6 on crLicense6.licenseid = crQual6.license_id '
                'left join cp2.trnquallang crLang on crLang.career_id = crBusicr.career_id '
                'left join cp2.mstotrlang mstlang1 on crLang.otrlang1_id = mstlang1.otrlangid '
                'left join cp2.mstotrlang mstlang2 on crLang.otrlang2_id = mstlang2.otrlangid '
                'left join cp2.mstotrlang mstlang3 on crLang.otrlang3_id = mstlang3.otrlangid '
                'left join cp2.mstlanguagelevel englishLanguagelevel on englishLanguagelevel.languagelevelid = crLang.englishlevel_id '
                'left join cp2.mstlanguagelevel languagelevel1 on languagelevel1.languagelevelid = crLang.otrlang1level_id '
                'left join cp2.mstlanguagelevel languagelevel2 on languagelevel2.languagelevelid = crLang.otrlang2level_id '
                'left join cp2.mstlanguagelevel languagelevel3 on languagelevel3.languagelevelid = crLang.otrlang3level_id '
                'where crBase.career_id = %s '
                'group by '
                'crBase.career_id '
                ',crlstschl.lstschlname '
                ',crBase.expcomp_num '
                ',mstindsctg_1.indsctgname '
                ',mstindsctg_2.indsctgname '
                ',mstindsctg_3.indsctgname '
                ',mstindsctg_4.indsctgname '
                ',mstindsctg_5.indsctgname '
                ',mstocup3class_1.ocup3classname '
                ',mstocup3class_2.ocup3classname '
                ',mstocup3class_3.ocup3classname '
                ',mstocup3class_4.ocup3classname '
                ',mstocup3class_5.ocup3classname '
                ',wishmstindsctg_1.indsctgname '
                ',wishmstindsctg_2.indsctgname '
                ',wishmstindsctg_3.indsctgname '
                ',wishmstindsctg_4.indsctgname '
                ',wishmstindsctg_5.indsctgname '
                ',wishmstocup3class_1.ocup3classname '
                ',wishmstocup3class_2.ocup3classname '
                ',wishmstocup3class_3.ocup3classname '
                ',wishmstocup3class_4.ocup3classname '
                ',wishmstocup3class_5.ocup3classname '
                ',crbasepref.wishwkareaname '
                ',crbase.wishsalary_num '
                ',crlicense1.licensename '
                ',crqual1.qualyr '
                ',crqual1.qualmon '
                ',crlicense2.licensename '
                ',crqual2.qualyr '
                ',crqual2.qualmon '
                ',crlicense3.licensename '
                ',crqual3.qualyr '
                ',crqual3.qualmon '
                ',crlicense4.licensename '
                ',crqual4.qualyr '
                ',crqual4.qualmon '
                ',crlicense5.licensename '
                ',crqual5.qualyr '
                ',crqual5.qualmon '
                ',crlang.toeicy '
                ',crlang.toeicm '
                ',crlang.toeic '
                ',crlang.toefly '
                ',crlang.toeflm '
                ',crlang.toefl '
                ',crlang.englishlevel_id '
                ',crlang.otrlang1level_id '
                ',crlang.otrlang2level_id '
                ',crlang.otrlang3level_id '
                ',mstlang1.otrlangname '
                ',mstlang2.otrlangname  '
                ',mstlang3.otrlangname '
                ',languagelevel1.languagelevelname '
                ',languagelevel2.languagelevelname '
                ',languagelevel3.languagelevelname '
                ',crReg.regstatusname '
                ',crBase.birth_date '
                ',crSex.sexname '
                ',englishLanguagelevel.languagelevelname '

            )
            cursor.execute(pSql, [crId])

            # カラム名を取得する
            returtColumns = [col[0] for col in cursor.description]

            result = cursor.fetchall()

            resultData = [dict(zip(returtColumns, row))for row in result]

            # ヘッダー作成
        response_header: dict = {
            # 'Content-Type' : 'application/json;charset=UTF-8',
            'HTTP-response-code': status.HTTP_200_OK
        }

        # ボディ作成
        response_data: dict = {
            'results': resultData,
        }

        return JsonResponse(
            status=status.HTTP_200_OK,
            headers=response_header,
            data=response_data,
            safe=False,
            json_dumps_params={'ensure_ascii': False}
        )
