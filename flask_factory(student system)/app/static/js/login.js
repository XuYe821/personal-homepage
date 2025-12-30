$(document).ready(function () {
    $.get("https://v1.hitokoto.cn", {c:'i'},
        function (data, textStatus, jqXHR) {
            $("#hitokoto-text").text(data.hitokoto); // 输出.hitokoto字段
            if (data.from_who) {
                $("#hitokoto-from").text(data.from_who+"——" + data.from); // 输出.from字段
            } else {
                $("#hitokoto-from").text(data.from); // 输出.from字段
            }
        },
        "json"
    );
});