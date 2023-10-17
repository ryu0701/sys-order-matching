from email import message
from django.db import models
from project import postgresqlAccessor_stg , postgresqlAccessor_prod
from django.conf import settings


#log出力用
import logging
from logging import getLogger, StreamHandler, Formatter,FileHandler
from datetime import datetime,timedelta,date
from pathlib import Path

# Create your models here.
class sql_models:
    def login_check(LoginData):

        # username = LoginData.get('userid')
        # Password = LoginData.get('password')
        username = LoginData.get('employee_number')
        Password = LoginData.get('pass_number')

        #ここでSQL作成する？
        sql = "select "
        sql += "mits_username , mits_password , staff.staff_no ,stfdb_staff.search_full_name ,section.section_name "
        sql += "from public.stfdb_staff "
        sql += "LEFT JOIN public.t_m_02_staff staff on staff.t_m_02_staff_sk = stfdb_staff.t_m_02_staff_sk "
        sql += "LEFT JOIN public.t_m_01_section section on staff.section_cd = section.section_cd "
        sql += "where "
        sql += "mits_username ='" + username + "' "
        sql += "AND "
        sql += "mits_password ='" + Password + "' "
        
        user_record = Get_records_stg(sql)

        return user_record

    def get_prefecture(search_data):

        search_prefecture = ""
        if search_data != "":
            search_prefecture = search_data.getlist('prefecture_honsya')

        #ここでSQL作成する？
        sql = "select "
        sql += "id, name, "
        if search_data != "":
            sql += "case when name in ( " + ArrayToStr_sql(search_prefecture) + " ) then 'checked' else '' end as checked "
        else:
            sql += "'' as checked "
        sql += "from pjm.mst_pref "

        prefecture_records = Get_records_stg(sql)

        return prefecture_records

    def get_opportunity(search_data):

        print(search_data)
        if search_data != "":
            prefecture_honsya = search_data.getlist('prefecture_honsya')

        #ここでSQL作成する？
        sql = "select "
        sql += "name, new_opportunity_autono , new_prefecture "
        sql += "from doc.opportunity " #pjm.trn_order

        if search_data != "":
            sql += "where "
            sql += "new_prefecture in ( " + ArrayToStr_sql(prefecture_honsya) + " ) "

        sql += "limit 100"

        opportunity_records = Get_records_stg(sql)

        return opportunity_records

# マスタ
# public
class PubTM01Section(models.Model):
    t_m_01_section_sk = models.BigIntegerField(primary_key=True)
    section_cd = models.CharField(unique=True, max_length=10)
    section_name = models.CharField(max_length=100)
    srvc_fld_cd = models.CharField(max_length=2, blank=True, null=True)
    brnch_office_cd = models.CharField(max_length=2, blank=True, null=True)
    disp_order = models.IntegerField()
    default_disp_flg = models.IntegerField()
    last_effective_dt = models.DateField(blank=True, null=True)
    deleted_flg = models.IntegerField()
    version = models.BigIntegerField()
    audit_created_at = models.DateTimeField()
    audit_created_by = models.CharField(max_length=64)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)
    job_ofr_pblc_site_div_cd = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'public' + "\".\"" + 't_m_01_section'


class PubTM02Staff(models.Model):
    t_m_02_staff_sk = models.BigIntegerField(primary_key=True)
    ode_user_sk = models.BigIntegerField(unique=True)
    staff_no = models.BigIntegerField(unique=True)
    last_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=10)
    search_full_name = models.CharField(max_length=20)
    last_name_kana = models.CharField(max_length=20)
    first_name_kana = models.CharField(max_length=20)
    search_full_name_kana = models.CharField(max_length=20)
    section_cd = models.CharField(max_length=10)
    dept_div_cd = models.CharField(max_length=2)
    intrnl_email_address = models.CharField(max_length=255, blank=True, null=True)
    other_email_address = models.CharField(max_length=255, blank=True, null=True)
    sending_email_trgt_flg = models.IntegerField()
    employee_cd = models.CharField(max_length=10, blank=True, null=True)
    new_graduate_mid_career_div_cd = models.CharField(max_length=2, blank=True, null=True)
    hired_dt = models.DateField(blank=True, null=True)
    transferred_dt = models.DateField(blank=True, null=True)
    disp_order = models.IntegerField()
    last_effective_dt = models.DateField(blank=True, null=True)
    deleted_flg = models.IntegerField()
    version = models.BigIntegerField()
    audit_created_at = models.DateTimeField()
    audit_created_by = models.CharField(max_length=64)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'public' + "\".\"" + 't_m_02_staff'


