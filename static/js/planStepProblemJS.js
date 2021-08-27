//目标- 计划 - 问题 - 方案

$(document).ready(function () {
    $("input[name='btnAddDown']").click(function () {
        var planStepProblemId = $(this).parent().find("select[name='selectlist']")[0].value
        var problemName = $(this).parent().find("select[name='selectlist']").find("option:selected")[0].innerText
        var id = $(this).parent().parent().find("td:first").data("id")
        // var problemName = $(this).parent().parent().find("td:eq(1)")[0].innerText

        console.log("planStepProblemId : ", planStepProblemId, "problemName : ", problemName)
        $.get("/addPlanStepProblemDown/", {
            "id": id,
            "jsonDown": "["+JSON.stringify({"id": planStepProblemId, "name": problemName})+"]"
        }, function (e) {
        // alert(e)
            location.reload()
        })

    })
    $("input[name='btnAddUp']").click(function () {
        var planStepProblemId = $(this).parent().find("select[name='selectlist']")[0].value
        var problemName = $(this).parent().find("select[name='selectlist']").find("option:selected")[0].innerText
         var id = $(this).parent().parent().find("td:first").data("id")
        console.log("planStepProblemId : ", planStepProblemId, "problemName : ", problemName)
         $.get("/addPlanStepProblemUp/", {
            "id": id,
             "jsonUp": "["+JSON.stringify({"id": planStepProblemId, "name": problemName})+"]"
        }, function (e) {
        // alert(e)
             location.reload()
        })

    })

    $("input[name='planStepProblemSchemeIn']").click(function () {
        //目标名
        var proname = $("#proName")[0].innerText

        console.log("proname:", proname)
        // 计划名
        var planName = $("#planName")[0].innerText


        var planStepProblemId = $(this).parent().parent().find("td:first").data("id")
        var problemName = $(this).parent().parent().find("td:eq(1)")[0].innerText

        var step = $("#stepId")[0].value
        console.log("step:", step)

        var searchUrl = encodeURI("/planStepProblemSchemePage/?&planStepProblemId="
            + planStepProblemId + "&proname=" + proname + "&planName=" + planName +
            "&step=" + step + "&problemName=" + problemName);
        window.location.href = searchUrl;


    })


})