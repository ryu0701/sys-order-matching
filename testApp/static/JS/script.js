/* vueファイルにまとめるため不要
// bar UI
(function() {
    "use strict";
    var init = function() {

        var slider = new rSlider({
            target: "#slider",
            values: ['下限なし', '300万円', '400万円', '500万円', '600万円', '700万円', '上限なし'],
            range: true,
            set: ['300万円', '500万円'],
            onChange: function(vals) {
                console.log(vals);
            },
        });
    };
    window.onload = init;
})();

// detail UI
$(function() {
    $('.section').hide();

    $('.secList').on('click', function() {
        $('.section').not($($(this).attr('href'))).hide();
        $('.default').hide();
        $($(this).attr('href')).fadeToggle(200);
    });
});

// Multipul select
$(function() {
    $(".cp_tabpanels input[type='checkbox']").on("click", function() {
        $(this).parent().find('input').prop("checked", $(this).prop("checked"));
    });
});

// Dropdown Menu
$('.dropdown').click(function() {
    $(this).attr('tabindex', 1).focus();
    $(this).toggleClass('active');
    $(this).find('.dropdown-menu').slideToggle(300);
});
$('.dropdown').focusout(function() {
    $(this).removeClass('active');
    $(this).find('.dropdown-menu').slideUp(300);
});
$('.dropdown .dropdown-menu li').click(function() {
    $(this).parents('.dropdown').find('span').text($(this).text());
    $(this).parents('.dropdown').find('input').attr('value', $(this).attr('id'));
});

$('.dropdown-menu li').click(function() {
    var input = '<strong>' + $(this).parents('.dropdown').find('input').val() + '</strong>',
        msg = '<span class="msg">Hidden input value: ';
    $('.msg').html(msg + input + '</span>');
});

MicroModal.init();

// Table select
function preloader() {
    let table = document.getElementById("save-table");
    let rows = table.querySelectorAll("table tr");

    let backgroundcolor_dict = {};
    let tr_color = window.getComputedStyle(rows[0], "").color;

    rows.forEach((row) => {
        // 行ごとに背景色が異なるため全ての行の変更前の背景色を取得
        backgroundcolor_dict[String(row.rowIndex)] = window.getComputedStyle(
            row,
            ""
        ).backgroundColor;

        row.addEventListener(
            "click",
            function() {
                // 一度全て元の配色
                rows.forEach((click_row) => {
                    click_row.style.backgroundColor =
                        backgroundcolor_dict[String(row.rowIndex)];
                    click_row.style.color = tr_color;
                });
                // 選択された行のみ配色変更
                row.style.backgroundColor = "#E6F3FF";
                row.style.color = "#333333";

                // if (row.querySelector("input").type == "radio") {
                //     row.querySelector('input[type="radio"]').checked = true;
                // }
                if (row.querySelector("input").type == "checkbox") {
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
*/