class StfdbStaff(models.Model):
    stfdb_staff_sk = models.BigAutoField(primary_key=True)
    t_m_02_staff_sk = models.BigIntegerField(blank=True, null=True)
    stfdb_auth = models.IntegerField(blank=True, null=True)
    staff_st = models.CharField(max_length=2)
    via_mag = models.IntegerField()
    linked_mits = models.IntegerField()
    main_role = models.CharField(max_length=2, blank=True, null=True)
    emplymnt_frm_div_cd = models.CharField(max_length=2)
    employee_cd = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    first_name = models.CharField(max_length=10)
    search_full_name = models.CharField(max_length=20)
    last_name_kana = models.CharField(max_length=20)
    first_name_kana = models.CharField(max_length=20)
    search_full_name_kana = models.CharField(max_length=20)
    identifier_name_1 = models.CharField(max_length=20, blank=True, null=True)
    identifier_name_2 = models.CharField(max_length=20, blank=True, null=True)
    intrnl_email_address = models.CharField(max_length=255)
    other_email_address = models.CharField(max_length=255)
    private_phone_pre = models.CharField(max_length=8, blank=True, null=True)
    private_phone_mid = models.CharField(max_length=6, blank=True, null=True)
    private_phone_suf = models.CharField(max_length=6, blank=True, null=True)
    search_full_private_phone = models.CharField(max_length=20, blank=True, null=True)
    private_mail_addr = models.CharField(max_length=255, blank=True, null=True)
    new_graduate_mid_career_div_cd = models.CharField(max_length=2)
    hired_dt = models.DateField(blank=True, null=True)
    transferred_dt = models.DateField(blank=True, null=True)
    last_work_dt = models.DateField(blank=True, null=True)
    resign_dt = models.DateField(blank=True, null=True)
    mits_username = models.CharField(max_length=64)
    mits_password = models.CharField(max_length=255)
    stfdb_m_ipad_sk = models.IntegerField(blank=True, null=True)
    stfdb_m_staff_card_sk = models.IntegerField(blank=True, null=True)
    stfdb_m_sales_phone_sk = models.IntegerField(blank=True, null=True)
    stfdb_m_wifi_sk = models.IntegerField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    disp_order = models.IntegerField()
    deleted_flg = models.IntegerField(blank=True, null=True)
    version = models.BigIntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)
    stfdb_m_smart_phone_sk = models.IntegerField(blank=True, null=True)
    gmail_cookie_cnt = models.IntegerField(blank=True, null=True)
    line_created_dt = models.DateField(blank=True, null=True)
    account_type = models.IntegerField(blank=True, null=True)
    iphone_pre = models.CharField(max_length=8, blank=True, null=True)
    iphone_mid = models.CharField(max_length=6, blank=True, null=True)
    iphone_suf = models.CharField(max_length=6, blank=True, null=True)
    search_full_iphone = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'public' + "\".\"" + 'stfdb_staff'


