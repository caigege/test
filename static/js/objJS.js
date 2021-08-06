//目标- 计划
$(document).ready(function () {
    $("#projectIn").click(function () {
        // alert($("#selectlist")[0].attr("value"))
        // alert($("#selectlist")[0].value)
        var projectId = $("#selectlist")[0].value

        // $.get("/planPage/",{"projectId":projectId})
        var searchUrl = encodeURI("/planPage/?&projectId="
            + projectId);
        window.location.href = searchUrl;

    })


})