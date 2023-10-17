from rest_framework import serializers
from testApp.models import *

class StfdbStaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = StfdbStaff
        fields = ('mits_username', 'mits_password')

# マスタ
# public
class PubTM01SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubTM01Section
        fields = ('section_cd', 'section_name')


class PubTM02StaffSerializer(serializers.ModelSerializer):

    class Meta:
        model = PubTM02Staff
        fields = ('staff_no', 'search_full_name')


# cp2
class Cp2MstuserSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cp2Mstuser
        fields = ('userid', 'username')


class Cp2MstteamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cp2Mstteam
        fields = ('id', 'name',  'disp_order')


# pjm
class MstPrefSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstPref
        fields = ('id', 'name',  'disp_order')


class MstApproachStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstApproachStatus
        fields = ('id', 'name',  'disp_order')


class MstContactWaysSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstContactWays
        fields = ('id', 'name',  'disp_order')


class MstMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstMedia
        fields = ('id', 'name',  'disp_order')


class MstCitySerializer(serializers.ModelSerializer):

    class Meta:
        model = MstCity
        fields = ('id', 'name',  'disp_order')


class MstDispOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstDispOrder
        fields = ('id', 'name',  'disp_order')



class MstIndustryLbc01Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstIndustryLbc01
        fields = ('id', 'name',  'disp_order')


class MstIndustryLbc02Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstIndustryLbc02
        fields = ('id', 'name',  'disp_order')


class MstIndustryLbc03Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstIndustryLbc03
        fields = ('id', 'name',  'disp_order')


class MstOccupation01Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstOccupation01
        fields = ('id_01', 'name',  'disp_order')


class MstOccupation02Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstOccupation02
        fields = ('id_02', 'name',  'disp_order')


class MstOccupation03Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstOccupation03
        fields = ('id', 'name',  'disp_order')


class MstCareerStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstCareerStatus
        fields = ('id', 'name',  'disp_order')


class MstLastSchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstLastSchool
        fields = ('id', 'name',  'disp_order')


class MstEnglishLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstEnglishLevel
        fields = ('id', 'name',  'disp_order')



class MstOtherLangageSerializer(serializers.ModelSerializer):

    class Meta:
        model = MstOtherLangage
        fields = ('id', 'name',  'disp_order')


class MstLicense01Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstLicense01
        fields = ('id', 'name',  'disp_order')


class MstLicense02Serializer(serializers.ModelSerializer):

    class Meta:
        model = MstLicense02
        fields = ('id', 'name',  'disp_order')



# トランザクション
# cp2
class Cp2TrnclientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cp2Trnclient
        fields = "__all__"


# pjm
class TrnClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnClient
        fields = (
            'trn_client_sk','lbc_cd','client_name_full','industry_id_01','industry_id_02','industry_id_03','address_full','employee_number','foundation_ym','capital','amount_sales','url','tel','keep_flg','keep_updated_staff_no','keep_updated_staff_no','keep_updated_at'
            )


class TrnClientMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnClientMatch
        fields = "__all__"


# class TrnClientIndustrySerializer(serializers.ModelSerializer):

#     class Meta:
#         model = TrnClientIndustry
#         fields = "__all__"



class TrnClientContactHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnClientContactHistory
        fields = "__all__"



class TrnClientCustomTelSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnClientCustomTel
        fields = "__all__"


class TrnOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnOrder
        fields = ('trn_order_sk','media_id','title','job_description','annual_income_min','annual_income_max','url','regist_date')



class TrnOrderMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnOrderMatch
        fields = "__all__"


class TrnOrderOccupationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnOrderOccupation
        fields = "__all__"


class TrnOrderWorkLocationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnOrderWorkLocation
        fields = "__all__"



class TrnCareerSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnCareer
        fields = ('career_id','birthday','gender_id')


class TrnCareerMatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnCareerMatch
        fields = "__all__"


class TrnCareerWishOccupationSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnCareerWishOccupation
        fields = "__all__"


class TrnCareerWishWorkPrefSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnCareerWishWorkPref
        fields = "__all__"


class TrnCareerLicenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnCareerLicense
        fields = "__all__"



class TrnSearchParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnSearchParameter
        fields =  "__all__"


class TrnSearchLatestHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = TrnSearchLatestHistory
        fields = ('trn_search_latest_history_sk','staff_no','content','audit_updated_at')