# cp2
class Cp2Mstuser(models.Model):
    userid = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    username = models.CharField(max_length=300, blank=True, null=True)
    pwd = models.CharField(max_length=300, blank=True, null=True)
    loginforbidflg = models.SmallIntegerField(blank=True, null=True)
    teamid = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    retireflg = models.SmallIntegerField(blank=True, null=True)
    loginid = models.CharField(max_length=120, blank=True, null=True)
    email = models.CharField(max_length=600, blank=True, null=True)
    disporder = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    insertdate = models.DateTimeField(blank=True, null=True)
    updatedate = models.DateTimeField(blank=True, null=True)
    updateusrid = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    deleteflg = models.DateTimeField(blank=True, null=True)
    orgflg = models.CharField(max_length=60, blank=True, null=True)
    ecareer_accountid = models.CharField(max_length=60, blank=True, null=True)
    mainavi_accountid = models.CharField(max_length=150, blank=True, null=True)
    auth_co_p = models.SmallIntegerField(blank=True, null=True)
    auth_co_m = models.SmallIntegerField(blank=True, null=True)
    auth_sel_p = models.SmallIntegerField(blank=True, null=True)
    auth_sel_m = models.SmallIntegerField(blank=True, null=True)
    auth_web = models.SmallIntegerField(blank=True, null=True)
    auth_admin = models.SmallIntegerField(blank=True, null=True)
    smtpauthid = models.CharField(max_length=900, blank=True, null=True)
    smtpauthpw = models.CharField(max_length=90, blank=True, null=True)
    pop3id = models.CharField(max_length=900, blank=True, null=True)
    pop3pw = models.CharField(max_length=90, blank=True, null=True)
    en_accountid = models.CharField(max_length=60, blank=True, null=True)
    staff_id = models.CharField(max_length=60, blank=True, null=True)
    username_kana = models.CharField(max_length=600, blank=True, null=True)
    auth_cros = models.SmallIntegerField(blank=True, null=True)
    auth_del_p = models.SmallIntegerField(blank=True, null=True)
    auth_edit_e = models.SmallIntegerField(blank=True, null=True)
    auth_pro_advisor = models.SmallIntegerField(blank=True, null=True)
    auth_batchsales = models.SmallIntegerField(blank=True, null=True)
    staff_no = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    god_id = models.CharField(max_length=20, blank=True, null=True)
    auth_batchupdate = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cp2' + "\".\"" + 'mstuser'


