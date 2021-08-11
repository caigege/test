//目标- 计划 - 问题 - 方案

$(document).ready(function () {
    // <button id="passbtn">通过</button>
    //                    <button id="failbtn">失败</button>
    $("button[name='failbtn']").click(function () {

        var planStepProblemSchemeId = $(this).parent().parent().find("td").eq(0).attr("id");
        var result = 0;
        $.get("/planStepProblemSchemeJudge/", {
                "planStepProblemSchemeId": planStepProblemSchemeId,
                "result": result,
            }, function (data) {
                console.log(data)
                alert(data.msg)
                window.location.reload()
            }
        )
    })

    $("button[name='passbtn']").click(function () {

        var planStepProblemSchemeId = $(this).parent().parent().find("td").eq(0).attr("id");
        var result = 1;
        $.get("/planStepProblemSchemeJudge/", {
                "planStepProblemSchemeId": planStepProblemSchemeId,
                "result": result,
            }, function (data) {
                alert(data.msg)
                window.location.reload()
            }
        )
    })

    $("button[name='fx']").click(function () {

        var s = $(" p")[0].innerText
        // alert(s)
        // 问题id
        var planStepProblemId = $("input[name='planStepProblemId']")[0].value
         // alert(planStepProblemId)
        // console.log("planStepProblemId:" + planStepProblemId)
        $.get("/analysisPageGetProblemAtt/",{"planStepProblemId":planStepProblemId},function(e){
            console.log("****",typeof (e),e)
            localStorage.setItem("problemAtt",e)
        })
        // console.log("problemAtt : ",localStorage.getItem("problemAtt"))

        var searchUrl = encodeURI("/analysisPage/?&planStepProblemId=" + planStepProblemId)
        // "&planStepProblemId="
        // + planStepProblemId + "&proname=" + proname + "&planName=" + planName +
        // "&step=" + step + "&problemName=" + problemName);
        window.location.href = searchUrl;
    })


})