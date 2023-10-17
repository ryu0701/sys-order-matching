(function () {
  'user strict';

  //呼び出し？
  Vue.component('paginate', VuejsPaginate);
  Vue.use(window['vue-js-toggle-button'].default); // 20231004 新井追記

  //認証
  axios.defaults.xsrfCookieName = 'csrftoken';
  axios.defaults.xsrfHeaderName = 'X-CSRFTOKEN';

  var vm = new Vue({
    el: '#search',
    data: {
      //ここから求人検索用------------------
      //20231004 新井追記 new_flgs
      new_flgs: [
        {
          id: 'client',
          name: '新着企業',
          checked: false,
        },
        {
          id: 'order',
          name: '新着求人アリ',
          checked: false,
        },
      ],
      op_mediums: [
        {
          //求人媒体
          id: '01',
          code: 1,
          name: 'static/image/Recruit_Holdings_logo.svg',
          checked: '',
        },
        {
          id: '02',
          code: 2,
          name: 'static/image/logo_doda.png',
          checked: '',
        },
      ],
      op_mediums: [
        {
          //求人媒体
          id: '01',
          code: 1,
          name: 'static/image/Recruit_Holdings_logo.svg',
          checked: '',
        },
        {
          id: '02',
          code: 2,
          name: 'static/image/logo_doda.png',
          checked: '',
        },
      ],
      client_words: '', //企業検索
      industries: [], //業種マスタ
      industry_data_name: [], //業種namaデータ
      industry_data: [], //業種データ
      honsya_prefs: [], //本社都道府県
      kinmu_prefs: [], //勤務地
      income_min: 0, //年収
      income_max: 1000000000,
      occupation: [], //職種
      occupation_data: [], //職種データ
      keep_status: [
        {
          //キープステータス
          id: 1,
          name: 'キープ中',
          checked: 'checked',
        },
        {
          id: 2,
          name: '他者キープ',
          checked: '',
        },
        {
          id: 3,
          name: '未設定',
          checked: 'checked',
        },
      ],
      cp2_client_ras: [], //cp2企業RAマスタ
      cp2_client_ras_data: [], //cp2企業RAデータ
      approach_date_start: '', //アプローチ日時
      approach_status: [], //アプローチ最新結果
      approach_date_end: '',
      except_approach_date_start: '', //アプローチ日時(指定期間アプローチなし検索)
      except_approach_date_end: '',
      users: [], //アプローチ者
      bussinesinits: [], //アプローチ者部署
      cp2_client_id: '', //cp2企業id検索
      lbc_code: '', //lbc検索

      //ここから求職者マッチング検索用--------------------
      lead_active_master: [
        {
          id: 1,
          code: 3,
          name: '有効',
          checked: 'checked',
        },
        {
          id: 0,
          code: 4,
          name: '非有効',
          checked: '',
        },
      ], //有効非有効マスタ
      lead_active: 1, //有効非有効データ
      lead_status: [], //求職者ステータス
      lead_age_from: '', //年齢from
      lead_age_to: '', //年齢to
      lead_gender: [
        {
          id: 1,
          name: '男性',
          checked: '',
        },
        {
          id: 2,
          name: '女性',
          checked: '',
        },
      ], //性別
      lead_occupation: [], //希望職種マスタ
      lead_occupation_data: [], //希望職種データ
      lead_prefs: [], //希望都道府県
      lead_last_school: [], //最終学歴
      lead_english_level: [], //英語レベル
      lead_now_income_min: '', //現在年収min
      lead_now_income_max: '', //現在年収max
      lead_hope_income_min: '', //希望年収min
      lead_hope_income_max: '', //希望年収max
      lead_company_history_min: '', //経験社数min
      lead_company_history_max: '', //経験社数max
      lead_languages: [], //その他言語
      lead_skills: [], //資格マスタ
      lead_skills_data: [], //資格データ

      //メイン画面----------------------------------------
      exit_nomach: '',
      exit_nopublic: 'checked',
      select_sort: [
        {
          name: '求職者マッチング降順',
          id: 1,
        },
      ], //ソート条件初期値
      sorts: [], //ソート条件一覧
      ops: [],
      LbcList: [],
      custm_tel_items: {
        //電話番号編集用OBJ
        custm_tel: '',
        custm_hstry: [],
      },
      contact_hstry_item: {
        //連絡履歴追加用OBJ
        approach_date: '',
        approach: [],
        appoint_date: '',
        approach_comment: '',
        select_appoint: '--選択してください--',
        parPage: 2,
        currentPage: 1,
        contact_hstry_bk: [],
      },
      search_conditions: '', //検索条件名
      search_contents: [], //取得した保存済みの検索条件
      total_count: '', //トータルカウント
      total_count_disp: '', //トータルカウント表示部分
      search_param: [], //ページネーション用検索条件
      loading: false, //ローディング
      select_save: [], //選択した保存条件
      setinterval: '', //キープ取得タイマー
      client_page: 1, //ページネーション現在のページ数
      page_jump_num: null, //ページジャンプ用指定ページ数
      contact_pages: {
        //連絡履歴現在のページ数
        contact_page_0: 1,
        contact_page_1: 1,
        contact_page_2: 1,
        contact_page_3: 1,
        contact_page_4: 1,
        contact_page_5: 1,
        contact_page_6: 1,
        contact_page_7: 1,
        contact_page_8: 1,
        contact_page_9: 1,
      },
      //ここから求人詳細----------------------------------------
      company_name: '',
      url: '',
      offer_ttl: '',
      job_context: '',
      job_media: '',
      open_date: '',
      match_num: '',
      match_career: [],

      //ここから求職者詳細----------------------------------------
      cp2_careerid: '123456', //CP2ID
      career_data: '活動中/29歳/女性', //求職者概要
      lstschlname: '大学', //最終学歴
      expcomp_num: 1, //経験社数
      exp_industry: 'ソフトウェアベンダ', //経験業種
      exp_occupation: 'プログラマ（オープン・WEB）', //経験職種
      wish_industry: 'WEBサービス・WEBメディア（EC/SaaS/ASP/ポータル/SNS等）', //希望業種
      wish_occupation: '社内システム企画', //希望職種
      wish_wkpref: '東京都', //希望勤務地
      wishannualincm_num: '400', //希望年収

      wkperiode_date1: '1992/04~2000/08', //期間
      compname1: '株式会社日本リース', //企業名
      dept1: '横ｈ間支店', //部署名
      indsctgname1: 'リース・クレジット・信販', //#業種
      annualincm1: '0', //#年収
      wkcontents1: '', ////職務内容
      wkperiode_date2: '', //期間2
      compname2: '', //企業名2
      dept2: '', //部署名2
      indsctgname2: '', //業種2
      annualincm2: '', //年収2
      wkcontents2: '', //職務内容2
      wkperiode_date3: '', //期間3
      compname3: '', //企業名3
      dept3: '', //部署名3
      indsctgname3: '', //業種3
      annualincm3: '', //年収3
      wkcontents3: '', //職務内容3
      wkperiode_date4: '', //期間4
      compname4: '', //企業名4
      dept4: '', //部署名4
      indsctgname4: '', //業種4
      annualincm4: '', //年収4
      wkcontents4: '', //職務内容4
      wkperiode_date5: '', //期間5
      compname5: '', //企業名5
      dept5: '', //部署名5
      indsctgname5: '', //業種5
      annualincm5: '', //年収5
      wkcontents5: '', //職務内容5

      Schcperiode_date1: '~1992/3', //期間1
      gradname1: '卒業', //卒業区分1
      schlname1: '文教大学', //学校名1
      schldeptname1: '女子短期大学部文芸科', //学部1
      Schcperiode_date2: '~1996/3', //期間2
      gradname2: '卒業', //卒業区分2
      schlname2: '株式会社マイナビ', //学校名2
      schldeptname2: '紹介事業部', //学部2
      Schcperiode_date3: '', //期間3
      gradname3: '', //卒業区分3
      schlname3: '', //学校名3
      schldeptname3: '', //学部3
      Schcperiode_date4: '', //期間4
      gradname4: '', //卒業区分4
      schlname4: '', //学校名4
      schldeptname4: '', //学部4
      Schcperiode_date5: '', //期間5
      gradname5: '', //卒業区分5
      schlname5: '', //学校名5
      schldeptname5: '', //学部5
      licensename1: '', //資格名1
      qual_date1: '', // 取得1
      licensename2: '', //資格名2
      qual_date2: '', // 取得2
      licensename3: '', //資格名3
      qual_date3: '', // 取得3
      licensename4: '', //資格名4
      qual_date4: '', // 取得4
      licensename5: '', //資格名5
      qual_date5: '', // 取得5

      toeic: '', //TOEIC
      toefl: '', //TOEFUL
      english_level: '', //英語
      otrlang1: '', //その他言語1
      otrlang2: '', //その他言語2
      otrlang3: '', //その他言語3

      login_staff_no: '', //ログイン情報
      login_staff_name: '', //ログイン情報
      login_staff_section: '', //ログイン情報
    },
    created: async function () {
      //初期値取得

      //業種マスタ
      var Industry = {
        method: 'GET',
        url: 'api/v1/mstData/mstIndustry',
        responseType: 'json',
      };
      var response_Industry = await axios.request(Industry);
      response_Industry.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.industries = response_Industry.data['results'];

      //職種マスタ
      var Occupation = {
        method: 'GET',
        url: 'api/v1/mstData/mstOccupation',
        responseType: 'json',
      };
      var response_Occupation = await axios.request(Occupation);
      response_Occupation.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.occupation = response_Occupation.data['results'];
      //都道府県マスタ
      var config_pref = {
        method: 'GET',
        url: 'api/v1/mstData/mstpref',
        responseType: 'json',
      };
      var response_pref = await axios.request(config_pref);
      response_pref.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.honsya_prefs = response_pref.data['results'];
      //都道府県マスタ2(なぜか二回やらないといけない…後回し)
      var config_pref2 = {
        method: 'GET',
        url: 'api/v1/mstData/mstpref',
        responseType: 'json',
      };
      var response_pref2 = await axios.request(config_pref2);
      response_pref2.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.kinmu_prefs = response_pref2.data['results'];

      //アプローチステータス
      var config_app = {
        method: 'GET',
        url: 'api/v1/mstData/mstapproach',
        responseType: 'json',
      };
      var response_app = await axios.request(config_app);
      response_app.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      response_app.data['results'] = this.approach_status = response_app.data['results'];
      this.contact_hstry_item.approach = response_app.data['results'];
      //cp2企業担当マスタ
      var cp2mstuser = {
        method: 'GET',
        url: 'api/v1/mstData/mstCp2User',
        responseType: 'json',
      };
      var response_cp2mstuser = await axios.request(cp2mstuser);
      this.cp2_client_ras = response_cp2mstuser.data['results'];

      //アプローチ者マスタ
      var mstStaff = {
        method: 'GET',
        url: 'api/v1/mstData/mstStaff',
        responseType: 'json',
      };
      var response_mstStaff = await axios.request(mstStaff);
      this.users = response_mstStaff.data['results'];

      //アプローチ者部署マスタ
      var mstSection = {
        method: 'GET',
        url: 'api/v1/mstData/mstSection',
        responseType: 'json',
      };
      var response_mstSection = await axios.request(mstSection);
      this.bussinesinits = response_mstSection.data['results'];
      //求職者ステータスマスタ
      var config_lstatus = {
        method: 'GET',
        url: 'api/v1/mstData/mstcrstatus',
        responseType: 'json',
      };
      var response_lstatus = await axios.request(config_lstatus);
      response_lstatus.data['results'].forEach((element) => {
        if (element.id == '3' || element.id == '4') {
          element['checked'] = 'checked';
        } else {
          element['checked'] = '';
        }
      });
      this.lead_status = response_lstatus.data['results'];
      //希望職種マスタ
      var hope_Occupation = {
        method: 'GET',
        url: 'api/v1/mstData/mstOccupation',
        responseType: 'json',
      };
      var response_hope_Occupation = await axios.request(hope_Occupation);
      response_hope_Occupation.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.lead_occupation = response_hope_Occupation.data['results'];

      //希望勤務地マスタ
      var config_lpref = {
        method: 'GET',
        url: 'api/v1/mstData/mstpref',
        responseType: 'json',
      };
      var response_lpref = await axios.request(config_lpref);
      response_lpref.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.lead_prefs = response_lpref.data['results'];
      //最終学歴マスタ
      var lastschool = {
        method: 'GET',
        url: 'api/v1/mstData/mstlastschool',
        responseType: 'json',
      };
      var response_lastschool = await axios.request(lastschool);
      this.lead_last_school = response_lastschool.data['results'];
      //英語レベルマスタ
      var englishlv = {
        method: 'GET',
        url: 'api/v1/mstData/mstenglishlv',
        responseType: 'json',
      };
      var response_englishlv = await axios.request(englishlv);
      this.lead_english_level = response_englishlv.data['results'];
      //その他言語マスタ
      var otherlang = {
        method: 'GET',
        url: 'api/v1/mstData/mstotherlang',
        responseType: 'json',
      };
      var response_otherlang = await axios.request(otherlang);
      this.lead_languages = response_otherlang.data['results'];
      //資格マスタ
      var License = {
        method: 'GET',
        url: 'api/v1/mstData/mstLicense',
        responseType: 'json',
      };
      var response_License = await axios.request(License);
      response_License.data['results'].forEach((element) => {
        element['checked'] = '';
      });
      this.lead_skills = response_License.data['results'];

      //並び替えマスタ
      var config_sort = {
        method: 'GET',
        url: 'api/v1/mstData/mstdisp',
        responseType: 'json',
      };
      var response_sort = await axios.request(config_sort);
      this.sorts = response_sort.data['results'];
      this.select_sort = response_sort.data['results'][0];
    },
    mounted: function () {
      //モーダルを動かす魔法
      this.init();

      // bar UI by Omae
      var slider = new rSlider({
        target: '#slider',
        values: ['下限なし', '300万円', '400万円', '500万円', '600万円', '700万円', '上限なし'],
        range: true,
        set: ['下限なし', '上限なし'],
        onChange: function (vals) {
          console.log(vals);
          //カンマで配列に分ける
          var min = vals.split(',')[0];
          var max = vals.split(',')[1];
          console.log(min);
          console.log(max);

          if (min != '下限なし') {
            min = min.replace('万円', '');
            min = Number(min) * 10000;
          } else {
            min = 0; //割と適当
          }

          if (max != '上限なし') {
            max = max.replace('万円', '');
            max = Number(max) * 10000;
          } else {
            max = 1000000000; //割と適当
          }
          //代入
          vm.income_min = min;
          vm.income_max = max;
        },
      });
      /*
      var slider2 = new rSlider({
        target: "#slider2",
        values: ['下限なし', '300万円', '400万円', '500万円', '600万円', '700万円', '上限なし'],
        range: true,
        set: ['300万円', '500万円'],
        onChange: function(vals) {
          console.log(vals);
          //カンマで配列に分ける
          var min = vals.split(',')[0]
          var max = vals.split(',')[1]
          console.log(min);
          console.log(max);

          if(min != "下限なし"){
            min = min.replace("万円","")
            min = Number(min)
          }else{
            min = 0
          }


          if(max != "上限なし"){
            max = max.replace("万円","")
            max = Number(max)
          }else{
            max = 1000000000
          }
          //代入
          vm.lead_now_income_min = min
          vm.lead_now_income_max = max
        },
      });

      var slider3 = new rSlider({
        target: "#slider3",
        values: ['下限なし', '300万円', '400万円', '500万円', '600万円', '700万円', '上限なし'],
        range: true,
        set: ['300万円', '500万円'],
        onChange: function(vals) {
          console.log(vals);
          //カンマで配列に分ける
          var min = vals.split(',')[0]
          var max = vals.split(',')[1]
          console.log(min);
          console.log(max);

          if(min != "下限なし"){
            min = min.replace("万円","")
            min = Number(min)
          }else{
            min = 0
          }

          if(max != "上限なし"){
            max = max.replace("万円","")
            max = Number(max)
          }else{
            max = 1000000000
          }
          //代入
          vm.lead_hope_income_min = min
          vm.lead_hope_income_max = max
        },
      });
      */

      $(document).ready(function () {
        tippy('.tooltip_icon', { allowHTML: true });
      });
    },
    updated: function () {
      $('.dropdown').focusout(function () {
        $(this).removeClass('active');
        $(this).find('.dropdown-menu').slideUp(300);
      });

      $(function () {
        // 表示されている場合の処理
        if ($('.default').css('display') == 'block') {
          $('.section').hide();
        }
      });

      $(document).ready(function () {
        tippy('.tooltip_icon', { allowHTML: true });
      });
    },
    methods: {
      init() {
        //micromodal動かす用
        MicroModal.init({});
      },
      //全選択がチェックされた時用
      all_selected(all) {
        var element_all = all.target;
        var parent_element = element_all.parentElement;
        let child_elements = parent_element.querySelectorAll('input');
        for (var i = 0; i < child_elements.length; i++) {
          if (element_all.checked) {
            child_elements[i].checked = true;
          } else {
            child_elements[i].checked = false;
          }
        }
      },
      //求職者マッチング条件モーダル閉じる用
      modal_close() {
        var trigger_match = document.getElementById('trigger_match');
        trigger_match.checked = false;
      },
      async search_client(page_num) {
        //企業反映用

        this.loading = true; //ロード

        clearTimeout(this.setinterval); //キープ取得インターバル削除

        //ここから企業求人検索用----------------------
        var new_flg_client = this.new_flgs[0].checked; // 20231004 新井追記
        var new_flg_order = this.new_flgs[1].checked; // 20231004 新井追記
        var op_mediums = this.op_mediums.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var key_words = this.client_words;
        var industries = this.industry_data;

        var honsya_prefs = this.honsya_prefs.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var kinmu_prefs = this.kinmu_prefs.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var income_min = this.income_min;
        var income_max = this.income_max;
        var occupation = this.occupation_data;

        var keep_status = this.keep_status.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        keep_status = Array.from(new Set(keep_status));

        var cp2_client_raids = $('.cp2_user_id').val();

        var approach_date_start = this.approach_date_start;
        var approach_date_end = this.approach_date_end;

        var except_approach_date_start = this.except_approach_date_start;
        var except_approach_date_end = this.except_approach_date_end;

        var approach_status = this.approach_status
          .filter((value) => value['checked'] == true || value['checked'] == 'checked')
          .map((value) => value['id']);

        var approach_users = $('.approach_users').val();

        var approach_sections = $('.approach_sections').val();

        var cp2_client_id = this.cp2_client_id;
        var lbc_code = this.lbc_code;
        var sort_id = this.select_sort.id;

        //ここから求職者マッチング情報----------------------
        var lead_active = this.lead_active;
        var lead_status = this.lead_status.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var lead_age_from = this.lead_age_from;
        var lead_age_to = this.lead_age_to;
        var lead_gender = this.lead_gender.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var lead_occupation = this.lead_occupation_data;

        var lead_prefs = this.lead_prefs.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var lead_last_school = $('.school').val();
        var lead_english_level = $('.english').val();
        var lead_now_income_min = this.lead_now_income_min;
        var lead_now_income_max = this.lead_now_income_max;
        var lead_hope_income_min = this.lead_hope_income_min;
        var lead_hope_income_max = this.lead_hope_income_max;
        var lead_company_history_min = this.lead_company_history_min;
        var lead_company_history_max = this.lead_company_history_max;
        var lead_languages = $('.languages').val();
        var lead_skills = this.lead_skills_data;

        //おまけ
        var exit_nomach = this.exit_nomach;
        var exit_nopublic = this.exit_nopublic;
        var page_num = page_num;
        var sort_id = this.select_sort.id;

        var params = {
          // ここにクエリパラメータを指定する
          new_flg_client: new_flg_client, // 20231004 新井追記
          new_flg_order: new_flg_order, // 20231004 新井追記
          op_mediums: op_mediums,
          key_words: key_words,
          industries: industries,
          honsya_prefs: honsya_prefs,
          kinmu_prefs: kinmu_prefs,
          income_min: income_min,
          income_max: income_max,
          occupation: occupation,
          keep_status: keep_status,
          cp2_client_raids: cp2_client_raids,
          approach_date_start: approach_date_start,
          approach_date_end: approach_date_end,
          except_approach_date_start: except_approach_date_start,
          except_approach_date_end: except_approach_date_end,
          approach_status: approach_status,
          approach_users: approach_users,
          approach_sections: approach_sections,
          cp2_client_id: cp2_client_id,
          lbc_code: lbc_code,
          exit_nomach: exit_nomach,
          exit_nopublic: exit_nopublic,
          page_num: page_num,
          sort_id: sort_id,
          lead_active: lead_active,
          lead_status: lead_status,
          lead_age_from: lead_age_from,
          lead_age_to: lead_age_to,
          lead_gender: lead_gender,
          lead_occupation: lead_occupation,
          lead_prefs: lead_prefs,
          lead_last_school: lead_last_school,
          lead_english_level: lead_english_level,
          lead_now_income_min: lead_now_income_min,
          lead_now_income_max: lead_now_income_max,
          lead_hope_income_min: lead_hope_income_min,
          lead_hope_income_max: lead_hope_income_max,
          lead_company_history_min: lead_company_history_min,
          lead_company_history_max: lead_company_history_max,
          lead_languages: lead_languages,
          lead_skills: lead_skills,
        };

        //ページネーション用に検索条件保存しておく
        this.search_param = params;
        // console.log(params)
        var config = {
          method: 'GET',
          url: 'api/v1/search',
          params: params,
          responseType: 'json',
        };

        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        this.total_count = response.data['total_count'];
        this.total_count_disp = response.data['total_count'].toLocaleString(); //企業件数
        this.ops = response.data['results']; //データ戻し
        this.contact_hstry_item.contact_hstry_bk = response.data['results'].map((item) => item['contact_histry']);
        this.LbcList = response.data['LbcList'];
        this.login_staff_no = response.data['login_staff_no'];
        this.login_staff_name = response.data['login_staff_name'];
        this.login_staff_section = response.data['login_staff_section'];

        if (this.ops.length == 0) {
          this.loading = false;
          window.alert('検索結果が０件でした。条件を変更して再度お試しください。');
          return;
        }

        //ためしまだ
        var foundation_y = '';
        var foundation_m = '';

        for (let i = 0; i < response.data['results'].length; i++) {
          //設立年月
          if (this.ops[i]['foundation_ym'] != null) {
            foundation_y = String(this.ops[i]['foundation_ym']).slice(0, 4);
            foundation_m = String(this.ops[i]['foundation_ym']).slice(4);
            this.ops[i]['foundation_ym'] = foundation_y + '年' + foundation_m + '月';
          }
          //金額
          if (this.ops[i]['capital'] != null) {
            this.ops[i]['capital'] = this.ops[i]['capital'].toLocaleString();
          }
          //資本金
          if (this.ops[i]['amount_sales'] != null) {
            this.ops[i]['amount_sales'] = this.ops[i]['amount_sales'].toLocaleString();
          }
          //年収From
          if (this.ops[i]['order'] != null) {
            for (let j = 0; j < this.ops[i]['order'].length; j++) {
              if (this.ops[i]['order'][j]['order_annual_income_min'] != null) {
                this.ops[i]['order'][j]['order_annual_income_min'] = this.ops[i]['order'][j]['order_annual_income_min'].toLocaleString();
              }
            }
          }
          //年収To
          if (this.ops[i]['order'] != null) {
            for (let j = 0; j < this.ops[i]['order'].length; j++) {
              if (this.ops[i]['order'][j]['order_annual_income_max'] != null) {
                this.ops[i]['order'][j]['order_annual_income_max'] = this.ops[i]['order'][j]['order_annual_income_max'].toLocaleString();
              }
            }
          }
          //キープ日
          if (this.ops[i]['keep_disp_date'] != null) {
            this.ops[i]['keep_disp_date'] = moment(this.ops[i]['keep_disp_date']).format('YYYY/MM/DD HH:mm');
          }
          //連絡履歴：アプローチ日
          if (this.ops[i]['contact_histry'] != null) {
            for (let j = 0; j < this.ops[i]['contact_histry'].length; j++) {
              this.ops[i]['contact_histry'][j]['contact_history_contact_date'] = moment(
                this.ops[i]['contact_histry'][j]['contact_history_contact_date']
              ).format('YYYY/MM/DD HH:mm');
              this.ops[i]['contact_histry'][j]['contact_history_scheduled_date'] = moment(
                this.ops[i]['contact_histry'][j]['contact_history_scheduled_date']
              ).format('YYYY/MM/DD');
              this.ops[i]['contact_histry'][j]['contact_history_body_tippy'] = String(
                this.ops[i]['contact_histry'][j]['contact_history_body']
              ).replace(/\n/g, '<br/>');
            }
          }
        }

        //再検索時の処理
        var len = Object.keys(this.contact_pages).length;
        if (page_num == 1) {
          //ページネーションリセットしたい
          this.client_page = 1;

          //求人詳細リセット
          $('.section').hide();
          $('.default').show();
        }

        //連絡履歴のページを1に戻す
        var pagination_elms = this.$refs;
        for (let i = 0; i < len; i++) {
          this.contact_pages['contact_page_' + i] = 1;
          let key_name = 'paginate' + i;
          if (!pagination_elms[key_name] || !pagination_elms[key_name][0]) {
            continue;
          }
          let target_pagination = pagination_elms[key_name][0];
          target_pagination.innerValue = 1;
        }

        $('.show_trigger').prop('checked', false);

        //ここからキープ取得開始
        this.setinterval = setTimeout(this.keep_interval, 30000);

        this.loading = false;
      },
      async put_keeping(lbc_cd, index) {
        //キープ機能登録用
        this.loading = true;

        var target_op = this.ops[index];
        var now_keep_flg = target_op['keep_disp_flg'];
        var update_keep_flg = 0;
        if (now_keep_flg == '0') {
          update_keep_flg = 1;
        }

        //まずはキープがバッティングしてないかどうか確認する
        var get_params = {
          lbc_cd: [lbc_cd],
        };

        var get_config = {
          method: 'GET',
          url: 'api/v1/keepClient',
          params: get_params,
          responseType: 'json',
        };

        var get_response = await axios.request(get_config);

        var check_flg = get_response.data['results'][0]['keep_flg'];

        if (check_flg == '1' && update_keep_flg == 1) {
          swal({
            title: '',
            text: 'すでに他の人がキープをしています',
            icon: 'error',
          });

          //データ書き換え
          this.ops[index]['keep_disp_flg'] = check_flg;
          this.ops[index]['keep_disp_staff_no'] = get_response.data['results'][0]['staff_no'];
          this.ops[index]['keep_disp_staff_name'] = get_response.data['results'][0]['staff_name'];
          this.ops[index]['keep_disp_section_name'] = get_response.data['results'][0]['section_name'];
          this.ops[index]['keep_disp_date'] = moment(get_response.data['results'][0]['keep_date']).format('YYYY/MM/DD HH:mm');
          this.loading = false;
          return;
        }

        //バッティングしていなければPUT処理開始
        var params = {
          lbc_cd: lbc_cd,
          update_keep_flg: update_keep_flg,
        };

        var config = {
          method: 'PUT',
          url: 'api/v1/keepClient',
          params: params,
          responseType: 'json',
        };
        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        if (response.data['keep_flg'] == 0 && response.data['error_code'] == 'keep_limit_over') {
          swal({
            title: '',
            text: 'キープ数の上限' + response.data['max_keep_count'] + '件に達しているため、キープできません。',
            icon: 'error',
          });

          this.loading = false;
          return;
        }

        //うまくいったら値を変える
        this.ops[index]['keep_disp_flg'] = update_keep_flg;
        this.ops[index]['keep_disp_staff_no'] = this.login_staff_no;
        this.ops[index]['keep_disp_staff_name'] = this.login_staff_name;
        this.ops[index]['keep_disp_section_name'] = this.login_staff_section;
        this.ops[index]['keep_disp_date'] = moment().format('YYYY/MM/DD HH:mm');

        this.loading = false;
      },
      async keep_interval() {
        //キープずっと取得用
        console.log('30秒毎に処理');

        //表示されている企業のキープ状況を取得
        /*
        var keeping_params = {
          "lbc_cd":this.LbcList
        }
        var keeping_confing = {
          method:'GET',
          url:'api/v1/keepClient',
          params:keeping_params,
          responseType: 'json'
        }
        var keeping_response = await axios.request(keeping_confing);
        var keeping_data = keeping_response.data["results"]

        //取得したら全体の企業に戻す
        debugger
        this.ops.forEach(function(element,index){
          Vue.$set(this.ops[index], 'keep_disp_flg', keeping_data[index]["keep_flg"])
          Vue.$set(this.ops[index], 'keep_disp_staff_no', keeping_data[index]["staff_no"])
          Vue.$set(this.ops[index], 'keep_disp_staff_name', keeping_data[index]["staff_name"])
          Vue.$set(this.ops[index], 'keep_disp_staff_section', keeping_data[index]["section_name"])
          Vue.$set(this.ops[index], 'keep_disp_date', moment(keeping_data[index]["keep_date"]).format("YYYY/MM/DD HH:mm"))
          //element['keep_disp_flg'] = keeping_data[index]["keep_flg"]
          //element['keep_disp_staff_no'] = keeping_data[index]["keep_disp_staff_no"]
          //element['keep_disp_staff_name'] = keeping_data[index]["keep_disp_staff_name"]
          //element['keep_disp_staff_section'] = keeping_data[index]["section_name"]
          //element['keep_disp_date'] = moment(keeping_data[index]["keep_date"]).format("YYYY/MM/DD HH:mm")
        });
        keeping_data.forEach(function(element,index){
          var context = this.ops[index]
          this.ops.splice(index,1,context)
        });
        */
      },
      async put_sort(sort) {
        //並び替え選択肢用

        var id = sort.id;
        if (id == '7' || id == '8') {
          if (
            !confirm(
              '処理に時間がかかりますが、よろしいですか。\r\n \r\n※「求職者マッチング条件」を設定していない場合には処理に時間を要します。\r\n　ある程度条件を設定した上でご利用ください。'
            )
          ) {
            return false;
          }
        }
        this.select_sort = sort;
        this.loading = true;

        //キープ取得インターバル削除
        clearTimeout(this.setinterval);

        //再度サーチするよ
        var params = this.search_param;

        params['page_num'] = 1;
        params['sort_id'] = id;
        var config = {
          method: 'GET',
          url: 'api/v1/search',
          params: params,
          responseType: 'json',
        };
        var response = await axios.request(config);

        /////////メイン処理と同じ/////////
        this.total_count = response.data['total_count'];
        this.total_count_disp = response.data['total_count'].toLocaleString(); //企業件数
        this.ops = response.data['results']; //データ戻し
        this.contact_hstry_item.contact_hstry_bk = response.data['results'].map((item) => item['contact_histry']);
        this.LbcList = response.data['LbcList'];
        var foundation_y = '';
        var foundation_m = '';
        for (let i = 0; i < response.data['results'].length; i++) {
          //設立年月
          if (this.ops[i]['foundation_ym'] != null) {
            foundation_y = String(this.ops[i]['foundation_ym']).slice(0, 4);
            foundation_m = String(this.ops[i]['foundation_ym']).slice(4);
            this.ops[i]['foundation_ym'] = foundation_y + '年' + foundation_m + '月';
          }
          //金額
          if (this.ops[i]['capital'] != null) {
            this.ops[i]['capital'] = this.ops[i]['capital'].toLocaleString();
          }
          if (this.ops[i]['amount_sales'] != null) {
            this.ops[i]['amount_sales'] = this.ops[i]['amount_sales'].toLocaleString();
          }

          //年収From
          if (this.ops[i]['order'] != null) {
            for (let j = 0; j < this.ops[i]['order'].length; j++) {
              if (this.ops[i]['order'][j]['order_annual_income_min'] != null) {
                this.ops[i]['order'][j]['order_annual_income_min'] = this.ops[i]['order'][j]['order_annual_income_min'].toLocaleString();
              }
            }
          }
          //年収To
          if (this.ops[i]['order'] != null) {
            for (let j = 0; j < this.ops[i]['order'].length; j++) {
              if (this.ops[i]['order'][j]['order_annual_income_max'] != null) {
                this.ops[i]['order'][j]['order_annual_income_max'] = this.ops[i]['order'][j]['order_annual_income_max'].toLocaleString();
              }
            }
          }
          //キープ日
          if (this.ops[i]['keep_disp_date'] != null) {
            this.ops[i]['keep_disp_date'] = moment(this.ops[i]['keep_disp_date']).format('YYYY/MM/DD HH:mm');
          }
          //連絡履歴：アプローチ日
          if (this.ops[i]['contact_histry'] != null) {
            for (let j = 0; j < this.ops[i]['contact_histry'].length; j++) {
              this.ops[i]['contact_histry'][j]['contact_history_contact_date'] = moment(
                this.ops[i]['contact_histry'][j]['contact_history_contact_date']
              ).format('YYYY/MM/DD HH:mm');
              this.ops[i]['contact_histry'][j]['contact_history_scheduled_date	'] = moment(
                this.ops[i]['contact_histry'][j]['contact_history_scheduled_date	']
              ).format('YYYY/MM/DD');
              this.ops[i]['contact_histry'][j]['contact_history_body_tippy'] = String(
                this.ops[i]['contact_histry'][j]['contact_history_body']
              ).replace(/\n/g, '<br/>');
            }
          }
        }
        /////////メイン処理と同じ/////////
        //ここからキープ取得開始
        this.setinterval = setTimeout(this.keep_interval, 30000);

        this.loading = false;
      },
      put_appoint(e) {
        //アポの選択肢用
        var name = e.name;
        this.contact_hstry_item.select_appoint = name;
      },
      sort_letaring(e) {
        //select_modal用
        // Dropdown Menu
        $(e.target.parentElement.parentElement).attr('tabindex', 1).focus();
        $(e.target.parentElement.parentElement).toggleClass('active');
        $(e.target.parentElement.parentElement).find('.dropdown-menu').slideToggle(300);
      },
      async clickCallback_contact(pageNum) {
        //連絡履歴ページネーションクリック関数

        var pagination_elms = this.$refs;

        var targetIndex = 0; //何番目のページネーションが押されたを取得

        for (let i = 0; i < 10; i++) {
          let key_name = 'paginate' + i;
          if (!pagination_elms[key_name] || !pagination_elms[key_name][0]) {
            continue;
          }

          let target_pagination = pagination_elms[key_name][0];
          let inner_active = target_pagination.innerValue;
          let target_el = target_pagination.$el;
          let target_children = Array.from(target_el.children);

          let target_calassNames = target_children.map((elem) => elem.className);

          const target_index = target_calassNames.indexOf('page-numbers active');

          if (target_index != inner_active) {
            targetIndex = i;
            break;
          }
        }

        //page_numとtargetIndexを使用してというかあれだね、それを送ればいいんだね
        var LbcCd = this.LbcList[targetIndex];

        var params = {
          page_num: pageNum,
          LbcCd: LbcCd,
        };

        var config = {
          method: 'GET',
          url: 'api/v1/contactHistory',
          params: params,
          responseType: 'json',
        };

        var response = await axios.request(config);

        //データを対象の企業の連絡履歴に戻すops[target_index]["contact_histry"]
        var results = response.data['results'];
        this.ops[targetIndex]['contact_history_total_count'] = results[0]['total_count'];
        this.ops[targetIndex]['contact_histry'] = results;
        for (let j = 0; j < this.ops[targetIndex]['contact_histry'].length; j++) {
          this.ops[targetIndex]['contact_histry'][j]['contact_history_contact_date'] = moment(
            this.ops[targetIndex]['contact_histry'][j]['contact_history_contact_date']
          ).format('YYYY/MM/DD HH:mm');
          this.ops[targetIndex]['contact_histry'][j]['contact_history_scheduled_date'] = moment(
            this.ops[targetIndex]['contact_histry'][j]['contact_history_scheduled_date']
          ).format('YYYY/MM/DD');
          this.ops[targetIndex]['contact_histry'][j]['contact_history_body_tippy'] = String(
            this.ops[targetIndex]['contact_histry'][j]['contact_history_body']
          ).replace(/\n/g, '<br/>');
        }
      },
      async post_contacths(lbc_cd) {
        //連絡履歴登録用

        //アプローチIDを出す
        var select_appoint = this.contact_hstry_item.select_appoint;
        var target_approach_array = this.contact_hstry_item.approach.filter((u) => u.name == select_appoint);
        if (target_approach_array.length == 0) {
          swal({
            title: '',
            text: 'アプローチ結果を選択してください',
            icon: 'error',
          }).then(function (result) {
            return;
          });
        }
        var approach_id = target_approach_array[0]['id'];
        var appoint_date = '';
        if (this.contact_hstry_item.appoint_date != '') {
          appoint_date = moment(this.contact_hstry_item.appoint_date).format('YYYY-MM-DD HH:mm:ss');
        }

        var params = {
          lbc_cd: lbc_cd,
          approach_date: moment(this.contact_hstry_item.approach_date).format('YYYY-MM-DD HH:mm:ss'),
          appoint_date: appoint_date,
          approach_comment: this.contact_hstry_item.approach_comment,
          approach_id: approach_id,
        };

        var config = {
          method: 'POST',
          url: 'api/v1/contactHistory',
          params: params,
        };

        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        //値のクリアと連絡履歴の反映について
        this.contact_hstry_item.approach_date = '';
        this.contact_hstry_item.appoint_date = '';
        this.contact_hstry_item.approach_comment = '';

        var params = {
          page_num: 1,
          LbcCd: lbc_cd,
        };

        var targetIndex = this.LbcList.indexOf(lbc_cd);

        var config = {
          method: 'GET',
          url: 'api/v1/contactHistory',
          params: params,
          responseType: 'json',
        };

        var response = await axios.request(config);

        //データを対象の企業の連絡履歴に戻すops[target_index]["contact_histry"]
        var results = response.data['results'];
        this.ops[targetIndex]['contact_history_total_count'] = results[0]['total_count'];
        this.ops[targetIndex]['contact_histry'] = results;
        for (let j = 0; j < this.ops[targetIndex]['contact_histry'].length; j++) {
          this.ops[targetIndex]['contact_histry'][j]['contact_history_contact_date'] = moment(
            this.ops[targetIndex]['contact_histry'][j]['contact_history_contact_date']
          ).format('YYYY/MM/DD HH:mm');
          this.ops[targetIndex]['contact_histry'][j]['contact_history_scheduled_date'] = moment(
            this.ops[targetIndex]['contact_histry'][j]['contact_history_scheduled_date']
          ).format('YYYY/MM/DD');
        }
      },
      async search_custmtel(lbc_cd) {
        //カスタム電話番号取得用

        var params = this.search_param;

        var params = {
          lbc_cd: lbc_cd,
        };

        var config = {
          method: 'GET',
          url: 'api/v1/customTel',
          params: params,
          responseType: 'json',
        };

        var response = await axios.request(config);

        this.custm_tel_items.custm_hstry = response.data['results'];
      },
      async post_custmtel(lbc_cd, index) {
        //カスタム電話番号登録用

        var params = {
          lbc_cd: lbc_cd,
          tel: this.custm_tel_items.custm_tel,
        };

        var config = {
          method: 'POST',
          url: 'api/v1/customTel',
          params: params,
        };

        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        //lbc_cdから配列検索して、tel_customに値入れてあげる
        this.ops.filter((elem) => elem.lbc_cd == lbc_cd)[0]['tel_custom'] = this.custm_tel_items.custm_tel;

        //値のクリアと追加…これはAPIではなく変数に入れるだけにしたいね
        this.custm_tel_items.custm_tel = '';

        var config = {
          method: 'GET',
          url: 'api/v1/customTel',
          params: params,
          responseType: 'json',
        };

        var response = await axios.request(config);

        this.custm_tel_items.custm_hstry = response.data['results'];

        //最終更新者戻す
        var targetIndex = this.LbcList.indexOf(lbc_cd);
        var results = response.data['results'];
        this.ops[targetIndex]['tel_custom_disp_update_info'] = results[0]['disp_update_disp'];

        //もしクレームなら
        if (this.contact_hstry_item.select_appoint == 'クレーム') {
          this.ops[index].alert_flg = 1;
        }
      },

      //クリア機能------------------------------------------
      clear_search() {
        //新着フラグ 20231004 新井追記
        for (let i = 0; i < this.new_flgs.length; i++) {
          this.new_flgs[i]['checked'] = false;
        }
        //求人媒体
        for (let i = 0; i < this.op_mediums.length; i++) {
          this.op_mediums[i]['checked'] = '';
        }
        //業種
        this.industry_data.splice(0, this.industry_data.length);
        setTimeout(() => {
          // ここに遅らせた後に行いたい処理を書く。関数でもOK
          viewChangeIndustry();
        }, 100);

        //職種
        this.occupation_data.splice(0, this.occupation_data.length);

        //企業名
        this.client_words = '';

        //年収
        this.income_min = 0;
        this.income_max = 1000000000;
        //キープステータス
        for (let i = 0; i < this.keep_status.length; i++) {
          this.keep_status[i]['checked'] = '';
        }

        //アプローチ日時
        this.approach_date_start = '';
        this.approach_date_end = '';

        // アプローチ日時(指定期間アプローチなし検索)
        this.except_approach_date_start = '';
        this.except_approach_date_end = '';

        //アプローチ最新結果
        for (let i = 0; i < this.approach_status.length; i++) {
          this.approach_status[i]['checked'] = '';
        }
        //アプローチ者
        $('.js-example-basic-multiple').val(null).trigger('change');
        //アプローチ所属
        $('.js-example-basic-multiple').val(null).trigger('change');
        //CP2企業ID
        this.cp2_client_id = '';
        //LBCコード
        this.lbc_code = '';
      },

      //マッチング求職者クリア
      clear_lead_search() {
        //求職者ステータス
        for (let i = 0; i < this.lead_status.length; i++) {
          this.lead_status[i]['checked'] = '';
        }
        //年齢from
        this.lead_age_from = '';
        //年齢to
        this.lead_age_to = '';
        //性別
        for (let i = 0; i < this.lead_gender.length; i++) {
          this.lead_gender[i]['checked'] = '';
        }
        //最終学歴
        $('.school').val(null).trigger('change');
        //英語レベル
        $('.english').val(null).trigger('change');

        this.lead_now_income_min = '';
        this.lead_now_income_max = '';

        this.lead_hope_income_min = '';
        this.lead_hope_income_max = '';
        this.lead_company_history_min = null;
        this.lead_company_history_max = null;
        $('.languages').val(null).trigger('change');
      },
      //業種クリア
      clear_indsctg() {
        this.industry_data.splice(0, this.industry_data.length);
        setTimeout(() => {
          // ここに遅らせた後に行いたい処理を書く。関数でもOK
          viewChangeIndustry();
        }, 100);
      },
      //本社所在地クリア
      clear_honsya_pref() {
        for (let i = 0; i < this.honsya_prefs.length; i++) {
          this.honsya_prefs[i]['checked'] = '';
        }
      },
      //勤務地クリア
      clear_kin_pref() {
        for (let i = 0; i < this.kinmu_prefs.length; i++) {
          this.kinmu_prefs[i]['checked'] = '';
        }
      },
      //職種クリア
      clear_occupation() {
        this.occupation_data.splice(0, this.occupation_data.length);
      },
      //資格クリア
      clear_skills() {
        this.lead_skills_data.splice(0, this.lead_skills_data.length);
      },
      //希望職種クリア
      clear_lead_occupation() {
        this.lead_occupation_data.splice(0, this.lead_occupation_data.length);
      },
      //希望勤務地クリア
      clear_lead_prefs() {
        for (let i = 0; i < this.lead_prefs.length; i++) {
          this.lead_prefs[i]['checked'] = '';
        }
      },
      //-----------------クリア機能ここまで

      on_contacthstry(e) {
        //連絡履歴の追加推したときに日程反映したい

        var now = moment().format(); // 2020-04-22T22:14:25+09:00
        var now2 = moment().format('YYYY-MM-DDTHH:mm'); // 2020-04-22T22:14:25
        this.contact_hstry_item.approach_date = now2;
      },
      all_selected_indust(all, index) {
        //すべて選択用
        var element_all = all.target;
        var parent_element = element_all.parentElement;
        let child_elements = parent_element.querySelectorAll('input');
        for (var i = 0; i < child_elements.length; i++) {
          if (element_all.checked) {
            child_elements[i].checked = true;
          } else {
            child_elements[i].checked = false;
          }
        }
        var target02 = this.industries[index]['industory_02'];
        var len = target02.length;
        var new_arr = [];
        for (var i = 0; i < len; i++) {
          var target03 = target02[i]['industory_03'];
          var ids_03 = target03.map((elem) => elem['id_full']);
          Array.prototype.push.apply(new_arr, ids_03);
        }
        if (element_all.checked) {
          Array.prototype.push.apply(this.industry_data, new_arr);
        } else {
          this.industry_data = this.industry_data.filter((i) => new_arr.indexOf(i) == -1);
        }
      },
      all_selected_occup(all, index) {
        //すべて選択用
        var element_all = all.target;
        var parent_element = element_all.parentElement;
        let child_elements = parent_element.querySelectorAll('input');
        for (var i = 0; i < child_elements.length; i++) {
          if (element_all.checked) {
            child_elements[i].checked = true;
          } else {
            child_elements[i].checked = false;
          }
        }
        var target02 = this.occupation[index]['industory_02'];
        var len = target02.length;
        var new_arr = [];
        for (var i = 0; i < len; i++) {
          var target03 = target02[i]['industory_03'];
          var ids_03 = target03.map((elem) => elem['id']);
          Array.prototype.push.apply(new_arr, ids_03);
        }
        if (element_all.checked) {
          Array.prototype.push.apply(this.occupation_data, new_arr);
        } else {
          this.occupation_data = this.occupation_data.filter((i) => new_arr.indexOf(i) == -1);
        }
      },
      all_selected_lead_occup(all, index) {
        //すべて選択用
        var element_all = all.target;
        var parent_element = element_all.parentElement;
        let child_elements = parent_element.querySelectorAll('input');
        for (var i = 0; i < child_elements.length; i++) {
          if (element_all.checked) {
            child_elements[i].checked = true;
          } else {
            child_elements[i].checked = false;
          }
        }

        var target02 = this.lead_occupation[index]['industory_02'];
        var len = target02.length;
        var new_arr = [];
        for (var i = 0; i < len; i++) {
          var target03 = target02[i]['industory_03'];
          var ids_03 = target03.map((elem) => elem['id']);
          Array.prototype.push.apply(new_arr, ids_03);
        }
        if (element_all.checked) {
          Array.prototype.push.apply(this.lead_occupation_data, new_arr);
        } else {
          this.lead_occupation_data = this.lead_occupation_data.filter((i) => new_arr.indexOf(i) == -1);
        }
      },
      async show_detail_order(e, order_sk, client_name) {
        //詳細画面表示用

        $('.section').hide();
        $('.section')
          .not($($(e.target).attr('href')))
          .hide();
        $('.default').hide();
        $($(e.target).attr('href')).fadeToggle(200);
        e.preventDefault();

        //詳細表示と取得
        var params = {
          trn_order_sk: order_sk,
        };
        var detail_order = {
          method: 'GET',
          url: 'api/v1/getOrder',
          params: params,
          responseType: 'json',
        };
        var response_detail_order = await axios.request(detail_order);

        var target_data = response_detail_order.data['results'][0];
        this.company_name = client_name;
        this.offer_ttl = target_data['title'];
        this.job_context = target_data['job_description'].substr(0, 115) + '...';
        this.open_date = moment(target_data['regist_date']).format('YYYY/MM/DD');
        this.url = target_data['url'];
        if (target_data['media_id'] == 1) {
          this.job_media = this.op_mediums[0].name;
        } else {
          this.job_media = this.op_mediums[1].name;
        }

        //マッチング求職者一覧のAPI
        params = this.search_param;
        params['trn_order_sk'] = order_sk;

        var match_career = {
          method: 'GET',
          url: 'api/v1/matchCareer',
          params: params,
          responseType: 'json',
        };
        var response_match_career = await axios.request(match_career);
        this.match_career = response_match_career.data['results'];
        this.match_num = this.match_career.length;
      },
      async get_career(trn_career_sk) {
        //求職者情報取得用
        var params = {
          trn_career_sk: trn_career_sk,
        };
        var detail_career = {
          method: 'GET',
          url: 'api/v1/getCareer',
          params: params,
          responseType: 'json',
        };
        var response_detail_career = await axios.request(detail_career);
        var career_data = response_detail_career.data['results'][0];

        this.cp2_careerid = career_data.career_id;
        this.career_data = career_data.career_data;
        this.lstschlname = career_data.lstschlname;
        this.expcomp_num = career_data.expcomp_num;
        this.exp_industry = career_data.exp_industry;
        this.exp_occupation = career_data.exp_occupation;
        this.wish_industry = career_data.wish_industry;
        this.wish_occupation = career_data.wish_occupation;
        this.wish_wkpref = career_data.wish_wkpref;
        this.wishannualincm_num = career_data.wishannualincm_num;

        this.wkperiode_date1 = career_data.wkperiode_date1;
        this.compname1 = career_data.compname1;
        this.dept1 = career_data.dept1;
        this.indsctgname1 = career_data.indsctgname1;
        this.annualincm1 = career_data.annualincm1;
        this.wkcontents1 = career_data.wkcontents1;
        this.wkperiode_date2 = career_data.wkperiode_date2;
        this.compname2 = career_data.compname2;
        this.dept2 = career_data.dept2;
        this.indsctgname2 = career_data.indsctgname2;
        this.annualincm2 = career_data.annualincm2;
        this.wkcontents2 = career_data.wkcontents2;
        this.wkperiode_date3 = career_data.wkperiode_date3;
        this.compname3 = career_data.compname3;
        this.dept3 = career_data.dept3;
        this.indsctgname3 = career_data.indsctgname3;
        this.annualincm3 = career_data.annualincm3;
        this.wkcontents3 = career_data.wkcontents3;
        this.wkperiode_date4 = career_data.wkperiode_date4;
        this.compname4 = career_data.compname4;
        this.dept4 = career_data.dept4;
        this.indsctgname4 = career_data.indsctgname4;
        this.annualincm4 = career_data.annualincm4;
        this.wkcontents4 = career_data.wkcontents4;
        this.wkperiode_date5 = career_data.wkperiode_date5;
        this.compname5 = career_data.compname5;
        this.dept5 = career_data.dept5;
        this.indsctgname5 = career_data.indsctgname5;
        this.annualincm5 = career_data.annualincm5;
        this.wkcontents5 = career_data.wkcontents5;

        this.Schcperiode_date1 = career_data.Schcperiode_date1;
        this.gradname1 = career_data.gradname1;
        this.schlname1 = career_data.schlname1;
        this.schldeptname1 = career_data.schldeptname1;
        this.Schcperiode_date2 = career_data.Schcperiode_date2;
        this.gradname2 = career_data.gradname2;
        this.schlname2 = career_data.schlname2;
        this.schldeptname2 = career_data.schldeptname2;
        this.Schcperiode_date3 = career_data.Schcperiode_date3;
        this.gradname3 = career_data.gradname3;
        this.schlname3 = career_data.schlname3;
        this.schldeptname3 = career_data.schldeptname3;
        this.Schcperiode_date4 = career_data.Schcperiode_date4;
        this.gradname4 = career_data.gradname4;
        this.schlname4 = career_data.schlname4;
        this.schldeptname4 = career_data.schldeptname4;
        this.Schcperiode_date5 = career_data.Schcperiode_date5;
        this.gradname5 = career_data.gradname5;
        this.schlname5 = career_data.schlname5;
        this.schldeptname5 = career_data.schldeptname5;
        this.licensename1 = career_data.licensename1;
        this.qual_date1 = career_data.qual_date1;
        this.licensename2 = career_data.licensename2;
        this.qual_date2 = career_data.qual_date2;
        this.licensename3 = career_data.licensename3;
        this.qual_date3 = career_data.qual_date3;
        this.licensename4 = career_data.licensename4;
        this.qual_date4 = career_data.qual_date4;
        this.licensename5 = career_data.licensename5;
        this.qual_date5 = career_data.qual_date5;

        this.toeic = career_data.toeic;
        this.toefl = career_data.toefl;
        this.english_level = career_data.english_level;
        this.otrlang1 = career_data.otrlang1;
        this.otrlang2 = career_data.otrlang2;
        this.otrlang3 = career_data.otrlang3;
      },
      async post_params() {
        //検索条件保存
        var title = this.search_conditions;

        //タイトルなければエラー
        if (title == '') {
          swal({
            title: '',
            text: '検索条件名を入力して下さい',
            icon: 'error',
          });
          return;
        }

        //ここから企業求人検索用----------------------
        var new_flg_client = this.new_flgs[0].checked; // 20231004 新井追記
        var new_flg_order = this.new_flgs[1].checked; // 20231004 新井追記
        var op_mediums = this.op_mediums.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var key_words = this.client_words;
        var industries = this.industry_data;
        var industries_text = document.getElementById('disp_industries').textContent;

        var honsya_prefs = this.honsya_prefs.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var kinmu_prefs = this.kinmu_prefs.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var income_min = this.income_min;
        var income_max = this.income_max;
        var occupation = this.occupation_data;

        var keep_status = this.keep_status.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);

        var cp2_client_raids = $('.cp2_user_id').val();

        var approach_date_start = this.approach_date_start;
        var approach_date_end = this.approach_date_end;

        var except_approach_date_start = this.except_approach_date_start;
        var except_approach_date_end = this.except_approach_date_end;

        var approach_status = this.approach_status
          .filter((value) => value['checked'] == true || value['checked'] == 'checked')
          .map((value) => value['id']);

        var approach_users = $('.approach_users').val();

        var approach_sections = $('.approach_sections').val();

        var cp2_client_id = this.cp2_client_id;
        var lbc_code = this.lbc_code;
        var sort_id = this.select_sort.id;

        //ここから求職者マッチング情報----------------------
        var lead_active = this.lead_active;
        var lead_status = this.lead_status.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var lead_age_from = this.lead_age_from;
        var lead_age_to = this.lead_age_to;
        var lead_gender = this.lead_gender.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var lead_occupation = this.lead_occupation_data;

        var lead_prefs = this.lead_prefs.filter((value) => value['checked'] == true || value['checked'] == 'checked').map((value) => value['id']);
        var lead_last_school = $('.school').val();
        var lead_english_level = $('.english').val();
        var lead_now_income_min = this.lead_now_income_min;
        var lead_now_income_max = this.lead_now_income_max;
        var lead_hope_income_min = this.lead_hope_income_min;
        var lead_hope_income_max = this.lead_hope_income_max;
        var lead_company_history_min = this.lead_company_history_min;
        var lead_company_history_max = this.lead_company_history_max;
        var lead_languages = $('.languages').val();
        var lead_skills = this.lead_skills_data;
        var obj = {
          new_flg_client: new_flg_client, // 20231004 新井追記
          new_flg_order: new_flg_order, // 20231004 新井追記
          op_mediums: op_mediums,
          key_words: key_words,
          industries: industries,
          industries_text: industries_text,
          honsya_prefs: honsya_prefs,
          kinmu_prefs: kinmu_prefs,
          income_min: income_min,
          income_max: income_max,
          occupation: occupation,
          keep_status: keep_status,
          cp2_client_raids: cp2_client_raids,
          approach_date_start: approach_date_start,
          approach_date_end: approach_date_end,
          except_approach_date_start: except_approach_date_start,
          except_approach_date_end: except_approach_date_end,
          approach_status: approach_status,
          approach_users: approach_users,
          approach_sections: approach_sections,
          cp2_client_id: cp2_client_id,
          lbc_code: lbc_code,
          lead_active: lead_active,
          lead_status: lead_status,
          lead_age_from: lead_age_from,
          lead_age_to: lead_age_to,
          lead_gender: lead_gender,
          lead_occupation: lead_occupation,
          lead_prefs: lead_prefs,
          lead_last_school: lead_last_school,
          lead_english_level: lead_english_level,
          lead_now_income_min: lead_now_income_min,
          lead_now_income_max: lead_now_income_max,
          lead_hope_income_min: lead_hope_income_min,
          lead_hope_income_max: lead_hope_income_max,
          lead_company_history_min: lead_company_history_min,
          lead_company_history_max: lead_company_history_max,
          lead_languages: lead_languages,
          lead_skills: lead_skills,
        };

        var params_data = JSON.stringify(obj);
        var params = {
          title: title,
          content: params_data,
        };

        var config = {
          method: 'POST',
          url: 'api/v1/searchParameter',
          params: params,
          responseType: 'json',
        };

        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        //うまくいったらOKとクリアと閉じる
        swal({
          title: 'success!',
          text: '検索条件を保存しました',
          icon: 'success',
        });
        this.search_conditions = '';

        var trigger_save = document.getElementById('trigger_save');
        trigger_save.checked = false;
      },
      async get_params() {
        //検索条件取得

        var params = {
          trn_search_parameter_sk: '',
        };
        var config = {
          method: 'GET',
          url: 'api/v1/searchParameter',
          responseType: 'json',
        };
        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        this.search_contents = response.data['results'];

        this.search_contents.forEach((element) => {
          element['audit_created_at'] = moment(element['audit_created_at']).format('YYYY/MM/DD hh:mm');
          element['checked'] = '';
        });
      },
      async put_params(s_content, deleted_flg) {
        //検索条件更新

        var params = {
          trn_search_parameter_sk: s_content.trn_search_parameter_sk,
          title: s_content.title,
          disp_order: s_content.disp_order,
          deleted_flg: deleted_flg,
        };

        var config = {
          method: 'PUT',
          url: 'api/v1/searchParameter',
          params: params,
        };
        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }

        swal({
          title: 'success!',
          text: '検索条件を更新しました',
          icon: 'success',
        });

        //更新した結果戻す
        config = {
          method: 'GET',
          url: 'api/v1/searchParameter',
          responseType: 'json',
        };
        response = await axios.request(config);

        this.search_contents = response.data['results'];

        this.search_contents.forEach((element) => {
          element['audit_created_at'] = moment(element['audit_created_at']).format('YYYY/MM/DD hh:mm');
          element['checked'] = '';
        });
      },
      async set_params() {
        //検索条件取得とセット

        var target_content = this.select_save;

        //無かったらリターン
        if (target_content.length == 0) {
          swal({
            title: '',
            text: 'セットしたい検索条件を選択してください',
            icon: 'error',
          });
          return;
        }
        //SKで指定
        var target_sk = target_content;

        var params = {
          trn_search_parameter_sk: target_sk,
        };

        var config = {
          method: 'GET',
          url: 'api/v1/searchParameter',
          params: params,
          responseType: 'json',
        };

        try {
          var response = await axios.request(config);
        } catch (e) {
          var error_401 = e.message.indexOf('401') > -1;
          if (error_401) {
            //セッションエラーとページ遷移
            window.alert('セッションが切れました。ログイン画面に戻ります。');
            window.location.href = './';
          }
        }
        var data = JSON.parse(response.data['results'][0]['content']);

        //取得したらレスポンスを変数に入れる
        //ここから企業求人検索用----------------------
        this.new_flgs[0].checked = data['new_flg_client']; // 20231004 新井追記
        this.new_flgs[1].checked = data['new_flg_order']; // 20231004 新井追記
        this.op_mediums.forEach(function (element) {
          var check = data['op_mediums'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        this.client_words = data['key_words'];
        this.industry_data = data['industries'];
        this.industries.forEach(function (element) {
          var check = data['industries'].indexOf(element['id_full']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        document.getElementById('disp_industries').textContent = data['industries_text'];

        this.honsya_prefs.forEach(function (element) {
          var check = data['honsya_prefs'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        this.kinmu_prefs.forEach(function (element) {
          var check = data['kinmu_prefs'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        this.income_min = data['income_min'];
        this.income_max = data['income_max'];
        this.occupation_data = data['occupation'];
        this.occupation.forEach(function (element) {
          var check = data['occupation'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });

        this.keep_status.forEach(function (element) {
          var check = data['keep_status'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });

        var cp2_client_raids = data['cp2_client_raids'];
        $('.cp2_user_id').val(cp2_client_raids);
        $('.cp2_user_id').val(cp2_client_raids).trigger('change');

        this.approach_date_start = data['approach_date_start'];
        this.approach_date_end = data['approach_date_end'];

        this.except_approach_date_start = data['except_approach_date_start'];
        this.except_approach_date_end = data['except_approach_date_end'];

        this.approach_status.forEach(function (element) {
          var check = data['approach_status'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = true;
          } else {
            element['checked'] = '';
          }
        });
        var approach_users = data['approach_users'];
        $('.approach_users').val(approach_users);
        $('.approach_users').val(approach_users).trigger('change');

        var approach_sections = data['approach_sections'];
        $('.approach_sections').val(approach_sections);
        $('.approach_sections').val(approach_sections).trigger('change');

        this.cp2_client_id = data['cp2_client_id'];
        this.lbc_code = data['lbc_code'];

        //ここから求職者マッチング情報----------------------
        this.lead_active = data['lead_active'];

        this.lead_active_master.forEach(function (element, index) {
          var check = data['lead_active'] == element['id'];
          if (check) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });

        this.lead_status.forEach(function (element) {
          var check = data['lead_status'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        this.lead_age_from = data['lead_age_from'];
        this.lead_age_to = data['lead_age_to'];
        this.lead_gender.forEach(function (element) {
          var check = data['lead_gender'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        this.lead_occupation_data = data['lead_occupation'];
        this.lead_occupation_data.forEach(function (element) {
          var check = data['lead_occupation'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });
        this.lead_prefs.forEach(function (element) {
          var check = data['lead_prefs'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });

        var lead_last_school = data['lead_last_school'];
        $('.school').val(lead_last_school);
        $('.school').val(lead_last_school).trigger('change');

        var lead_english_level = data['lead_english_level'];
        $('.english').val(lead_english_level);
        $('.english').val(lead_english_level).trigger('change');

        this.lead_now_income_min = data['lead_now_income_min'];
        this.lead_now_income_max = data['lead_now_income_max'];
        this.lead_hope_income_min = data['lead_hope_income_min'];
        this.lead_hope_income_max = data['lead_hope_income_max'];
        this.lead_company_history_min = data['lead_company_history_min'];
        this.lead_company_history_max = data['lead_company_history_max'];

        var lead_languages = data['lead_languages'];
        $('.languages').val(lead_languages);
        $('.languages').val(lead_languages).trigger('change');

        this.lead_skills_data = data['lead_skills'];
        this.lead_skills.forEach(function (element) {
          var check = data['lead_skills'].indexOf(element['id']);
          if (check != -1) {
            element['checked'] = 'checked';
          } else {
            element['checked'] = '';
          }
        });

        var min = data['income_min'] / 10000;
        var max = data['income_max'] / 10000;
        var min_text;
        var max_text;

        if (min == 0) {
          min_text = '下限なし';
        } else {
          min_text = String(min) + '万円';
        }
        if (max == 100000) {
          max_text = '上限なし';
        } else {
          max_text = String(max) + '万円';
        }

        //スライダー再編集
        document.getElementsByClassName('slider-container')[0].children[1].remove();
        var slider = new rSlider({
          target: '#slider',
          values: ['下限なし', '300万円', '400万円', '500万円', '600万円', '700万円', '上限なし'],
          range: true,
          set: [min_text, max_text],
          onChange: function (vals) {
            console.log(vals);
            //カンマで配列に分ける
            var min = vals.split(',')[0];
            var max = vals.split(',')[1];
            console.log(min);
            console.log(max);

            if (min != '下限なし') {
              min = min.replace('万円', '');
              min = Number(min) * 10000;
            } else {
              min = 0; //割と適当
            }

            if (max != '上限なし') {
              max = max.replace('万円', '');
              max = Number(max) * 10000;
            } else {
              max = 1000000000; //割と適当
            }
            //代入
            vm.income_min = min;
            vm.income_max = max;
          },
        });

        //すべてのチェックボックス外したい
        $('.all_selecor').prop('checked', false);

        swal({
          title: 'success!',
          text: '検索条件をセットしました',
          icon: 'success',
        });

        var modal_check = document.getElementById('modal-check');
        modal_check.checked = false;
      },
      page_jump() {
        //ページジャンプ

        var page_jump_num = Number(this.page_jump_num);
        var max_page_num = Math.ceil(this.total_count / 10);

        //ページネーションと同じ値なら何もしない
        if (this.client_page == page_jump_num) {
          return;
        }

        // null、空文字、数値以外、負の値の場合処理を終了
        if (page_jump_num == null || page_jump_num == 0 || !Number.isInteger(page_jump_num) || Math.sign(page_jump_num) == -1) {
          swal({
            title: '',
            text: '不正な値が指定されています。',
            icon: 'error',
          });
          return;
        } else if (page_jump_num > max_page_num) {
          // 指定ページ数が上限を超えていた場合エラーを出力
          swal({
            title: '',
            text: '指定ページ数が総ページ数を超えています。',
            icon: 'error',
          });
          return;
        }

        // ページネーションの値を変更
        this.client_page = page_jump_num;

        // 検索APIを実行
        this.search_client(page_jump_num);

        // 入力した値をクリア
        this.page_jump_num = null;
      },
    },
    computed: {
      getPageCount_client() {
        //総ページ数算出関数
        return Math.ceil(this.total_count / 10);
      },
      getPageCount_contact(total) {
        //連絡履歴ページ数算出関数
        return Math.ceil(total / 2);
      },
    },
    delimiters: ['[[', ']]'],
  });
})();

// by Omae
// Multipul select
// Table select
function preloader() {
  let table = document.getElementById('save-table');
  let rows = table.querySelectorAll('table tr');

  let backgroundcolor_dict = {};
  let tr_color = window.getComputedStyle(rows[0], '').color;

  rows.forEach((row) => {
    // 行ごとに背景色が異なるため全ての行の変更前の背景色を取得
    backgroundcolor_dict[String(row.rowIndex)] = window.getComputedStyle(row, '').backgroundColor;

    row.addEventListener(
      'click',
      function () {
        // 一度全て元の配色
        rows.forEach((click_row) => {
          click_row.style.backgroundColor = backgroundcolor_dict[String(row.rowIndex)];
          click_row.style.color = tr_color;
        });
        // 選択された行のみ配色変更
        row.style.backgroundColor = '#E6F3FF';
        row.style.color = '#333333';

        // if (row.querySelector("input").type == "radio") {
        //     row.querySelector('input[type="radio"]').checked = true;
        // }
        if (row.querySelector('input').type == 'checkbox') {
          if (row.querySelector('input[type="checkbox"]').checked == false) {
            row.querySelector('input[type="checkbox"]').checked = true;
          } else {
            row.querySelector('input[type="checkbox"]').checked = false;
          }
        }
      },
      false
    );
  });
}

window.onload = preloader;

// appoint select
function viewChange() {
  if (document.getElementById('item_history_result')) {
    id = document.getElementById('item_history_result').value;
    if (id == 'result03') {
      document.getElementById('item_date_approach_plan').style.display = 'block';
    } else if ('') {
      document.getElementById('item_date_approach_plan').style.display = 'none';
    }
  }
  window.onload = viewChange;
}
// select multipul
$(document).ready(function () {
  $('.js-example-basic-multiple').select2();
  viewChangeIndustry();

  $('.set_disp_info').click(function () {
    viewChangeIndustry();
  });
});

// Display Industry(jQuery)
function viewChangeIndustry() {
  var flg = null;
  var disp_word = '';
  $('.industry_data').each(function (i, data) {
    flg = $(data).prop('checked');

    if (flg == true) {
      disp_word = disp_word + $(data).data('industry_name') + '／';
    }
  });
  disp_word = disp_word.slice(0, -1);

  document.getElementById('disp_industries').textContent = disp_word;
}