class Cp2Mstteam(models.Model):
    teamid = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    teamname = models.CharField(max_length=300, blank=True, null=True)
    areaid = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    teamleader = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    disporder = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    insertdate = models.DateTimeField(blank=True, null=True)
    updatedate = models.DateTimeField(blank=True, null=True)
    updateusrid = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    deleteflg = models.DateTimeField(blank=True, null=True)
    finance_code = models.CharField(max_length=600, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cp2' + "\".\"" + 'mstteam'


# pjm
class MstApproachStatus(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_approach_status'


class MstContactWays(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_contact_ways'


class MstMedia(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_media'



class MstPref(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table =  'pjm' + "\".\"" + 'mst_pref'



class MstCity(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    pref_id = models.BigIntegerField(blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_city'



class MstDispOrder(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_disp_order'



class MstIndustryLbc01(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_industry_lbc_01'



class MstIndustryLbc02(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=200, blank=True, null=True)
    id_01 = models.CharField(max_length=5, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_industry_lbc_02'



class MstIndustryLbc03(models.Model):
    id = models.CharField(primary_key=True, max_length=5)
    name = models.CharField(max_length=200, blank=True, null=True)
    id_01 = models.CharField(max_length=5, blank=True, null=True)
    id_02 = models.CharField(max_length=5, blank=True, null=True)
    id_full = models.CharField(max_length=15, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_industry_lbc_03'



class MstOccupation01(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_occupation_01'



class MstOccupation02(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=200, blank=True, null=True)
    id_01 = models.CharField(max_length=6, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_occupation_02'



class MstOccupation03(models.Model):
    id = models.CharField(primary_key=True, max_length=6)
    name = models.CharField(max_length=200, blank=True, null=True)
    id_01 = models.CharField(max_length=6, blank=True, null=True)
    id_02 = models.CharField(max_length=6, blank=True, null=True)
    id_full = models.CharField(max_length=25, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_occupation_03'



class MstCareerStatus(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_career_status'



class MstLastSchool(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_last_school'



class MstEnglishLevel(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_english_level'



class MstOtherLangage(models.Model):
    id = models.BigIntegerField(primary_key=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_other_langage'



class MstLicense01(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=200, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_license_01'



class MstLicense02(models.Model):
    id = models.CharField(primary_key=True, max_length=15)
    name = models.CharField(max_length=200, blank=True, null=True)
    id_01 = models.CharField(max_length=15, blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'mst_license_02'


# トランザクション
# cp2スキーマ
class Cp2Trnclient(models.Model):
    client_id = models.DecimalField(primary_key=True, max_digits=13, decimal_places=0)
    insert_date = models.DateTimeField(blank=True, null=True)
    update_date = models.DateTimeField(blank=True, null=True)
    updateuser_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    delete_date = models.DateTimeField(blank=True, null=True)
    corpformfront = models.CharField(max_length=120, blank=True, null=True)
    corpformback = models.CharField(max_length=120, blank=True, null=True)
    clientname = models.CharField(max_length=300)
    clientnamekana = models.CharField(max_length=300)
    hp_corpname = models.CharField(max_length=300, blank=True, null=True)
    indsctg_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    capital = models.CharField(max_length=120, blank=True, null=True)
    capital_flg = models.SmallIntegerField(blank=True, null=True)
    salesamount = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    salesamount_flg = models.SmallIntegerField(blank=True, null=True)
    ordinaryprofit = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    employee_num = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    foundyr = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    foundmon = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    listed_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    market_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    frigncptl_flg = models.SmallIntegerField(blank=True, null=True)
    venture_flg = models.SmallIntegerField(blank=True, null=True)
    clienturl = models.CharField(max_length=600, blank=True, null=True)
    zip_id = models.CharField(max_length=21, blank=True, null=True)
    pref_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    addr1 = models.CharField(max_length=300, blank=True, null=True)
    addr2 = models.CharField(max_length=420, blank=True, null=True)
    addr3 = models.CharField(max_length=300, blank=True, null=True)
    busicontents = models.CharField(max_length=12000, blank=True, null=True)
    compfeature = models.CharField(max_length=12000, blank=True, null=True)
    wkhoursh = models.CharField(max_length=6, blank=True, null=True)
    wkhoursm = models.CharField(max_length=6, blank=True, null=True)
    wkhoureh = models.CharField(max_length=6, blank=True, null=True)
    wkhourem = models.CharField(max_length=6, blank=True, null=True)
    flextime_flg = models.CharField(max_length=6, blank=True, null=True)
    annualholidays = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    comphouse_dorm_flg = models.CharField(max_length=6, blank=True, null=True)
    healthinsurance_flg = models.SmallIntegerField(blank=True, null=True)
    welfarepension_flg = models.SmallIntegerField(blank=True, null=True)
    unemplyinsrnc_flg = models.SmallIntegerField(blank=True, null=True)
    accidentinsrnc_flg = models.SmallIntegerField(blank=True, null=True)
    insurancetext = models.CharField(max_length=600, blank=True, null=True)
    travelallowance_flg = models.SmallIntegerField(blank=True, null=True)
    housingallowance_flg = models.SmallIntegerField(blank=True, null=True)
    familyallowance_flg = models.SmallIntegerField(blank=True, null=True)
    ovrtmallowance_flg = models.SmallIntegerField(blank=True, null=True)
    salesallowance_flg = models.SmallIntegerField(blank=True, null=True)
    areaallowance_flg = models.SmallIntegerField(blank=True, null=True)
    allowancetext = models.CharField(max_length=600, blank=True, null=True)
    cngr_cndlholiday_flg = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    newyearholiday_flg = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    summarholiday_flg = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    paidholiday_flg = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    holidaytext = models.CharField(max_length=600, blank=True, null=True)
    writtenexam_flg = models.SmallIntegerField(blank=True, null=True)
    essay_flg = models.SmallIntegerField(blank=True, null=True)
    explanatory_flg = models.SmallIntegerField(blank=True, null=True)
    aptitudetest_flg = models.SmallIntegerField(blank=True, null=True)
    workpresentation_flg = models.SmallIntegerField(blank=True, null=True)
    qualsklchk_flg = models.SmallIntegerField(blank=True, null=True)
    interview_num = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    trial_flg = models.CharField(max_length=6, blank=True, null=True)
    trialperiod = models.CharField(max_length=12, blank=True, null=True)
    emplycompetition = models.CharField(max_length=4800, blank=True, null=True)
    rcmndnotes = models.CharField(max_length=4800, blank=True, null=True)
    sexratio = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    recievedetails_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    manager_flg = models.CharField(max_length=6, blank=True, null=True)
    clientsize = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    companyrank = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    hp_busiresume = models.CharField(max_length=12000, blank=True, null=True)
    regstatus_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    chargearea_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    chargeteam_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    charge_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    oldclient_id = models.CharField(max_length=60, blank=True, null=True)
    next_date = models.DateTimeField(blank=True, null=True)
    busicontents_web = models.CharField(max_length=12000, blank=True, null=True)
    compfeature_web = models.CharField(max_length=12000, blank=True, null=True)
    stockholder = models.CharField(max_length=3000, blank=True, null=True)
    compcompany = models.CharField(max_length=1200, blank=True, null=True)
    busicompany = models.CharField(max_length=12000, blank=True, null=True)
    compstyle = models.CharField(max_length=12000, blank=True, null=True)
    client_email = models.CharField(max_length=300, blank=True, null=True)
    focus_flg = models.SmallIntegerField(blank=True, null=True)
    salesstatus_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    focusrank_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    focusrankmemo = models.CharField(max_length=300, blank=True, null=True)
    clienttel = models.CharField(max_length=60, blank=True, null=True)
    clientfax = models.CharField(max_length=60, blank=True, null=True)
    representativepost = models.CharField(max_length=300, blank=True, null=True)
    representativename = models.CharField(max_length=600, blank=True, null=True)
    found_flg = models.SmallIntegerField(blank=True, null=True)
    employee_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    employee_flg = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    employeememo = models.CharField(max_length=300, blank=True, null=True)
    employeecomposition = models.CharField(max_length=12000, blank=True, null=True)
    employeecomposition_flg = models.SmallIntegerField(blank=True, null=True)
    officememo = models.CharField(max_length=12000, blank=True, null=True)
    retirementage_num = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    continuedemp_flg = models.SmallIntegerField(blank=True, null=True)
    retirementagememo = models.CharField(max_length=600, blank=True, null=True)
    resultamount1_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    resultamount2_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    planresultyr_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    planresultmon_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    planresultamount1_a = models.CharField(max_length=300, blank=True, null=True)
    planresultamount1_b = models.CharField(max_length=300, blank=True, null=True)
    actualresultyr1_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    actualresultmon1_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    actualresultamount1_a = models.CharField(max_length=300, blank=True, null=True)
    actualresultamount1_b = models.CharField(max_length=300, blank=True, null=True)
    actualresultyr2_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    actualresultmon2_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    actualresultamount2_a = models.CharField(max_length=300, blank=True, null=True)
    actualresultamount2_b = models.CharField(max_length=300, blank=True, null=True)
    tenurestatus_id = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    clientmobiletel = models.CharField(max_length=60, blank=True, null=True)
    features_id = models.CharField(max_length=3000, blank=True, null=True)
    foundation = models.CharField(max_length=3000, blank=True, null=True)
    corplocation = models.CharField(max_length=3000, blank=True, null=True)
    planresult = models.CharField(max_length=3000, blank=True, null=True)
    actualresult1 = models.CharField(max_length=3000, blank=True, null=True)
    actualresult2 = models.CharField(max_length=3000, blank=True, null=True)
    planresultamount1_a2 = models.CharField(max_length=3000, blank=True, null=True)
    actualresultamount1_a2 = models.CharField(max_length=3000, blank=True, null=True)
    actualresultamount2_a2 = models.CharField(max_length=3000, blank=True, null=True)
    ordinaryprofit2 = models.CharField(max_length=3000, blank=True, null=True)
    zip_id2 = models.CharField(max_length=3000, blank=True, null=True)
    memo = models.TextField(blank=True, null=True)
    creditid = models.CharField(max_length=120, blank=True, null=True)
    creditidchkyr = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    creditidchkmn = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    creditidchkdy = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    asocialid = models.CharField(max_length=120, blank=True, null=True)
    asocialidchkyr = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    asocialidchkmn = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    asocialidchkdy = models.DecimalField(max_digits=13, decimal_places=0, blank=True, null=True)
    agreementmemo = models.CharField(max_length=12000, blank=True, null=True)
    is_march_flg = models.SmallIntegerField(blank=True, null=True)
    lbccode = models.CharField(max_length=66, blank=True, null=True)
    otherdivisionmemo = models.CharField(max_length=3000, blank=True, null=True)
    client_catchphrase = models.CharField(max_length=60, blank=True, null=True)
    facilitytype_id = models.SmallIntegerField(blank=True, null=True)
    passivesmoking_id = models.SmallIntegerField(blank=True, null=True)
    passivesmokingmeasures_id = models.SmallIntegerField(blank=True, null=True)
    passivesmokingmemo = models.CharField(max_length=200, blank=True, null=True)
    emergencymemo = models.CharField(max_length=1000, blank=True, null=True)
    clienturl_pickup_thismonth = models.CharField(max_length=200, blank=True, null=True)
    asocialstate = models.CharField(max_length=40, blank=True, null=True)
    acquisitionroute_id = models.SmallIntegerField(blank=True, null=True)
    clienturl_introduction_video = models.CharField(max_length=200, blank=True, null=True)
    lbc_update_date = models.DateTimeField(blank=True, null=True)
    is_os_link_flg = models.SmallIntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cp2' + "\".\"" + 'trnclient'


# pjmスキーマ
class TrnClient(models.Model):
    trn_client_sk = models.BigAutoField(primary_key=True)
    lbc_cd = models.CharField(max_length=20, blank=True, null=True)
    client_name_full = models.CharField(max_length=200, blank=True, null=True)
    address_full = models.CharField(max_length=500, blank=True, null=True)
    zip_cd = models.CharField(max_length=7, blank=True, null=True)
    pref_id = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    address_01 = models.CharField(max_length=200, blank=True, null=True)
    address_02 = models.CharField(max_length=200, blank=True, null=True)
    employee_number = models.CharField(max_length=100, blank=True, null=True)
    foundation_ym = models.IntegerField(blank=True, null=True)
    capital = models.IntegerField(blank=True, null=True)
    amount_sales = models.CharField(max_length=100, blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    industry_id_01 = models.CharField(max_length=15, blank=True, null=True)
    industry_id_02 = models.CharField(max_length=15, blank=True, null=True)
    industry_id_03 = models.CharField(max_length=15, blank=True, null=True)
    keep_flg = models.SmallIntegerField(blank=True, null=True)
    keep_updated_staff_no = models.BigIntegerField(blank=True, null=True)
    keep_updated_at = models.DateTimeField(blank=True, null=True)
    lastest_contact_staff_no = models.BigIntegerField(blank=True, null=True)
    lastest_contact_date = models.DateTimeField(blank=True, null=True)
    lastest_contact_approach_id = models.IntegerField(blank=True, null=True)
    lastest_contact_audit_created_at = models.DateTimeField(blank=True, null=True)
    lastest_contact_audit_created_by = models.DateTimeField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_client'


class TrnClientMatch(models.Model):
    trn_client_match_sk = models.BigAutoField(primary_key=True)
    lbc_cd = models.CharField(max_length=20, blank=True, null=True)
    client_id = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_client_match'


class TrnClientContactHistory(models.Model):
    trn_client_contact_history_sk = models.BigAutoField(primary_key=True)
    lbc_cd = models.CharField(max_length=20, blank=True, null=True)
    staff_no = models.BigIntegerField(blank=True, null=True)
    approach_id = models.IntegerField(blank=True, null=True)
    contact_ways_id = models.IntegerField(blank=True, null=True)
    contact_date = models.DateTimeField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    scheduled_date = models.DateTimeField(blank=True, null=True)
    regist_type = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_client_contact_history'



class TrnClientCustomTel(models.Model):
    trn_client_custom_tel_sk = models.BigAutoField(primary_key=True)
    lbc_cd = models.CharField(max_length=20, blank=True, null=True)
    tel = models.CharField(max_length=30, blank=True, null=True)
    staff_no = models.BigIntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_client_custom_tel'



class TrnOrder(models.Model):
    trn_order_sk = models.BigAutoField(primary_key=True)
    trn_client_sk = models.BigIntegerField(blank=True, null=True)
    lbc_cd = models.CharField(max_length=20, blank=True, null=True)
    media_id = models.IntegerField(blank=True, null=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=500, blank=True, null=True)
    annual_income_min = models.IntegerField(blank=True, null=True)
    annual_income_max = models.IntegerField(blank=True, null=True)
    regist_date = models.DateTimeField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_order'



class TrnOrderMatch(models.Model):
    trn_order_match_sk = models.BigAutoField(primary_key=True)
    trn_order_sk = models.BigIntegerField(blank=True, null=True)
    cp2_order_id = models.IntegerField(blank=True, null=True)
    match_value_01 = models.IntegerField(blank=True, null=True)
    match_value_02 = models.IntegerField(blank=True, null=True)
    match_value_03 = models.IntegerField(blank=True, null=True)
    match_value_04 = models.IntegerField(blank=True, null=True)
    match_value_05 = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_order_match'



class TrnOrderOccupation(models.Model):
    trn_order_occupation_sk = models.BigAutoField(primary_key=True)
    trn_order_sk = models.BigIntegerField(blank=True, null=True)
    occupation_id = models.CharField(max_length=25, blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_order_occupation'



class TrnOrderWorkLocation(models.Model):
    trn_order_work_location_sk = models.BigAutoField(primary_key=True)
    trn_order_sk = models.BigIntegerField(blank=True, null=True)
    pref_id = models.IntegerField(blank=True, null=True)
    city_id = models.IntegerField(blank=True, null=True)
    location_name = models.CharField(max_length=500, blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_order_work_location'


class TrnCareer(models.Model):
    trn_career_sk = models.BigAutoField(primary_key=True)
    career_id = models.IntegerField(blank=True, null=True)
    valid_flg = models.IntegerField(blank=True, null=True)
    career_status = models.IntegerField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    gender_id = models.IntegerField(blank=True, null=True)
    exp_company_num = models.IntegerField(blank=True, null=True)
    last_school_id = models.IntegerField(blank=True, null=True)
    english_level_id = models.IntegerField(blank=True, null=True)
    other_langage_1_id = models.IntegerField(blank=True, null=True)
    other_langage_2_id = models.IntegerField(blank=True, null=True)
    other_langage_3_id = models.IntegerField(blank=True, null=True)
    current_salary = models.IntegerField(blank=True, null=True)
    wish_salary = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_career'



class TrnCareerMatch(models.Model):
    trn_career_match_sk = models.BigAutoField(primary_key=True)
    trn_order_sk = models.CharField(max_length=20, blank=True, null=True)
    career_id = models.IntegerField(blank=True, null=True)
    match_value_01 = models.IntegerField(blank=True, null=True)
    match_value_02 = models.IntegerField(blank=True, null=True)
    match_value_03 = models.IntegerField(blank=True, null=True)
    match_value_04 = models.IntegerField(blank=True, null=True)
    match_value_05 = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_career_match'



class TrnCareerWishOccupation(models.Model):
    trn_career_wish_occupation_sk = models.BigAutoField(primary_key=True)
    career_id = models.BigIntegerField(blank=True, null=True)
    occupation_id = models.CharField(max_length=6, blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_career_wish_occupation'



class TrnCareerWishWorkPref(models.Model):
    trn_career_wish_work_pref_sk = models.BigAutoField(primary_key=True)
    career_id = models.BigIntegerField(blank=True, null=True)
    pref_id = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_career_wish_work_pref'



class TrnCareerLicense(models.Model):
    trn_career_license_sk = models.BigAutoField(primary_key=True)
    career_id = models.BigIntegerField(blank=True, null=True)
    license_id = models.CharField(max_length=15, blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_career_license'



class TrnSearchParameter(models.Model):
    trn_search_parameter_sk = models.BigAutoField(primary_key=True)
    staff_no = models.BigIntegerField(blank=True, null=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    type = models.IntegerField(blank=True, null=True)
    copy_sk = models.BigIntegerField(blank=True, null=True)
    original_sk = models.BigIntegerField(blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_search_parameter'



class TrnSearchLatestHistory(models.Model):
    trn_search_latest_history_sk = models.BigAutoField(primary_key=True)
    staff_no = models.BigIntegerField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    disp_order = models.IntegerField(blank=True, null=True)
    deleted_flg = models.IntegerField(blank=True, null=True)
    audit_created_at = models.DateTimeField(blank=True, null=True)
    audit_created_by = models.CharField(max_length=64, blank=True, null=True)
    audit_updated_at = models.DateTimeField(blank=True, null=True)
    audit_updated_by = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'pjm' + "\".\"" + 'trn_search_latest_history'
        
def ArrayToStr_sql(array):

    target = ""

    if array != "":
        for i ,val in enumerate(array):
            if i > 0:
                target += " , "
            target += "'" + val + "'"

    return target


def Get_records_stg(sql):

    ########################
    #①Postgresqlへの接続
    ########################


    #postgreSQLに接続（接続情報は環境変数、PG_XXX）

    try:
        obj_postgresql = postgresqlAccessor_stg.postgresqlAccessor_stg()

        #クエリ実行
        results = obj_postgresql.excecuteQuery(sql)

        return results

    except Exception as e:
        print("error")
        print(e)

        return

def Get_records_prd(sql):

    ########################
    #①Postgresqlへの接続
    ########################


    #postgreSQLに接続（接続情報は環境変数、PG_XXX）

    try:
        obj_postgresql = postgresqlAccessor_prod.postgresqlAccessor_prod()

        #クエリ実行
        results = obj_postgresql.excecuteQuery(sql)

        return results

    except Exception as e:
        print("error")
        print(e)

        return
    
def put_log(path,obj):
    
    logger = getLogger("Log")

    # --------------------------------
    # 1.loggerの設定
    # --------------------------------

    # loggerのログレベル設定(ハンドラに渡すエラーメッセージのレベル)
    logger.setLevel(logging.DEBUG)


    # --------------------------------
    # 2.handlerの設定
    # --------------------------------
    # ログ出力フォーマット設定
    handler_format = Formatter("%(asctime)s [%(filename)s:%(lineno)d] %(levelname)-8s %(message)s")

    # ---- 2-1.標準出力のhandler ----
    # handlerの生成
    stream_handler = StreamHandler()

    # handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
    stream_handler.setLevel(logging.DEBUG)

    # ログ出力フォーマット設定
    stream_handler.setFormatter(handler_format)

    # ---- 2-2.テキスト出力のhandler ----
    # handlerの生成
    now = datetime.now()
    
    #ここにログを保存したいファイルのパスと命名規則を記入
    print(path + 'app_log_'+ now.strftime('%Y%m%d') + '.log')
    file_handler = FileHandler(path + 'app_log.'+ now.strftime('%Y%m%d'), encoding='utf-8')

    # handlerのログレベル設定(ハンドラが出力するエラーメッセージのレベル)
    file_handler.setLevel(logging.DEBUG)

    # ログ出力フォーマット設定
    file_handler.setFormatter(handler_format)

    # --------------------------------
    # 3.loggerにhandlerをセット
    # --------------------------------
    # 標準出力のhandlerをセット
    logger.addHandler(stream_handler)
    # テキスト出力のhandlerをセット
    logger.addHandler(file_handler)

    #変数セット
    message = "Login Success!"
    staff_no = obj["user_records"]["staff_no"]
    staff_name = obj["user_records"]["staff_name"]
    staff_section = obj["user_records"]["staff_section"]

    log_message = message + ' ' + str(staff_no) + ' ' + staff_section + ' ' + staff_name

    #logger.infoで書き出せます
    logger.info(log_message)

    return logger