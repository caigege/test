//目标- 计划 - 问题 - 方案

$(document).ready(function () {
    $("#planStepProblemSchemeIn").click(function () {
        //目标名
        var proname = $("#proName")[0].innerText

        console.log("proname:",proname)
        // 计划名
        var planName = $("#planName")[0].innerText
        var planStepProblemId = $("#selectlist")[0].value
        var problemName = $("#selectlist").find("option:selected")[0].innerText

        var step = $("#stepId")[0].value
        console.log("step:", step)

        var searchUrl = encodeURI("/planStepProblemSchemePage/?&planStepProblemId="
            + planStepProblemId + "&proname=" + proname + "&planName=" + planName +
            "&step=" + step + "&problemName=" + problemName);
        window.location.href = searchUrl;


    })


})